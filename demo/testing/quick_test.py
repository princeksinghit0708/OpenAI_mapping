#!/usr/bin/env python3
"""
Quick test for sentence-transformers
"""

print("🔍 Quick sentence-transformers test...")

# Test 1: Basic import
try:
    import sentence_transformers
    print(f"✅ Import successful: {sentence_transformers.__version__}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    exit(1)

# Test 2: Import specific class
try:
    from sentence_transformers import SentenceTransformer
    print("✅ SentenceTransformer import successful")
except ImportError as e:
    print(f"❌ SentenceTransformer import failed: {e}")
    exit(1)

# Test 3: Check available models
try:
    print("📚 Available models in sentence_transformers:")
    print(dir(sentence_transformers))
except Exception as e:
    print(f"❌ Error listing models: {e}")

# Test 4: Try to create a simple model
try:
    print("\n🧪 Testing model creation...")
    # Use a very small model for testing
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("✅ Model created successfully!")
    
    # Test encoding
    test_sentences = ["Hello world", "This is a test"]
    embeddings = model.encode(test_sentences)
    print(f"✅ Generated embeddings shape: {embeddings.shape}")
    
except Exception as e:
    print(f"❌ Model test failed: {e}")
    print("This might be a network/model download issue")

print("\n�� Test completed!")
