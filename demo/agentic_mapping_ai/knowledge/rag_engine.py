"""
RAG (Retrieval Augmented Generation) Engine for intelligent context retrieval using FAISS
"""

import asyncio
import json
import pickle
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

import faiss
from sentence_transformers import SentenceTransformer
from loguru import logger

from agentic_mapping_ai.config.settings import settings


@dataclass
class RetrievalResult:
    """Result from RAG retrieval"""
    content: str
    metadata: Dict[str, Any]
    score: float
    source: str


class RAGEngine:
    """
    RAG Engine for intelligent context retrieval and knowledge management using FAISS
    
    Features:
    - Vector similarity search using FAISS
    - Context-aware retrieval
    - Knowledge base management
    - Continuous learning from feedback
    - Persistent storage of embeddings and metadata
    """
    
    def __init__(self, collection_name: str = "mapping_knowledge"):
        self.collection_name = collection_name
        self.embedding_model = None
        self.faiss_index = None
        self.is_initialized = False
        
        # Storage paths
        self.base_path = Path(settings.vector_db.faiss_persist_directory if hasattr(settings.vector_db, 'faiss_persist_directory') else "./data/faiss_db")
        self.index_path = self.base_path / f"{collection_name}_index.faiss"
        self.metadata_path = self.base_path / f"{collection_name}_metadata.json"
        self.id_mapping_path = self.base_path / f"{collection_name}_id_mapping.json"
        
        # In-memory storage for metadata and mappings
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self.document_store: Dict[int, str] = {}
        self.document_metadata: List[Dict[str, Any]] = []  # Missing attribute
        self.next_index = 0
        
        # Initialize asynchronously
        asyncio.create_task(self._initialize())
    
    async def _initialize(self):
        """Initialize the RAG engine with FAISS"""
        try:
            # Initialize embedding model with fallback
            logger.info(f"Loading embedding model: {settings.vector_db.embedding_model}")
            
            # Try to load model with offline fallback
            try:
                self.embedding_model = SentenceTransformer(settings.vector_db.embedding_model)
                logger.info("✅ Successfully loaded embedding model")
            except Exception as model_error:
                logger.warning(f"Failed to load embedding model: {model_error}")
                logger.info("🔄 Falling back to simple embedding simulation for demo")
                self.embedding_model = None  # Will use simulated embeddings
            
            # Create base directory if it doesn't exist
            self.base_path.mkdir(parents=True, exist_ok=True)
            
            # Load existing index and metadata if available
            if self.index_path.exists() and self.embedding_model is not None:
                await self._load_existing_index()
            elif self.embedding_model is not None:
                await self._create_new_index()
            else:
                # Offline mode - create minimal index
                logger.info("🔄 Running in offline mode - limited RAG functionality")
                await self._create_offline_index()
            
            logger.info(f"Initialized FAISS RAG engine with collection: {self.collection_name}")
            self.is_initialized = True
            
            # Initialize with default knowledge if index is empty and model available
            if self.embedding_model is not None and self._get_document_count() == 0:
                await self._initialize_default_knowledge()
                
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {str(e)}")
            logger.info("🔄 RAG engine running in minimal mode")
            self.is_initialized = False
    
    async def _create_new_index(self):
        """Create a new FAISS index"""
        # Get embedding dimension
        test_embedding = self._encode_texts(["test"])
        embedding_dim = test_embedding.shape[1]
        
        # Create FAISS index (using IndexFlatIP for cosine similarity)
        self.faiss_index = faiss.IndexFlatIP(embedding_dim)
        
        logger.info(f"Created new FAISS index with dimension: {embedding_dim}")
    
    async def _create_offline_index(self):
        """Create a minimal index for offline mode"""
        import numpy as np
        import hashlib
        
        # Create a simple 384-dimensional index (default for many models)
        embedding_dim = 384
        self.faiss_index = faiss.IndexFlatIP(embedding_dim)
        
        logger.info(f"Created offline FAISS index with dimension {embedding_dim}")
        
        # Add some demo data for offline mode
        demo_texts = [
            "Banking account transformation mapping",
            "Customer data field mapping", 
            "Transaction processing logic",
            "Data validation rules",
            "PySpark code generation"
        ]
        
        for text in demo_texts:
            # Create simple hash-based embedding
            embedding = self._create_simple_embedding(text, embedding_dim)
            self.faiss_index.add(embedding.reshape(1, -1).astype('float32'))
            
            # Store metadata
            self.document_metadata.append({
                'content': text,
                'metadata': {'source': 'demo', 'offline_mode': True},
                'id': f"demo_{len(self.document_metadata)}"
            })
    
    def _create_simple_embedding(self, text: str, dim: int) -> 'numpy.ndarray':
        """Create a simple hash-based embedding for offline mode"""
        import numpy as np
        import hashlib
        
        # Create hash of text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Convert hash to numbers and normalize
        numbers = [ord(c) for c in text_hash]
        
        # Extend/truncate to desired dimension
        if len(numbers) < dim:
            numbers = numbers * (dim // len(numbers) + 1)
        numbers = numbers[:dim]
        
        # Normalize to unit vector
        embedding = np.array(numbers, dtype=np.float32)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def _get_document_count(self) -> int:
        """Get the number of documents in the index"""
        if self.faiss_index is not None:
            return self.faiss_index.ntotal
        return 0
    
    def _encode_text(self, text: str) -> 'numpy.ndarray':
        """Encode text with fallback for offline mode"""
        if self.embedding_model is not None:
            # Use real model
            return self.embedding_model.encode([text])[0]
        else:
            # Use simple embedding for offline mode
            return self._create_simple_embedding(text, 384)
    
    def _encode_texts(self, texts: list) -> 'numpy.ndarray':
        """Encode multiple texts with fallback for offline mode"""
        if self.embedding_model is not None:
            # Use real model
            return self.embedding_model.encode(texts)
        else:
            # Use simple embeddings for offline mode
            import numpy as np
            embeddings = []
            for text in texts:
                embeddings.append(self._create_simple_embedding(text, 384))
            return np.array(embeddings)
    
    async def _load_existing_index(self):
        """Load existing FAISS index and metadata"""
        try:
            # Load FAISS index
            self.faiss_index = faiss.read_index(str(self.index_path))
            
            # Load metadata
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r') as f:
                    metadata_data = json.load(f)
                    # Convert string keys back to int
                    self.metadata_store = {int(k): v for k, v in metadata_data['metadata'].items()}
                    self.document_store = {int(k): v for k, v in metadata_data['documents'].items()}
            
            # Load ID mappings
            if self.id_mapping_path.exists():
                with open(self.id_mapping_path, 'r') as f:
                    mapping_data = json.load(f)
                    self.id_to_index = mapping_data['id_to_index']
                    # Convert string keys back to int for index_to_id
                    self.index_to_id = {int(k): v for k, v in mapping_data['index_to_id'].items()}
                    self.next_index = mapping_data.get('next_index', 0)
            
            logger.info(f"Loaded existing FAISS index with {self.faiss_index.ntotal} vectors")
            
        except Exception as e:
            logger.error(f"Failed to load existing index: {str(e)}")
            await self._create_new_index()
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.faiss_index, str(self.index_path))
            
            # Save metadata and documents
            metadata_data = {
                'metadata': {str(k): v for k, v in self.metadata_store.items()},
                'documents': {str(k): v for k, v in self.document_store.items()}
            }
            with open(self.metadata_path, 'w') as f:
                json.dump(metadata_data, f, indent=2)
            
            # Save ID mappings
            mapping_data = {
                'id_to_index': self.id_to_index,
                'index_to_id': {str(k): v for k, v in self.index_to_id.items()},
                'next_index': self.next_index
            }
            with open(self.id_mapping_path, 'w') as f:
                json.dump(mapping_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save index: {str(e)}")
    
    def _get_document_count(self) -> int:
        """Get total number of documents in the index"""
        return self.faiss_index.ntotal if self.faiss_index else 0
    
    async def _initialize_default_knowledge(self):
        """Initialize collection with default knowledge"""
        try:
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
        Add knowledge to the FAISS vector store
        
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
            embedding = self._encode_text(content)
            # Normalize for cosine similarity
            embedding = embedding / np.linalg.norm(embedding)
            
            # Generate ID if not provided
            if not doc_id:
                doc_id = f"doc_{datetime.utcnow().timestamp()}"
            
            # Check if document already exists
            if doc_id in self.id_to_index:
                logger.warning(f"Document {doc_id} already exists, updating instead")
                return await self.update_knowledge(doc_id, content, metadata)
            
            # Add to FAISS index
            current_index = self.next_index
            self.faiss_index.add(embedding.reshape(1, -1))
            
            # Store metadata and mappings
            self.metadata_store[current_index] = metadata
            self.document_store[current_index] = content
            self.id_to_index[doc_id] = current_index
            self.index_to_id[current_index] = doc_id
            self.next_index += 1
            
            # Save to disk
            self._save_index()
            
            logger.debug(f"Added knowledge document: {doc_id} at index {current_index}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to add knowledge: {str(e)}")
            raise
    
    async def add_knowledge_batch(self, knowledge_items: List[Dict[str, Any]]) -> List[str]:
        """Add multiple knowledge items in batch using FAISS"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            contents = []
            metadatas = []
            ids = []
            
            for i, item in enumerate(knowledge_items):
                content = item["content"]
                metadata = {k: v for k, v in item.items() if k != "content"}
                doc_id = f"doc_{i}_{datetime.utcnow().timestamp()}"
                
                contents.append(content)
                metadatas.append(metadata)
                ids.append(doc_id)
            
            # Generate embeddings in batch
            embeddings = self._encode_texts(contents)
            # Normalize embeddings for cosine similarity
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            
            # Add to FAISS index
            start_index = self.next_index
            self.faiss_index.add(embeddings)
            
            # Store metadata and mappings
            for i, (doc_id, content, metadata) in enumerate(zip(ids, contents, metadatas)):
                current_index = start_index + i
                self.metadata_store[current_index] = metadata
                self.document_store[current_index] = content
                self.id_to_index[doc_id] = current_index
                self.index_to_id[current_index] = doc_id
            
            self.next_index += len(knowledge_items)
            
            # Save to disk
            self._save_index()
            
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
        Retrieve relevant knowledge based on query using FAISS
        
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
            if self.faiss_index.ntotal == 0:
                logger.debug("No documents in index")
                return []
            
            # Generate query embedding
            query_embedding = self._encode_text(query)
            # Normalize for cosine similarity
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            
            # Search in FAISS index
            search_k = min(max_results * 2, self.faiss_index.ntotal)  # Search more to allow for filtering
            scores, indices = self.faiss_index.search(query_embedding.reshape(1, -1), search_k)
            
            # Process results
            retrieval_results = []
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx == -1:  # FAISS returns -1 for empty slots
                    continue
                    
                # Convert score to similarity (FAISS returns inner product for normalized vectors)
                similarity = float(score)
                
                # Apply similarity threshold
                if similarity_threshold and similarity < similarity_threshold:
                    continue
                
                # Get metadata and document
                metadata = self.metadata_store.get(idx, {})
                content = self.document_store.get(idx, "")
                doc_id = self.index_to_id.get(idx, f"doc_{idx}")
                
                # Apply category filter
                if category_filter and metadata.get("category") != category_filter:
                    continue
                
                retrieval_results.append(RetrievalResult(
                    content=content,
                    metadata=metadata,
                    score=similarity,
                    source=doc_id
                ))
                
                # Stop if we have enough results
                if len(retrieval_results) >= max_results:
                    break
            
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
        """Update existing knowledge in FAISS (requires rebuilding index)"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Check if document exists
            if doc_id not in self.id_to_index:
                logger.error(f"Document {doc_id} not found")
                return False
            
            # Get the index
            idx = self.id_to_index[doc_id]
            
            # Update metadata and content
            self.metadata_store[idx] = metadata
            self.document_store[idx] = content
            
            # For FAISS, we need to rebuild the index for the updated embedding
            # Generate new embedding
            embedding = self._encode_text(content)
            embedding = embedding / np.linalg.norm(embedding)
            
            # Note: FAISS doesn't support direct updates, so we rebuild the entire index
            # For production, consider using FAISS IndexIDMap for better update support
            await self._rebuild_index_with_updated_embedding(idx, embedding)
            
            # Save to disk
            self._save_index()
            
            logger.debug(f"Updated knowledge document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update knowledge: {str(e)}")
            return False
    
    async def _rebuild_index_with_updated_embedding(self, update_idx: int, new_embedding: np.ndarray):
        """Rebuild FAISS index with updated embedding"""
        # Get all embeddings
        all_embeddings = []
        
        for i in range(self.faiss_index.ntotal):
            if i == update_idx:
                # Use new embedding for updated document
                all_embeddings.append(new_embedding)
            else:
                # Get existing embedding from index
                embedding = self.faiss_index.reconstruct(i)
                all_embeddings.append(embedding)
        
        # Rebuild index
        if all_embeddings:
            embeddings_array = np.array(all_embeddings)
            self.faiss_index.reset()
            self.faiss_index.add(embeddings_array)
    
    async def delete_knowledge(self, doc_id: str) -> bool:
        """Delete knowledge by ID (requires rebuilding index)"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Check if document exists
            if doc_id not in self.id_to_index:
                logger.error(f"Document {doc_id} not found")
                return False
            
            # Get the index to delete
            delete_idx = self.id_to_index[doc_id]
            
            # Remove from stores
            del self.metadata_store[delete_idx]
            del self.document_store[delete_idx]
            del self.id_to_index[doc_id]
            del self.index_to_id[delete_idx]
            
            # Rebuild index without the deleted document
            await self._rebuild_index_excluding(delete_idx)
            
            # Save to disk
            self._save_index()
            
            logger.debug(f"Deleted knowledge document: {doc_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete knowledge: {str(e)}")
            return False
    
    async def _rebuild_index_excluding(self, exclude_idx: int):
        """Rebuild FAISS index excluding a specific index"""
        # Collect all embeddings except the one to exclude
        all_embeddings = []
        new_mappings = {}
        new_metadata = {}
        new_documents = {}
        new_id_to_index = {}
        new_index_to_id = {}
        new_idx = 0
        
        for i in range(self.faiss_index.ntotal):
            if i != exclude_idx:
                # Get existing embedding
                embedding = self.faiss_index.reconstruct(i)
                all_embeddings.append(embedding)
                
                # Update mappings
                if i in self.index_to_id:
                    doc_id = self.index_to_id[i]
                    new_id_to_index[doc_id] = new_idx
                    new_index_to_id[new_idx] = doc_id
                
                if i in self.metadata_store:
                    new_metadata[new_idx] = self.metadata_store[i]
                
                if i in self.document_store:
                    new_documents[new_idx] = self.document_store[i]
                
                new_idx += 1
        
        # Rebuild index
        if all_embeddings:
            embeddings_array = np.array(all_embeddings)
            self.faiss_index.reset()
            self.faiss_index.add(embeddings_array)
        else:
            self.faiss_index.reset()
        
        # Update mappings
        self.metadata_store = new_metadata
        self.document_store = new_documents
        self.id_to_index = new_id_to_index
        self.index_to_id = new_index_to_id
        self.next_index = new_idx
    
    async def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics from FAISS"""
        if not self.is_initialized:
            await self._initialize()
        
        try:
            count = self._get_document_count()
            
            # Analyze categories from metadata
            categories = set()
            for metadata in self.metadata_store.values():
                if "category" in metadata:
                    categories.add(metadata["category"])
            
            return {
                "total_documents": count,
                "categories": list(categories),
                "collection_name": self.collection_name,
                "embedding_model": settings.vector_db.embedding_model,
                "is_initialized": self.is_initialized,
                "index_type": "FAISS",
                "storage_path": str(self.base_path)
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
        Perform semantic search and return formatted context using FAISS
        
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
        """Learn from user feedback and add to FAISS index"""
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
        """Perform health check on FAISS RAG engine"""
        health_status = {
            "is_initialized": self.is_initialized,
            "embedding_model_loaded": self.embedding_model is not None,
            "faiss_index_available": self.faiss_index is not None,
            "index_accessible": False,
            "document_count": 0,
            "storage_accessible": False,
            "last_check": datetime.utcnow().isoformat()
        }
        
        try:
            if self.faiss_index:
                health_status["index_accessible"] = True
                health_status["document_count"] = self.faiss_index.ntotal
            
            # Check storage accessibility
            health_status["storage_accessible"] = self.base_path.exists()
            
            # Test retrieval
            if self.faiss_index and self.faiss_index.ntotal > 0:
                test_results = await self.retrieve("test query", max_results=1)
                health_status["retrieval_working"] = len(test_results) >= 0
            else:
                health_status["retrieval_working"] = True  # No documents to retrieve
                
        except Exception as e:
            health_status["error"] = str(e)
        
        return health_status