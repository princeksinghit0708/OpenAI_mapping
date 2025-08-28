"""
Pragmatic Enhanced Agent - Best of Both Worlds
Selective LiteLLM integration without disrupting current working system
"""

import os
import asyncio
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import json

# Core imports
from agents.base_agent import BaseAgent, AgentConfig
from core.models import AgentTask, AgentType, TaskStatus
from knowledge.rag_engine import RAGEngine

# Conditional imports based on environment
try:
    import litellm
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger


class PragmaticAgentConfig(AgentConfig):
    """Enhanced config with pragmatic options"""
    enable_multi_provider: bool = False
    enable_cost_tracking: bool = True
    enable_fallbacks: bool = True
    primary_model: str = "gpt-4"
    fallback_model: str = "gpt-3.5-turbo"
    max_cost_per_request: float = 0.50
    

class PragmaticEnhancedAgent(BaseAgent):
    """
    Pragmatic Enhanced Agent - Smart integration approach
    
    Features:
    - Optional LiteLLM integration (enable via environment variable)
    - Graceful fallback to current structure if LiteLLM unavailable
    - Cost tracking and basic optimization
    - Simple multi-provider support when needed
    - Zero disruption to existing functionality
    """
    
    def __init__(
        self, 
        config: PragmaticAgentConfig,
        rag_engine: Optional[RAGEngine] = None,
        tools: Optional[List] = None
    ):
        self.config = config  
        self.rag_engine = rag_engine
        self.tools = tools or []
        
        # Cost tracking
        self.request_count = 0
        self.total_cost = 0.0
        self.cost_history = []
        
        # Initialize LLM based on configuration and availability
        self.llm_provider = self._setup_smart_llm()
        self.fallback_llm = self._setup_fallback_llm()
        
        # Memory and other components (keep existing structure)
        super().__init__(config, rag_engine, tools)
        
        logger.info(f"Pragmatic agent initialized", 
                   multi_provider=self._is_multi_provider_enabled(),
                   cost_tracking=config.enable_cost_tracking)
    
    def _is_multi_provider_enabled(self) -> bool:
        """Check if multi-provider mode should be enabled"""
        return (
            self.config.enable_multi_provider and 
            LITELLM_AVAILABLE and 
            os.getenv("ENABLE_MULTI_PROVIDER", "false").lower() == "true"
        )
    
    def _setup_smart_llm(self):
        """Setup LLM with smart provider selection"""
        
        if self._is_multi_provider_enabled():
            logger.info("Initializing multi-provider LLM with LiteLLM")
            return self._setup_litellm_router()
        else:
            logger.info("Initializing single-provider LLM with LangChain")
            return self._setup_langchain_llm()
    
    def _setup_litellm_router(self):
        """Setup LiteLLM router with basic providers"""
        try:
            # Simple router configuration
            router_config = [
                {
                    "model_name": "primary",
                    "litellm_params": {
                        "model": self.config.primary_model,
                        "api_key": os.getenv("OPENAI_API_KEY")
                    }
                }
            ]
            
            # Add Claude if available
            if os.getenv("ANTHROPIC_API_KEY"):
                router_config.append({
                    "model_name": "claude",
                    "litellm_params": {
                        "model": "claude-3-sonnet-20240229",
                        "api_key": os.getenv("ANTHROPIC_API_KEY")
                    }
                })
            
            # Add Gemini if available  
            if os.getenv("GOOGLE_API_KEY"):
                router_config.append({
                    "model_name": "gemini",
                    "litellm_params": {
                        "model": "gemini-pro",
                        "api_key": os.getenv("GOOGLE_API_KEY")
                    }
                })
            
            return litellm.Router(
                model_list=router_config,
                fallbacks=[{"primary": ["claude", "gemini"]}] if len(router_config) > 1 else []
            )
            
        except Exception as e:
            logger.warning(f"Failed to setup LiteLLM router: {e}")
            return self._setup_langchain_llm()
    
    def _setup_langchain_llm(self):
        """Setup traditional LangChain LLM"""
        try:
            return ChatOpenAI(
                model=self.config.primary_model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
        except Exception as e:
            logger.error(f"Failed to setup LangChain LLM: {e}")
            raise
    
    def _setup_fallback_llm(self):
        """Setup fallback LLM for reliability"""
        if not self.config.enable_fallbacks:
            return None
            
        try:
            return ChatOpenAI(
                model=self.config.fallback_model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
        except Exception as e:
            logger.warning(f"Failed to setup fallback LLM: {e}")
            return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def smart_generate(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Smart generation with fallbacks and cost tracking
        """
        start_time = datetime.now()
        
        try:
            # Try primary LLM
            response = await self._generate_with_provider(
                self.llm_provider, messages, **kwargs
            )
            
            # Track success
            self._track_request(response, start_time, "primary")
            return response
            
        except Exception as primary_error:
            logger.warning(f"Primary LLM failed: {primary_error}")
            
            # Try fallback if available
            if self.fallback_llm:
                try:
                    logger.info("Attempting fallback LLM")
                    response = await self._generate_with_provider(
                        self.fallback_llm, messages, **kwargs
                    )
                    
                    # Track fallback usage
                    self._track_request(response, start_time, "fallback")
                    return response
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback LLM also failed: {fallback_error}")
            
            # Both failed, re-raise original error
            raise primary_error
    
    async def _generate_with_provider(
        self, 
        provider, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Generate with specific provider"""
        
        if self._is_multi_provider_enabled() and hasattr(provider, 'acompletion'):
            # LiteLLM path
            response = await provider.acompletion(
                model="primary",  # Use configured primary model
                messages=messages,
                **kwargs
            )
            
            return {
                "content": response.choices[0].message.content,
                "provider": "litellm",
                "model": response.model,
                "usage": response.usage.dict() if response.usage else {},
                "cost": self._estimate_cost(response.usage) if response.usage else 0.0
            }
            
        else:
            # LangChain path
            response = await provider.agenerate([messages])
            content = response.generations[0][0].text
            
            # Estimate usage for cost tracking
            estimated_tokens = len(content.split()) * 1.3  # Rough estimate
            
            return {
                "content": content,
                "provider": "langchain",
                "model": self.config.primary_model,
                "usage": {
                    "total_tokens": estimated_tokens,
                    "prompt_tokens": len(str(messages).split()) * 1.3,
                    "completion_tokens": len(content.split()) * 1.3
                },
                "cost": self._estimate_cost_simple(estimated_tokens)
            }
    
    def _estimate_cost(self, usage) -> float:
        """Estimate cost from usage stats"""
        if not usage:
            return 0.0
        
        # GPT-4 pricing (approximate)
        prompt_cost = usage.get("prompt_tokens", 0) * 0.00003
        completion_cost = usage.get("completion_tokens", 0) * 0.00006
        return prompt_cost + completion_cost
    
    def _estimate_cost_simple(self, total_tokens: float) -> float:
        """Simple cost estimation"""
        return total_tokens * 0.00003  # Average cost per token
    
    def _track_request(self, response: Dict[str, Any], start_time: datetime, provider_type: str):
        """Track request for analytics"""
        if not self.config.enable_cost_tracking:
            return
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        cost = response.get("cost", 0.0)
        
        # Update counters
        self.request_count += 1
        self.total_cost += cost
        
        # Store history
        self.cost_history.append({
            "timestamp": end_time.isoformat(),
            "provider_type": provider_type,
            "provider": response.get("provider"),
            "model": response.get("model"),
            "cost": cost,
            "duration": duration,
            "tokens": response.get("usage", {}).get("total_tokens", 0)
        })
        
        # Keep only recent history (last 100 requests)
        if len(self.cost_history) > 100:
            self.cost_history = self.cost_history[-100:]
        
        logger.debug(f"Request tracked: ${cost:.4f} in {duration:.2f}s using {provider_type}")
    
    async def execute_task(self, task: AgentTask) -> AgentTask:
        """
        Execute task with enhanced capabilities but maintain existing interface
        """
        self.current_task = task
        start_time = datetime.now()
        
        try:
            logger.info(f"Starting pragmatic task execution", task_id=task.id)
            
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            task.updated_at = datetime.utcnow()
            
            # Get RAG context if available
            context = ""
            if self.rag_engine:
                context = await self._get_rag_context(task.input_data)
            
            # Execute core logic (maintains existing interface)
            result = await self._execute_core_logic(task.input_data, context)
            
            # Enhance result with pragmatic features
            result = await self._enhance_result_pragmatically(result, task.input_data)
            
            # Update task with results
            task.output_data = result
            task.status = TaskStatus.COMPLETED
            task.updated_at = datetime.utcnow()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Pragmatic task execution completed", 
                       task_id=task.id, 
                       execution_time=execution_time,
                       requests_made=self.request_count,
                       total_cost=self.total_cost)
            
        except Exception as e:
            logger.error(f"Pragmatic task execution failed", task_id=task.id, error=str(e))
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            task.updated_at = datetime.utcnow()
        
        return task
    
    async def _enhance_result_pragmatically(
        self, 
        result: Dict[str, Any], 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add pragmatic enhancements to results"""
        
        # Add cost and performance metrics
        result["pragmatic_metrics"] = {
            "total_requests": self.request_count,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_request": round(self.total_cost / max(1, self.request_count), 4),
            "multi_provider_enabled": self._is_multi_provider_enabled(),
            "fallback_available": self.fallback_llm is not None
        }
        
        # Add provider information
        if self.cost_history:
            last_request = self.cost_history[-1]
            result["last_request_info"] = {
                "provider": last_request["provider"],
                "model": last_request["model"],
                "cost": last_request["cost"],
                "duration": last_request["duration"]
            }
        
        return result
    
    def get_cost_analytics(self) -> Dict[str, Any]:
        """Get detailed cost analytics"""
        if not self.cost_history:
            return {"message": "No cost data available"}
        
        # Calculate analytics
        total_cost = sum(req["cost"] for req in self.cost_history)
        avg_cost = total_cost / len(self.cost_history)
        avg_duration = sum(req["duration"] for req in self.cost_history) / len(self.cost_history)
        
        # Provider breakdown
        provider_stats = {}
        for req in self.cost_history:
            provider = req["provider_type"]
            if provider not in provider_stats:
                provider_stats[provider] = {"count": 0, "cost": 0.0}
            provider_stats[provider]["count"] += 1
            provider_stats[provider]["cost"] += req["cost"]
        
        return {
            "total_requests": len(self.cost_history),
            "total_cost": round(total_cost, 4),
            "average_cost_per_request": round(avg_cost, 4),
            "average_duration": round(avg_duration, 2),
            "provider_breakdown": provider_stats,
            "multi_provider_enabled": self._is_multi_provider_enabled(),
            "cost_savings_potential": self._calculate_savings_potential()
        }
    
    def _calculate_savings_potential(self) -> Dict[str, Any]:
        """Calculate potential savings with multi-provider setup"""
        if not self.cost_history or self._is_multi_provider_enabled():
            return {"message": "Multi-provider already enabled or no data"}
        
        current_avg_cost = sum(req["cost"] for req in self.cost_history) / len(self.cost_history)
        
        # Estimate savings with cheaper alternatives
        estimated_savings = current_avg_cost * 0.3  # Conservative 30% savings estimate
        monthly_savings = estimated_savings * len(self.cost_history) * 30 / max(1, len(self.cost_history))
        
        return {
            "current_avg_cost": round(current_avg_cost, 4),
            "estimated_savings_per_request": round(estimated_savings, 4),
            "estimated_monthly_savings": round(monthly_savings, 2),
            "recommendation": "Consider enabling multi-provider mode" if monthly_savings > 10 else "Current setup is cost-effective"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Enhanced health check"""
        health_status = await super().health_check()
        
        # Add pragmatic metrics
        health_status.update({
            "pragmatic_features": {
                "multi_provider_enabled": self._is_multi_provider_enabled(),
                "fallback_enabled": self.fallback_llm is not None,
                "cost_tracking_enabled": self.config.enable_cost_tracking,
                "litellm_available": LITELLM_AVAILABLE
            },
            "usage_stats": {
                "total_requests": self.request_count,
                "total_cost": round(self.total_cost, 4),
                "average_cost": round(self.total_cost / max(1, self.request_count), 4)
            }
        })
        
        return health_status


# Factory function for easy instantiation
def create_pragmatic_agent(
    agent_type: str,
    enable_multi_provider: bool = None,
    **kwargs
) -> PragmaticEnhancedAgent:
    """Create a pragmatic enhanced agent with smart defaults"""
    
    # Auto-detect multi-provider based on environment
    if enable_multi_provider is None:
        enable_multi_provider = (
            LITELLM_AVAILABLE and 
            os.getenv("ENABLE_MULTI_PROVIDER", "false").lower() == "true"
        )
    
    config = PragmaticAgentConfig(
        name=f"Pragmatic {agent_type.title()} Agent",
        description=f"Enhanced {agent_type} agent with smart provider selection",
        enable_multi_provider=enable_multi_provider,
        **kwargs
    )
    
    return PragmaticEnhancedAgent(config)