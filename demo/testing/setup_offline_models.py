#!/usr/bin/env python3
"""
Offline Model Setup Guide
Helps set up Hugging Face models for offline use
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_installation():
    """Check what's already installed"""
    print("Checking Current Installation")
    print("=" * 50)
    
    packages = {
        "transformers": "Hugging Face Transformers library",
        "torch": "PyTorch for model inference",
        "sentence-transformers": "Sentence embeddings",
        "langchain": "LangChain framework",
        "accelerate": "Model acceleration utilities"
    }
    
    installed = {}
    
    for package, description in packages.items():
        try:
            # Use a more robust import method
            if package == "torch":
                import torch
                version = torch.__version__
            elif package == "sentence-transformers":
                # Handle hyphenated package name correctly
                import sentence_transformers
                version = sentence_transformers.__version__
            elif package == "transformers":
                import transformers
                version = transformers.__version__
            elif package == "langchain":
                import langchain
                version = langchain.__version__
            elif package == "accelerate":
                import accelerate
                version = accelerate.__version__
            else:
                module = __import__(package)
                version = getattr(module, '__version__', 'Unknown')
            
            installed[package] = version
            print(f"OK {package}: {version} - {description}")
        except ImportError as e:
            installed[package] = None
            print(f"ERROR {package}: Not installed - {description}")
            print(f"   Error: {e}")
        except Exception as e:
            installed[package] = None
            print(f"ERROR {package}: Error checking - {description}")
            print(f"   Error: {e}")
    
    return installed

def install_packages():
    """Guide through package installation"""
    print("\nPackage Installation Guide")
    print("=" * 50)
    
    print("Step 1: Install Core Libraries")
    print("Run these commands in your terminal:")
    print()
    
    commands = [
        "pip install transformers",
        "pip install torch",
        "pip install sentence-transformers",
        "pip install langchain langchain-community",
        "pip install accelerate safetensors"
    ]
    
    for cmd in commands:
        print(f"   {cmd}")
    
    print()
    print("Note: This step requires internet connection")
    print("After installation: Models will work offline")
    
    return commands

def download_models():
    """Guide through model downloading"""
    print("\nModel Download Guide")
    print("=" * 50)
    
    print("Step 2: Download Models (One-time setup)")
    print("Run this script to download models:")
    print()
    
    script_content = '''#!/usr/bin/env python3
"""
Model Downloader Script
Downloads models for offline use
"""

def download_models():
    print("Downloading models for offline use...")
    
    models = [
        "microsoft/DialoGPT-small",      # Small chat model
        "sentence-transformers/all-MiniLM-L6-v2",  # Embeddings
        "gpt2"                           # Text generation
    ]
    
    for model_name in models:
        try:
            print(f"\\nDownloading: {model_name}")
            
            if "sentence-transformers" in model_name:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer(model_name)
                print(f"OK {model_name} downloaded successfully")
            else:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                print(f"OK {model_name} downloaded successfully")
                
        except Exception as e:
            print(f"Failed to download {model_name}: {e}")
    
    print("\\nModel download complete!")
    print("These models will now work offline")

if __name__ == "__main__":
    download_models()
'''
    
    # Save the script
    script_path = os.path.join(os.path.dirname(__file__), "download_models.py")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"Script saved to: {script_path}")
    print("Run it with: python download_models.py")
    print()
    print("Note: This step requires internet connection")
    print("After download: Models cached locally")

def test_offline_mode():
    """Test if models can work offline"""
    print("\nTesting Offline Mode")
    print("=" * 50)
    
    try:
        # Try to import transformers
        import transformers
        print("OK Transformers library available")
        
        # Check cache directory
        cache_dir = transformers.file_utils.default_cache_path
        print(f"Cache directory: {cache_dir}")
        
        if os.path.exists(cache_dir):
            print("OK Cache directory exists")
            
            # Look for downloaded models
            cache_contents = os.listdir(cache_dir)
            model_dirs = [d for d in cache_contents if os.path.isdir(os.path.join(cache_dir, d))]
            
            if model_dirs:
                print(f"OK Found {len(model_dirs)} cached models:")
                for model_dir in model_dirs[:5]:  # Show first 5
                    print(f"   {model_dir}")
                if len(model_dirs) > 5:
                    print(f"   ... and {len(model_dirs) - 5} more")
            else:
                print("No cached models found")
        else:
            print("Cache directory not found")
        
        return True
        
    except ImportError:
        print("Transformers not installed")
        return False
    except Exception as e:
        print(f"Error checking offline mode: {e}")
        return False

def create_offline_test():
    """Create a test script for offline model usage"""
    print("\nCreating Offline Test Script")
    print("=" * 50)
    
    test_script = '''#!/usr/bin/env python3
"""
Offline Model Test
Tests if models work without internet
"""

def test_offline_models():
    print("Testing Offline Model Usage")
    print("=" * 40)
    
    try:
        # Test 1: Load model from cache
        print("Loading model from local cache...")
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch
        
        # Use local_files_only=True to prevent internet connection
        tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small', local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained('microsoft/DialoGPT-small', local_files_only=True)
        print("OK Model loaded from cache - no internet needed!")
        
        # Test 2: Generate text
        print("\\nTesting text generation...")
        input_text = "Hello, how are you?"
        inputs = tokenizer.encode(input_text, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"OK Generated response: {response}")
        
        return True
        
    except Exception as e:
        print(f"Offline test failed: {e}")
        print("Make sure models are downloaded first")
        return False

if __name__ == "__main__":
    test_offline_models()
'''
    
    # Save the test script
    test_path = os.path.join(os.path.dirname(__file__), "test_offline_models.py")
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(f"Offline test script saved to: {test_path}")
    print("Run it with: python test_offline_models.py")

def provide_offline_workflow():
    """Provide complete offline workflow"""
    print("\nComplete Offline Workflow")
    print("=" * 50)
    
    print("Step-by-Step Process:")
    print()
    print("1. Install Libraries (needs internet ONCE)")
    print("   pip install transformers torch sentence-transformers")
    print()
    print("2. Download Models (needs internet ONCE)")
    print("   python download_models.py")
    print()
    print("3. Test Offline Mode (no internet needed)")
    print("   python test_offline_models.py")
    print()
    print("4. Use in Your Application (no internet needed)")
    print("   Models work from local cache")
    print()
    print("Key Points:")
    print("   Installation: One-time internet needed")
    print("   Model download: One-time internet needed")
    print("   Usage: Completely offline")
    print("   Cache: Models stored locally")
    print("   Updates: Manual when needed")

def main():
    """Main function"""
    print("Hugging Face Offline Setup Guide")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check current installation
    installed = check_installation()
    
    # Provide installation guide
    install_packages()
    
    # Guide through model downloading
    download_models()
    
    # Test offline capabilities
    test_offline_mode()
    
    # Create offline test script
    create_offline_test()
    
    # Provide complete workflow
    provide_offline_workflow()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if any(installed.values()):
        print("OK Some packages already installed")
    else:
        print("No packages installed yet")
    
    print("\nNext Steps:")
    print("1. Install packages (if not done)")
    print("2. Download models (if not done)")
    print("3. Test offline functionality")
    print("4. Use models in your application")
    
    print("\nSetup guide complete!")

if __name__ == "__main__":
    main()
