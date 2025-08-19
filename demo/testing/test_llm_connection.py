#!/usr/bin/env python3
"""
Simple LLM Connection Test
Tests if agents can connect to llm_service.py and get responses
"""

import sys
import os

# Add the correct paths to import from demo/agentic_mapping_ai
current_dir = os.path.dirname(os.path.abspath(__file__))
demo_dir = os.path.dirname(current_dir)
agentic_dir = os.path.join(demo_dir, "agentic_mapping_ai")

# Add both the agentic_mapping_ai directory and its parent to the path
sys.path.insert(0, agentic_dir)
sys.path.insert(0, demo_dir)

print(f"Python path:")
print(f"  Current dir: {current_dir}")
print(f"  Demo dir: {demo_dir}")
print(f"  Agentic dir: {agentic_dir}")
print(f"  Added to sys.path: {agentic_dir}")

def test_llm_service_import():
    """Test if llm_service can be imported"""
    print("\nTesting LLM Service Import...")
    
    try:
        from llm_service import LLMService
        print("OK: LLM service imported successfully")
        return True
    except ImportError as e:
        print(f"ERROR: Could not import LLM service: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error importing LLM service: {e}")
        return False

def test_llm_service_creation():
    """Test if LLM service can be created"""
    print("\nTesting LLM Service Creation...")
    
    try:
        from llm_service import LLMService
        
        # Try to create the service
        llm_service = LLMService()
        print("OK: LLM service created successfully")
        return llm_service
    except Exception as e:
        print(f"ERROR: Could not create LLM service: {e}")
        return None

def test_basic_response():
    """Test if we can get a basic response"""
    print("\nTesting Basic Response...")
    
    try:
        from llm_service import LLMService
        
        llm_service = LLMService()
        
        # Test with a simple prompt
        test_prompt = "Hello, can you respond with a simple greeting?"
        
        print(f"  Sending prompt: {test_prompt}")
        
        # Try to get a response
        response = llm_service.get_response(test_prompt)
        
        if response:
            print(f"  OK: Got response: {response[:100]}...")
            return True
        else:
            print("  ERROR: No response received")
            return False
            
    except Exception as e:
        print(f"  ERROR: Could not get response: {e}")
        return False

def test_agent_connection():
    """Test if agents can use the LLM service"""
    print("\nTesting Agent Connection...")
    
    try:
        from agents.chat_agent import ConversationalAgent
        from llm_service import LLMService
        
        # Create LLM service
        llm_service = LLMService()
        
        # Create a chat agent
        agent = ConversationalAgent(llm_service=llm_service)
        print("  OK: Chat agent created successfully")
        
        # Test agent response
        test_message = "Hello, I'm testing the agent connection"
        print(f"  Testing agent with: {test_message}")
        
        response = agent.process_message(test_message)
        
        if response:
            print(f"  OK: Agent responded: {response[:100]}...")
            return True
        else:
            print("  ERROR: Agent did not respond")
            return False
            
    except Exception as e:
        print(f"  ERROR: Agent connection failed: {e}")
        return False

def test_claude_model():
    """Test if Claude model is working"""
    print("\nTesting Claude Model...")
    
    try:
        from llm_service import LLMService
        
        llm_service = LLMService()
        
        # Test Claude-specific prompt
        claude_prompt = "You are Claude. Please respond with 'Hello from Claude' and nothing else."
        
        print(f"  Sending Claude prompt: {claude_prompt}")
        
        response = llm_service.get_response(claude_prompt)
        
        if response:
            print(f"  OK: Claude responded: {response}")
            if "claude" in response.lower() or "hello" in response.lower():
                print("  OK: Response appears to be from Claude")
                return True
            else:
                print("  WARNING: Response doesn't seem to be from Claude")
                return False
        else:
            print("  ERROR: No response from Claude")
            return False
            
    except Exception as e:
        print(f"  ERROR: Claude test failed: {e}")
        return False

def main():
    """Main test function"""
    print("LLM Connection Test")
    print("=" * 50)
    
    # Test 1: Import
    import_ok = test_llm_service_import()
    
    if not import_ok:
        print("\nCRITICAL: Cannot import LLM service. Stopping tests.")
        return
    
    # Test 2: Service creation
    service_ok = test_llm_service_creation()
    
    if not service_ok:
        print("\nCRITICAL: Cannot create LLM service. Stopping tests.")
        return
    
    # Test 3: Basic response
    response_ok = test_basic_response()
    
    # Test 4: Agent connection
    agent_ok = test_agent_connection()
    
    # Test 5: Claude model
    claude_ok = test_claude_model()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    print(f"LLM Service Import: {'OK' if import_ok else 'FAILED'}")
    print(f"Service Creation: {'OK' if service_ok else 'FAILED'}")
    print(f"Basic Response: {'OK' if response_ok else 'FAILED'}")
    print(f"Agent Connection: {'OK' if agent_ok else 'FAILED'}")
    print(f"Claude Model: {'OK' if claude_ok else 'FAILED'}")
    
    if claude_ok:
        print("\nSUCCESS: Claude model is working!")
        print("Your agents can connect and get responses.")
    elif response_ok:
        print("\nPARTIAL: Basic LLM responses work but Claude may have issues.")
        print("Check your Claude API configuration.")
    else:
        print("\nFAILED: LLM service is not working.")
        print("Check your API keys and network connection.")

if __name__ == "__main__":
    main()
