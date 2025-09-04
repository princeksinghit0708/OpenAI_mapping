#!/usr/bin/env python3
"""
Offline FAISS Similarity Search Engine - No Internet Required
Uses built-in Python libraries and local text processing
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
import re
from collections import Counter
import math

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OfflineTextEmbedder:
    """
    Offline text embedding using TF-IDF and word frequency
    No internet required - uses built-in Python libraries
    """
    
    def __init__(self):
        self.vocabulary = {}
        self.idf_scores = {}
        self.doc_frequencies = {}
        self.total_docs = 0
        
    def build_vocabulary(self, texts: List[str]):
        """Build vocabulary from texts"""
        all_words = []
        for text in texts:
            words = self._tokenize(text)
            all_words.extend(words)
        
        # Count word frequencies
        word_counts = Counter(all_words)
        
        # Build vocabulary (keep words that appear at least 2 times)
        self.vocabulary = {word: idx for idx, word in enumerate(word_counts.keys()) if word_counts[word] >= 2}
        
        # Calculate document frequencies
        for text in texts:
            words = set(self._tokenize(text))
            for word in words:
                if word in self.vocabulary:
                    self.doc_frequencies[word] = self.doc_frequencies.get(word, 0) + 1
        
        self.total_docs = len(texts)
        
        # Calculate IDF scores
        for word in self.vocabulary:
            if word in self.doc_frequencies:
                self.idf_scores[word] = math.log(self.total_docs / self.doc_frequencies[word])
            else:
                self.idf_scores[word] = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        # Convert to lowercase and split on non-alphanumeric characters
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def encode(self, text: str) -> np.ndarray:
        """Encode text to vector using TF-IDF"""
        words = self._tokenize(text)
        word_counts = Counter(words)
        
        # Create TF-IDF vector
        vector = np.zeros(len(self.vocabulary))
        
        for word, count in word_counts.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                tf = count / len(words)  # Term frequency
                idf = self.idf_scores.get(word, 0)  # Inverse document frequency
                vector[idx] = tf * idf
        
        # Normalize vector
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector

class OfflineFAISSSimilarityEngine:
    """
    Offline FAISS similarity search engine - No internet required
    Uses local text processing and TF-IDF embeddings
    """
    
    def __init__(self, 
                 dimension: int = 1000,  # Adjust based on vocabulary size
                 collection_name: str = "offline_chat_similarity_db"):
        self.dimension = dimension
        self.collection_name = collection_name
        self.embedder = OfflineTextEmbedder()
        self.index = None
        self.metadata_store = {}
        self.metadata_path = Path(f"data/{collection_name}_metadata.json")
        self.index_path = Path(f"data/{collection_name}_index.faiss")
        
        # Create data directory
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize FAISS index
        self._initialize_index()
        
        # Load existing data
        self._load_data()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product for cosine similarity
    
    def _load_data(self):
        """Load existing metadata and index"""
        try:
            if self.metadata_path.exists():
                with open(self.metadata_path, 'r') as f:
                    self.metadata_store = json.load(f)
                logger.info(f"Loaded {len(self.metadata_store)} existing records")
            
            if self.index_path.exists():
                self.index = faiss.read_index(str(self.index_path))
                logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    
    def _save_data(self):
        """Save metadata and index"""
        try:
            with open(self.metadata_path, 'w') as f:
                json.dump(self.metadata_store, f, indent=2)
            
            if self.index is not None:
                faiss.write_index(self.index, str(self.index_path))
        except Exception as e:
            logger.error(f"Could not save data: {e}")
    
    def add_chat_interaction(self, 
                           user_input: str, 
                           ai_response: str, 
                           context: Dict[str, Any] = None,
                           feedback_score: float = None,
                           category: str = "general") -> str:
        """Add a chat interaction to the similarity database"""
        try:
            # Create interaction text
            interaction_text = f"{user_input} {ai_response}"
            
            # Generate embedding
            embedding = self.embedder.encode(interaction_text)
            
            # Resize embedding to match dimension
            if len(embedding) < self.dimension:
                embedding = np.pad(embedding, (0, self.dimension - len(embedding)))
            elif len(embedding) > self.dimension:
                embedding = embedding[:self.dimension]
            
            # Add to FAISS index
            self.index.add(embedding.reshape(1, -1))
            
            # Store metadata
            interaction_id = f"chat_{len(self.metadata_store)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.metadata_store[interaction_id] = {
                "user_input": user_input,
                "ai_response": ai_response,
                "context": context or {},
                "feedback_score": feedback_score,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "interaction_text": interaction_text
            }
            
            # Save data
            self._save_data()
            
            logger.info(f"Added chat interaction: {interaction_id}")
            return interaction_id
            
        except Exception as e:
            logger.error(f"Error adding chat interaction: {e}")
            return None
    
    def find_similar_interactions(self, 
                                query: str, 
                                top_k: int = 5,
                                category: str = None) -> List[Dict[str, Any]]:
        """Find similar chat interactions"""
        try:
            if self.index.ntotal == 0:
                return []
            
            # Generate query embedding
            query_embedding = self.embedder.encode(query)
            
            # Resize embedding to match dimension
            if len(query_embedding) < self.dimension:
                query_embedding = np.pad(query_embedding, (0, self.dimension - len(query_embedding)))
            elif len(query_embedding) > self.dimension:
                query_embedding = query_embedding[:self.dimension]
            
            # Search FAISS index
            scores, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
            
            # Get metadata for results
            results = []
            interaction_ids = list(self.metadata_store.keys())
            
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(interaction_ids):
                    interaction_id = interaction_ids[idx]
                    metadata = self.metadata_store[interaction_id]
                    
                    # Filter by category if specified
                    if category and metadata.get("category") != category:
                        continue
                    
                    results.append({
                        "interaction_id": interaction_id,
                        "similarity_score": float(score),
                        "user_input": metadata["user_input"],
                        "ai_response": metadata["ai_response"],
                        "category": metadata.get("category", "general"),
                        "timestamp": metadata.get("timestamp"),
                        "context": metadata.get("context", {})
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar interactions: {e}")
            return []
    
    def get_chat_suggestions(self, 
                           current_input: str, 
                           max_suggestions: int = 3) -> List[str]:
        """Get chat suggestions based on similar interactions"""
        try:
            similar_interactions = self.find_similar_interactions(
                current_input, 
                top_k=max_suggestions * 2  # Get more to filter
            )
            
            suggestions = []
            for interaction in similar_interactions:
                if interaction["similarity_score"] > 0.3:  # Threshold for relevance
                    suggestions.append(interaction["ai_response"])
            
            return suggestions[:max_suggestions]
            
        except Exception as e:
            logger.error(f"Error getting chat suggestions: {e}")
            return []
    
    def train_on_existing_data(self, training_data: List[Dict[str, str]]):
        """Train the embedder on existing data"""
        try:
            texts = []
            for item in training_data:
                if "user_input" in item and "ai_response" in item:
                    texts.append(f"{item['user_input']} {item['ai_response']}")
            
            if texts:
                self.embedder.build_vocabulary(texts)
                logger.info(f"Trained embedder on {len(texts)} examples")
            
        except Exception as e:
            logger.error(f"Error training on existing data: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return {
            "total_interactions": len(self.metadata_store),
            "index_size": self.index.ntotal if self.index else 0,
            "vocabulary_size": len(self.embedder.vocabulary),
            "dimension": self.dimension
        }
