#!/usr/bin/env python3
"""
Offline Chat Suggestion Manager - No Internet Required
Uses local text processing and pattern matching
"""

import json
import re
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from collections import Counter, defaultdict
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OfflineChatSuggestionManager:
    """
    Offline chat suggestion manager using local text processing
    No internet required - uses built-in Python libraries
    """
    
    def __init__(self, data_dir: str = "data/offline_chat_suggestions"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.suggestions_db = {}
        self.patterns_db = {}
        self.category_keywords = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
            "help": ["help", "assist", "support", "how to", "what is", "explain"],
            "data": ["data", "file", "excel", "csv", "json", "process", "analyze"],
            "mapping": ["map", "mapping", "transform", "convert", "schema"],
            "validation": ["validate", "check", "verify", "test", "error"],
            "code": ["code", "generate", "create", "build", "script", "function"],
            "general": ["general", "other", "misc"]
        }
        
        self.load_data()
    
    def load_data(self):
        """Load existing suggestion data"""
        try:
            suggestions_file = self.data_dir / "suggestions.json"
            if suggestions_file.exists():
                with open(suggestions_file, 'r') as f:
                    self.suggestions_db = json.load(f)
            
            patterns_file = self.data_dir / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    self.patterns_db = json.load(f)
            
            logger.info(f"Loaded {len(self.suggestions_db)} suggestions and {len(self.patterns_db)} patterns")
        except Exception as e:
            logger.warning(f"Could not load existing data: {e}")
    
    def save_data(self):
        """Save suggestion data"""
        try:
            suggestions_file = self.data_dir / "suggestions.json"
            with open(suggestions_file, 'w') as f:
                json.dump(self.suggestions_db, f, indent=2)
            
            patterns_file = self.data_dir / "patterns.json"
            with open(patterns_file, 'w') as f:
                json.dump(self.patterns_db, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save data: {e}")
    
    def _categorize_interaction(self, user_input: str, ai_response: str) -> str:
        """Categorize interaction based on keywords"""
        text = f"{user_input} {ai_response}".lower()
        
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return "general"
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    async def add_chat_interaction(self,
                                 user_input: str,
                                 ai_response: str,
                                 context: Dict[str, Any] = None,
                                 feedback_score: float = None,
                                 category: str = "general") -> str:
        """Add a chat interaction to the suggestion database"""
        try:
            # Auto-categorize if not specified
            if category == "general":
                category = self._categorize_interaction(user_input, ai_response)
            
            # Generate interaction ID
            interaction_id = f"offline_chat_{len(self.suggestions_db)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Extract keywords
            keywords = self._extract_keywords(f"{user_input} {ai_response}")
            
            # Store interaction
            self.suggestions_db[interaction_id] = {
                "user_input": user_input,
                "ai_response": ai_response,
                "context": context or {},
                "feedback_score": feedback_score,
                "category": category,
                "keywords": keywords,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update patterns
            self._update_patterns(user_input, ai_response, category, keywords)
            
            # Save data
            self.save_data()
            
            logger.info(f"Added offline chat interaction: {interaction_id}")
            return interaction_id
            
        except Exception as e:
            logger.error(f"Error adding chat interaction: {e}")
            return None
    
    def _update_patterns(self, user_input: str, ai_response: str, category: str, keywords: List[str]):
        """Update pattern database for better suggestions"""
        if category not in self.patterns_db:
            self.patterns_db[category] = {
                "common_phrases": Counter(),
                "response_templates": Counter(),
                "keyword_patterns": defaultdict(list)
            }
        
        # Update common phrases
        phrases = re.findall(r'\b\w+(?:\s+\w+){1,3}\b', user_input.lower())
        for phrase in phrases:
            self.patterns_db[category]["common_phrases"][phrase] += 1
        
        # Update response templates
        response_start = ai_response.split()[0:3]  # First 3 words
        if response_start:
            template = " ".join(response_start)
            self.patterns_db[category]["response_templates"][template] += 1
        
        # Update keyword patterns
        for keyword in keywords:
            self.patterns_db[category]["keyword_patterns"][keyword].append(user_input)
    
    def get_suggestions(self, 
                       current_input: str, 
                       max_suggestions: int = 3,
                       category: str = None) -> List[str]:
        """Get chat suggestions based on current input"""
        try:
            suggestions = []
            current_keywords = self._extract_keywords(current_input)
            
            # If category specified, search within that category
            search_categories = [category] if category else list(self.suggestions_db.keys())
            
            # Score interactions based on keyword overlap
            scored_interactions = []
            
            for interaction_id, interaction in self.suggestions_db.items():
                if category and interaction.get("category") != category:
                    continue
                
                # Calculate keyword overlap score
                interaction_keywords = set(interaction.get("keywords", []))
                current_keywords_set = set(current_keywords)
                
                if current_keywords_set:
                    overlap_score = len(interaction_keywords.intersection(current_keywords_set)) / len(current_keywords_set)
                else:
                    overlap_score = 0
                
                # Add phrase matching score
                phrase_score = 0
                if category and category in self.patterns_db:
                    for phrase in self.patterns_db[category]["common_phrases"]:
                        if phrase in current_input.lower():
                            phrase_score += self.patterns_db[category]["common_phrases"][phrase]
                
                total_score = overlap_score + (phrase_score * 0.1)
                
                if total_score > 0:
                    scored_interactions.append((total_score, interaction))
            
            # Sort by score and get top suggestions
            scored_interactions.sort(key=lambda x: x[0], reverse=True)
            
            for score, interaction in scored_interactions[:max_suggestions * 2]:
                if score > 0.1:  # Minimum relevance threshold
                    suggestions.append(interaction["ai_response"])
            
            # If not enough suggestions, add some general ones
            if len(suggestions) < max_suggestions:
                general_suggestions = [
                    "How can I help you with data processing?",
                    "Would you like me to analyze your data?",
                    "I can help you with mapping and transformation tasks.",
                    "Let me know what specific task you need assistance with."
                ]
                suggestions.extend(general_suggestions[:max_suggestions - len(suggestions)])
            
            return suggestions[:max_suggestions]
            
        except Exception as e:
            logger.error(f"Error getting suggestions: {e}")
            return ["I'm here to help! What would you like to do?"]
    
    def get_category_suggestions(self, category: str, max_suggestions: int = 5) -> List[str]:
        """Get suggestions for a specific category"""
        try:
            category_interactions = [
                interaction for interaction in self.suggestions_db.values()
                if interaction.get("category") == category
            ]
            
            if not category_interactions:
                return self._get_default_category_suggestions(category)
            
            # Return most recent responses
            suggestions = [interaction["ai_response"] for interaction in category_interactions[-max_suggestions:]]
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting category suggestions: {e}")
            return self._get_default_category_suggestions(category)
    
    def _get_default_category_suggestions(self, category: str) -> List[str]:
        """Get default suggestions for a category"""
        default_suggestions = {
            "greeting": [
                "Hello! How can I assist you today?",
                "Hi there! What would you like to work on?",
                "Good to see you! How can I help?"
            ],
            "help": [
                "I can help you with data processing, mapping, and analysis tasks.",
                "What specific task would you like assistance with?",
                "I'm here to help with your data-related questions."
            ],
            "data": [
                "I can help you process and analyze your data files.",
                "What type of data are you working with?",
                "I can assist with Excel, CSV, and JSON data processing."
            ],
            "mapping": [
                "I can help you create mapping rules between different data schemas.",
                "What source and target schemas are you working with?",
                "I can assist with data transformation and mapping tasks."
            ],
            "validation": [
                "I can help you validate your data and check for errors.",
                "What validation rules do you need to apply?",
                "I can assist with data quality checks and validation."
            ],
            "code": [
                "I can help you generate code for data processing tasks.",
                "What programming language would you like to use?",
                "I can assist with creating scripts and functions."
            ]
        }
        
        return default_suggestions.get(category, ["How can I help you today?"])
    
    def get_stats(self) -> Dict[str, Any]:
        """Get suggestion manager statistics"""
        category_counts = Counter(interaction.get("category", "unknown") for interaction in self.suggestions_db.values())
        
        return {
            "total_interactions": len(self.suggestions_db),
            "categories": dict(category_counts),
            "patterns_learned": len(self.patterns_db),
            "data_directory": str(self.data_dir)
        }
