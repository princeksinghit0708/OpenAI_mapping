#!/usr/bin/env python3
"""
🤖 Agent Manager for Chat-Based Demo
Manages and integrates all available AI agents from different directories
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio

class AgentManager:
    """
    Manages all available AI agents for the chat-based demo
    """
    
    def __init__(self):
        self.agents = {}
        self.agent_status = {}
        self.available_agents = []
        self.agents_source = "unknown"
        
        # Initialize agent discovery
        self._discover_agents()
        self._initialize_agents()
    
    def _discover_agents(self):
        """Discover all available agents from different directories"""
        print("🔍 Discovering available AI agents...")
        
        # Check main agentic_mapping_ai directory
        main_agents_dir = Path(__file__).parent.parent.parent / "agentic_mapping_ai" / "agents"
        demo_agents_dir = Path(__file__).parent.parent.parent / "demo" / "agentic_mapping_ai" / "agents"
        
        self.available_agents = []
        
        # Check main agents (most advanced)
        if main_agents_dir.exists():
            main_agents = list(main_agents_dir.glob("*.py"))
            if main_agents:
                print(f"✅ Found {len(main_agents)} agents in main directory")
                self.available_agents.extend([f"main:{agent.stem}" for agent in main_agents])
        
        # Check demo agents
        if demo_agents_dir.exists():
            demo_agents = list(demo_agents_dir.glob("*.py"))
            if demo_agents:
                print(f"✅ Found {len(demo_agents)} agents in demo directory")
                self.available_agents.extend([f"demo:{agent.stem}" for agent in demo_agents])
        
        print(f"📊 Total agents discovered: {len(self.available_agents)}")
    
    def _initialize_agents(self):
        """Initialize available agents"""
        print("🚀 Initializing AI agents...")
        
        try:
            # Try to import from main directory first (most advanced)
            self._import_main_agents()
        except Exception as e:
            print(f"⚠️  Main agents import failed: {e}")
            try:
                # Fallback to demo agents
                self._import_demo_agents()
            except Exception as e:
                print(f"⚠️  Demo agents import failed: {e}")
                self._setup_fallback_agents()
    
    def _import_main_agents(self):
        """Import agents from main agentic_mapping_ai directory"""
        try:
            # Add main agents directory to path
            main_agents_path = Path(__file__).parent.parent.parent / "agentic_mapping_ai" / "agents"
            main_agents_path_str = str(main_agents_path)
            
            if main_agents_path_str not in sys.path:
                sys.path.insert(0, main_agents_path_str)
            
            print(f"🔧 Added to path: {main_agents_path_str}")
            
            # Import enhanced agents
            import enhanced_orchestrator_v2
            import enhanced_metadata_validator_v2
            import enhanced_code_generator_v2
            import enhanced_base_agent
            
            # Store agent classes
            self.agents['orchestrator'] = enhanced_orchestrator_v2.EnhancedOrchestrator
            self.agents['metadata_validator'] = enhanced_metadata_validator_v2.create_enhanced_metadata_validator
            self.agents['code_generator'] = enhanced_code_generator_v2.create_enhanced_code_generator
            self.agents['config'] = enhanced_base_agent.EnhancedAgentConfig
            
            self.agents_source = "main_advanced"
            print("✅ Successfully imported advanced agents from main directory")
            
        except Exception as e:
            raise Exception(f"Failed to import main agents: {e}")
    
    def _import_demo_agents(self):
        """Import agents from demo directory"""
        try:
            # Add demo agents directory to path
            demo_agents_path = Path(__file__).parent.parent.parent / "demo" / "agentic_mapping_ai" / "agents"
            demo_agents_path_str = str(demo_agents_path)
            
            if demo_agents_path_str not in sys.path:
                sys.path.insert(0, demo_agents_path_str)
            
            print(f"🔧 Added to path: {demo_agents_path_str}")
            
            # Import demo agents
            import enhanced_orchestrator_v2
            import metadata_validator
            import code_generator
            import test_generator
            
            # Store agent classes
            self.agents['orchestrator'] = enhanced_orchestrator_v2.EnhancedOrchestrator
            self.agents['metadata_validator'] = metadata_validator.MetadataValidatorAgent
            self.agents['code_generator'] = code_generator.CodeGeneratorAgent
            self.agents['test_generator'] = test_generator.TestGeneratorAgent
            
            self.agents_source = "demo"
            print("✅ Successfully imported demo agents")
            
        except Exception as e:
            raise Exception(f"Failed to import demo agents: {e}")
    
    def _setup_fallback_agents(self):
        """Setup fallback agents when imports fail"""
        print("⚠️  Setting up fallback agents...")
        
        self.agents_source = "fallback"
        
        # Create mock agents for fallback mode
        class MockAgent:
            def __init__(self, name):
                self.name = name
            
            async def execute_task(self, task):
                return {
                    'success': True,
                    'result': f'Mock {self.name} agent executed task: {task}',
                    'agent_type': 'mock'
                }
        
        self.agents['orchestrator'] = MockAgent("Orchestrator")
        self.agents['metadata_validator'] = MockAgent("Metadata Validator")
        self.agents['code_generator'] = MockAgent("Code Generator")
        self.agents['test_generator'] = MockAgent("Test Generator")
        
        print("✅ Fallback agents configured")
    
    def get_agent(self, agent_type: str):
        """Get a specific agent by type"""
        return self.agents.get(agent_type)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all available agents"""
        return self.agents.copy()
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            'agents_source': self.agents_source,
            'total_agents': len(self.agents),
            'available_agent_types': list(self.agents.keys()),
            'agent_details': {}
        }
        
        for agent_type, agent in self.agents.items():
            status['agent_details'][agent_type] = {
                'type': type(agent).__name__,
                'status': 'active' if agent else 'inactive',
                'source': self.agents_source
            }
        
        return status
    
    async def test_agents(self) -> Dict[str, Any]:
        """Test all available agents"""
        print("🧪 Testing all AI agents...")
        
        test_results = {}
        
        for agent_type, agent in self.agents.items():
            try:
                # Create a simple test task
                test_task = {
                    'task_id': f'test_{agent_type}',
                    'task_type': 'test',
                    'input_data': {'test': True},
                    'status': 'pending'
                }
                
                # Execute test task
                if hasattr(agent, 'execute_task'):
                    result = await agent.execute_task(test_task)
                    test_results[agent_type] = {
                        'status': 'success',
                        'result': result
                    }
                else:
                    test_results[agent_type] = {
                        'status': 'no_execute_method',
                        'result': f'Agent {agent_type} has no execute_task method'
                    }
                    
            except Exception as e:
                test_results[agent_type] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        print("✅ Agent testing completed")
        return test_results
    
    def get_agent_info(self) -> str:
        """Get formatted agent information"""
        info = f"""🤖 **AI Agent Status Report**

📊 **Agent Source**: {self.agents_source}
🔢 **Total Agents**: {len(self.agents)}
📋 **Available Agents**: {', '.join(self.agents.keys())}

📁 **Agent Details**:"""
        
        for agent_type, agent in self.agents.items():
            agent_class = type(agent).__name__
            info += f"\n   • **{agent_type}**: {agent_class} ({self.agents_source})"
        
        info += f"""

💡 **Integration Status**: {'✅ Fully Integrated' if self.agents_source != 'fallback' else '⚠️ Fallback Mode'}
🚀 **Ready for**: {'Production Use' if self.agents_source == 'main_advanced' else 'Demo/Testing' if self.agents_source == 'demo' else 'Basic Operations'}"""
        
        return info

# Create global agent manager instance
agent_manager = AgentManager()

# Export for easy access
__all__ = ['AgentManager', 'agent_manager']
