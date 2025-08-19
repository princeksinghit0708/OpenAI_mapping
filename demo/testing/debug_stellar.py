#!/usr/bin/env python3
"""
Debug STELLAR Connection Script
This script helps identify why STELLAR is failing in test_llm_service.py
"""

import sys
import os

# Add the correct path to the ai_service_layer directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
ai_service_path = os.path.join(parent_parent_dir, 'ai_service_layer')

# Add the path to sys.path
sys.path.append(ai_service_path)

try:
    from llm_service import LLMService
    
    print("✅ LLM Service imported successfully!")
    
    # Create instance
    llm_service = LLMService()
    
    print(f"🔧 Service type: {type(llm_service)}")
    print(f"🔧 STELLAR URL: {llm_service.stellar_url}")
    print(f"🔧 STELLAR URL: {llm_service.stellar_url}")
    print(f"🔧 Token method available: {'Yes' if hasattr(llm_service, '_get_fresh_token') else 'No'}")
    
    # Test STELLAR with the correct model
    print("\n🧪 Testing STELLAR connection...")
    
    test_messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Say hello in one word.'}
    ]
    
    try:
        response = llm_service.query_llm(
            model='Meta-Llama-3.2-90B-Vision-Instruct',
            messages=test_messages,
            llm_provider='stellar',
            temperature=0.1
        )
        
        print(f"✅ STELLAR Response: {response}")
        
    except Exception as e:
        print(f"❌ STELLAR Error: {e}")
        print(f"❌ Error type: {type(e)}")
        
        # Check if it's an authentication issue
        if "424" in str(e) or "Failed Dependency" in str(e):
            print("\n🔍 424 Error Analysis:")
            print("This usually means:")
            print("1. Model not supported by the provider")
            print("2. Pricing not configured")
            print("3. Authentication issues")
            print("4. Provider configuration problems")
        
        import traceback
        traceback.print_exc()
    
    # Test with a different model to see if it's model-specific
    print("\n🧪 Testing STELLAR with alternative model...")
    
    try:
        response = llm_service.query_llm(
            model='Meta-Llama-3.3-70B-Instruct',  # Alternative model
            messages=test_messages,
            llm_provider='stellar',
            temperature=0.1
        )
        
        print(f"✅ STELLAR Alternative Response: {response}")
        
    except Exception as e:
        print(f"❌ STELLAR Alternative Error: {e}")
    
    # Check environment variables
    print("\n🔍 Environment Variables:")
    print(f"BASE_URL: {os.getenv('BASE_URL', 'Not set')}")
    print(f"HTTP_PROXY: {os.getenv('HTTP_PROXY', 'Not set')}")
    print(f"HTTPS_PROXY: {os.getenv('HTTPS_PROXY', 'Not set')}")
    
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Looking for llm_service.py in: {ai_service_path}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
