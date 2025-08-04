"""
FAISS Vector Database Integration using OpenAI Embeddings
Optimized for production use with GPT-4
"""
import faiss
import numpy as np
import openai
from typing import List, Dict, Tuple, Optional
import pickle
import json
from pathlib import Path

class FAISSIntegration:
    """Production-ready FAISS integration using OpenAI embeddings"""
    
    def __init__(self, openai_api_key: str, dimension: int = 1536):  # OpenAI embeddings are 1536D
        openai.api_key = openai_api_key
        self.dimension = dimension
        self.index: Optional[faiss.IndexFlatL2] = None
        self.metadata: List[Dict] = []
        self.embeddings_cache: Dict[str, np.ndarray] = {}
        
    def create_index(self) -> None:
        """Create optimized FAISS index"""
        # Using IVF index for better performance with large datasets
        quantizer = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIVFFlat(quantizer, self.dimension, min(100, len(self.metadata)))
        
    def get_embedding(self, text: str, cache: bool = True) -> np.ndarray:
        """Get OpenAI embedding with caching"""
        if cache and text in self.embeddings_cache:
            return self.embeddings_cache[text]
        
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text
            )
            embedding = np.array(response['data'][0]['embedding'], dtype='float32')
            
            if cache:
                self.embeddings_cache[text] = embedding
            
            return embedding
            
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return np.zeros(self.dimension, dtype='float32')
    
    def build_searchable_text(self, mapping: Dict) -> str:
        """Create optimized searchable text from mapping data"""
        # Build comprehensive text representation
        components = []
        
        # Core fields
        if mapping.get('staging_table'):
            components.append(f"Table: {mapping['staging_table']}")
        if mapping.get('column_name'):
            components.append(f"Column: {mapping['column_name']}")
        if mapping.get('mapping_type'):
            components.append(f"Type: {mapping['mapping_type']}")
        if mapping.get('data_type'):
            components.append(f"DataType: {mapping['data_type']}")
        
        # Transformation logic - make it searchable
        if mapping.get('transformation_logic'):
            logic = mapping['transformation_logic']
            components.append(f"Logic: {logic}")
            
            # Extract key patterns for better search
            if 'upper' in logic.lower():
                components.append("Transform: UPPERCASE")
            if 'lower' in logic.lower():
                components.append("Transform: LOWERCASE")
            if 'concat' in logic.lower():
                components.append("Transform: CONCATENATION")
            if 'case when' in logic.lower():
                components.append("Transform: CONDITIONAL")
            if 'substring' in logic.lower():
                components.append("Transform: SUBSTRING")
        
        # Additional metadata
        if mapping.get('is_nullable') is False:
            components.append("Constraint: NOT_NULL")
        
        return " | ".join(components)
    
    def add_mappings(self, mappings: List[Dict]) -> None:
        """Add mappings to vector database with intelligent indexing"""
        if not mappings:
            return
        
        # Create searchable texts
        texts = [self.build_searchable_text(m) for m in mappings]
        
        # Get embeddings in batch (more efficient)
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        
        embeddings_array = np.array(embeddings, dtype='float32')
        
        # Initialize or train index
        if self.index is None:
            self.create_index()
            self.index.train(embeddings_array)
        
        # Add to index
        self.index.add(embeddings_array)
        
        # Store metadata
        self.metadata.extend(mappings)
    
    def search(self, query: str, top_k: int = 5, threshold: float = None) -> List[Tuple[Dict, float]]:
        """Intelligent similarity search with relevance filtering"""
        if self.index is None or len(self.metadata) == 0:
            return []
        
        # Enhance query for better results
        enhanced_query = self._enhance_query(query)
        
        # Get query embedding
        query_embedding = self.get_embedding(enhanced_query)
        query_array = query_embedding.reshape(1, -1)
        
        # Search
        k = min(top_k * 2, len(self.metadata))  # Get more results for filtering
        distances, indices = self.index.search(query_array, k)
        
        # Filter and rank results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                relevance_score = self._calculate_relevance(query, self.metadata[idx], dist)
                
                if threshold is None or relevance_score >= threshold:
                    results.append((self.metadata[idx], relevance_score))
        
        # Sort by relevance and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def _enhance_query(self, query: str) -> str:
        """Enhance query for better search results"""
        # Add context to improve search
        enhancements = []
        
        query_lower = query.lower()
        
        # Detect intent and add context
        if any(word in query_lower for word in ['derive', 'transform', 'calculate']):
            enhancements.append("transformation logic derivation")
        
        if any(word in query_lower for word in ['lookup', 'reference', 'goldref']):
            enhancements.append("gold reference lookup join")
        
        if any(word in query_lower for word in ['null', 'blank', 'empty']):
            enhancements.append("null handling validation")
        
        if any(word in query_lower for word in ['direct', 'map', 'copy']):
            enhancements.append("direct mapping column")
        
        enhanced = f"{query} {' '.join(enhancements)}".strip()
        return enhanced
    
    def _calculate_relevance(self, query: str, mapping: Dict, distance: float) -> float:
        """Calculate relevance score with intelligent ranking"""
        # Convert distance to similarity (0-1 scale)
        base_similarity = 1 / (1 + distance)
        
        # Boost score based on exact matches
        boost = 1.0
        query_terms = query.lower().split()
        
        # Check for exact matches in key fields
        for term in query_terms:
            if term in str(mapping.get('column_name', '')).lower():
                boost *= 1.5
            if term in str(mapping.get('staging_table', '')).lower():
                boost *= 1.3
            if term in str(mapping.get('mapping_type', '')).lower():
                boost *= 1.2
        
        # Apply boost with cap
        relevance = min(base_similarity * boost, 1.0)
        
        return relevance
    
    def find_similar_patterns(self, mapping: Dict, top_k: int = 3) -> List[Dict]:
        """Find similar mapping patterns for reuse"""
        # Create query from mapping characteristics
        query_parts = []
        
        if mapping.get('mapping_type'):
            query_parts.append(f"mapping type {mapping['mapping_type']}")
        
        if mapping.get('transformation_logic'):
            # Extract transformation pattern
            logic = mapping['transformation_logic'].lower()
            if 'case when' in logic:
                query_parts.append("conditional transformation case when")
            elif 'concat' in logic:
                query_parts.append("concatenation transformation")
            elif 'substring' in logic:
                query_parts.append("substring extraction")
        
        if mapping.get('data_type'):
            query_parts.append(f"data type {mapping['data_type']}")
        
        query = " ".join(query_parts)
        
        # Search for similar patterns
        results = self.search(query, top_k=top_k)
        
        # Filter out the same mapping
        similar = []
        for result, score in results:
            if (result.get('column_name') != mapping.get('column_name') or 
                result.get('staging_table') != mapping.get('staging_table')):
                similar.append(result)
        
        return similar[:top_k]
    
    def save(self, path: str) -> None:
        """Save index and metadata to disk"""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        if self.index is not None:
            faiss.write_index(self.index, str(path))
        
        # Save metadata and cache
        meta_path = path.with_suffix('.meta.pkl')
        with open(meta_path, 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'embeddings_cache': self.embeddings_cache,
                'dimension': self.dimension
            }, f)
    
    def load(self, path: str) -> None:
        """Load index and metadata from disk"""
        path = Path(path)
        
        # Load FAISS index
        if path.exists():
            self.index = faiss.read_index(str(path))
        
        # Load metadata and cache
        meta_path = path.with_suffix('.meta.pkl')
        if meta_path.exists():
            with open(meta_path, 'rb') as f:
                data = pickle.load(f)
                self.metadata = data.get('metadata', [])
                self.embeddings_cache = data.get('embeddings_cache', {})
                self.dimension = data.get('dimension', 1536)
    
    def get_statistics(self) -> Dict:
        """Get index statistics for monitoring"""
        stats = {
            'total_mappings': len(self.metadata),
            'index_trained': self.index is not None,
            'cache_size': len(self.embeddings_cache),
            'mapping_types': {},
            'tables': []
        }
        
        # Count mapping types
        for mapping in self.metadata:
            mtype = mapping.get('mapping_type', 'unknown')
            stats['mapping_types'][mtype] = stats['mapping_types'].get(mtype, 0) + 1
        
        # Get unique tables
        tables = set(m.get('staging_table', '') for m in self.metadata)
        stats['tables'] = list(tables)
        
        return stats 