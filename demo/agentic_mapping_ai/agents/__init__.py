"""
Demo Agents Package
Self-contained demo agents that don't depend on main agents directory
"""

# Import local demo agents only
try:
    from .enhanced_orchestrator_v2 import EnhancedOrchestrator
    from .metadata_validator import MetadataValidatorAgent
    from .code_generator import CodeGeneratorAgent
    from .test_generator import TestGeneratorAgent
    from .enhanced_base_agent import EnhancedAgentConfig
    
    AGENTS_SOURCE = "demo_local"
    print("Successfully imported demo agents locally")
    
except ImportError as e:
    print(f"Demo agents import failed: {e}")
    AGENTS_SOURCE = "failed"
    print("All agent imports failed - system may not function properly")

# Export available agents
__all__ = [
    'EnhancedOrchestrator',
    'MetadataValidatorAgent',
    'CodeGeneratorAgent',
    'TestGeneratorAgent',
    'EnhancedAgentConfig',
    'AGENTS_SOURCE'
]