#!/usr/bin/env python3
"""
Offline Model Test
Tests if models work without internet
"""

def test_offline_models():
    print("🧪 Testing Offline Model Usage")
    print("=" * 40)
    
    try:
        # Test 1: Load model from cache
        print("📥 Loading model from local cache...")
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # Use local_files_only=True to prevent internet connection
        tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small', local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-small', local_files_only=True)
        print("✅ Model loaded from cache - no internet needed!")
        
        # Test 2: Generate text
        print("\n💬 Testing text generation...")
        input_text = "Hello, how are you?"
        inputs = tokenizer.encode(input_text, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✅ Generated response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Offline test failed: {e}")
        print("💡 Make sure models are downloaded first")
        return False

if __name__ == "__main__":
    test_offline_models()
