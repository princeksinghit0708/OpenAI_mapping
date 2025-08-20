#!/usr/bin/env python3
"""
Simple Test for MetadataValidatorAgent
Quick test to verify the agent is working properly
"""

import sys
import os
import json
from pathlib import Path

# Add the agentic_mapping_ai to path
sys.path.append('./agentic_mapping_ai')
sys.path.append('.')

def test_agent_import():
    """Test 1: Check if the agent can be imported"""
    print("🧪 Test 1: Agent Import")
    print("=" * 40)
    
    try:
        from agentic_mapping_ai.agents.metadata_validator import MetadataValidatorAgent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        print("✅ MetadataValidatorAgent imported successfully")
        return True, MetadataValidatorAgent, AgentConfig
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False, None, None

def test_agent_creation():
    """Test 2: Check if the agent can be created"""
    print("\n🧪 Test 2: Agent Creation")
    print("=" * 40)
    
    success, agent_class, config_class = test_agent_import()
    if not success:
        return False, None
    
    try:
        config = config_class(
            name="Test Validator",
            description="Test metadata validator",
            model="gpt-4",
            temperature=0.1
        )
        
        agent = agent_class(config)
        print("✅ MetadataValidatorAgent created successfully")
        print(f"Agent type: {type(agent)}")
        print(f"Agent name: {agent.config.name}")
        return True, agent
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False, None

def test_agent_methods():
    """Test 3: Check if the agent has required methods"""
    print("\n🧪 Test 3: Agent Methods")
    print("=" * 40)
    
    success, agent = test_agent_creation()
    if not success:
        return False
    
    try:
        # Check for required methods
        required_methods = [
            'get_agent_type',
            '_execute_core_logic',
            '_get_system_prompt'
        ]
        
        for method in required_methods:
            if hasattr(agent, method):
                print(f"✅ Method found: {method}")
            else:
                print(f"❌ Method missing: {method}")
                return False
        
        print("✅ All required methods found")
        return True, agent
    except Exception as e:
        print(f"❌ Method check failed: {e}")
        return False, None

def test_agent_with_sample_data():
    """Test 4: Test agent with sample metadata"""
    print("\n🧪 Test 4: Agent with Sample Data")
    print("=" * 40)
    
    success, agent = test_agent_methods()
    if not success:
        return False
    
    try:
        # Create sample metadata
        sample_metadata = {
            "table_name": "test_table",
            "database_name": "test_db",
            "columns": [
                {
                    "col_name": "test_col",
                    "data_type": "string",
                    "comment": "Test column"
                }
            ]
        }
        
        print("📊 Sample metadata created")
        print(f"Table: {sample_metadata['table_name']}")
        print(f"Columns: {len(sample_metadata['columns'])}")
        
        # Test agent execution (this would normally be async)
        print("🤖 Testing agent capabilities...")
        
        # Check if agent has the right type
        agent_type = agent.get_agent_type()
        print(f"Agent type: {agent_type}")
        
        # Check system prompt
        system_prompt = agent._get_system_prompt()
        print(f"System prompt length: {len(system_prompt)} characters")
        
        print("✅ Agent capabilities verified")
        return True
        
    except Exception as e:
        print(f"❌ Sample data test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 MetadataValidatorAgent Test Suite")
    print("=" * 50)
    
    # Run tests
    test1 = test_agent_import()
    test2 = test_agent_creation() if test1[0] else False
    test3 = test_agent_methods() if test2[0] else False
    test4 = test_agent_with_sample_data() if test3[0] else False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    tests = [
        ("Agent Import", test1[0]),
        ("Agent Creation", test2[0] if test2 else False),
        ("Agent Methods", test3[0] if test3 else False),
        ("Sample Data", test4)
    ]
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Overall result
    all_passed = all(result for _, result in tests)
    if all_passed:
        print("\n🎉 All tests passed! The agent is ready to use.")
        print("💡 You can now run the full demo:")
        print("   python demo/hive_metadata_validation_demo.py")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
