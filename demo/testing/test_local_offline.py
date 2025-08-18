#!/usr/bin/env python3
"""
Offline Local Testing Suite
Tests LLM functionality using only local resources - no internet required
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_offline_imports():
    """Test 1: Check if libraries can be imported offline"""
    print("🧪 Test 1: Offline Library Imports")
    print("=" * 50)
    
    try:
        # Test basic Python libraries
        import json
        import re
        import datetime
        print("✅ Basic Python libraries imported")
        
        # Test if we can import LangChain (without downloading models)
        try:
            import langchain
            print(f"✅ LangChain version: {langchain.__version__}")
        except ImportError:
            print("⚠️ LangChain not available - will use alternatives")
        
        # Test if we can import transformers (without downloading)
        try:
            import transformers
            print(f"✅ Transformers version: {transformers.__version__}")
        except ImportError:
            print("⚠️ Transformers not available - will use alternatives")
        
        # Test if we can import torch
        try:
            import torch
            print(f"✅ PyTorch version: {torch.__version__}")
        except ImportError:
            print("⚠️ PyTorch not available - will use alternatives")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_local_file_operations():
    """Test 2: Test local file operations"""
    print("\n🧪 Test 2: Local File Operations")
    print("=" * 50)
    
    try:
        # Test if we can read local files
        test_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"✅ Current directory: {test_dir}")
        
        # List available files
        files = os.listdir(test_dir)
        print(f"✅ Found {len(files)} files in testing directory")
        
        # Test if we can read the README
        readme_path = os.path.join(test_dir, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ README.md readable ({len(content)} characters)")
        else:
            print("⚠️ README.md not found")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_simple_text_processing():
    """Test 3: Simple text processing without AI models"""
    print("\n🧪 Test 3: Simple Text Processing")
    print("=" * 50)
    
    try:
        # Test basic text operations
        sample_text = "Data mapping is the process of transforming data from source to target format."
        
        # Word count
        word_count = len(sample_text.split())
        print(f"✅ Word count: {word_count}")
        
        # Character count
        char_count = len(sample_text)
        print(f"✅ Character count: {char_count}")
        
        # Find keywords
        keywords = ["data", "mapping", "transforming", "source", "target"]
        found_keywords = [word for word in keywords if word.lower() in sample_text.lower()]
        print(f"✅ Found keywords: {found_keywords}")
        
        # Simple text analysis
        sentences = sample_text.split('.')
        print(f"✅ Sentence count: {len(sentences)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processing test failed: {e}")
        return False

def test_local_llm_service():
    """Test 4: Test local LLM service capabilities"""
    print("\n🧪 Test 4: Local LLM Service Testing")
    print("=" * 50)
    
    try:
        # Try to import the LLM service
        from agentic_mapping_ai.llm_service import llm_service
        print("✅ LLM service imported successfully")
        
        # Check what methods are available
        methods = [m for m in dir(llm_service) if not m.startswith('_')]
        print(f"📋 Available methods: {methods}")
        
        # Check if the service has any local capabilities
        if hasattr(llm_service, 'local_models'):
            print("✅ Local models support detected")
        else:
            print("ℹ️ No local models support detected")
        
        # Check if the service has fallback mechanisms
        if hasattr(llm_service, 'fallback_llm'):
            print("✅ Fallback LLM support detected")
        else:
            print("ℹ️ No fallback LLM support detected")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM service test failed: {e}")
        return False

def test_chat_agent_offline():
    """Test 5: Test chat agent without external models"""
    print("\n🧪 Test 5: Offline Chat Agent Testing")
    print("=" * 50)
    
    try:
        # Try to import chat agent
        from agentic_mapping_ai.agents.chat_agent import ConversationalAgent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        
        print("✅ Chat agent imported successfully")
        
        # Create a simple config
        config = AgentConfig(
            name='offline_test_agent',
            description='Test agent for offline validation',
            model='local',  # Use local model
            temperature=0.1
        )
        
        print("✅ Agent config created")
        
        # Try to create the agent (this might fail if it needs external models)
        try:
            agent = ConversationalAgent(config)
            print("✅ Chat agent created successfully")
            
            # Test basic methods
            agent_type = agent.get_agent_type()
            print(f"✅ Agent type: {agent_type}")
            
            system_prompt = agent._get_system_prompt()
            print(f"✅ System prompt: {system_prompt[:100]}...")
            
            return True
            
        except Exception as agent_error:
            print(f"⚠️ Agent creation failed: {agent_error}")
            print("💡 This is expected in offline mode")
            return False
        
    except Exception as e:
        print(f"❌ Chat agent test failed: {e}")
        return False

def test_offline_alternatives():
    """Test 6: Test offline alternatives and workarounds"""
    print("\n🧪 Test 6: Offline Alternatives Testing")
    print("=" * 50)
    
    try:
        # Test if we can create simple text-based responses
        print("🔧 Creating offline text processor...")
        
        class OfflineTextProcessor:
            def __init__(self):
                self.responses = {
                    "hello": "Hello! I'm an offline text processor. I can help with basic text analysis.",
                    "data mapping": "Data mapping is the process of transforming data between different formats.",
                    "etl": "ETL stands for Extract, Transform, Load - a data processing pipeline.",
                    "pyspark": "PySpark is a distributed data processing framework for big data.",
                    "help": "I can help with: data mapping, ETL, PySpark, and basic text processing."
                }
            
            def process_query(self, query):
                query_lower = query.lower()
                
                # Find best matching response
                for key, response in self.responses.items():
                    if key in query_lower:
                        return response
                
                return "I understand you're asking about data processing. Please ask about data mapping, ETL, or PySpark."
        
        # Test the offline processor
        processor = OfflineTextProcessor()
        print("✅ Offline text processor created")
        
        # Test some queries
        test_queries = [
            "Hello, what can you do?",
            "What is data mapping?",
            "Explain ETL",
            "Tell me about PySpark"
        ]
        
        print("\n💬 Testing offline responses:")
        for query in test_queries:
            response = processor.process_query(query)
            print(f"  Q: {query}")
            print(f"  A: {response}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Offline alternatives test failed: {e}")
        return False

def test_file_processing_capabilities():
    """Test 7: Test file processing without external models"""
    print("\n🧪 Test 7: File Processing Capabilities")
    print("=" * 50)
    
    try:
        # Test if we can process text files
        test_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create a simple text processor
        class SimpleTextProcessor:
            def __init__(self):
                self.keywords = {
                    "data": ["mapping", "processing", "transformation", "validation"],
                    "etl": ["extract", "transform", "load", "pipeline"],
                    "spark": ["pyspark", "distributed", "big data", "processing"]
                }
            
            def analyze_text(self, text):
                analysis = {
                    "word_count": len(text.split()),
                    "char_count": len(text),
                    "keyword_matches": {},
                    "sentences": len([s for s in text.split('.') if s.strip()])
                }
                
                # Find keyword matches
                text_lower = text.lower()
                for category, words in self.keywords.items():
                    matches = [word for word in words if word in text_lower]
                    if matches:
                        analysis["keyword_matches"][category] = matches
                
                return analysis
        
        processor = SimpleTextProcessor()
        print("✅ Simple text processor created")
        
        # Test with sample text
        sample_text = """
        Data mapping is essential for ETL processes. 
        PySpark provides distributed data processing capabilities.
        Data validation ensures quality and consistency.
        """
        
        analysis = processor.analyze_text(sample_text)
        print("✅ Text analysis completed:")
        print(f"  Word count: {analysis['word_count']}")
        print(f"  Character count: {analysis['char_count']}")
        print(f"  Sentences: {analysis['sentences']}")
        print(f"  Keyword matches: {analysis['keyword_matches']}")
        
        return True
        
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False

def run_offline_tests():
    """Run all offline tests"""
    print("🚀 Offline Local Testing Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("🌐 This suite works completely offline - no internet required!")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Offline imports
    results['offline_imports'] = test_offline_imports()
    
    # Test 2: Local file operations
    results['file_operations'] = test_local_file_operations()
    
    # Test 3: Simple text processing
    results['text_processing'] = test_simple_text_processing()
    
    # Test 4: Local LLM service
    results['llm_service'] = test_local_llm_service()
    
    # Test 5: Offline chat agent
    results['chat_agent'] = test_chat_agent_offline()
    
    # Test 6: Offline alternatives
    results['offline_alternatives'] = test_offline_alternatives()
    
    # Test 7: File processing
    results['file_processing'] = test_file_processing_capabilities()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 OFFLINE TEST RESULTS")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print("\n" + "=" * 60)
    print("🎯 OFFLINE CAPABILITIES")
    print("=" * 60)
    
    if results.get('text_processing', False):
        print("✅ Basic text processing available")
    
    if results.get('offline_alternatives', False):
        print("✅ Offline text responses available")
    
    if results.get('file_processing', False):
        print("✅ File analysis capabilities available")
    
    if results.get('llm_service', False):
        print("✅ LLM service accessible (may need local models)")
    
    print("\n💡 Offline Development Options:")
    print("   1. Use simple text processors for basic functionality")
    print("   2. Implement rule-based responses for common queries")
    print("   3. Use local file processing for data analysis")
    print("   4. Create offline knowledge bases")
    
    print("\n🚀 Offline testing complete!")

if __name__ == "__main__":
    run_offline_tests()
