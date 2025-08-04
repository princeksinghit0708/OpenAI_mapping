"""
RAG (Retrieval Augmented Generation) Engine for intelligent context retrieval
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from loguru import logger

from config.settings import settings


@dataclass
class RetrievalResult:
    """Result from RAG retrieval"""
    content: str
    metadata: Dict[str, Any]
    score: float
    source: str


class RAGEngine:
    """
    RAG Engine for intelligent context retrieval and knowledge management
    
    Features:
    - Vector similarity search
    - Context-aware retrieval
    - Knowledge base management
    - Continuous learning from feedback
    """
    
    def __init__(self, collection_name: str = "mapping_knowledge"):
        self.collection_name = collection_name
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self.is_initialized = False
        
        # Initialize asynchronously
        asyncio.create_task(self._initialize())
    
    async def _initialize(self):
        """Initialize the RAG engine"""
        try:
            # Initialize embedding model
            logger.info(f"Loading embedding model: {settings.vector_db.embedding_model}")
            self.embedding_model = SentenceTransformer(settings.vector_db.embedding_model)
            
            # Initialize Chroma client
            if settings.vector_db.type == "chroma":
                self.chroma_client = chromadb.PersistentClient(
                    path=settings.vector_db.chroma_persist_directory,
                    settings=Settings(allow_reset=True)
                )
                
                # Get or create collection
                self.collection = self.chroma_client.get_or_create_collection(
                    name=self.collection_name,
                    metadata={"description": "Knowledge base for mapping and code generation"}
                )
                
                logger.info(f"Initialized RAG engine with collection: {self.collection_name}")
                self.is_initialized = True
                
                # Initialize with default knowledge if collection is empty
                await self._initialize_default_knowledge()
                
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {str(e)}")
            self.is_initialized = False
    
    async def _initialize_default_knowledge(self):
        """Initialize collection with default knowledge"""
        try:
            # Check if collection has documents
            if self.collection.count() == 0:
                logger.info("Initializing with default knowledge base")
                
                default_knowledge = [
                    {
                        "content": """
                        PySpark Data Type Mapping Best Practices:
                        - StringType() for VARCHAR and TEXT fields
                        - IntegerType() for INT fields, LongType() for BIGINT
                        - DoubleType() for FLOAT and DECIMAL fields
                        - BooleanType() for BOOLEAN fields
                        - DateType() for DATE fields, TimestampType() for DATETIME
                        - ArrayType() for arrays, StructType() for nested objects
                        Always use nullable=True unless field is explicitly required.
                        """,
                        "category": "pyspark_patterns",
                        "title": "Data Type Mapping"
                    },
                    {
                        "content": """
                        Schema Validation Patterns:
                        1. Check required fields: providedKey, displayName, physicalName, dataType
                        2. Validate providedKey format: "database.table.field"
                        3. Ensure data types are consistent and valid
                        4. Verify nullable constraints match business rules
                        5. Check for meaningful descriptions
                        6. Validate field name conventions
                        """,
                        "category": "validation_patterns",
                        "title": "Schema Validation Rules"
                    },
                    {
                        "content": """
                        PySpark Performance Optimization:
                        - Use .cache() for DataFrames accessed multiple times
                        - Partition data appropriately with .repartition() or .coalesce()
                        - Use broadcast joins for small lookup tables
                        - Avoid wide transformations when possible
                        - Use vectorized operations over UDFs
                        - Configure spark.sql.adaptive.enabled=true
                        - Set appropriate spark.sql.adaptive.coalescePartitions.enabled
                        """,
                        "category": "performance_optimization",
                        "title": "PySpark Performance Tips"
                    },
                    {
                        "content": """
                        Error Handling Best Practices:
                        - Validate input data before processing
                        - Use try-except blocks for external operations
                        - Log errors with context and stack traces
                        - Implement graceful degradation for non-critical failures
                        - Use data quality checks throughout pipeline
                        - Implement retry mechanisms for transient failures
                        - Always clean up resources in finally blocks
                        """,
                        "category": "error_handling",
                        "title": "Error Handling Patterns"
                    },
                    {
                        "content": """
                        Database Name Extraction Patterns:
                        1. First check field-level providedKey values
                        2. Look for dictionary.providedKey in document root
                        3. Search for database/db_name/schema keys recursively
                        4. Extract last part of dot-separated providedKey
                        5. Validate against common naming conventions
                        6. Fallback to intelligent LLM-based extraction
                        """,
                        "category": "extraction_patterns",
                        "title": "Database Name Extraction"
                    }
                ]
                
                await self.add_knowledge_batch(default_knowledge)
                logger.info(f"Added {len(default_knowledge)} default knowledge entries")
                
        except Exception as e:
            logger.error(f"Failed to initialize default knowledge: {str(e)}")
    
    async def add_knowledge(
        self, 
        content: str, 
        metadata: Dict[str, Any], 
        doc_id: Optional[str] = None
    ) -> str:
        """
        Add knowledge to the vector store
        
        Args:
            content: Text content to store
            metadata: Associated metadata
            doc_id: Optional document ID
            
        Returns:
            Document ID
        """
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Generate embedding
            embedding = self.embedding_model.encode([content])[0].tolist()
            
            # Generate ID if not provided
            if not doc_id:
                doc_id = f"doc_{datetime.utcnow().timestamp()}"
            
            # Add to collection
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.debug(f"Added knowledge document: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to add knowledge: {str(e)}")
            raise
    
    async def add_knowledge_batch(self, knowledge_items: List[Dict[str, Any]]) -> List[str]:
        """Add multiple knowledge items in batch"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            contents = []
            metadatas = []
            ids = []
            
            for item in knowledge_items:
                content = item["content"]
                metadata = {k: v for k, v in item.items() if k != "content"}
                doc_id = f"doc_{len(ids)}_{datetime.utcnow().timestamp()}"
                
                contents.append(content)
                metadatas.append(metadata)
                ids.append(doc_id)
            
            # Generate embeddings in batch
            embeddings = self.embedding_model.encode(contents).tolist()
            
            # Add to collection
            self.collection.add(
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(knowledge_items)} knowledge items in batch")
            return ids
            
        except Exception as e:
            logger.error(f"Failed to add knowledge batch: {str(e)}")
            raise
    
    async def retrieve(
        self, 
        query: str, 
        max_results: int = 5,
        similarity_threshold: float = None,
        category_filter: Optional[str] = None
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant knowledge based on query
        
        Args:
            query: Search query
            max_results: Maximum number of results
            similarity_threshold: Minimum similarity score
            category_filter: Filter by category
            
        Returns:
            List of retrieval results
        """
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0].tolist()
            
            # Prepare where clause for filtering
            where = {}
            if category_filter:
                where["category"] = category_filter
            
            # Search in collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                where=where if where else None
            )
            
            # Process results
            retrieval_results = []
            
            if results and results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i] if results["distances"] else 0
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    # Apply similarity threshold
                    if similarity_threshold and similarity < similarity_threshold:
                        continue
                    
                    metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                    doc_id = results["ids"][0][i] if results["ids"] else f"doc_{i}"
                    
                    retrieval_results.append(RetrievalResult(
                        content=doc,
                        metadata=metadata,
                        score=similarity,
                        source=doc_id
                    ))
            
            logger.debug(f"Retrieved {len(retrieval_results)} results for query: {query[:50]}...")
            return retrieval_results
            
        except Exception as e:
            logger.error(f"Failed to retrieve knowledge: {str(e)}")
            return []
    
    async def update_knowledge(
        self, 
        doc_id: str, 
        content: str, 
        metadata: Dict[str, Any]
    ) -> bool:
        """Update existing knowledge"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Generate new embedding
            embedding = self.embedding_model.encode([content])[0].tolist()
            
            # Update in collection
            self.collection.update(
                ids=[doc_id],
                documents=[content],
                embeddings=[embedding],
                metadatas=[metadata]
            )
            
            logger.debug(f"Updated knowledge document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update knowledge: {str(e)}")
            return False
    
    async def delete_knowledge(self, doc_id: str) -> bool:
        """Delete knowledge by ID"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            self.collection.delete(ids=[doc_id])
            logger.debug(f"Deleted knowledge document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete knowledge: {str(e)}")
            return False
    
    async def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            count = self.collection.count()
            
            # Get sample of metadata to analyze categories
            sample_results = self.collection.get(limit=100)
            categories = set()
            
            if sample_results and sample_results["metadatas"]:
                for metadata in sample_results["metadatas"]:
                    if "category" in metadata:
                        categories.add(metadata["category"])
            
            return {
                "total_documents": count,
                "categories": list(categories),
                "collection_name": self.collection_name,
                "embedding_model": settings.vector_db.embedding_model,
                "is_initialized": self.is_initialized
            }
            
        except Exception as e:
            logger.error(f"Failed to get knowledge stats: {str(e)}")
            return {"error": str(e)}
    
    async def semantic_search_with_context(
        self, 
        query: str, 
        context_window: int = 3,
        max_results: int = 5
    ) -> Tuple[List[RetrievalResult], str]:
        """
        Perform semantic search and return formatted context
        
        Args:
            query: Search query
            context_window: Number of related documents to include
            max_results: Maximum results
            
        Returns:
            Tuple of (results, formatted_context)
        """
        results = await self.retrieve(query, max_results=max_results)
        
        # Format context for LLM consumption
        context_parts = []
        
        for i, result in enumerate(results):
            context_parts.append(f"""
Context {i+1} (Score: {result.score:.3f}):
Category: {result.metadata.get('category', 'general')}
Title: {result.metadata.get('title', 'Untitled')}
Content: {result.content}
""")
        
        formatted_context = "\n".join(context_parts)
        
        return results, formatted_context
    
    async def learn_from_feedback(
        self, 
        query: str, 
        helpful_content: str, 
        feedback_score: float,
        category: str = "feedback"
    ):
        """Learn from user feedback"""
        try:
            metadata = {
                "category": category,
                "title": f"Feedback for: {query[:50]}",
                "original_query": query,
                "feedback_score": feedback_score,
                "timestamp": datetime.utcnow().isoformat(),
                "source": "user_feedback"
            }
            
            await self.add_knowledge(helpful_content, metadata)
            logger.info(f"Added feedback-based knowledge for query: {query[:50]}")
            
        except Exception as e:
            logger.error(f"Failed to learn from feedback: {str(e)}")
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on RAG engine"""
        health_status = {
            "is_initialized": self.is_initialized,
            "embedding_model_loaded": self.embedding_model is not None,
            "chroma_client_connected": self.chroma_client is not None,
            "collection_accessible": False,
            "document_count": 0,
            "last_check": datetime.utcnow().isoformat()
        }
        
        try:
            if self.collection:
                health_status["collection_accessible"] = True
                health_status["document_count"] = self.collection.count()
                
            # Test retrieval
            test_results = await self.retrieve("test query", max_results=1)
            health_status["retrieval_working"] = len(test_results) >= 0
            
        except Exception as e:
            health_status["error"] = str(e)
        
        return health_status