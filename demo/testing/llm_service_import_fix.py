#!/usr/bin/env python3
"""
Corrected LLM Service Import Script for Office Laptop
This script fixes the import path and creates the LLMService instance correctly
"""

import sys
import os

# Add the correct path to the ai_service_layer directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)  # Go up one more level to reach the main Mapping directory
ai_service_path = os.path.join(parent_parent_dir, 'ai_service_layer')

# Add the path to sys.path
sys.path.append(ai_service_path)

try:
    # Import the LLMService class
    from llm_service import LLMService
    
    # Create an instance of the service
    llm_service = LLMService()
    
    print("✅ LLM Service imported successfully!")
    print(f"Service type: {type(llm_service)}")
    print(f"Available methods: {[m for m in dir(llm_service) if not m.startswith('_')]}")
    
    # Test basic functionality
    print("\n🧪 Testing basic functionality...")
    
    # Test with a simple message
    test_messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Hello! Please respond with "Hello from LLM Service!"'}
    ]
    
    try:
        response = llm_service.call_default_llm(messages=test_messages, temperature=0.1)
        print(f"✅ Test response: {response}")
    except Exception as e:
        print(f"⚠️ Basic test failed (this is expected if helix is not configured): {e}")
    
    print("\n🚀 LLM Service is ready to use!")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Looking for llm_service.py in: {ai_service_path}")
    
    # List files in the directory to help debug
    if os.path.exists(ai_service_path):
        print(f"Files in {ai_service_path}:")
        for file in os.listdir(ai_service_path):
            print(f"  - {file}")
    else:
        print(f"Directory {ai_service_path} does not exist")
        
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
