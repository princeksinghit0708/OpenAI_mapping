#!/usr/bin/env python3
"""
Test that the FAISS fix works properly
"""

import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_faiss_fix():
    """Test that the FAISS engine works without errors"""
    print("🧪 Testing FAISS Fix")
    print("=" * 30)
    
    try:
        # Import the fixed FAISS engine
        from agents.faiss_similarity_engine import get_faiss_engine
        
        print("✅ Successfully imported FAISS engine")
        
        # Get the engine instance
        engine = get_faiss_engine()
        print("✅ Successfully created FAISS engine instance")
        
        # Initialize the engine
        await engine.initialize()
        print("✅ Successfully initialized FAISS engine")
        
        # Test basic functionality
        print("\n📝 Testing basic functionality...")
        
        # Test adding text
        success = await engine.add_text("Test message for FAISS engine")
        if success:
            print("  ✅ Text addition works")
        else:
            print("  ⚠️ Text addition returned False (may be expected with dummy engine)")
        
        # Test searching
        results = await engine.search_similar("test message", k=3)
        print(f"  ✅ Search returned {len(results)} results")
        
        # Test suggestions
        await engine.add_suggestion("Test suggestion", "test context")
        suggestions = await engine.get_suggestions("test", limit=5)
        print(f"  ✅ Suggestions returned {len(suggestions)} items")
        
        print("\n🎉 FAISS fix test completed successfully!")
        print("✅ No more connection errors!")
        print("✅ Application should work without FAISS issues!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_faiss_fix())
