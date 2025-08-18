#!/usr/bin/env python3
"""
Model Downloader Script
Downloads models for offline use or uses locally cached models
"""

import os
from pathlib import Path

def check_cached_models():
    """Check what models are already cached locally"""
    print("Checking for locally cached models...")
    
    try:
        import transformers
        cache_dir = transformers.file_utils.default_cache_path
        print(f"Cache directory: {cache_dir}")
        
        if os.path.exists(cache_dir):
            cache_contents = os.listdir(cache_dir)
            model_dirs = [d for d in cache_contents if os.path.isdir(os.path.join(cache_dir, d)) and not d.startswith('.')]
            
            if model_dirs:
                print(f"Found {len(model_dirs)} cached models:")
                for model_dir in model_dirs:
                    print(f"  - {model_dir}")
                return True
            else:
                print("No cached models found")
                return False
        else:
            print("Cache directory not found")
            return False
            
    except ImportError:
        print("Transformers not installed")
        return False
    except Exception as e:
        print(f"Error checking cache: {e}")
        return False

def download_models():
    """Download models for offline use"""
    print("Attempting to download models for offline use...")
    print("Note: This requires internet connection")
    
    models = [
        "microsoft/DialoGPT-small",      # Small chat model
        "all-MiniLM-L6-v2",              # Embeddings (sentence-transformers)
        "gpt2"                           # Text generation
    ]
    
    success_count = 0
    
    for model_name in models:
        try:
            print(f"\nDownloading: {model_name}")
            
            if "all-MiniLM-L6-v2" in model_name:
                # Handle sentence-transformers model
                try:
                    from sentence_transformers import SentenceTransformer
                    print("  Loading sentence-transformers model...")
                    model = SentenceTransformer(model_name)
                    print(f"  OK {model_name} loaded successfully")
                    success_count += 1
                except Exception as e:
                    print(f"  Failed to load {model_name}: {e}")
                    
            else:
                # Handle transformers models
                try:
                    from transformers import AutoTokenizer, AutoModelForCausalLM
                    print("  Loading transformers model...")
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    model = AutoModelForCausalLM.from_pretrained(model_name)
                    print(f"  OK {model_name} loaded successfully")
                    success_count += 1
                except Exception as e:
                    print(f"  Failed to load {model_name}: {e}")
                    
        except Exception as e:
            print(f"  Failed to download {model_name}: {e}")
            print("  This might be due to network restrictions")
    
    print(f"\nDownload summary: {success_count}/{len(models)} models successful")
    
    if success_count == 0:
        print("\nNo models could be downloaded due to network issues.")
        print("You can still use locally cached models if available.")
    else:
        print(f"\n{success_count} models are now available for offline use!")

def test_local_models():
    """Test if locally cached models work"""
    print("\nTesting locally cached models...")
    
    try:
        # Test sentence-transformers if available
        try:
            from sentence_transformers import SentenceTransformer
            print("Testing sentence-transformers...")
            
            # Try to find a cached model
            cache_dir = Path.home() / ".cache" / "torch" / "sentence_transformers"
            if cache_dir.exists():
                cached_models = list(cache_dir.glob("*"))
                if cached_models:
                    model_path = str(cached_models[0])
                    print(f"  Found cached model: {model_path}")
                    model = SentenceTransformer(model_path)
                    test_sentences = ["Hello world", "This is a test"]
                    embeddings = model.encode(test_sentences)
                    print(f"  OK Generated embeddings: {embeddings.shape}")
                else:
                    print("  No cached sentence-transformers models found")
            else:
                print("  No sentence-transformers cache directory found")
                
        except ImportError:
            print("  sentence-transformers not available")
        except Exception as e:
            print(f"  Error testing sentence-transformers: {e}")
        
        # Test transformers if available
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            print("\nTesting transformers...")
            
            # Check for cached models
            cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
            if cache_dir.exists():
                cached_models = list(cache_dir.glob("models--*"))
                if cached_models:
                    print(f"  Found {len(cached_models)} cached models:")
                    for model_dir in cached_models[:3]:  # Show first 3
                        print(f"    - {model_dir.name}")
                    print("  Models are available for offline use")
                else:
                    print("  No cached transformers models found")
            else:
                print("  No transformers cache directory found")
                
        except ImportError:
            print("  transformers not available")
        except Exception as e:
            print(f"  Error testing transformers: {e}")
            
    except Exception as e:
        print(f"Error testing local models: {e}")

def create_offline_usage_guide():
    """Create a guide for using models offline"""
    print("\nCreating offline usage guide...")
    
    guide_content = '''# Offline Model Usage Guide

## Using Cached Models

If you have models cached locally, you can use them without internet:

### 1. Sentence Transformers (Embeddings)
```python
from sentence_transformers import SentenceTransformer

# Use cached model
model = SentenceTransformer("path/to/cached/model")
embeddings = model.encode(["Hello world"])
```

### 2. Transformers (Text Generation)
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Use cached model with local_files_only=True
tokenizer = AutoTokenizer.from_pretrained("path/to/cached/model", local_files_only=True)
model = AutoModelForCausalLM.from_pretrained("path/to/cached/model", local_files_only=True)
```

## Finding Cached Models

### Sentence Transformers Cache:
- Windows: `%USERPROFILE%\\.cache\\torch\\sentence_transformers`
- Linux/Mac: `~/.cache/torch/sentence_transformers`

### Transformers Cache:
- Windows: `%USERPROFILE%\\.cache\\huggingface\\hub`
- Linux/Mac: `~/.cache/huggingface/hub`

## Offline Testing

Run the test script to verify offline functionality:
```bash
python test_offline_models.py
```
'''
    
    guide_path = os.path.join(os.path.dirname(__file__), "OFFLINE_USAGE_GUIDE.md")
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"Offline usage guide saved to: {guide_path}")

def main():
    """Main function"""
    print("Model Download and Offline Setup")
    print("=" * 50)
    
    # Check what's already cached
    has_cached = check_cached_models()
    
    if has_cached:
        print("\nYou have locally cached models available!")
        print("These can be used offline without downloading.")
    
    # Try to download new models
    print("\n" + "=" * 50)
    download_models()
    
    # Test local models
    print("\n" + "=" * 50)
    test_local_models()
    
    # Create usage guide
    print("\n" + "=" * 50)
    create_offline_usage_guide()
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    
    if has_cached:
        print("You can use your cached models offline.")
        print("Run 'python test_offline_models.py' to test them.")
    else:
        print("No cached models found.")
        print("You'll need internet access to download models first.")

if __name__ == "__main__":
    main()
