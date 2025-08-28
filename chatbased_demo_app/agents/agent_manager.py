#!/usr/bin/env python3
"""
Agent Manager for Chat-Based Demo
Manages and integrates all available AI agents from the consolidated agents directory
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio

class AgentManager:
    """
    Manages all available AI agents for the chat-based demo
    Uses the consolidated agents structure from agentic_mapping_ai/agents/
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
        """Discover all available agents from the consolidated structure"""
        print("Discovering available AI agents from consolidated structure...")
        
        # Check consolidated agents directory
        consolidated_agents_dir = Path(__file__).parent.parent.parent / "agentic_mapping_ai" / "agents"
        
        self.available_agents = []
        
        if consolidated_agents_dir.exists():
            # Discover agents by category
            categories = ['core', 'enhanced_v2', 'enhanced', 'basic', 'specialized', 'chat']
            
            for category in categories:
                category_dir = consolidated_agents_dir / category
                if category_dir.exists():
                    agent_files = list(category_dir.glob("*.py"))
                    init_files = [f for f in agent_files if f.name == "__init__.py"]
                    agent_files = [f for f in agent_files if f.name != "__init__.py"]
                    
                    if agent_files:
                        print(f"Found {len(agent_files)} agents in {category}/")
                        self.available_agents.extend([f"{category}:{agent.stem}" for agent in agent_files])
        else:
            print("Consolidated agents directory not found")
        
        print(f"Total agents discovered: {len(self.available_agents)}")
    
    def _initialize_agents(self):
        """Initialize available agents from consolidated structure"""
        print("Initializing AI agents from consolidated structure...")
        
        try:
            # Try to import from consolidated agents directory
            self._import_consolidated_agents()
        except Exception as e:
            print(f"Consolidated agents import failed: {e}")
            try:
                # Fallback to demo agents
                self._import_demo_agents()
            except Exception as e:
                print(f"Demo agents import failed: {e}")
                self._setup_fallback_agents()
    
    def _import_consolidated_agents(self):
        """Import agents from consolidated agents directory"""
        try:
            # Add parent directory to path for imports
            parent_dir = Path(__file__).parent.parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            print(f"Added to path: {parent_dir}")
            
            # Import from consolidated agents
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
            
            # Store agent classes
            self.agents['orchestrator'] = EnhancedOrchestrator
            self.agents['metadata_validator'] = create_enhanced_metadata_validator
            self.agents['code_generator'] = create_enhanced_code_generator
            self.agents['config'] = EnhancedAgentConfig
            
            # Store additional agents
            self.agents['base_agent'] = BaseAgent
            self.agents['enhanced_agent_v2_config'] = EnhancedAgentV2Config
            self.agents['enhanced_base_agent'] = EnhancedBaseAgent
            self.agents['pragmatic_enhanced'] = PragmaticEnhancedAgent
            self.agents['basic_code_generator'] = CodeGeneratorAgent
            self.agents['basic_metadata_validator'] = MetadataValidatorAgent
            self.agents['basic_orchestrator'] = OrchestratorAgent
            self.agents['goldref_validator'] = GoldRefValidator
            self.agents['pyspark_generator'] = PySparkCodeGenerator
            self.agents['transformation_agent'] = TransformationAgent
            self.agents['test_generator'] = TestGeneratorAgent
            self.agents['chat_agent'] = ChatAgent
            
            self.agents_source = "consolidated"
            print("Successfully imported all agents from consolidated structure")
            
        except Exception as e:
            raise Exception(f"Failed to import consolidated agents: {e}")
    
    def _import_demo_agents(self):
        """Import agents from demo directory as fallback"""
        try:
            # Add parent directory to path for imports
            parent_dir = Path(__file__).parent.parent.parent
            if str(parent_dir) not in sys.path:
                sys.path.insert(0, str(parent_dir))
            
            print(f"Added to path: {parent_dir}")
            
            # Import demo agents
            from demo.agentic_mapping_ai.agents import (
                EnhancedOrchestrator,
                MetadataValidatorAgent,
                CodeGeneratorAgent,
                TestGeneratorAgent,
                EnhancedAgentConfig
            )
            
            # Store agent classes
            self.agents['orchestrator'] = EnhancedOrchestrator
            self.agents['metadata_validator'] = MetadataValidatorAgent
            self.agents['code_generator'] = CodeGeneratorAgent
            self.agents['test_generator'] = TestGeneratorAgent
            self.agents['config'] = EnhancedAgentConfig
            
            self.agents_source = "demo"
            print("Successfully imported demo agents as fallback")
            
        except Exception as e:
            raise Exception(f"Failed to import demo agents: {e}")
    
    def _setup_fallback_agents(self):
        """Setup fallback agents when imports fail"""
        print("Setting up fallback agents...")
        
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
        
        print("Fallback agents configured")
    
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
        print("Testing all AI agents...")
        
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
        
        print("Agent testing completed")
        return test_results
    
    def get_agent_info(self) -> str:
        """Get formatted agent information"""
        info = f"""AI Agent Status Report

Agent Source: {self.agents_source}
Total Agents: {len(self.agents)}
Available Agents: {', '.join(self.agents.keys())}

Agent Details:"""
        
        for agent_type, agent in self.agents.items():
            agent_class = type(agent).__name__
            info += f"\n   • {agent_type}: {agent_class} ({self.agents_source})"
        
        info += f"""

Integration Status: {'Fully Integrated' if self.agents_source != 'fallback' else 'Fallback Mode'}
Ready for: {'Production Use' if self.agents_source == 'consolidated' else 'Demo/Testing' if self.agents_source == 'demo' else 'Basic Operations'}"""
        
        return info

# Create global agent manager instance
agent_manager = AgentManager()

# Export for easy access
__all__ = ['AgentManager', 'agent_manager']
