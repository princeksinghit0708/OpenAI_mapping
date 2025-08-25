"""
Enhanced Agent v2 - Full LangChain + LiteLLM Integration
This is the production-ready version that replaces the base_agent.py
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from uuid import uuid4
import os

# LangChain imports
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.tools import BaseTool
from langchain.callbacks import get_openai_callback
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# LiteLLM imports
import litellm
from litellm import completion, acompletion, Router
from litellm.exceptions import AuthenticationError, RateLimitError, ContextWindowExceededError

# Enhanced utilities
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import structlog
from loguru import logger

# Internal imports
from core.models import AgentTask, AgentType, TaskStatus
from knowledge.rag_engine import RAGEngine
from config.settings import settings


# Set up structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# Enable LangChain caching
set_llm_cache(InMemoryCache())


class EnhancedAgentConfig:
    """Enhanced configuration for agents"""
    def __init__(
        self,
        name: str,
        description: str,
        agent_type: str,
        primary_model: str = "gpt-4",
        fallback_models: List[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 2000,
        max_cost_per_request: float = 0.50,
        max_iterations: int = 5,
        timeout: int = 300,
        enable_memory: bool = True,
        memory_type: str = "window",
        memory_window_size: int = 10,
        enable_fallbacks: bool = True,
        enable_cost_tracking: bool = True,
        enable_multi_provider: bool = False,
        **kwargs
    ):
        self.name = name
        self.description = description
        self.agent_type = agent_type
        self.primary_model = primary_model
        self.fallback_models = fallback_models or ["gpt-3.5-turbo"]
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_cost_per_request = max_cost_per_request
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.enable_memory = enable_memory
        self.memory_type = memory_type
        self.memory_window_size = memory_window_size
        self.enable_fallbacks = enable_fallbacks
        self.enable_cost_tracking = enable_cost_tracking
        self.enable_multi_provider = enable_multi_provider
        
        # Add any additional kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)


class LLMProvider:
    """Enhanced LLM provider with LangChain + LiteLLM integration"""
    
    def __init__(self, config: EnhancedAgentConfig):
        self.config = config
        self.current_provider = config.primary_model
        self.fallback_providers = config.fallback_models
        self.request_count = 0
        self.total_cost = 0.0
        self.cost_history = []
        
        # Setup providers
        self._setup_providers()
        
        # Initialize LangChain LLMs for compatibility
        self.langchain_llms = self._setup_langchain_llms()
        
        # Initialize LiteLLM router if multi-provider enabled
        self.litellm_router = self._setup_litellm_router() if config.enable_multi_provider else None
        
        logger.info(f"LLM Provider initialized", 
                   multi_provider=config.enable_multi_provider,
                   primary_model=config.primary_model)
    
    def _setup_providers(self):
        """Setup provider configurations"""
        # Configure LiteLLM with API keys
        if os.getenv("OPENAI_API_KEY"):
            litellm.openai_key = os.getenv("OPENAI_API_KEY")
        if os.getenv("ANTHROPIC_API_KEY"):
            litellm.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if os.getenv("GOOGLE_API_KEY"):
            litellm.google_key = os.getenv("GOOGLE_API_KEY")
        
        # Set LiteLLM settings
        litellm.set_verbose = settings.debug
        litellm.drop_params = True
        litellm.request_timeout = self.config.timeout
    
    def _setup_langchain_llms(self) -> Dict[str, Any]:
        """Setup LangChain LLMs for backwards compatibility"""
        llms = {}
        
        try:
            # OpenAI
            if os.getenv("OPENAI_API_KEY"):
                llms["openai"] = ChatOpenAI(
                    model=self.config.primary_model,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
        except Exception as e:
            logger.warning(f"Failed to setup OpenAI LangChain LLM: {e}")
        
        try:
            # Anthropic
            if os.getenv("ANTHROPIC_API_KEY"):
                llms["anthropic"] = ChatAnthropic(
                    model="claude-3-sonnet-20240229",
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
        except Exception as e:
            logger.warning(f"Failed to setup Anthropic LangChain LLM: {e}")
        
        return llms
    
    def _setup_litellm_router(self) -> Optional[Router]:
        """Setup LiteLLM router for multi-provider support"""
        try:
            model_list = []
            
            # Add available models
            if os.getenv("OPENAI_API_KEY"):
                model_list.append({
                    "model_name": "gpt-4",
                    "litellm_params": {
                        "model": "gpt-4",
                        "api_key": os.getenv("OPENAI_API_KEY")
                    }
                })
                model_list.append({
                    "model_name": "gpt-3.5-turbo",
                    "litellm_params": {
                        "model": "gpt-3.5-turbo",
                        "api_key": os.getenv("OPENAI_API_KEY")
                    }
                })
            
            if os.getenv("ANTHROPIC_API_KEY"):
                model_list.append({
                    "model_name": "claude-3-sonnet",
                    "litellm_params": {
                        "model": "claude-3-sonnet-20240229",
                        "api_key": os.getenv("ANTHROPIC_API_KEY")
                    }
                })
            
            if os.getenv("GOOGLE_API_KEY"):
                model_list.append({
                    "model_name": "gemini-pro",
                    "litellm_params": {
                        "model": "gemini-pro",
                        "api_key": os.getenv("GOOGLE_API_KEY")
                    }
                })
            
            if not model_list:
                logger.warning("No API keys found for multi-provider setup")
                return None
            
            # Create router with fallbacks
            router = Router(
                model_list=model_list,
                fallbacks=[
                    {"gpt-4": ["claude-3-sonnet", "gpt-3.5-turbo"]},
                    {"claude-3-sonnet": ["gpt-4", "gpt-3.5-turbo"]},
                    {"gemini-pro": ["gpt-3.5-turbo", "gpt-4"]}
                ]
            )
            
            logger.info(f"LiteLLM router setup with {len(model_list)} models")
            return router
            
        except Exception as e:
            logger.error(f"Failed to setup LiteLLM router: {e}")
            return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((RateLimitError, ContextWindowExceededError))
    )
    async def generate(
        self, 
        messages: List[Dict[str, str]], 
        use_langchain: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using either LangChain or LiteLLM
        
        Args:
            messages: List of message dictionaries
            use_langchain: If True, use LangChain LLMs for compatibility
            **kwargs: Additional parameters
            
        Returns:
            Response dictionary with content, provider info, and metrics
        """
        start_time = time.time()
        
        try:
            if use_langchain:
                return await self._generate_with_langchain(messages, **kwargs)
            elif self.config.enable_multi_provider and self.litellm_router:
                return await self._generate_with_litellm_router(messages, **kwargs)
            else:
                return await self._generate_with_litellm_direct(messages, **kwargs)
                
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            # Try fallback approach
            if not use_langchain and self.langchain_llms:
                logger.info("Trying LangChain fallback")
                return await self._generate_with_langchain(messages, **kwargs)
            raise
    
    async def _generate_with_langchain(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using LangChain LLMs"""
        
        # Convert messages to LangChain format
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
            # system messages are handled in prompt template
        
        # Try primary LLM
        primary_llm = self.langchain_llms.get("openai")
        if not primary_llm and self.langchain_llms:
            primary_llm = list(self.langchain_llms.values())[0]
        
        if not primary_llm:
            raise Exception("No LangChain LLM available")
        
        # Generate response
        response = await primary_llm.agenerate([langchain_messages])
        content = response.generations[0][0].text
        
        # Estimate metrics
        estimated_tokens = len(content.split()) * 1.3
        estimated_cost = self._estimate_cost_simple(estimated_tokens)
        
        return {
            "content": content,
            "provider": "langchain",
            "model": self.config.primary_model,
            "usage": {
                "total_tokens": int(estimated_tokens),
                "prompt_tokens": int(len(str(messages).split()) * 1.3),
                "completion_tokens": int(len(content.split()) * 1.3)
            },
            "cost": estimated_cost,
            "response_time": time.time() - time.time()
        }
    
    async def _generate_with_litellm_router(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using LiteLLM router"""
        
        response = await self.litellm_router.acompletion(
            model=self.config.primary_model,
            messages=messages,
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs
        )
        
        # Extract metrics
        usage = response.usage.dict() if response.usage else {}
        cost = self._estimate_cost(usage)
        
        return {
            "content": response.choices[0].message.content,
            "provider": "litellm_router",
            "model": response.model,
            "usage": usage,
            "cost": cost,
            "response_time": time.time() - time.time()
        }
    
    async def _generate_with_litellm_direct(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate using direct LiteLLM calls"""
        
        response = await acompletion(
            model=self.config.primary_model,
            messages=messages,
            temperature=kwargs.get("temperature", self.config.temperature),
            max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
            **kwargs
        )
        
        # Extract metrics
        usage = response.usage.dict() if response.usage else {}
        cost = self._estimate_cost(usage)
        
        return {
            "content": response.choices[0].message.content,
            "provider": "litellm_direct",
            "model": response.model,
            "usage": usage,
            "cost": cost,
            "response_time": time.time() - time.time()
        }
    
    def _estimate_cost(self, usage: Dict[str, Any]) -> float:
        """Estimate cost from usage stats"""
        if not usage:
            return 0.0
        
        # Model-specific pricing (simplified)
        pricing = {
            "gpt-4": {"prompt": 0.00003, "completion": 0.00006},
            "gpt-3.5-turbo": {"prompt": 0.000001, "completion": 0.000002},
            "claude-3-sonnet": {"prompt": 0.000015, "completion": 0.000075},
            "gemini-pro": {"prompt": 0.0000005, "completion": 0.0000015}
        }
        
        model_pricing = pricing.get(self.config.primary_model, pricing["gpt-4"])
        
        prompt_cost = usage.get("prompt_tokens", 0) * model_pricing["prompt"]
        completion_cost = usage.get("completion_tokens", 0) * model_pricing["completion"]
        
        return prompt_cost + completion_cost
    
    def _estimate_cost_simple(self, total_tokens: float) -> float:
        """Simple cost estimation for fallback"""
        return total_tokens * 0.00003  # Average cost per token
    
    def get_langchain_llm(self, provider: str = "openai"):
        """Get LangChain LLM for compatibility"""
        return self.langchain_llms.get(provider)


class EnhancedBaseAgent(ABC):
    """
    Enhanced Base Agent with full LangChain + LiteLLM integration
    
    This is the production-ready version that replaces base_agent.py
    """
    
    def __init__(
        self,
        config: EnhancedAgentConfig,
        rag_engine: Optional[RAGEngine] = None,
        tools: Optional[List[BaseTool]] = None
    ):
        self.config = config
        self.rag_engine = rag_engine
        self.tools = tools or []
        self.current_task: Optional[AgentTask] = None
        
        # Initialize enhanced LLM provider
        self.llm_provider = LLMProvider(config)
        
        # Initialize memory
        self.memory = self._setup_memory()
        
        # Initialize agent executor for LangChain compatibility
        self.agent_executor = self._setup_agent_executor()
        
        # Structured logger
        self.logger = structlog.get_logger().bind(
            agent_type=config.agent_type,
            agent_name=config.name
        )
        
        self.logger.info("Enhanced agent initialized")
    
    def _setup_memory(self):
        """Setup enhanced memory system"""
        if not self.config.enable_memory:
            return None
        
        memory_type = self.config.memory_type
        
        if memory_type == "window":
            return ConversationBufferWindowMemory(
                k=self.config.memory_window_size,
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        elif memory_type == "summary":
            # Use LangChain LLM for summaries
            langchain_llm = self.llm_provider.get_langchain_llm()
            if langchain_llm:
                return ConversationSummaryMemory(
                    llm=langchain_llm,
                    memory_key="chat_history",
                    return_messages=True,
                    input_key="input",
                    output_key="output"
                )
        
        # Fallback to buffer memory
        from langchain.memory import ConversationBufferMemory
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="input",
            output_key="output"
        )
    
    def _setup_agent_executor(self) -> Optional[AgentExecutor]:
        """Setup agent executor for LangChain tools"""
        if not self.tools:
            return None
        
        try:
            # Get LangChain LLM for agent executor
            langchain_llm = self.llm_provider.get_langchain_llm()
            if not langchain_llm:
                return None
            
            # Create prompt template
            system_prompt = self._get_system_prompt()
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
            
            # Create agent
            agent = create_openai_functions_agent(
                llm=langchain_llm,
                tools=self.tools,
                prompt=prompt_template
            )
            
            return AgentExecutor(
                agent=agent,
                tools=self.tools,
                memory=self.memory,
                max_iterations=self.config.max_iterations,
                verbose=settings.debug,
                return_intermediate_steps=True
            )
            
        except Exception as e:
            self.logger.warning(f"Failed to setup agent executor: {e}")
            return None
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def get_agent_type(self) -> AgentType:
        """Get the agent type"""
        pass
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """Execute a task with enhanced capabilities"""
        self.current_task = task
        start_time = time.time()
        
        try:
            self.logger.info("Starting enhanced task execution", task_id=task.id)
            
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.utcnow()
            
            # Prepare enhanced context
            context = ""
            if self.rag_engine:
                context = await self._get_rag_context(task.input_data)
            
            # Execute core logic
            result = await self._execute_core_logic(task.input_data, context)
            
            # Add enhanced metadata
            result["enhanced_metadata"] = {
                "agent_type": self.config.agent_type,
                "model_used": self.llm_provider.config.primary_model,
                "multi_provider_enabled": self.config.enable_multi_provider,
                "total_requests": self.llm_provider.request_count,
                "total_cost": round(self.llm_provider.total_cost, 4),
                "execution_time": time.time() - start_time
            }
            
            # Update task with results
            task.output_data = result
            task.status = TaskStatus.COMPLETED
            task.updated_at = datetime.utcnow()
            
            execution_time = time.time() - start_time
            self.logger.info(
                "Enhanced task execution completed",
                task_id=task.id,
                execution_time=execution_time,
                requests_made=self.llm_provider.request_count,
                total_cost=self.llm_provider.total_cost
            )
            
        except Exception as e:
            self.logger.error("Enhanced task execution failed", task_id=task.id, error=str(e))
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.utcnow()
        
        return task
    
    async def _get_rag_context(self, input_data: Dict[str, Any]) -> str:
        """Get RAG context"""
        if not self.rag_engine:
            return ""
        
        # Create query from input data
        query = json.dumps(input_data, indent=2)[:500]  # Limit query size
        
        # Retrieve relevant context
        results = await self.rag_engine.retrieve(query, max_results=5)
        
        # Format context
        context_parts = []
        for result in results:
            context_parts.append(f"Context: {result.content}")
        
        return "\n\n".join(context_parts)
    
    @abstractmethod
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """Execute the core logic of the agent"""
        pass
    
    async def chat(self, message: str, use_langchain: bool = False) -> str:
        """Chat with the agent using either LangChain or LiteLLM"""
        try:
            if use_langchain and self.agent_executor:
                # Use LangChain agent executor
                result = await self.agent_executor.ainvoke({"input": message})
                return result.get("output", "No response generated")
            else:
                # Use enhanced LLM provider
                messages = [{"role": "user", "content": message}]
                response = await self.llm_provider.generate(messages, use_langchain=use_langchain)
                return response["content"]
                
        except Exception as e:
            self.logger.error(f"Chat error: {str(e)}")
            return f"I encountered an error: {str(e)}"
    
    async def health_check(self) -> Dict[str, Any]:
        """Enhanced health check"""
        health_status = {
            "agent_type": self.config.agent_type,
            "agent_name": self.config.name,
            "status": "healthy",
            "features": {
                "langchain_integration": True,
                "litellm_integration": True,
                "multi_provider": self.config.enable_multi_provider,
                "memory_enabled": self.config.enable_memory,
                "rag_enabled": self.rag_engine is not None,
                "tools_count": len(self.tools)
            },
            "metrics": {
                "total_requests": self.llm_provider.request_count,
                "total_cost_usd": round(self.llm_provider.total_cost, 4),
                "primary_model": self.config.primary_model
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Test LLM connectivity
        try:
            test_messages = [{"role": "user", "content": "Say 'OK' if you can respond"}]
            test_response = await self.llm_provider.generate(test_messages, max_tokens=10)
            
            health_status["llm_status"] = "connected"
            health_status["test_response"] = test_response["content"]
            health_status["last_provider"] = test_response["provider"]
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["llm_status"] = "disconnected"
            health_status["error"] = str(e)
        
        return health_status


# Factory function for easy creation
def create_enhanced_agent(
    agent_type: str,
    name: str = None,
    description: str = None,
    enable_multi_provider: bool = None,
    **kwargs
) -> EnhancedAgentConfig:
    """Create enhanced agent configuration with smart defaults"""
    
    # Auto-detect multi-provider based on available API keys
    if enable_multi_provider is None:
        api_key_count = sum([
            bool(os.getenv("OPENAI_API_KEY")),
            bool(os.getenv("ANTHROPIC_API_KEY")),
            bool(os.getenv("GOOGLE_API_KEY"))
        ])
        enable_multi_provider = api_key_count > 1
    
    return EnhancedAgentConfig(
        name=name or f"Enhanced {agent_type.title()} Agent",
        description=description or f"Enhanced {agent_type} agent with LangChain + LiteLLM",
        agent_type=agent_type,
        enable_multi_provider=enable_multi_provider,
        **kwargs
    )