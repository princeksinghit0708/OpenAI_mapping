#!/usr/bin/env python3
"""
Advanced FAISS Similarity Search Engine for Chat-Based Demo
Features: Complex similarity search, chat suggestion storage, model training data
"""

import numpy as np
import json
import pickle
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import faiss
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAISSSimilarityEngine:
    """
    Advanced FAISS similarity search engine with chat suggestion storage
    """
    
    def __init__(self, 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 dimension: int = 384,
                 collection_name: str = "chat_similarity_db"):
        
        self.embedding_model_name = embedding_model
        self.dimension = dimension
        self.collection_name = collection_name
        
        # Initialize components
        self.embedding_model = None
        self.faiss_index = None
        self.is_initialized = False
        
        # Storage paths
        self.base_path = Path(f"./data/faiss_db/{collection_name}")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.index_path = self.base_path / f"{collection_name}_index.faiss"
        self.metadata_path = self.base_path / f"{collection_name}_metadata.json"
        self.suggestions_path = self.base_path / f"{collection_name}_suggestions.json"
        self.training_data_path = self.base_path / f"{collection_name}_training_data.json"
        
        # In-memory storage
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.suggestions_store: Dict[int, Dict[str, Any]] = {}
        self.training_data_store: Dict[int, Dict[str, Any]] = {}
        self.id_to_index: Dict[str, int] = {}
        self.index_to_id: Dict[int, str] = {}
        self.next_index = 0
        
        # Don't initialize automatically - will be done on first use
        # asyncio.create_task(self._initialize())
    
    async def _initialize(self):
        """Initialize the FAISS similarity engine"""
        try:
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            self.embedding_model = SentenceTransformer(self.embedding_model_name)
            
            # Load existing index and metadata if available
            if self.index_path.exists():
                await self._load_existing_index()
            else:
                await self._create_new_index()
            
            # Load existing data
            await self._load_existing_data()
            
            logger.info(f"FAISS Similarity Engine initialized: {self.collection_name}")
            self.is_initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize FAISS engine: {str(e)}")
            self.is_initialized = False
    
    async def _create_new_index(self):
        """Create a new FAISS index"""
        try:
            # Get embedding dimension from model
            test_embedding = self.embedding_model.encode(["test"])
            self.dimension = test_embedding.shape[1]
            
            # Create optimized FAISS index for similarity search
            # Using IndexFlatIP for inner product (cosine similarity when normalized)
            self.faiss_index = faiss.IndexFlatIP(self.dimension)
            
            # Add normalization for better similarity search
            self.faiss_index = faiss.IndexIDMap(self.faiss_index)
            
            logger.info(f"Created new FAISS index with dimension: {self.dimension}")
            
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {str(e)}")
            raise
    
    async def _load_existing_index(self):
        """Load existing FAISS index"""
        try:
            self.faiss_index = faiss.read_index(str(self.index_path))
            logger.info(f"Loaded existing FAISS index: {self.index_path}")
            
        except Exception as e:
            logger.error(f"Failed to load existing index: {str(e)}")
            await self._create_new_index()
    
    async def _load_existing_data(self):
        """Load existing metadata and suggestions"""
        try:
            # Load metadata
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r') as f:
                    data = json.load(f)
                    self.metadata_store = data.get('metadata_store', {})
                    self.suggestions_store = data.get('suggestions_store', {})
                    self.training_data_store = data.get('training_data_store', {})
                    self.id_to_index = data.get('id_to_index', {})
                    self.index_to_id = data.get('index_to_id', {})
                    self.next_index = data.get('next_index', 0)
                
                logger.info(f"Loaded existing data: {len(self.metadata_store)} items")
            
        except Exception as e:
            logger.error(f"Failed to load existing data: {str(e)}")
    
    async def _save_data(self):
        """Save all data to disk"""
        try:
            data = {
                'metadata_store': self.metadata_store,
                'suggestions_store': self.suggestions_store,
                'training_data_store': self.training_data_store,
                'id_to_index': self.id_to_index,
                'index_to_id': self.index_to_id,
                'next_index': self.next_index,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.metadata_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            # Save FAISS index
            if self.faiss_index:
                faiss.write_index(self.faiss_index, str(self.index_path))
            
            logger.debug("Data saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")
    
    async def add_chat_suggestion(self, 
                                 user_input: str, 
                                 ai_response: str, 
                                 context: Dict[str, Any] = None,
                                 feedback_score: float = None,
                                 category: str = "general") -> str:
        """
        Add a chat suggestion to the FAISS database
        
        Args:
            user_input: User's chat input
            ai_response: AI agent's response
            context: Additional context (file info, agent used, etc.)
            feedback_score: User feedback score (0.0 to 1.0)
            category: Category for organization
            
        Returns:
            Suggestion ID
        """
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Combine user input and AI response for embedding
            combined_text = f"User: {user_input}\nAI: {ai_response}"
            
            # Generate embedding
            embedding = self.embedding_model.encode([combined_text])[0]
            embedding = embedding / np.linalg.norm(embedding)  # Normalize
            
            # Generate ID
            suggestion_id = f"suggestion_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.next_index}"
            
            # Store in FAISS
            current_index = self.next_index
            self.faiss_index.add_with_ids(embedding.reshape(1, -1), np.array([current_index]))
            
            # Store metadata
            metadata = {
                'user_input': user_input,
                'ai_response': ai_response,
                'category': category,
                'feedback_score': feedback_score,
                'timestamp': datetime.now().isoformat(),
                'context': context or {},
                'embedding_dim': self.dimension,
                'type': 'chat_suggestion'
            }
            
            self.metadata_store[current_index] = metadata
            self.id_to_index[suggestion_id] = current_index
            self.index_to_id[current_index] = suggestion_id
            
            # Store in suggestions store
            self.suggestions_store[current_index] = {
                'suggestion_id': suggestion_id,
                'user_input': user_input,
                'ai_response': ai_response,
                'category': category,
                'feedback_score': feedback_score,
                'context': context or {},
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in training data store
            self.training_data_store[current_index] = {
                'input': user_input,
                'output': ai_response,
                'category': category,
                'feedback_score': feedback_score,
                'context': context or {},
                'timestamp': datetime.now().isoformat(),
                'embedding': embedding.tolist()  # Store for training
            }
            
            self.next_index += 1
            
            # Save to disk
            await self._save_data()
            
            logger.info(f"Added chat suggestion: {suggestion_id}")
            return suggestion_id
            
        except Exception as e:
            logger.error(f"Failed to add chat suggestion: {str(e)}")
            raise
    
    async def find_similar_suggestions(self, 
                                     query: str, 
                                     top_k: int = 5, 
                                     category: str = None,
                                     min_similarity: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find similar chat suggestions based on query
        
        Args:
            query: Search query
            top_k: Number of results to return
            category: Filter by category
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar suggestions with scores
        """
        if not self.is_initialized:
            await self._initialize()
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            query_embedding = query_embedding / np.linalg.norm(query_embedding)
            
            # Search FAISS index
            query_array = query_embedding.reshape(1, -1)
            scores, indices = self.faiss_index.search(query_array, min(top_k * 2, self.next_index))
            
            results = []
            for score, index in zip(scores[0], indices[0]):
                if index == -1:  # FAISS returns -1 for invalid indices
                    continue
                
                if score < min_similarity:
                    continue
                
                if index in self.suggestions_store:
                    suggestion = self.suggestions_store[index].copy()
                    suggestion['similarity_score'] = float(score)
                    suggestion['index'] = int(index)
                    
                    # Filter by category if specified
                    if category and suggestion.get('category') != category:
                        continue
                    
                    results.append(suggestion)
                    
                    if len(results) >= top_k:
                        break
            
            # Sort by similarity score
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            logger.info(f"Found {len(results)} similar suggestions for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to find similar suggestions: {str(e)}")
            return []
    
    async def get_suggestions_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get suggestions filtered by category"""
        try:
            results = []
            for index, suggestion in self.suggestions_store.items():
                if suggestion.get('category') == category:
                    results.append(suggestion.copy())
                    if len(results) >= limit:
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to get suggestions by category: {str(e)}")
            return []
    
    async def update_feedback(self, suggestion_id: str, feedback_score: float) -> bool:
        """Update feedback score for a suggestion"""
        try:
            if suggestion_id in self.id_to_index:
                index = self.id_to_index[suggestion_id]
                
                if index in self.suggestions_store:
                    self.suggestions_store[index]['feedback_score'] = feedback_score
                
                if index in self.training_data_store:
                    self.training_data_store[index]['feedback_score'] = feedback_score
                
                if index in self.metadata_store:
                    self.metadata_store[index]['feedback_score'] = feedback_score
                
                await self._save_data()
                logger.info(f"Updated feedback for {suggestion_id}: {feedback_score}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to update feedback: {str(e)}")
            return False
    
    async def export_training_data(self, 
                                 output_path: str = None, 
                                 format: str = "json",
                                 include_embeddings: bool = True) -> str:
        """
        Export training data for model training
        
        Args:
            output_path: Output file path
            format: Export format (json, csv, pickle)
            include_embeddings: Whether to include embeddings
            
        Returns:
            Path to exported file
        """
        try:
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"./data/training_data/training_data_{timestamp}.{format}"
            
            # Create output directory
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare training data
            training_data = []
            for index, data in self.training_data_store.items():
                export_data = {
                    'input': data['input'],
                    'output': data['output'],
                    'category': data['category'],
                    'feedback_score': data['feedback_score'],
                    'context': data['context'],
                    'timestamp': data['timestamp']
                }
                
                if include_embeddings:
                    export_data['embedding'] = data['embedding']
                
                training_data.append(export_data)
            
            # Export based on format
            if format == "json":
                with open(output_path, 'w') as f:
                    json.dump(training_data, f, indent=2, default=str)
            
            elif format == "pickle":
                with open(output_path, 'wb') as f:
                    pickle.dump(training_data, f)
            
            elif format == "csv":
                import pandas as pd
                df = pd.DataFrame(training_data)
                df.to_csv(output_path, index=False)
            
            logger.info(f"Exported {len(training_data)} training examples to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to export training data: {str(e)}")
            raise
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                'total_suggestions': len(self.suggestions_store),
                'total_training_examples': len(self.training_data_store),
                'categories': {},
                'feedback_distribution': {},
                'embedding_dimension': self.dimension,
                'faiss_index_size': self.faiss_index.ntotal if self.faiss_index else 0,
                'last_updated': datetime.now().isoformat()
            }
            
            # Category distribution
            for suggestion in self.suggestions_store.values():
                category = suggestion.get('category', 'unknown')
                stats['categories'][category] = stats['categories'].get(category, 0) + 1
            
            # Feedback distribution
            for suggestion in self.suggestions_store.values():
                score = suggestion.get('feedback_score')
                if score is not None:
                    score_range = f"{int(score * 10) * 0.1:.1f}-{(int(score * 10) + 1) * 0.1:.1f}"
                    stats['feedback_distribution'][score_range] = stats['feedback_distribution'].get(score_range, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    async def search_complex_similarity(self, 
                                      query: str, 
                                      filters: Dict[str, Any] = None,
                                      top_k: int = 10,
                                      similarity_threshold: float = 0.3) -> List[Dict[str, Any]]:
        """
        Complex similarity search with advanced filtering
        
        Args:
            query: Search query
            filters: Advanced filters (category, feedback_score, date_range, etc.)
            top_k: Number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            Filtered and ranked results
        """
        try:
            # Get base similarity results
            base_results = await self.find_similar_suggestions(
                query, 
                top_k=top_k * 2,  # Get more results for filtering
                min_similarity=similarity_threshold
            )
            
            # Apply filters
            filtered_results = []
            for result in base_results:
                if self._apply_filters(result, filters):
                    filtered_results.append(result)
                    if len(filtered_results) >= top_k:
                        break
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Complex similarity search failed: {str(e)}")
            return []
    
    def _apply_filters(self, result: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Apply filters to a result"""
        if not filters:
            return True
        
        try:
            for key, value in filters.items():
                if key == 'category' and result.get('category') != value:
                    return False
                
                elif key == 'min_feedback_score' and result.get('feedback_score', 0) < value:
                    return False
                
                elif key == 'max_feedback_score' and result.get('feedback_score', 1) > value:
                    return False
                
                elif key == 'date_range':
                    start_date, end_date = value
                    result_date = datetime.fromisoformat(result.get('timestamp', ''))
                    if start_date and result_date < start_date:
                        return False
                    if end_date and result_date > end_date:
                        return False
                
                elif key == 'context_key' and key in filters:
                    context_value = filters['context_key']
                    if context_value not in str(result.get('context', {})):
                        return False
            
            return True
            
        except Exception as e:
            logger.error(f"Filter application failed: {str(e)}")
            return True
    
    async def cleanup_old_suggestions(self, days_old: int = 30) -> int:
        """Clean up old suggestions to save space"""
        try:
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            removed_count = 0
            
            indices_to_remove = []
            for index, suggestion in self.suggestions_store.items():
                timestamp = datetime.fromisoformat(suggestion.get('timestamp', '')).timestamp()
                if timestamp < cutoff_date:
                    indices_to_remove.append(index)
            
            # Remove old suggestions
            for index in indices_to_remove:
                if index in self.suggestions_store:
                    del self.suggestions_store[index]
                if index in self.training_data_store:
                    del self.training_data_store[index]
                if index in self.metadata_store:
                    del self.metadata_store[index]
                removed_count += 1
            
            # Rebuild FAISS index
            if removed_count > 0:
                await self._rebuild_index()
                await self._save_data()
            
            logger.info(f"Cleaned up {removed_count} old suggestions")
            return removed_count
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return 0
    
    async def _rebuild_index(self):
        """Rebuild FAISS index after cleanup"""
        try:
            # Create new index
            self.faiss_index = faiss.IndexFlatIP(self.dimension)
            self.faiss_index = faiss.IndexIDMap(self.faiss_index)
            
            # Re-add all remaining embeddings
            for index, metadata in self.metadata_store.items():
                if index in self.training_data_store:
                    embedding = np.array(self.training_data_store[index]['embedding'])
                    self.faiss_index.add_with_ids(embedding.reshape(1, -1), np.array([index]))
            
            logger.info("FAISS index rebuilt successfully")
            
        except Exception as e:
            logger.error(f"Index rebuild failed: {str(e)}")

# Create global instance (lazy initialization)
faiss_similarity_engine = None

def get_faiss_engine():
    """Get or create the FAISS similarity engine instance"""
    global faiss_similarity_engine
    if faiss_similarity_engine is None:
        faiss_similarity_engine = FAISSSimilarityEngine()
    return faiss_similarity_engine

# Export for easy access
__all__ = ['FAISSSimilarityEngine', 'get_faiss_engine']
