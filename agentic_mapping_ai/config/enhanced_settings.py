"""
Enhanced Configuration with LangChain + LiteLLM Support
Provides multi-provider LLM support, advanced agent features, and better scalability
"""

import os
from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, Field
from pathlib import Path


class LiteLLMSettings(BaseSettings):
    """LiteLLM configuration for multi-provider support"""
    
    # Provider configurations - Updated for token-based authentication
    providers: Dict[str, Dict[str, Any]] = Field(default={
        "azure": {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.1,
            "cost_per_token": 0.00003,  # GPT-4 pricing
            "priority": 1,  # Higher priority = preferred
            "auth_type": "token"
        },
        "stellar": {
            "model": "Meta-Llama-3.2-90B-Vision-Instruct",
            "max_tokens": 2000,
            "temperature": 0.1,
            "cost_per_token": 0.000015,
            "priority": 2,
            "auth_type": "token"
        },
        "gemini": {
            "model": "gemini-2.5-pro",
            "max_tokens": 2000,
            "temperature": 0.1,
            "cost_per_token": 0.0000005,  # Gemini pricing
            "priority": 3,
            "auth_type": "token"
        },
        "claude": {
            "model": "claude-3-7-sonnet@20250219",
            "max_tokens": 2000,
            "temperature": 0.1,
            "cost_per_token": 0.000015,  # Claude pricing
            "priority": 4,
            "auth_type": "token"
        }
    })
    
    # Routing configuration
    routing_strategy: str = Field(default="cost_optimized")  # cost_optimized, performance, balanced
    fallback_enabled: bool = Field(default=True)
    max_retries: int = Field(default=3)
    retry_delay: float = Field(default=1.0)
    timeout: float = Field(default=30.0)
    
    # Rate limiting
    rate_limit_rpm: int = Field(default=60)  # Requests per minute
    rate_limit_tpm: int = Field(default=50000)  # Tokens per minute
    
    # Cost management
    max_cost_per_request: float = Field(default=0.50)
    daily_cost_limit: float = Field(default=100.0)
    
    class Config:
        env_prefix = "LITELLM_"


class LangChainSettings(BaseSettings):
    """Enhanced LangChain configuration"""
    
    # Memory configuration
    memory_type: str = Field(default="conversation_buffer_window")  # buffer, summary, entity, window
    memory_window_size: int = Field(default=10)
    memory_persist: bool = Field(default=True)
    memory_storage_path: str = Field(default="./data/memory")
    
    # Prompt template configuration
    template_directory: str = Field(default="./templates/langchain")
    custom_templates: Dict[str, str] = Field(default={})
    
    # Chain configuration
    chain_type: str = Field(default="sequential")  # sequential, parallel, conditional
    max_chain_length: int = Field(default=10)
    chain_timeout: float = Field(default=300.0)
    
    # Tool integration
    enable_tools: bool = Field(default=True)
    tool_timeout: float = Field(default=30.0)
    max_tool_iterations: int = Field(default=5)
    
    # Observability
    enable_tracing: bool = Field(default=True)
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = Field(default="agentic-mapping-ai")
    
    # Caching
    enable_caching: bool = Field(default=True)
    cache_ttl: int = Field(default=3600)  # 1 hour
    
    class Config:
        env_prefix = "LANGCHAIN_"


class EnhancedAgentSettings(BaseSettings):
    """Enhanced agent configuration with LangChain + LiteLLM"""
    
    # Agent types and their preferred models
    agent_model_mapping: Dict[str, Dict[str, Any]] = Field(default={
        "metadata_validator": {
            "primary_model": "openai",
            "fallback_models": ["anthropic", "google"],
            "task_complexity": "medium",
            "max_cost": 0.10
        },
        "code_generator": {
            "primary_model": "openai", 
            "fallback_models": ["anthropic"],
            "task_complexity": "high",
            "max_cost": 0.30
        },
        "orchestrator": {
            "primary_model": "anthropic",
            "fallback_models": ["openai", "google"],
            "task_complexity": "medium",
            "max_cost": 0.20
        },
        "test_generator": {
            "primary_model": "google",
            "fallback_models": ["openai", "anthropic"],
            "task_complexity": "low",
            "max_cost": 0.05
        }
    })
    
    # Multi-agent coordination
    enable_parallel_execution: bool = Field(default=True)
    max_concurrent_agents: int = Field(default=5)
    agent_communication_enabled: bool = Field(default=True)
    
    # Advanced features
    enable_self_reflection: bool = Field(default=True)
    enable_planning: bool = Field(default=True)
    enable_learning: bool = Field(default=True)
    
    class Config:
        env_prefix = "ENHANCED_AGENT_"


class ObservabilitySettings(BaseSettings):
    """Enhanced monitoring and observability"""
    
    # Metrics
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)
    custom_metrics: List[str] = Field(default=[
        "llm_requests_total",
        "llm_tokens_used",
        "llm_cost_usd",
        "agent_execution_time",
        "workflow_success_rate"
    ])
    
    # Tracing
    enable_tracing: bool = Field(default=True)
    trace_sample_rate: float = Field(default=0.1)
    
    # Logging
    log_level: str = Field(default="INFO")
    structured_logging: bool = Field(default=True)
    log_llm_requests: bool = Field(default=True)
    log_retention_days: int = Field(default=30)
    
    # Alerting
    enable_alerts: bool = Field(default=True)
    alert_on_errors: bool = Field(default=True)
    alert_on_cost_threshold: bool = Field(default=True)
    cost_alert_threshold: float = Field(default=50.0)
    
    class Config:
        env_prefix = "OBSERVABILITY_"


class EnhancedAppSettings(BaseSettings):
    """Enhanced application settings with all improvements"""
    
    # Basic app info
    name: str = Field(default="Agentic Mapping AI Enhanced")
    version: str = Field(default="2.0.0")
    debug: bool = Field(default=False)
    
    # Enhanced configurations
    litellm: LiteLLMSettings = LiteLLMSettings()
    langchain: LangChainSettings = LangChainSettings()
    agents: EnhancedAgentSettings = EnhancedAgentSettings()
    observability: ObservabilitySettings = ObservabilitySettings()
    
    # Original configurations (kept for compatibility)
    vector_db_type: str = Field(default="chroma")
    chroma_persist_directory: str = Field(default="./data/chroma_db")
    
    # API settings
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    
    # Performance settings
    enable_async: bool = Field(default=True)
    max_workers: int = Field(default=10)
    request_timeout: float = Field(default=300.0)
    
    # Security settings
    enable_auth: bool = Field(default=False)
    api_key_required: bool = Field(default=False)
    rate_limit_enabled: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
enhanced_settings = EnhancedAppSettings()


def get_optimal_model_for_task(task_type: str, complexity: str = "medium") -> str:
    """Get the optimal model for a specific task"""
    
    # Task complexity to model mapping
    complexity_mapping = {
        "low": ["google", "local", "anthropic"],
        "medium": ["openai", "anthropic", "google"],
        "high": ["openai", "anthropic"]
    }
    
    # Get agent preferences
    agent_config = enhanced_settings.agents.agent_model_mapping.get(task_type, {})
    primary_model = agent_config.get("primary_model", "openai")
    
    # Check if primary model is suitable for complexity
    suitable_models = complexity_mapping.get(complexity, ["openai"])
    
    if primary_model in suitable_models:
        return primary_model
    else:
        return suitable_models[0]


def get_fallback_models(primary_model: str) -> List[str]:
    """Get fallback models for a primary model"""
    
    fallback_mapping = {
        "openai": ["anthropic", "google", "azure"],
        "anthropic": ["openai", "google", "azure"],
        "google": ["openai", "anthropic", "azure"],
        "azure": ["openai", "anthropic", "google"],
        "local": ["google", "anthropic", "openai"]
    }
    
    return fallback_mapping.get(primary_model, ["openai", "anthropic"])


def ensure_enhanced_directories():
    """Ensure all enhanced directories exist"""
    directories = [
        "./data/memory",
        "./data/traces",
        "./data/metrics",
        "./logs/structured",
        "./templates/langchain",
        "./cache/llm",
        "./monitoring/dashboards"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


# Initialize enhanced directories on import
ensure_enhanced_directories()