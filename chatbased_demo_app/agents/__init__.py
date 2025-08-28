"""
Chat-Based Demo Agents Integration
Imports and integrates all available AI agents from the consolidated agents directory
"""

import sys
import os
from pathlib import Path

# Add parent directories to path for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir))

# Import from main consolidated agentic_mapping_ai directory
try:
    from agentic_mapping_ai.agents import (
        # Core and base agents
        BaseAgent, AgentConfig, AgentFactory,
        EnhancedAgentConfig, EnhancedAgentV2Config, EnhancedBaseAgent,
        
        # Enhanced V2 agents (most advanced)
        EnhancedOrchestrator,
        create_enhanced_metadata_validator,
        create_enhanced_code_generator,
        
        # Enhanced agents
        PragmaticEnhancedAgent,
        
        # Basic agents
        CodeGeneratorAgent,
        MetadataValidatorAgent,
        OrchestratorAgent,
        
        # Specialized agents
        GoldRefValidator,
        PySparkCodeGenerator,
        TransformationAgent,
        
        # Chat-specific agents
        TestGeneratorAgent,
        ChatAgent
    )
    
    print("Successfully imported all agents from consolidated main directory")
    AGENTS_SOURCE = "main_consolidated"
    
except ImportError as e:
    print(f"Main consolidated agents import failed: {e}")
    print("Falling back to demo agents...")
    
    # Fallback to demo agents
    try:
        from demo.agentic_mapping_ai.agents import (
            EnhancedOrchestrator,
            MetadataValidatorAgent,
            CodeGeneratorAgent,
            TestGeneratorAgent,
            EnhancedAgentConfig
        )
        
        print("Successfully imported demo agents")
        AGENTS_SOURCE = "demo"
        
    except ImportError as e2:
        print(f"Demo agents import also failed: {e2}")
        AGENTS_SOURCE = "failed"
        print("All agent imports failed - system may not function properly")

# Export available agents
__all__ = [
    # Core and base agents
    'BaseAgent', 'AgentConfig', 'AgentFactory',
    'EnhancedAgentConfig', 'EnhancedAgentV2Config', 'EnhancedBaseAgent',
    
    # Enhanced V2 agents (most advanced)
    'EnhancedOrchestrator',
    'create_enhanced_metadata_validator',
    'create_enhanced_code_generator',
    
    # Enhanced agents
    'PragmaticEnhancedAgent',
    
    # Basic agents
    'MetadataValidatorAgent',
    'CodeGeneratorAgent',
    'OrchestratorAgent',
    
    # Specialized agents
    'GoldRefValidator',
    'PySparkCodeGenerator',
    'TransformationAgent',
    
    # Chat-specific agents
    'TestGeneratorAgent',
    'ChatAgent',
    
    # System info
    'AGENTS_SOURCE'
]
