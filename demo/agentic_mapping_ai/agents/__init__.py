"""
Agents package for Agentic Mapping AI Platform
Contains all AI agents for different tasks including enhanced v2 agents
"""

# Base and core agents
from .base_agent import BaseAgent, AgentConfig, AgentFactory
from .metadata_validator import MetadataValidatorAgent
from .code_generator import CodeGeneratorAgent  
from .orchestrator import OrchestratorAgent

# Enhanced v2 agents (most advanced)
from .enhanced_orchestrator_v2 import EnhancedOrchestrator
from .enhanced_metadata_validator_v2 import create_enhanced_metadata_validator
from .enhanced_code_generator_v2 import create_enhanced_code_generator
from .enhanced_base_agent import EnhancedAgentConfig

# Additional enhanced agents
from .enhanced_agent_v2 import EnhancedAgentV2
from .enhanced_metadata_validator import EnhancedMetadataValidator
from .enhanced_orchestrator_v2 import EnhancedOrchestratorV2
from .pragmatic_enhanced_agent import PragmaticEnhancedAgent

# Specialized agents
from .transformation_agent import TransformationAgent
from .pyspark_code_generator import PySparkCodeGenerator
from .goldref_validator import GoldRefValidator

# Test generator (if available)
try:
    from .test_generator import TestGeneratorAgent
    TEST_GENERATOR_AVAILABLE = True
except ImportError:
    TEST_GENERATOR_AVAILABLE = False

__all__ = [
    # Base and core agents
    "BaseAgent",
    "AgentConfig", 
    "AgentFactory",
    "MetadataValidatorAgent",
    "CodeGeneratorAgent",
    "OrchestratorAgent",
    
    # Enhanced v2 agents (most advanced)
    "EnhancedOrchestrator",
    "create_enhanced_metadata_validator",
    "create_enhanced_code_generator", 
    "EnhancedAgentConfig",
    
    # Additional enhanced agents
    "EnhancedAgentV2",
    "EnhancedMetadataValidator",
    "EnhancedOrchestratorV2",
    "PragmaticEnhancedAgent",
    
    # Specialized agents
    "TransformationAgent",
    "PySparkCodeGenerator",
    "GoldRefValidator",
]

# Add test generator if available
if TEST_GENERATOR_AVAILABLE:
    __all__.append("TestGeneratorAgent")