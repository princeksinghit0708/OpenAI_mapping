#!/usr/bin/env python3
"""
Test the offline FAISS engine functionality
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.offline_faiss_engine import get_offline_faiss_engine

async def test_offline_faiss():
    """Test the offline FAISS engine"""
    print("🧪 Testing Offline FAISS Engine")
    print("=" * 40)
    
    try:
        # Get the engine
        engine = get_offline_faiss_engine()
        
        # Initialize
        print("🔄 Initializing offline FAISS engine...")
        await engine.initialize()
        
        if engine.is_initialized:
            print("✅ Offline FAISS engine initialized successfully!")
        else:
            print("❌ Failed to initialize offline FAISS engine")
            return
        
        # Test adding text
        print("\n📝 Testing text addition...")
        test_texts = [
            "Hello, how can I help you with AA member matching?",
            "I need to find similar AA members based on their data",
            "What are the different matching criteria for AA members?",
            "How does the FAISS similarity search work?",
            "Can you help me with data quality validation?"
        ]
        
        for i, text in enumerate(test_texts):
            success = await engine.add_text(text, {"category": "test", "id": i})
            if success:
                print(f"  ✅ Added: {text[:50]}...")
            else:
                print(f"  ❌ Failed to add: {text[:50]}...")
        
        # Test searching
        print("\n🔍 Testing similarity search...")
        search_queries = [
            "AA member matching",
            "data quality",
            "similarity search",
            "help with validation"
        ]
        
        for query in search_queries:
            print(f"\n  Query: '{query}'")
            results = await engine.search_similar(query, k=3)
            
            if results:
                print(f"  Found {len(results)} similar texts:")
                for i, result in enumerate(results):
                    print(f"    {i+1}. {result['text'][:60]}... (similarity: {result['similarity']:.3f})")
            else:
                print("  No similar texts found")
        
        # Test suggestions
        print("\n💡 Testing suggestions...")
        suggestions = [
            "Check AA member data quality",
            "Validate matching criteria",
            "Run similarity search",
            "Export data to Excel"
        ]
        
        for suggestion in suggestions:
            success = await engine.add_suggestion(suggestion, "test context")
            if success:
                print(f"  ✅ Added suggestion: {suggestion}")
            else:
                print(f"  ❌ Failed to add suggestion: {suggestion}")
        
        # Test getting suggestions
        print("\n📋 Testing suggestion retrieval...")
        retrieved_suggestions = await engine.get_suggestions("data quality", limit=3)
        
        if retrieved_suggestions:
            print(f"  Found {len(retrieved_suggestions)} suggestions:")
            for i, suggestion in enumerate(retrieved_suggestions):
                print(f"    {i+1}. {suggestion.get('suggestion', 'N/A')}")
        else:
            print("  No suggestions found")
        
        print("\n🎉 Offline FAISS engine test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_offline_faiss())
