"""
Agents package for Agentic Mapping AI Platform
Contains all AI agents organized by functionality and capability level
"""

# Core and base agents
from .core import (
    BaseAgent, AgentConfig, AgentFactory,
    EnhancedAgentConfig, EnhancedAgentV2
)

# Enhanced V2 agents (most advanced)
from .enhanced_v2 import (
    EnhancedOrchestrator,
    create_enhanced_metadata_validator,
    create_enhanced_code_generator
)

# Enhanced agents
from .enhanced import PragmaticEnhancedAgent

# Basic agents
from .basic import (
    CodeGeneratorAgent,
    MetadataValidatorAgent,
    OrchestratorAgent
)

# Specialized agents
from .specialized import (
    GoldRefValidator,
    PySparkCodeGenerator,
    TransformationAgent
)

# Chat-specific agents
from .chat import (
    TestGeneratorAgent,
    ChatAgent
)

__all__ = [
    # Core and base agents
    "BaseAgent",
    "AgentConfig", 
    "AgentFactory",
    "EnhancedAgentConfig",
    "EnhancedAgentV2",
    
    # Enhanced V2 agents (most advanced)
    "EnhancedOrchestrator",
    "create_enhanced_metadata_validator",
    "create_enhanced_code_generator",
    
    # Enhanced agents
    "PragmaticEnhancedAgent",
    
    # Basic agents
    "CodeGeneratorAgent",
    "MetadataValidatorAgent",
    "OrchestratorAgent",
    
    # Specialized agents
    "GoldRefValidator",
    "PySparkCodeGenerator",
    "TransformationAgent",
    
    # Chat-specific agents
    "TestGeneratorAgent",
    "ChatAgent"
]