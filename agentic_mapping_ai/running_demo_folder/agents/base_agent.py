"""
Base Agent class for Agentic Mapping AI Platform
"""

import asyncio
import json
import time
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Type
from uuid import uuid4

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage
from langchain.tools import BaseTool
from loguru import logger
from pydantic import BaseModel

from core.models import AgentTask, AgentType, TaskStatus
from knowledge.rag_engine import RAGEngine

# Import the LLM Service for token-based authentication
# Commented out for demo to avoid vertexai dependency
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from llm_service import llm_service


class AgentConfig(BaseModel):
    """Configuration for agents"""
    name: str
    description: str
    model: str = "gpt-4"
    temperature: float = 0.1
    max_tokens: int = 2000
    max_iterations: int = 5
    timeout: int = 300
    enable_memory: bool = True
    enable_rag: bool = True


class BaseAgent(ABC):
    """
    Base class for all AI agents in the system
    
    Provides common functionality:
    - LLM integration
    - Memory management
    - RAG integration
    - Task execution tracking
    - Error handling
    """
    
    def __init__(
        self,
        config: AgentConfig,
        rag_engine: Optional[RAGEngine] = None,
        tools: Optional[List[BaseTool]] = None
    ):
        self.config = config
        self.rag_engine = rag_engine
        self.tools = tools or []
        self.memory = None
        self.agent_executor = None
        self.current_task: Optional[AgentTask] = None
        
        # Initialize LLM using token-based authentication
        # Commented out for demo to avoid vertexai dependency
        # self.llm_service = llm_service
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        
        # Initialize memory if enabled
        if config.enable_memory:
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                input_key="input",
                output_key="output"
            )
        
        # Setup agent
        self._setup_agent()
        
        logger.info(f"Initialized {self.__class__.__name__} with config: {config.name}")
    
    def _setup_agent(self):
        """Setup the agent with prompt and tools"""
        system_prompt = self._get_system_prompt()
        
        # Create prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Note: Agent executor functionality will be adapted to use LLM service directly
        # For now, we'll handle tool execution in the _execute_core_logic method
        self.agent_executor = None
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    @abstractmethod
    def get_agent_type(self) -> AgentType:
        """Get the agent type"""
        pass
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """
        Execute a task and return the updated task
        
        Args:
            task: The task to execute
            
        Returns:
            Updated task with results
        """
        self.current_task = task
        start_time = time.time()
        
        try:
            logger.info(f"Starting task {task.id} for {self.__class__.__name__}")
            
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.utcnow()
            
            # Prepare context if RAG is enabled
            context = ""
            if self.config.enable_rag and self.rag_engine:
                context = await self._get_rag_context(task.input_data)
            
            # Execute the core logic
            result = await self._execute_core_logic(task.input_data, context)
            
            # Update task with results
            task.output_data = result
            task.status = TaskStatus.COMPLETED
            task.updated_at = datetime.utcnow()
            
            execution_time = int((time.time() - start_time) * 1000)
            logger.info(f"Completed task {task.id} in {execution_time}ms")
            
        except Exception as e:
            logger.error(f"Task {task.id} failed: {str(e)}")
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.utcnow()
        
        return task
    
    async def _get_rag_context(self, input_data: Dict[str, Any]) -> str:
        """Get relevant context from RAG engine"""
        if not self.rag_engine:
            return ""
        
        # Create query from input data
        query = self._create_rag_query(input_data)
        
        # Retrieve relevant context
        results = await self.rag_engine.retrieve(query, max_results=5)
        
        # Format context
        context_parts = []
        for result in results:
            context_parts.append(f"Context: {result.content}")
        
        return "\n\n".join(context_parts)
    
    def _create_rag_query(self, input_data: Dict[str, Any]) -> str:
        """Create a query for RAG from input data"""
        # Default implementation - can be overridden by subclasses
        if isinstance(input_data, dict):
            return json.dumps(input_data, indent=2)
        return str(input_data)
    
    @abstractmethod
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute the core logic of the agent
        
        Args:
            input_data: Input data for the task
            context: RAG context if available
            
        Returns:
            Task output data
        """
        pass
    
    async def chat(self, message: str, context: str = "") -> str:
        """
        Have a conversation with the agent
        
        Args:
            message: User message
            context: Additional context
            
        Returns:
            Agent response
        """
        try:
            # Prepare messages for LLM service
            system_prompt = self._get_system_prompt()
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {message}"
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context: {context}\n\nUser: {message}"}
            ]
            
            # Use LLM service with token-based authentication
            response = self.llm_service.query_llm(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                llm_provider="azure"  # Default to azure, can be configured
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Chat error: {str(e)}")
            return f"I encountered an error: {str(e)}"
    
    def add_tool(self, tool: BaseTool):
        """Add a tool to the agent"""
        self.tools.append(tool)
        # Re-setup agent with new tools
        self._setup_agent()
    
    def get_memory_messages(self) -> List[BaseMessage]:
        """Get conversation history from memory"""
        if not self.memory:
            return []
        return self.memory.chat_memory.messages
    
    def clear_memory(self):
        """Clear conversation memory"""
        if self.memory:
            self.memory.clear()
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        try:
            # Test LLM connection using token-based service
            messages = [
                {"role": "system", "content": "You are a health check assistant."},
                {"role": "user", "content": "Say 'OK' if you can respond"}
            ]
            
            test_response = self.llm_service.query_llm(
                model=self.model,
                messages=messages,
                temperature=0.1,
                max_tokens=10,
                llm_provider="azure"
            )
            
            return {
                "status": "healthy",
                "agent_type": self.get_agent_type().value,
                "llm_status": "connected" if "OK" in test_response else "disconnected",
                "memory_enabled": self.config.enable_memory,
                "rag_enabled": self.config.enable_rag and self.rag_engine is not None,
                "tools_count": len(self.tools),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }


class AgentFactory:
    """Factory for creating agents"""
    
    _agent_registry: Dict[AgentType, Type[BaseAgent]] = {}
    
    @classmethod
    def register_agent(cls, agent_type: AgentType, agent_class: Type[BaseAgent]):
        """Register an agent class"""
        cls._agent_registry[agent_type] = agent_class
    
    @classmethod
    def create_agent(
        cls, 
        agent_type: AgentType, 
        config: AgentConfig,
        rag_engine: Optional[RAGEngine] = None,
        tools: Optional[List[BaseTool]] = None
    ) -> BaseAgent:
        """Create an agent instance"""
        if agent_type not in cls._agent_registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = cls._agent_registry[agent_type]
        return agent_class(config, rag_engine, tools)
    
    @classmethod
    def get_available_agents(cls) -> List[AgentType]:
        """Get list of available agent types"""
        return list(cls._agent_registry.keys())