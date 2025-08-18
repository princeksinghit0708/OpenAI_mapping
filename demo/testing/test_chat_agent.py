#!/usr/bin/env python3
"""
Chat Agent Testing Script
Tests the conversational AI agent functionality
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_chat_agent_creation():
    """Test if chat agent can be created"""
    print("🧪 Test 1: Chat Agent Creation")
    print("=" * 40)
    
    try:
        from agentic_mapping_ai.agents.chat_agent import ConversationalAgent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        
        # Create config
        config = AgentConfig(
            name='test_agent',
            description='Test agent for validation',
            model='claude-3-7-sonnet@20250219',
            temperature=0.1
        )
        
        # Create agent
        agent = ConversationalAgent(config)
        print("✅ Chat agent created successfully!")
        print(f"Agent type: {agent.get_agent_type()}")
        print(f"System prompt: {agent._get_system_prompt()[:100]}...")
        
        return True, agent
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_chat_agent_response(agent):
    """Test if chat agent can generate responses"""
    print("\n🧪 Test 2: Chat Agent Response Generation")
    print("=" * 40)
    
    try:
        # Test context
        context = {
            'session_id': 'test123',
            'user_intent': 'testing',
            'current_task': None,
            'uploaded_files': [],
            'workflow_status': 'idle'
        }
        
        # Test different types of messages
        test_messages = [
            "Hello! What can you help me with?",
            "I need help with data mapping",
            "Can you explain what you do?",
            "How do I upload an Excel file?"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n💬 Test message {i}: {message}")
            
            response = agent.generate_response(message, context)
            
            print(f"✅ Response: {response.message}")
            print(f"✅ Intent: {response.intent}")
            print(f"✅ Confidence: {response.confidence}")
            print(f"✅ Actions: {len(response.suggested_actions)} suggested")
        
        return True
        
    except Exception as e:
        print(f"❌ Response generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_agent_intent_detection(agent):
    """Test intent detection capabilities"""
    print("\n🧪 Test 3: Intent Detection")
    print("=" * 40)
    
    try:
        context = {
            'session_id': 'test123',
            'user_intent': 'testing',
            'current_task': None,
            'uploaded_files': [],
            'workflow_status': 'idle'
        }
        
        # Test different intents
        intent_tests = [
            ("I want to upload a file", "upload"),
            ("Generate some code for me", "generate"),
            ("Validate my data", "validate"),
            ("Run the workflow", "workflow"),
            ("Create test cases", "test"),
            ("I need help", "help"),
            ("What's the status?", "status"),
            ("Hello there", "greeting"),
            ("Thank you", "thanks")
        ]
        
        for message, expected_intent in intent_tests:
            response = agent.generate_response(message, context)
            detected_intent = response.intent
            
            status = "✅" if detected_intent == expected_intent else "⚠️"
            print(f"{status} '{message}' → Detected: {detected_intent} (Expected: {expected_intent})")
        
        return True
        
    except Exception as e:
        print(f"❌ Intent detection test failed: {e}")
        return False

def test_chat_agent_async_methods(agent):
    """Test async methods"""
    print("\n🧪 Test 4: Async Method Testing")
    print("=" * 40)
    
    try:
        import asyncio
        
        async def test_async():
            # Test async execution
            input_data = {
                "message": "Hello, test message",
                "context": {
                    "session_id": "test123",
                    "user_intent": "testing"
                }
            }
            
            result = await agent._execute_core_logic(input_data, "")
            print(f"✅ Async execution result: {result}")
            return True
        
        # Run async test
        success = asyncio.run(test_async())
        return success
        
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_chat_agent_tests():
    """Run all chat agent tests"""
    print("🚀 Chat Agent Testing Suite")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Creation
    success, agent = test_chat_agent_creation()
    results['creation'] = success
    
    if success and agent:
        # Test 2: Response generation
        results['response_generation'] = test_chat_agent_response(agent)
        
        # Test 3: Intent detection
        results['intent_detection'] = test_chat_agent_intent_detection(agent)
        
        # Test 4: Async methods
        results['async_methods'] = test_chat_agent_async_methods(agent)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CHAT AGENT TEST RESULTS")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n🎯 SUMMARY")
    print("=" * 50)
    
    if all(results.values()):
        print("🎉 All tests passed! Chat agent is fully functional!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return results

if __name__ == "__main__":
    run_chat_agent_tests()
