#!/usr/bin/env python3
"""
Quick LLM Service Test
Simple test to verify AI model responses
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_test():
    """Quick test of LLM service"""
    print("🚀 Quick LLM Service Test")
    print("=" * 40)
    
    try:
        # Test import
        print("📥 Importing LLM service...")
        from agentic_mapping_ai.llm_service import llm_service
        print("✅ Import successful!")
        
        # Test basic response
        print("\n💬 Testing AI response...")
        messages = [
            {'role': 'system', 'content': 'You are a helpful AI assistant.'},
            {'role': 'user', 'content': 'Say hello and tell me what you can do in one sentence.'}
        ]
        
        print(f"📤 Sending messages: {messages}")
        response = llm_service.call_default_llm(messages=messages)
        print(f"🤖 AI Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    if success:
        print("\n🎉 Quick test passed! LLM service is working.")
    else:
        print("\n💥 Quick test failed. Check the error above.")
