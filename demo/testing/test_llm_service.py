#!/usr/bin/env python3
"""
LLM Service Testing Script
Tests the LLM service to verify AI model responses and functionality
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_llm_service_import():
    """Test 1: Check if LLM service can be imported"""
    print("🧪 Test 1: LLM Service Import")
    print("=" * 50)
    
    try:
        from ai_service_layer.llm_service import LLMService
        llm_service = LLMService()
        print("✅ LLM Service imported successfully")
        print(f"Service type: {type(llm_service)}")
        print(f"Available methods: {[m for m in dir(llm_service) if not m.startswith('_')]}")
        return True, llm_service
    except ImportError:
        # Try alternative import path for demo environment
        try:
            sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agentic_mapping_ai'))
            from llm_service import LLMService
            llm_service = LLMService()
            print("✅ LLM Service imported successfully (demo path)")
            print(f"Service type: {type(llm_service)}")
            print(f"Available methods: {[m for m in dir(llm_service) if not m.startswith('_')]}")
            return True, llm_service
        except Exception as e2:
            print(f"❌ Import failed (both paths): {e2}")
            return False, None
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False, None

def test_llm_basic_response(llm_service):
    """Test 2: Basic LLM response generation"""
    print("\n🧪 Test 2: Basic LLM Response")
    print("=" * 50)
    
    try:
        # Test with a simple message
        messages = [
            {'role': 'system', 'content': 'You are a helpful data mapping assistant.'},
            {'role': 'user', 'content': 'Hello! Can you explain what data mapping is in 2 sentences?'}
        ]
        
        print("📤 Sending test message...")
        response = llm_service.call_default_llm(messages=messages, temperature=0.2)
        
        print("✅ LLM Response received:")
        print(f"Response: {response}")
        print(f"Response length: {len(str(response))} characters")
        return True
        
    except Exception as e:
        print(f"❌ Basic response failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm_providers(llm_service):
    """Test 3: Test different LLM providers"""
    print("\n🧪 Test 3: LLM Provider Testing")
    print("=" * 50)
    
    test_messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Say hello in one word.'}
    ]
    
    providers = ['claude', 'azure', 'stellar']
    results = {}
    
    for provider in providers:
        try:
            print(f"\n🔍 Testing {provider.upper()}...")
            
            if provider == 'claude':
                model = 'claude-3-7-sonnet@20250219'
            elif provider == 'azure':
                model = 'gpt-4'
            else:
                model = 'gpt-4'
            
            response = llm_service.query_llm(
                model=model,
                messages=test_messages,
                llm_provider=provider
            )
            
            print(f"✅ {provider.upper()}: {response[:100]}...")
            results[provider] = "SUCCESS"
            
        except Exception as e:
            print(f"❌ {provider.upper()}: {str(e)[:100]}...")
            results[provider] = f"FAILED: {str(e)[:50]}"
    
    return results

def test_chat_agent():
    """Test 4: Test chat agent with LLM integration"""
    print("\n🧪 Test 4: Chat Agent Testing")
    print("=" * 50)
    
    try:
        # Try main import path first
        try:
            from agentic_mapping_ai.agents.chat_agent import ConversationalAgent
            from agentic_mapping_ai.agents.base_agent import AgentConfig
        except ImportError:
            # Try demo path
            sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'agentic_mapping_ai'))
            from agents.chat_agent import ConversationalAgent
            from agents.base_agent import AgentConfig
        
        # Create a test config
        config = AgentConfig(
            name='test_chat_agent',
            description='Test agent for LLM validation',
            model='claude-3-7-sonnet@20250219',
            temperature=0.1
        )
        
        print("🔧 Creating chat agent...")
        chat_agent = ConversationalAgent(config)
        print("✅ Chat agent created successfully")
        
        # Test a simple message
        test_context = {
            'session_id': 'test123',
            'user_intent': 'testing',
            'current_task': None,
            'uploaded_files': [],
            'workflow_status': 'idle'
        }
        
        print("💬 Testing agent response generation...")
        response = chat_agent.generate_response('Hello! What can you help me with?', test_context)
        
        print(f"✅ Agent response: {response.message}")
        print(f"✅ Intent detected: {response.intent}")
        print(f"✅ Confidence: {response.confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chat agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test 5: Test API endpoints if server is running"""
    print("\n🧪 Test 5: API Endpoint Testing")
    print("=" * 50)
    
    try:
        import requests
        
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        print("🏥 Testing health endpoint...")
        health_response = requests.get(f"{base_url}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
            health_data = health_response.json()
            print(f"Health data: {json.dumps(health_data, indent=2)}")
        else:
            print(f"⚠️ Health endpoint returned {health_response.status_code}")
        
        # Test chat endpoint
        print("\n💬 Testing chat endpoint...")
        chat_data = {
            "message": "Hello! Can you explain data mapping in simple terms?",
            "session_id": "test123",
            "agent_type": "conversational"
        }
        
        chat_response = requests.post(
            f"{base_url}/api/v1/chat",
            json=chat_data,
            timeout=10
        )
        
        if chat_response.status_code == 200:
            print("✅ Chat endpoint working")
            chat_result = chat_response.json()
            print(f"Chat response: {json.dumps(chat_result, indent=2)}")
        else:
            print(f"⚠️ Chat endpoint returned {chat_response.status_code}")
            print(f"Response: {chat_response.text}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API server not running. Start it first with:")
        print("   cd demo/agentic_mapping_ai && python run_enhanced_application.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and provide summary"""
    print("🚀 LLM Service & AI Agent Testing Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Import
    success, llm_service = test_llm_service_import()
    results['import'] = success
    
    if success:
        # Test 2: Basic response
        results['basic_response'] = test_llm_basic_response(llm_service)
        
        # Test 3: Providers
        results['providers'] = test_llm_providers(llm_service)
        
        # Test 4: Chat agent
        results['chat_agent'] = test_chat_agent()
    
    # Test 5: API endpoints
    results['api_endpoints'] = test_api_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        if isinstance(result, dict):
            print(f"\n{test_name.upper()}:")
            for provider, status in result.items():
                print(f"  {provider}: {status}")
        else:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name.upper()}: {status}")
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS")
    print("=" * 60)
    
    if results.get('import', False):
        print("✅ LLM Service is working - you can use AI models!")
    else:
        print("❌ Fix LLM Service import issues first")
    
    if results.get('chat_agent', False):
        print("✅ Chat Agent is working - conversational AI is ready!")
    else:
        print("❌ Chat Agent needs attention")
    
    if results.get('api_endpoints', False):
        print("✅ API endpoints are working - web interface is ready!")
    else:
        print("❌ Start the API server to test web interface")
    
    print("\n🚀 Testing complete!")

if __name__ == "__main__":
    run_all_tests()
