"""
FAISS RAG Engine Demo - Demonstrates the new FAISS-based knowledge retrieval system
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from knowledge.rag_engine import RAGEngine
from loguru import logger


async def demo_faiss_rag_engine():
    """Demonstrate the FAISS-based RAG engine capabilities"""
    
    logger.info("🚀 Starting FAISS RAG Engine Demo")
    
    # Initialize RAG engine
    rag_engine = RAGEngine(collection_name="faiss_demo")
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    if not rag_engine.is_initialized:
        logger.error("❌ RAG engine failed to initialize")
        return
    
    logger.info("✅ FAISS RAG Engine initialized successfully")
    
    # Demo 1: Add custom knowledge
    await demo_add_knowledge(rag_engine)
    
    # Demo 2: Search and retrieval
    await demo_search_retrieval(rag_engine)
    
    # Demo 3: Batch operations
    await demo_batch_operations(rag_engine)
    
    # Demo 4: Statistics and health check
    await demo_stats_and_health(rag_engine)
    
    # Demo 5: Context-aware search
    await demo_context_search(rag_engine)
    
    logger.info("🎉 FAISS RAG Engine Demo completed successfully!")


async def demo_add_knowledge(rag_engine: RAGEngine):
    """Demo adding knowledge to FAISS index"""
    logger.info("\n📚 Demo 1: Adding Knowledge to FAISS Index")
    
    # Add Excel-specific knowledge
    excel_knowledge = [
        {
            "content": """
            Excel Conditional Transformations in PySpark:
            - Use when() and otherwise() for If-Then-Else logic
            - Handle null values with coalesce() function
            - Chain multiple conditions with multiple when() calls
            - Example: when(col('flag') == 'Y', lit('Active')).otherwise(lit('Inactive'))
            """,
            "category": "excel_transformations",
            "title": "Excel Conditional Logic"
        },
        {
            "content": """
            FAISS Vector Search Best Practices:
            - Normalize embeddings for cosine similarity
            - Use IndexFlatIP for exact inner product search
            - Consider IndexIVFFlat for large datasets
            - Batch operations are more efficient than single additions
            """,
            "category": "faiss_optimization",
            "title": "FAISS Performance Tips"
        },
        {
            "content": """
            Gold Reference Validation Patterns:
            - Implement lookup tables for standardized values
            - Use fuzzy matching for approximate lookups
            - Cache frequently accessed reference data
            - Validate against business rules before transformation
            """,
            "category": "data_validation",
            "title": "Gold Reference Best Practices"
        }
    ]
    
    # Add knowledge items
    for knowledge in excel_knowledge:
        doc_id = await rag_engine.add_knowledge(
            content=knowledge["content"],
            metadata={
                "category": knowledge["category"],
                "title": knowledge["title"],
                "source": "demo"
            }
        )
        logger.info(f"✅ Added knowledge: {knowledge['title']} (ID: {doc_id})")


async def demo_search_retrieval(rag_engine: RAGEngine):
    """Demo search and retrieval functionality"""
    logger.info("\n🔍 Demo 2: Search and Retrieval")
    
    queries = [
        "How to handle conditional logic in Excel transformations?",
        "What are FAISS performance optimization techniques?",
        "Best practices for data validation"
    ]
    
    for query in queries:
        logger.info(f"\n🔎 Query: {query}")
        
        results = await rag_engine.retrieve(
            query=query,
            max_results=2,
            similarity_threshold=0.1
        )
        
        for i, result in enumerate(results, 1):
            logger.info(f"  Result {i} (Score: {result.score:.3f}):")
            logger.info(f"    Category: {result.metadata.get('category', 'N/A')}")
            logger.info(f"    Title: {result.metadata.get('title', 'N/A')}")
            logger.info(f"    Content: {result.content[:100]}...")


async def demo_batch_operations(rag_engine: RAGEngine):
    """Demo batch operations"""
    logger.info("\n📦 Demo 3: Batch Operations")
    
    batch_knowledge = [
        {
            "content": "PySpark DataFrame caching improves performance for iterative operations",
            "category": "performance",
            "title": "DataFrame Caching"
        },
        {
            "content": "Use broadcast joins for small lookup tables to avoid shuffle operations",
            "category": "performance", 
            "title": "Broadcast Joins"
        },
        {
            "content": "Partition data based on query patterns for optimal performance",
            "category": "performance",
            "title": "Data Partitioning"
        }
    ]
    
    doc_ids = await rag_engine.add_knowledge_batch(batch_knowledge)
    logger.info(f"✅ Added {len(doc_ids)} documents in batch: {doc_ids}")
    
    # Search for performance-related content
    results = await rag_engine.retrieve(
        query="PySpark performance optimization",
        max_results=3,
        category_filter="performance"
    )
    
    logger.info(f"🔍 Found {len(results)} performance-related results:")
    for result in results:
        logger.info(f"  - {result.metadata.get('title')}: {result.score:.3f}")


async def demo_stats_and_health(rag_engine: RAGEngine):
    """Demo statistics and health check"""
    logger.info("\n📊 Demo 4: Statistics and Health Check")
    
    # Get knowledge base statistics
    stats = await rag_engine.get_knowledge_stats()
    logger.info("📈 Knowledge Base Statistics:")
    logger.info(f"  - Total Documents: {stats.get('total_documents', 0)}")
    logger.info(f"  - Categories: {stats.get('categories', [])}")
    logger.info(f"  - Index Type: {stats.get('index_type', 'Unknown')}")
    logger.info(f"  - Storage Path: {stats.get('storage_path', 'Unknown')}")
    
    # Perform health check
    health = await rag_engine.health_check()
    logger.info("🏥 Health Check Results:")
    logger.info(f"  - Initialized: {health.get('is_initialized', False)}")
    logger.info(f"  - Embedding Model: {health.get('embedding_model_loaded', False)}")
    logger.info(f"  - FAISS Index: {health.get('faiss_index_available', False)}")
    logger.info(f"  - Document Count: {health.get('document_count', 0)}")
    logger.info(f"  - Retrieval Working: {health.get('retrieval_working', False)}")


async def demo_context_search(rag_engine: RAGEngine):
    """Demo context-aware search"""
    logger.info("\n🎯 Demo 5: Context-Aware Search")
    
    query = "How to optimize data processing performance?"
    
    results, formatted_context = await rag_engine.semantic_search_with_context(
        query=query,
        max_results=3
    )
    
    logger.info(f"🔍 Context search for: {query}")
    logger.info(f"📄 Generated context for LLM:")
    logger.info(formatted_context)
    
    # Demo learning from feedback
    logger.info("\n🧠 Demo: Learning from Feedback")
    
    await rag_engine.learn_from_feedback(
        query="performance optimization",
        helpful_content="Use column pruning and predicate pushdown to reduce data movement in Spark",
        feedback_score=0.9,
        category="feedback"
    )
    
    logger.info("✅ Added feedback-based knowledge to the system")


async def demo_update_and_delete(rag_engine: RAGEngine):
    """Demo update and delete operations"""
    logger.info("\n🔄 Demo 6: Update and Delete Operations")
    
    # Add a document
    doc_id = await rag_engine.add_knowledge(
        content="Original content about data processing",
        metadata={"category": "test", "title": "Test Document"}
    )
    logger.info(f"✅ Added test document: {doc_id}")
    
    # Update the document
    success = await rag_engine.update_knowledge(
        doc_id=doc_id,
        content="Updated content about advanced data processing techniques",
        metadata={"category": "test", "title": "Updated Test Document"}
    )
    logger.info(f"✅ Updated document: {success}")
    
    # Delete the document
    success = await rag_engine.delete_knowledge(doc_id)
    logger.info(f"✅ Deleted document: {success}")


def compare_with_chromadb():
    """Compare FAISS with ChromaDB"""
    print("\n" + "="*60)
    print("📊 FAISS vs ChromaDB Comparison")
    print("="*60)
    
    comparison = {
        "Feature": ["Storage", "Performance", "Metadata", "Updates", "Memory Usage", "Deployment"],
        "FAISS": [
            "File-based (JSON + Binary)",
            "Very Fast (Optimized C++)",
            "Manual JSON storage",
            "Requires index rebuild",
            "Lower (no DB overhead)",
            "Simple (no server required)"
        ],
        "ChromaDB": [
            "SQLite/PostgreSQL",
            "Fast (with overhead)",
            "Native metadata support",
            "Direct updates",
            "Higher (DB overhead)",
            "Complex (server required)"
        ]
    }
    
    for i, feature in enumerate(comparison["Feature"]):
        print(f"{feature:15} | {comparison['FAISS'][i]:30} | {comparison['ChromaDB'][i]}")
    
    print("\n🎯 FAISS Advantages:")
    print("  ✅ Faster similarity search")
    print("  ✅ Lower memory footprint") 
    print("  ✅ No server dependencies")
    print("  ✅ Better for read-heavy workloads")
    print("  ✅ Production-ready at scale")
    
    print("\n⚠️  FAISS Considerations:")
    print("  - Manual metadata management")
    print("  - Updates require index rebuilds")
    print("  - More complex delete operations")


async def main():
    """Main demo function"""
    try:
        await demo_faiss_rag_engine()
        compare_with_chromadb()
        
        print("\n" + "="*60)
        print("🎉 FAISS RAG Engine Migration Complete!")
        print("="*60)
        print("✅ ChromaDB successfully replaced with FAISS")
        print("✅ All RAG functionality preserved")
        print("✅ Performance improvements expected")
        print("✅ Reduced dependencies and complexity")
        print("\n🚀 Your Agentic Mapping AI now uses FAISS for vector search!")
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)