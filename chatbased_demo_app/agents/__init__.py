"""
🤖 Chat-Based Demo Agents Integration
Imports and integrates all available AI agents from the parent directories
"""

# Import from main agentic_mapping_ai directory (most advanced)
try:
    from ...agentic_mapping_ai.agents.enhanced_orchestrator_v2 import EnhancedOrchestrator
    from ...agentic_mapping_ai.agents.enhanced_metadata_validator_v2 import create_enhanced_metadata_validator
    from ...agentic_mapping_ai.agents.enhanced_code_generator_v2 import create_enhanced_code_generator
    from ...agentic_mapping_ai.agents.enhanced_base_agent import EnhancedAgentConfig
    
    print("✅ Successfully imported advanced agents from main directory")
    AGENTS_SOURCE = "main_advanced"
    
except ImportError:
    # Fallback to demo agents
    try:
        from ...demo.agentic_mapping_ai.agents.enhanced_orchestrator_v2 import EnhancedOrchestrator
        from ...demo.agentic_mapping_ai.agents.metadata_validator import MetadataValidatorAgent
        from ...demo.agentic_mapping_ai.agents.code_generator import CodeGeneratorAgent
        from ...demo.agentic_mapping_ai.agents.test_generator import TestGeneratorAgent
        
        print("✅ Successfully imported demo agents")
        AGENTS_SOURCE = "demo"
        
    except ImportError:
        print("⚠️  Could not import agents - using fallback mode")
        AGENTS_SOURCE = "fallback"

# Export available agents
__all__ = [
    'EnhancedOrchestrator',
    'create_enhanced_metadata_validator',
    'create_enhanced_code_generator',
    'EnhancedAgentConfig',
    'MetadataValidatorAgent',
    'CodeGeneratorAgent',
    'TestGeneratorAgent',
    'AGENTS_SOURCE'
]
