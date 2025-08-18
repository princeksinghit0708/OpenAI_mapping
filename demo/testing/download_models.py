#!/usr/bin/env python3
"""
Model Downloader Script
Downloads models for offline use
"""

def download_models():
    print("📥 Downloading models for offline use...")
    
    models = [
        "microsoft/DialoGPT-small",      # Small chat model
        "sentence-transformers/all-MiniLM-L6-v2",  # Embeddings
        "gpt2"                           # Text generation
    ]
    
    for model_name in models:
        try:
            print(f"\n📥 Downloading: {model_name}")
            
            if "sentence-transformers" in model_name:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer(model_name)
                print(f"✅ {model_name} downloaded successfully")
            else:
                from transformers import AutoTokenizer, AutoModelForCausalLM
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                print(f"✅ {model_name} downloaded successfully")
                
        except Exception as e:
            print(f"❌ Failed to download {model_name}: {e}")
    
    print("\n🎉 Model download complete!")
    print("💡 These models will now work offline")

if __name__ == "__main__":
    download_models()
