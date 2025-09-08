#!/usr/bin/env python3
"""
Offline FAISS Similarity Search Engine
Handles cases where sentence-transformers models are not available
"""

import numpy as np
import json
import pickle
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import faiss
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OfflineFAISSEngine:
    """
    Offline FAISS similarity search engine that works without sentence-transformers
    Uses simple TF-IDF or basic text similarity when models are not available
    """
    
    def __init__(self, 
                 dimension: int = 384,
                 collection_name: str = "offline_chat_db"):
        
        self.dimension = dimension
        self.collection_name = collection_name
        
        # Initialize components
        self.faiss_index = None
        self.is_initialized = False
        self.embedding_model = None  # Will be None for offline mode
        
        # Storage paths
        self.base_path = Path(f"./data/faiss_db/{collection_name}")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.index_path = self.base_path / f"{collection_name}_index.faiss"
        self.metadata_path = self.base_path / f"{collection_name}_metadata.json"
        self.suggestions_path = self.base_path / f"{collection_name}_suggestions.json"
        
        # In-memory storage
        self.metadata = []
        self.suggestions = []
        
        # Simple text processing for offline mode
        self.vocabulary = set()
        self.word_to_id = {}
        self.id_to_word = {}
        self.next_word_id = 0
    
    async def initialize(self):
        """Initialize the offline FAISS engine"""
        try:
            logger.info("Initializing offline FAISS engine (no sentence-transformers required)")
            
            # Load existing index and metadata if available
            if self.index_path.exists():
                await self._load_existing_index()
            else:
                await self._create_new_index()
            
            # Load existing data
            await self._load_existing_data()
            
            logger.info(f"Offline FAISS Engine initialized: {self.collection_name}")
            self.is_initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize offline FAISS engine: {str(e)}")
            self.is_initialized = False
    
    async def _create_new_index(self):
        """Create a new FAISS index"""
        try:
            # Create a simple FAISS index
            self.faiss_index = faiss.IndexFlatL2(self.dimension)
            logger.info(f"Created new FAISS index with dimension {self.dimension}")
            
        except Exception as e:
            logger.error(f"Failed to create FAISS index: {str(e)}")
            raise
    
    async def _load_existing_index(self):
        """Load existing FAISS index"""
        try:
            self.faiss_index = faiss.read_index(str(self.index_path))
            logger.info(f"Loaded existing FAISS index from {self.index_path}")
            
        except Exception as e:
            logger.error(f"Failed to load existing index: {str(e)}")
            await self._create_new_index()
    
    async def _load_existing_data(self):
        """Load existing metadata and suggestions"""
        try:
            # Load metadata
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
                logger.info(f"Loaded {len(self.metadata)} metadata records")
            
            # Load suggestions
            if self.suggestions_path.exists():
                with open(self.suggestions_path, 'r', encoding='utf-8') as f:
                    self.suggestions = json.load(f)
                logger.info(f"Loaded {len(self.suggestions)} suggestions")
                
        except Exception as e:
            logger.error(f"Failed to load existing data: {str(e)}")
            self.metadata = []
            self.suggestions = []
    
    def _simple_text_embedding(self, text: str) -> np.ndarray:
        """Create a simple text embedding using basic text features"""
        if not text:
            return np.zeros(self.dimension)
        
        # Convert to lowercase and split into words
        words = text.lower().split()
        
        # Create a simple bag-of-words representation
        word_counts = {}
        for word in words:
            # Simple word cleaning
            word = word.strip('.,!?;:"()[]{}')
            if word:
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # Create embedding vector
        embedding = np.zeros(self.dimension)
        
        # Use word hashing to map words to embedding dimensions
        for word, count in word_counts.items():
            # Simple hash-based mapping
            hash_val = hash(word) % self.dimension
            embedding[hash_val] += count
        
        # Normalize the embedding
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    async def add_text(self, text: str, metadata: Dict[str, Any] = None) -> bool:
        """Add text to the FAISS index"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not text:
                return False
            
            # Create embedding
            embedding = self._simple_text_embedding(text)
            embedding = embedding.reshape(1, -1).astype('float32')
            
            # Add to FAISS index
            self.faiss_index.add(embedding)
            
            # Store metadata
            record_metadata = {
                'id': len(self.metadata),
                'text': text,
                'timestamp': datetime.now().isoformat(),
                **(metadata or {})
            }
            self.metadata.append(record_metadata)
            
            # Save data
            await self._save_data()
            
            logger.info(f"Added text to index: {text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add text: {str(e)}")
            return False
    
    async def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts"""
        try:
            if not self.is_initialized:
                await self.initialize()
            
            if not query or self.faiss_index.ntotal == 0:
                return []
            
            # Create query embedding
            query_embedding = self._simple_text_embedding(query)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            # Search
            distances, indices = self.faiss_index.search(query_embedding, min(k, self.faiss_index.ntotal))
            
            # Format results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.metadata):
                    result = {
                        'id': self.metadata[idx]['id'],
                        'text': self.metadata[idx]['text'],
                        'distance': float(distance),
                        'similarity': 1.0 / (1.0 + distance),  # Convert distance to similarity
                        'metadata': self.metadata[idx]
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search similar texts: {str(e)}")
            return []
    
    async def add_suggestion(self, suggestion: str, context: str = "") -> bool:
        """Add a chat suggestion"""
        try:
            suggestion_data = {
                'id': len(self.suggestions),
                'suggestion': suggestion,
                'context': context,
                'timestamp': datetime.now().isoformat(),
                'usage_count': 0
            }
            
            self.suggestions.append(suggestion_data)
            await self._save_data()
            
            logger.info(f"Added suggestion: {suggestion}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add suggestion: {str(e)}")
            return False
    
    async def get_suggestions(self, query: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        """Get chat suggestions"""
        try:
            if not query:
                # Return most recent suggestions
                return sorted(self.suggestions, 
                            key=lambda x: x['timestamp'], 
                            reverse=True)[:limit]
            
            # Search for similar suggestions
            similar_texts = await self.search_similar(query, limit)
            return [result['metadata'] for result in similar_texts if 'suggestion' in result['metadata']]
            
        except Exception as e:
            logger.error(f"Failed to get suggestions: {str(e)}")
            return []
    
    async def _save_data(self):
        """Save data to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.faiss_index, str(self.index_path))
            
            # Save metadata
            with open(self.metadata_path, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            
            # Save suggestions
            with open(self.suggestions_path, 'w', encoding='utf-8') as f:
                json.dump(self.suggestions, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Failed to save data: {str(e)}")

# Global instance
offline_faiss_engine = None

def get_offline_faiss_engine():
    """Get the global offline FAISS engine instance"""
    global offline_faiss_engine
    if offline_faiss_engine is None:
        offline_faiss_engine = OfflineFAISSEngine()
    return offline_faiss_engine

# Async initialization function
async def initialize_offline_engine():
    """Initialize the offline FAISS engine"""
    engine = get_offline_faiss_engine()
    await engine.initialize()
    return engine