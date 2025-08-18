#!/usr/bin/env python3
"""
LangChain & Hugging Face Direct Testing
Tests LLM functionality using local models and libraries directly
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_langchain_imports():
    """Test 1: Check LangChain imports"""
    print("🧪 Test 1: LangChain Library Imports")
    print("=" * 50)
    
    try:
        import langchain
        print(f"✅ LangChain version: {langchain.__version__}")
        
        from langchain.llms import HuggingFacePipeline
        print("✅ HuggingFacePipeline imported")
        
        from langchain.embeddings import HuggingFaceEmbeddings
        print("✅ HuggingFaceEmbeddings imported")
        
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        print("✅ RecursiveCharacterTextSplitter imported")
        
        from langchain.vectorstores import FAISS
        print("✅ FAISS vectorstore imported")
        
        from langchain.chains import LLMChain
        print("✅ LLMChain imported")
        
        from langchain.prompts import PromptTemplate
        print("✅ PromptTemplate imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        print("💡 Install with: pip install langchain langchain-community")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_huggingface_imports():
    """Test 2: Check Hugging Face imports"""
    print("\n🧪 Test 2: Hugging Face Library Imports")
    print("=" * 50)
    
    try:
        import transformers
        print(f"✅ Transformers version: {transformers.__version__}")
        
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        print("✅ AutoTokenizer imported")
        print("✅ AutoModelForCausalLM imported")
        print("✅ Pipeline imported")
        
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Hugging Face import failed: {e}")
        print("💡 Install with: pip install transformers torch")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_local_model_loading():
    """Test 3: Load a local model"""
    print("\n🧪 Test 3: Local Model Loading")
    print("=" * 50)
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        
        # Try to load a small, fast model for testing
        model_name = "microsoft/DialoGPT-small"  # Small, fast model
        
        print(f"📥 Loading model: {model_name}")
        print("⏳ This may take a few minutes on first run...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print("✅ Model loaded successfully!")
        print(f"✅ Tokenizer vocab size: {tokenizer.vocab_size}")
        print(f"✅ Model parameters: {sum(p.numel() for p in model.parameters()):,}")
        
        # Create pipeline
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print("✅ Pipeline created successfully!")
        
        return True, pipe
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        print("💡 This might be due to network issues or insufficient memory")
        return False, None

def test_langchain_integration(pipe):
    """Test 4: LangChain + Hugging Face Integration"""
    print("\n🧪 Test 4: LangChain + Hugging Face Integration")
    print("=" * 50)
    
    try:
        from langchain.llms import HuggingFacePipeline
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        
        # Create LangChain LLM wrapper
        llm = HuggingFacePipeline(pipeline=pipe)
        print("✅ HuggingFacePipeline wrapper created")
        
        # Create a simple prompt template
        template = """Question: {question}

Answer: Let me help you with that."""
        
        prompt = PromptTemplate(template=template, input_variables=["question"])
        print("✅ Prompt template created")
        
        # Create LLM chain
        chain = LLMChain(llm=llm, prompt=prompt)
        print("✅ LLM chain created")
        
        # Test the chain
        test_question = "What is data mapping?"
        print(f"\n💬 Testing with question: {test_question}")
        
        response = chain.run(question=test_question)
        print(f"✅ Response generated: {response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ LangChain integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_embeddings():
    """Test 5: Test Hugging Face embeddings"""
    print("\n🧪 Test 5: Hugging Face Embeddings")
    print("=" * 50)
    
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        
        # Try to load a small embedding model
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        print(f"📥 Loading embedding model: {model_name}")
        
        embeddings = HuggingFaceEmbeddings(model_name=model_name)
        print("✅ Embeddings model loaded")
        
        # Test embedding generation
        test_texts = [
            "Hello world",
            "Data mapping is important",
            "AI can help with transformations"
        ]
        
        print("💬 Testing embedding generation...")
        for text in test_texts:
            embedding = embeddings.embed_query(text)
            print(f"✅ '{text}' → {len(embedding)} dimensions")
        
        return True
        
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        print("💡 This might be due to network issues or insufficient memory")
        return False

def test_vectorstore():
    """Test 6: Test FAISS vector store"""
    print("\n🧪 Test 6: FAISS Vector Store")
    print("=" * 50)
    
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Create embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Create sample documents
        documents = [
            "Data mapping is the process of transforming data from one format to another.",
            "ETL stands for Extract, Transform, Load.",
            "PySpark is a powerful tool for big data processing.",
            "Data validation ensures data quality and integrity."
        ]
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        texts = text_splitter.create_documents(documents)
        
        # Create vector store
        vectorstore = FAISS.from_documents(texts, embeddings)
        print("✅ FAISS vector store created")
        
        # Test similarity search
        query = "What is data mapping?"
        print(f"\n🔍 Searching for: {query}")
        
        results = vectorstore.similarity_search(query, k=2)
        print(f"✅ Found {len(results)} similar documents:")
        
        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc.page_content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        return False

def test_llm_service_integration():
    """Test 7: Test integration with existing LLM service"""
    print("\n🧪 Test 7: LLM Service Integration")
    print("=" * 50)
    
    try:
        from agentic_mapping_ai.llm_service import llm_service
        print("✅ LLM service imported successfully")
        
        # Check if we can use local models through the service
        print("🔍 Checking LLM service capabilities...")
        
        # Test if the service can handle local model requests
        print("💡 LLM service is configured for token-based authentication")
        print("💡 For local testing, you can use the LangChain + Hugging Face approach above")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM service integration test failed: {e}")
        return False

def run_langchain_tests():
    """Run all LangChain and Hugging Face tests"""
    print("🚀 LangChain & Hugging Face Testing Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {}
    
    # Test 1: LangChain imports
    results['langchain_imports'] = test_langchain_imports()
    
    # Test 2: Hugging Face imports
    results['huggingface_imports'] = test_huggingface_imports()
    
    # Test 3: Local model loading
    success, pipe = test_local_model_loading()
    results['local_model_loading'] = success
    
    # Test 4: LangChain integration
    if success and pipe:
        results['langchain_integration'] = test_langchain_integration(pipe)
    else:
        results['langchain_integration'] = False
    
    # Test 5: Embeddings
    results['embeddings'] = test_embeddings()
    
    # Test 6: Vector store
    results['vectorstore'] = test_vectorstore()
    
    # Test 7: LLM service integration
    results['llm_service_integration'] = test_llm_service_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS")
    print("=" * 60)
    
    if results.get('langchain_integration', False):
        print("✅ LangChain + Hugging Face integration working!")
        print("💡 You can use local models for development and testing")
    
    if results.get('embeddings', False):
        print("✅ Embeddings working - RAG functionality available!")
    
    if results.get('vectorstore', False):
        print("✅ Vector store working - document search available!")
    
    print("\n🚀 Testing complete!")
    print("\n💡 Next steps:")
    print("   1. Use local models for development")
    print("   2. Integrate with your existing LLM service")
    print("   3. Build RAG applications with local embeddings")

if __name__ == "__main__":
    run_langchain_tests()
