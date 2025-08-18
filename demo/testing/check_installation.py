#!/usr/bin/env python3
"""
Check current installation and verify packages are working
"""

def check_installation():
    """Check if all required packages are installed and working"""
    print("🔍 Checking your current installation...")
    print("=" * 50)
    
    # Check transformers
    try:
        import transformers
        print(f"✅ transformers: {transformers.__version__}")
    except ImportError:
        print("❌ transformers: Not installed")
    
    # Check torch
    try:
        import torch
        print(f"✅ torch: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError:
        print("❌ torch: Not installed")
    
    # Check sentence-transformers
    try:
        import sentence_transformers
        print(f"✅ sentence-transformers: {sentence_transformers.__version__}")
        
        # Test if it actually works
        try:
            from sentence_transformers import SentenceTransformer
            print("   ✅ Import successful")
        except Exception as e:
            print(f"   ❌ Import failed: {e}")
            
    except ImportError:
        print("❌ sentence-transformers: Not installed")
    
    # Check langchain
    try:
        import langchain
        print(f"✅ langchain: {langchain.__version__}")
    except ImportError:
        print("❌ langchain: Not installed")
    
    # Check accelerate
    try:
        import accelerate
        print(f"✅ accelerate: {accelerate.__version__}")
    except ImportError:
        print("❌ accelerate: Not installed")
    
    print("\n" + "=" * 50)
    
    # Test sentence-transformers functionality
    print("\n🧪 Testing sentence-transformers functionality...")
    try:
        from sentence_transformers import SentenceTransformer
        
        # Try to load a small model
        print("   Loading test model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("   ✅ Model loaded successfully!")
        
        # Test encoding
        sentences = ["This is a test sentence."]
        embeddings = model.encode(sentences)
        print(f"   ✅ Generated embeddings: {embeddings.shape}")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        print("   This might be due to network issues or model download problems.")

if __name__ == "__main__":
    check_installation()
