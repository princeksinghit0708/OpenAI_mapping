"""
Chat-Based Demo Agents Integration
Imports and integrates all available AI agents from the parent directories
"""

# Import from main agentic_mapping_ai directory (most advanced)
try:
    from ...agentic_mapping_ai.agents import (
        EnhancedOrchestrator,
        create_enhanced_metadata_validator,
        create_enhanced_code_generator,
        EnhancedAgentConfig
    )
    
    print("Successfully imported advanced agents from main directory")
    AGENTS_SOURCE = "main_advanced"
    
except ImportError:
    # Fallback to demo agents
    try:
        from ...demo.agentic_mapping_ai.agents import (
            EnhancedOrchestrator,
            create_enhanced_metadata_validator,
            create_enhanced_code_generator,
            EnhancedAgentConfig,
            MetadataValidatorAgent,
            CodeGeneratorAgent
        )
        
        print("Successfully imported demo agents")
        AGENTS_SOURCE = "demo"
        
    except ImportError:
        print("Could not import agents - using fallback mode")
        AGENTS_SOURCE = "fallback"

# Try to import test generator if available
try:
    from ...demo.agentic_mapping_ai.agents import TestGeneratorAgent
    TEST_GENERATOR_AVAILABLE = True
except ImportError:
    TestGeneratorAgent = None
    TEST_GENERATOR_AVAILABLE = False

# Export available agents
__all__ = [
    'EnhancedOrchestrator',
    'create_enhanced_metadata_validator',
    'create_enhanced_code_generator',
    'EnhancedAgentConfig',
    'MetadataValidatorAgent',
    'CodeGeneratorAgent',
    'AGENTS_SOURCE',
]

# Add test generator if available
if TEST_GENERATOR_AVAILABLE:
    __all__.append('TestGeneratorAgent')
