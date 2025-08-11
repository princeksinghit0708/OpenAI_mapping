"""
Enhanced Base Agent with LangChain + LiteLLM Integration
Provides multi-provider LLM support, advanced chains, and better observability
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from uuid import uuid4

# LangChain imports
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.tools import BaseTool
from langchain.callbacks import get_openai_callback
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Token-based LLM Service
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_service import llm_service

# Observability
from prometheus_client import Counter, Histogram, Gauge
from loguru import logger
import structlog
from pydantic import BaseModel

# Internal imports
from core.models import AgentTask, AgentType, TaskStatus
from knowledge.rag_engine import RAGEngine
from config.enhanced_settings import enhanced_settings


# Metrics
llm_requests_total = Counter('llm_requests_total', 'Total LLM requests', ['provider', 'model', 'agent_type'])
llm_response_time = Histogram('llm_response_time_seconds', 'LLM response time', ['provider', 'model'])
llm_tokens_used = Counter('llm_tokens_used_total', 'Total tokens used', ['provider', 'model', 'type'])
llm_cost_usd = Counter('llm_cost_usd_total', 'Total cost in USD', ['provider', 'model'])
agent_execution_time = Histogram('agent_execution_time_seconds', 'Agent execution time', ['agent_type'])

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


class EnhancedAgentConfig(BaseModel):
    """Enhanced configuration for agents"""
    name: str
    description: str
    agent_type: str
    
    # LLM configuration - Token-based providers
    primary_model: str = "gpt-4"
    primary_provider: str = "azure" 
    fallback_models: List[str] = ["claude-3-7-sonnet@20250219", "gemini-2.5-pro"]
    fallback_providers: List[str] = ["claude", "gemini"]
    temperature: float = 0.1
    max_tokens: int = 2000
    max_cost_per_request: float = 0.50
    
    # Execution configuration
    max_iterations: int = 5
    timeout: int = 300
    enable_memory: bool = True
    memory_type: str = "window"  # buffer, window, summary
    memory_window_size: int = 10
    
    # Advanced features
    enable_self_reflection: bool = True
    enable_planning: bool = True
    enable_caching: bool = True
    enable_retry: bool = True
    max_retries: int = 3
    
    # Observability
    enable_tracing: bool = True
    enable_metrics: bool = True
    log_level: str = "INFO"


class LLMProvider:
    """Enhanced LLM provider with token-based authentication"""
    
    def __init__(self, config: EnhancedAgentConfig):
        self.config = config
        self.current_provider = config.primary_provider
        self.current_model = config.primary_model
        self.fallback_providers = config.fallback_providers
        self.fallback_models = config.fallback_models
        self.request_count = 0
        self.total_cost = 0.0
        
        # Use token-based LLM service
        self.llm_service = llm_service
        
        logger.info(
            "LLM Provider initialized with token-based authentication",
            provider=self.current_provider,
            model=self.current_model
        )
    
    async def generate(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate response with token-based authentication and fallback support"""
        
        # Primary attempt with current provider/model
        providers_to_try = [(self.current_provider, self.current_model)]
        
        # Add fallback providers and models
        for provider, model in zip(self.fallback_providers, self.fallback_models):
            providers_to_try.append((provider, model))
        
        last_error = None
        
        for provider, model in providers_to_try:
            try:
                start_time = time.time()
                
                # Use token-based LLM service
                response_content = self.llm_service.query_llm(
                    model=model,
                    messages=messages,
                    temperature=kwargs.get("temperature", self.config.temperature),
                    max_tokens=kwargs.get("max_tokens", self.config.max_tokens),
                    llm_provider=provider
                )
                
                # Calculate metrics
                response_time = time.time() - start_time
                
                # Estimate token usage (simplified)
                estimated_tokens = len(str(messages)) // 4 + len(response_content) // 4
                estimated_cost = estimated_tokens * 0.00002  # Rough estimate
                
                # Update metrics
                llm_requests_total.labels(
                    provider=provider, 
                    model=model, 
                    agent_type=self.config.agent_type
                ).inc()
                
                llm_response_time.labels(provider=provider, model=model).observe(response_time)
                llm_tokens_used.labels(provider=provider, model=model, type="total").inc(estimated_tokens)
                llm_cost_usd.labels(provider=provider, model=model).inc(estimated_cost)
                
                # Update instance metrics
                self.request_count += 1
                self.total_cost += estimated_cost
                
                # Log successful request
                logger.info(
                    "LLM request successful via token auth",
                    provider=provider,
                    model=model,
                    tokens=estimated_tokens,
                    cost=estimated_cost,
                    response_time=response_time
                )
                
                return {
                    "content": response_content,
                    "provider": provider,
                    "model": model,
                    "usage": {"total_tokens": estimated_tokens},
                    "cost": estimated_cost,
                    "response_time": response_time
                }
                
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Provider {provider} with model {model} failed, trying next",
                    error=str(e),
                    provider=provider,
                    model=model
                )
                continue
        
        # All providers failed
        raise Exception(f"All LLM providers failed. Last error: {str(last_error)}")


class EnhancedBaseAgent(ABC):
    """
    Enhanced base agent with LangChain + LiteLLM integration
    
    New features:
    - Multi-provider LLM support with automatic fallbacks
    - Advanced memory management
    - Better observability and metrics
    - Cost optimization
    - Self-reflection and planning capabilities
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
        
        # Initialize LLM provider
        self.llm_provider = LLMProvider(config)
        
        # Initialize memory
        self.memory = self._setup_memory()
        
        # Initialize agent executor
        self.agent_executor = None
        self._setup_agent()
        
        # Structured logger
        self.logger = structlog.get_logger().bind(
            agent_type=config.agent_type,
            agent_name=config.name
        )
        
        self.logger.info("Enhanced agent initialized", config=config.dict())
    
    def _setup_memory(self):
        """Setup advanced memory system"""
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
            return ConversationSummaryMemory(
                llm=self.llm_provider,  # Use our enhanced LLM
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        else:  # buffer
            from langchain.memory import ConversationBufferMemory
            return ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
    
    def _setup_agent(self):
        """Setup agent with enhanced capabilities"""
        system_prompt = self._get_system_prompt()
        
        # Enhanced prompt template with self-reflection
        if self.config.enable_self_reflection:
            system_prompt += """
            
            You have the ability to reflect on your work and improve your responses.
            After generating a response, briefly consider:
            1. Is this response accurate and complete?
            2. Could it be improved in any way?
            3. Are there any potential issues or edge cases?
            
            If you identify improvements, provide them.
            """
        
        # Planning capability
        if self.config.enable_planning:
            system_prompt += """
            
            You can create and follow plans for complex tasks:
            1. Break down complex tasks into smaller steps
            2. Execute steps systematically
            3. Adapt the plan based on intermediate results
            4. Track progress and dependencies
            """
        
        # Create enhanced prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True)
        ])
        
        # Setup agent executor if tools are available
        if self.tools:
            # This would need to be adapted for LiteLLM
            # For now, we'll handle tool usage in the execute methods
            pass
    
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
        
        with agent_execution_time.labels(agent_type=self.config.agent_type).time():
            try:
                self.logger.info("Starting task execution", task_id=task.id)
                
                # Update task status
                task.status = TaskStatus.IN_PROGRESS
                task.updated_at = datetime.utcnow()
                
                # Prepare enhanced context
                context = ""
                if self.rag_engine:
                    context = await self._get_enhanced_rag_context(task.input_data)
                
                # Planning phase (if enabled)
                plan = None
                if self.config.enable_planning:
                    plan = await self._create_execution_plan(task.input_data, context)
                
                # Execute with plan
                result = await self._execute_with_enhancements(
                    task.input_data, context, plan
                )
                
                # Self-reflection phase (if enabled)
                if self.config.enable_self_reflection:
                    result = await self._self_reflect_and_improve(result, task.input_data)
                
                # Update task with results
                task.output_data = result
                task.status = TaskStatus.COMPLETED
                task.updated_at = datetime.utcnow()
                
                execution_time = time.time() - start_time
                self.logger.info(
                    "Task execution completed",
                    task_id=task.id,
                    execution_time=execution_time,
                    llm_requests=self.llm_provider.request_count,
                    total_cost=self.llm_provider.total_cost
                )
                
            except Exception as e:
                self.logger.error(
                    "Task execution failed",
                    task_id=task.id,
                    error=str(e),
                    execution_time=time.time() - start_time
                )
                task.status = TaskStatus.FAILED
                task.error_message = str(e)
                task.updated_at = datetime.utcnow()
        
        return task
    
    async def _get_enhanced_rag_context(self, input_data: Dict[str, Any]) -> str:
        """Get enhanced RAG context with better relevance"""
        if not self.rag_engine:
            return ""
        
        # Create more intelligent query
        query = await self._create_intelligent_rag_query(input_data)
        
        # Retrieve with agent-specific filtering
        results = await self.rag_engine.retrieve(
            query=query,
            max_results=enhanced_settings.langchain.memory_window_size,
            category_filter=self.config.agent_type
        )
        
        # Format context with priorities
        context_parts = []
        for i, result in enumerate(results):
            priority = "HIGH" if result.score > 0.8 else "MEDIUM" if result.score > 0.6 else "LOW"
            context_parts.append(f"""
[PRIORITY: {priority}] Context {i+1}:
Title: {result.metadata.get('title', 'Untitled')}
Content: {result.content}
Relevance Score: {result.score:.3f}
""")
        
        return "\n".join(context_parts)
    
    async def _create_intelligent_rag_query(self, input_data: Dict[str, Any]) -> str:
        """Create an intelligent RAG query using LLM"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert at creating search queries. Given input data, create a concise but comprehensive search query to find relevant knowledge."
                },
                {
                    "role": "user", 
                    "content": f"Create a search query for this input data: {json.dumps(input_data, indent=2)}"
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=100)
            return response["content"].strip()
            
        except Exception as e:
            self.logger.warning("Failed to create intelligent RAG query", error=str(e))
            # Fallback to simple approach
            return json.dumps(input_data, indent=2)
    
    async def _create_execution_plan(
        self, 
        input_data: Dict[str, Any], 
        context: str
    ) -> Optional[Dict[str, Any]]:
        """Create an execution plan for complex tasks"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a planning expert for {self.config.agent_type} tasks.
                    Create a step-by-step execution plan for complex tasks.
                    Return a JSON plan with steps, dependencies, and estimated effort."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Task: {self.config.agent_type}
                    Input: {json.dumps(input_data, indent=2)}
                    Context: {context[:500]}...
                    
                    Create an execution plan.
                    """
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=500)
            plan_text = response["content"]
            
            # Try to parse as JSON, fallback to text plan
            try:
                plan = json.loads(plan_text)
            except:
                plan = {"steps": [plan_text], "type": "text"}
            
            self.logger.info("Execution plan created", plan=plan)
            return plan
            
        except Exception as e:
            self.logger.warning("Failed to create execution plan", error=str(e))
            return None
    
    async def _execute_with_enhancements(
        self,
        input_data: Dict[str, Any],
        context: str,
        plan: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute core logic with enhancements"""
        
        # If we have a plan, execute step by step
        if plan and plan.get("steps"):
            return await self._execute_planned_task(input_data, context, plan)
        else:
            # Execute normally
            return await self._execute_core_logic(input_data, context)
    
    async def _execute_planned_task(
        self,
        input_data: Dict[str, Any],
        context: str,
        plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute task following a plan"""
        
        steps = plan.get("steps", [])
        results = {}
        
        for i, step in enumerate(steps):
            self.logger.info(f"Executing plan step {i+1}/{len(steps)}", step=step)
            
            # Execute individual step
            step_result = await self._execute_plan_step(step, input_data, context, results)
            results[f"step_{i+1}"] = step_result
        
        return {
            "planned_execution": True,
            "plan": plan,
            "step_results": results,
            "final_result": results.get(f"step_{len(steps)}", {})
        }
    
    async def _execute_plan_step(
        self,
        step: str,
        input_data: Dict[str, Any],
        context: str,
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a single plan step"""
        
        # Prepare step context
        step_context = context
        if previous_results:
            step_context += f"\n\nPrevious Results: {json.dumps(previous_results, indent=2)}"
        
        # Execute step using core logic (can be overridden by subclasses)
        return await self._execute_core_logic({
            "step": step,
            "original_input": input_data,
            "step_context": step_context
        }, step_context)
    
    async def _self_reflect_and_improve(
        self,
        initial_result: Dict[str, Any],
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Self-reflect on the result and improve if needed"""
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"""You are a quality reviewer for {self.config.agent_type} outputs.
                    Review the initial result and suggest improvements.
                    If the result is good, say so. If it needs improvement, provide specific suggestions."""
                },
                {
                    "role": "user",
                    "content": f"""
                    Original Input: {json.dumps(input_data, indent=2)}
                    Initial Result: {json.dumps(initial_result, indent=2)}
                    
                    Please review and suggest improvements.
                    """
                }
            ]
            
            review_response = await self.llm_provider.generate(messages, max_tokens=300)
            review = review_response["content"]
            
            # Add reflection to result
            initial_result["self_reflection"] = {
                "review": review,
                "timestamp": datetime.utcnow().isoformat(),
                "reviewer": "self"
            }
            
            self.logger.info("Self-reflection completed", review=review)
            
        except Exception as e:
            self.logger.warning("Self-reflection failed", error=str(e))
        
        return initial_result
    
    @abstractmethod
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """Execute the core logic of the agent"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Enhanced health check"""
        health_status = {
            "agent_type": self.config.agent_type,
            "agent_name": self.config.name,
            "status": "healthy",
            "features": {
                "memory_enabled": self.config.enable_memory,
                "rag_enabled": self.rag_engine is not None,
                "planning_enabled": self.config.enable_planning,
                "self_reflection_enabled": self.config.enable_self_reflection,
                "caching_enabled": self.config.enable_caching
            },
            "metrics": {
                "total_requests": self.llm_provider.request_count,
                "total_cost_usd": self.llm_provider.total_cost,
                "current_provider": self.llm_provider.current_provider
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Test LLM connectivity
        try:
            test_response = await self.llm_provider.generate([
                {"role": "user", "content": "Say 'OK' if you can respond"}
            ], max_tokens=10)
            
            health_status["llm_status"] = "connected"
            health_status["test_response"] = test_response["content"]
            
        except Exception as e:
            health_status["status"] = "unhealthy"
            health_status["llm_status"] = "disconnected"
            health_status["error"] = str(e)
        
        return health_status