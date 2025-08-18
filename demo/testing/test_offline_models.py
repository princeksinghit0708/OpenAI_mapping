#!/usr/bin/env python3
"""
Offline Model Test
Tests if models work without internet using locally cached models
"""

import os
from pathlib import Path

def find_cached_models():
    """Find available cached models"""
    print("Searching for cached models...")
    
    models_found = []
    
    # Check sentence-transformers cache
    try:
        st_cache = Path.home() / ".cache" / "torch" / "sentence_transformers"
        if st_cache.exists():
            st_models = list(st_cache.glob("*"))
            if st_models:
                print(f"Found {len(st_models)} sentence-transformers models:")
                for model in st_models:
                    print(f"  - {model.name}")
                    models_found.append(("sentence-transformers", str(model)))
    except Exception as e:
        print(f"Error checking sentence-transformers cache: {e}")
    
    # Check transformers cache
    try:
        tf_cache = Path.home() / ".cache" / "huggingface" / "hub"
        if tf_cache.exists():
            tf_models = list(tf_cache.glob("models--*"))
            if tf_models:
                print(f"Found {len(tf_models)} transformers models:")
                for model in tf_models[:5]:  # Show first 5
                    print(f"  - {model.name}")
                    models_found.append(("transformers", str(model)))
                if len(tf_models) > 5:
                    print(f"    ... and {len(tf_models) - 5} more")
    except Exception as e:
        print(f"Error checking transformers cache: {e}")
    
    return models_found

def test_sentence_transformers_offline():
    """Test sentence-transformers with cached models"""
    print("\nTesting sentence-transformers offline...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        # Try to find a cached model
        cache_dir = Path.home() / ".cache" / "torch" / "sentence_transformers"
        if cache_dir.exists():
            cached_models = list(cache_dir.glob("*"))
            if cached_models:
                model_path = str(cached_models[0])
                print(f"  Testing model: {cached_models[0].name}")
                
                try:
                    model = SentenceTransformer(model_path)
                    test_sentences = ["Hello world", "This is a test sentence"]
                    embeddings = model.encode(test_sentences)
                    print(f"  OK Generated embeddings: {embeddings.shape}")
                    print(f"  OK Model works offline!")
                    return True
                except Exception as e:
                    print(f"  Error loading model: {e}")
                    return False
            else:
                print("  No cached sentence-transformers models found")
                return False
        else:
            print("  No sentence-transformers cache directory found")
            return False
            
    except ImportError:
        print("  sentence-transformers not installed")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_transformers_offline():
    """Test transformers with cached models"""
    print("\nTesting transformers offline...")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        # Check for cached models
        cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
        if cache_dir.exists():
            cached_models = list(cache_dir.glob("models--*"))
            if cached_models:
                # Try to use the first available model
                model_dir = cached_models[0]
                model_name = model_dir.name.replace("models--", "").replace("--", "/")
                print(f"  Testing model: {model_name}")
                
                try:
                    # Try to load with local_files_only=True
                    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True)
                    model = AutoModelForCausalLM.from_pretrained(str(model_dir), local_files_only=True)
                    print(f"  OK Model loaded successfully!")
                    
                    # Test basic functionality
                    input_text = "Hello"
                    inputs = tokenizer.encode(input_text, return_tensors="pt")
                    print(f"  OK Tokenization successful")
                    
                    print(f"  OK Model works offline!")
                    return True
                    
                except Exception as e:
                    print(f"  Error loading model: {e}")
                    return False
            else:
                print("  No cached transformers models found")
                return False
        else:
            print("  No transformers cache directory found")
            return False
            
    except ImportError:
        print("  transformers not installed")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def test_basic_functionality():
    """Test basic AI functionality without models"""
    print("\nTesting basic functionality...")
    
    try:
        # Test if we can import basic libraries
        import torch
        print(f"  OK PyTorch available: {torch.__version__}")
        
        import transformers
        print(f"  OK Transformers available: {transformers.__version__}")
        
        import sentence_transformers
        print(f"  OK Sentence-transformers available: {sentence_transformers.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"  Import error: {e}")
        return False
    except Exception as e:
        print(f"  Error: {e}")
        return False

def main():
    """Main function"""
    print("Offline Model Testing")
    print("=" * 50)
    
    # Find cached models
    cached_models = find_cached_models()
    
    if not cached_models:
        print("\nNo cached models found.")
        print("You'll need internet access to download models first.")
        print("Or copy models from another system that has them.")
    
    # Test basic functionality
    basic_ok = test_basic_functionality()
    
    # Test offline capabilities
    st_ok = test_sentence_transformers_offline()
    tf_ok = test_transformers_offline()
    
    # Summary
    print("\n" + "=" * 50)
    print("TESTING SUMMARY")
    print("=" * 50)
    
    print(f"Basic libraries: {'OK' if basic_ok else 'FAILED'}")
    print(f"Sentence-transformers offline: {'OK' if st_ok else 'FAILED'}")
    print(f"Transformers offline: {'OK' if tf_ok else 'FAILED'}")
    
    if cached_models:
        print(f"\nFound {len(cached_models)} cached models")
        print("These can be used offline!")
    else:
        print("\nNo cached models available")
        print("You need to download models when you have internet access")
    
    if st_ok or tf_ok:
        print("\nSUCCESS: You can use AI models offline!")
        print("Run your applications without internet connection.")
    else:
        print("\nLIMITED: Basic libraries work but no models available offline")
        print("You need cached models for full offline functionality.")

if __name__ == "__main__":
    main()
