#!/usr/bin/env python3
"""
Local Model Checker
Checks for locally available models and provides offline alternatives
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_huggingface_cache():
    """Check if there are any pre-downloaded models in Hugging Face cache"""
    print("🔍 Checking Hugging Face Cache for Local Models")
    print("=" * 60)
    
    # Common cache locations
    cache_paths = [
        os.path.expanduser("~/.cache/huggingface"),
        os.path.expanduser("~/AppData/Local/huggingface"),
        os.path.expanduser("~/Library/Caches/huggingface"),
        "C:/Users/*/AppData/Local/huggingface",
        "C:/Users/*/.cache/huggingface"
    ]
    
    found_models = []
    
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            print(f"📁 Found cache directory: {cache_path}")
            
            # Look for model directories
            try:
                for item in os.listdir(cache_path):
                    item_path = os.path.join(cache_path, item)
                    if os.path.isdir(item_path):
                        # Check if it looks like a model directory
                        if any(os.path.exists(os.path.join(item_path, f)) for f in ["config.json", "pytorch_model.bin", "tokenizer.json"]):
                            found_models.append(item)
                            print(f"  ✅ Found model: {item}")
            except PermissionError:
                print(f"  ⚠️ Permission denied accessing: {cache_path}")
            except Exception as e:
                print(f"  ⚠️ Error accessing: {cache_path} - {e}")
        else:
            print(f"❌ Cache directory not found: {cache_path}")
    
    return found_models

def check_local_model_files():
    """Check for local model files in the project directory"""
    print("\n🔍 Checking Project Directory for Local Models")
    print("=" * 60)
    
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Look for common model file patterns
    model_extensions = [".bin", ".safetensors", ".pt", ".pth", ".onnx"]
    config_files = ["config.json", "tokenizer.json", "tokenizer_config.json"]
    
    found_files = []
    
    for root, dirs, files in os.walk(project_root):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_root)
            
            if any(file.endswith(ext) for ext in model_extensions) or file in config_files:
                found_files.append(rel_path)
                print(f"  ✅ Found model file: {rel_path}")
    
    return found_files

def create_offline_model_config():
    """Create a configuration for offline model usage"""
    print("\n🔧 Creating Offline Model Configuration")
    print("=" * 60)
    
    config = {
        "offline_mode": True,
        "local_models": {
            "text_generation": {
                "type": "rule_based",
                "description": "Simple rule-based text generation",
                "capabilities": ["basic responses", "keyword matching", "template filling"]
            },
            "embeddings": {
                "type": "hash_based",
                "description": "Hash-based text similarity",
                "capabilities": ["text similarity", "keyword extraction", "basic clustering"]
            },
            "classification": {
                "type": "rule_based",
                "description": "Rule-based text classification",
                "capabilities": ["intent detection", "topic classification", "sentiment analysis"]
            }
        },
        "fallback_strategies": [
            "Use pre-defined responses for common queries",
            "Implement keyword-based matching",
            "Create template-based responses",
            "Use local file processing for data analysis"
        ]
    }
    
    print("✅ Offline configuration created:")
    for category, details in config["local_models"].items():
        print(f"  📋 {category}: {details['description']}")
        print(f"     Capabilities: {', '.join(details['capabilities'])}")
    
    return config

def test_offline_capabilities():
    """Test what offline capabilities are available"""
    print("\n🧪 Testing Offline Capabilities")
    print("=" * 60)
    
    capabilities = {}
    
    # Test 1: Basic text processing
    try:
        sample_text = "Data mapping transforms source data to target format"
        words = sample_text.split()
        word_count = len(words)
        capabilities['text_processing'] = True
        print(f"✅ Text processing: {word_count} words counted")
    except Exception as e:
        capabilities['text_processing'] = False
        print(f"❌ Text processing failed: {e}")
    
    # Test 2: Simple pattern matching
    try:
        import re
        patterns = {
            "data_mapping": r"data.*mapping",
            "etl": r"etl|extract|transform|load",
            "pyspark": r"pyspark|spark"
        }
        
        test_text = "We use data mapping in ETL processes with PySpark"
        matches = {}
        for name, pattern in patterns.items():
            if re.search(pattern, test_text, re.IGNORECASE):
                matches[name] = True
        
        capabilities['pattern_matching'] = True
        print(f"✅ Pattern matching: {len(matches)} patterns found")
    except Exception as e:
        capabilities['pattern_matching'] = False
        print(f"❌ Pattern matching failed: {e}")
    
    # Test 3: File operations
    try:
        current_dir = os.getcwd()
        files = os.listdir(current_dir)
        capabilities['file_operations'] = True
        print(f"✅ File operations: {len(files)} files in current directory")
    except Exception as e:
        capabilities['file_operations'] = False
        print(f"❌ File operations failed: {e}")
    
    # Test 4: JSON processing
    try:
        import json
        test_data = {"key": "value", "number": 42}
        json_string = json.dumps(test_data)
        parsed_data = json.loads(json_string)
        capabilities['json_processing'] = True
        print("✅ JSON processing: serialize/deserialize working")
    except Exception as e:
        capabilities['json_processing'] = False
        print(f"❌ JSON processing failed: {e}")
    
    return capabilities

def provide_offline_solutions():
    """Provide solutions for working offline"""
    print("\n💡 Offline Development Solutions")
    print("=" * 60)
    
    print("🚫 **Problem**: No internet access to download Hugging Face models")
    print("✅ **Solution**: Use offline alternatives and local processing")
    
    print("\n🔧 **Immediate Solutions**:")
    print("1. **Rule-based responses**: Create predefined answers for common queries")
    print("2. **Keyword matching**: Use pattern matching for intent detection")
    print("3. **Template filling**: Use response templates with variable substitution")
    print("4. **Local file processing**: Analyze files without external models")
    
    print("\n📚 **Offline Knowledge Base**:")
    print("1. **Create local documentation**: Store common Q&A pairs")
    print("2. **Build response templates**: Use structured response patterns")
    print("3. **Implement keyword indexing**: Create searchable local content")
    print("4. **Use file-based storage**: Store responses in JSON/CSV files")
    
    print("\n🔄 **Hybrid Approach**:")
    print("1. **Offline by default**: Work without internet connection")
    print("2. **Online when available**: Use external models when possible")
    print("3. **Graceful degradation**: Fall back to offline methods")
    print("4. **Local caching**: Store frequently used responses")
    
    print("\n📁 **File Structure for Offline Mode**:")
    print("demo/offline/")
    print("├── responses/          # Predefined response templates")
    print("├── knowledge/          # Local knowledge base")
    print("├── patterns/           # Pattern matching rules")
    print("└── templates/          # Response templates")

def main():
    """Main function to run all checks"""
    print("🚀 Local Model Availability Checker")
    print("=" * 60)
    print("🔍 Checking what models and capabilities are available offline")
    print("=" * 60)
    
    # Check 1: Hugging Face cache
    cached_models = check_huggingface_cache()
    
    # Check 2: Local model files
    local_files = check_local_model_files()
    
    # Check 3: Offline configuration
    offline_config = create_offline_model_config()
    
    # Check 4: Offline capabilities
    capabilities = test_offline_capabilities()
    
    # Check 5: Provide solutions
    provide_offline_solutions()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    print(f"📦 Cached models found: {len(cached_models)}")
    print(f"📁 Local model files: {len(local_files)}")
    print(f"🔧 Offline capabilities: {sum(capabilities.values())}/{len(capabilities)}")
    
    if cached_models:
        print("\n✅ **Good news**: You have some cached models available!")
        print("💡 You can use these for local inference")
    else:
        print("\n⚠️ **No cached models found**")
        print("💡 Use the offline alternatives provided above")
    
    print("\n🚀 Check complete! Use offline solutions for development.")

if __name__ == "__main__":
    main()
