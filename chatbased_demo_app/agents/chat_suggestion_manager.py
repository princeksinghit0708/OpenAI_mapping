#!/usr/bin/env python3
"""
Chat Suggestion Manager for Intelligent Chat Interface
Integrates with FAISS similarity engine for context-aware suggestions
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

from .faiss_similarity_engine import get_faiss_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatSuggestionManager:
    """
    Manages chat suggestions and integrates with FAISS similarity engine
    """
    
    def __init__(self):
        self.suggestion_history = []
        self.user_preferences = {}
        self.context_cache = {}
        
        # Initialize FAISS engine (lazy)
        self.faiss_engine = None
        
        # Suggestion categories
        self.categories = {
            'file_operations': 'File upload, analysis, and processing',
            'ai_agents': 'AI agent operations and testing',
            'workflow': 'Complete workflow execution',
            'validation': 'Metadata validation and analysis',
            'code_generation': 'PySpark code generation',
            'help': 'Help and documentation',
            'general': 'General chat and questions'
        }
    
    def _get_faiss_engine(self):
        """Get the FAISS engine instance"""
        if self.faiss_engine is None:
            self.faiss_engine = get_faiss_engine()
        return self.faiss_engine
    
    async def add_chat_interaction(self, 
                                  user_input: str, 
                                  ai_response: str, 
                                  context: Dict[str, Any] = None,
                                  feedback_score: float = None,
                                  category: str = "general") -> str:
        """
        Add a chat interaction to the suggestion database
        
        Args:
            user_input: User's input
            ai_response: AI's response
            context: Additional context
            feedback_score: User feedback (0.0 to 1.0)
            
        Returns:
            Suggestion ID
        """
        try:
            # Use provided category or determine based on content
            if category == "general":
                category = self._categorize_interaction(user_input, ai_response)
            
            # Add to FAISS database
            suggestion_id = await self._get_faiss_engine().add_chat_suggestion(
                user_input=user_input,
                ai_response=ai_response,
                context=context or {},
                feedback_score=feedback_score,
                category=category
            )
            
            # Add to local history
            self.suggestion_history.append({
                'suggestion_id': suggestion_id,
                'user_input': user_input,
                'ai_response': ai_response,
                'category': category,
                'feedback_score': feedback_score,
                'timestamp': datetime.now().isoformat(),
                'context': context or {}
            })
            
            logger.info(f"Added chat interaction: {suggestion_id} in category: {category}")
            return suggestion_id
            
        except Exception as e:
            logger.error(f"Failed to add chat interaction: {str(e)}")
            raise
    
    def _categorize_interaction(self, user_input: str, ai_response: str) -> str:
        """Automatically categorize chat interaction"""
        input_lower = user_input.lower()
        response_lower = ai_response.lower()
        
        # File operations
        if any(word in input_lower for word in ['upload', 'file', 'excel', 'analyze']):
            return 'file_operations'
        
        # AI agents
        if any(word in input_lower for word in ['agent', 'test', 'validate', 'generate']):
            return 'ai_agents'
        
        # Workflow
        if any(word in input_lower for word in ['workflow', 'pipeline', 'complete']):
            return 'workflow'
        
        # Validation
        if any(word in input_lower for word in ['validation', 'metadata', 'quality']):
            return 'validation'
        
        # Code generation
        if any(word in input_lower for word in ['code', 'pyspark', 'transformation']):
            return 'code_generation'
        
        # Help
        if any(word in input_lower for word in ['help', 'command', 'how']):
            return 'help'
        
        return 'general'
    
    async def get_smart_suggestions(self, 
                                   current_input: str, 
                                   user_context: Dict[str, Any] = None,
                                   top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Get intelligent suggestions based on current input and context
        
        Args:
            current_input: Current user input
            user_context: User context (file info, previous commands, etc.)
            top_k: Number of suggestions to return
            
        Returns:
            List of relevant suggestions
        """
        try:
            # Find similar suggestions using FAISS
            similar_suggestions = await self._get_faiss_engine().find_similar_suggestions(
                query=current_input,
                top_k=top_k * 2,  # Get more for filtering
                min_similarity=0.3
            )
            
            # Apply context-aware filtering
            filtered_suggestions = self._filter_by_context(similar_suggestions, user_context)
            
            # Rank by relevance and feedback
            ranked_suggestions = self._rank_suggestions(filtered_suggestions, current_input)
            
            # Return top suggestions
            return ranked_suggestions[:top_k]
            
        except Exception as e:
            logger.error(f"Failed to get smart suggestions: {str(e)}")
            return []
    
    def _filter_by_context(self, suggestions: List[Dict[str, Any]], user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter suggestions based on user context"""
        if not user_context:
            return suggestions
        
        filtered = []
        for suggestion in suggestions:
            context = suggestion.get('context', {})
            
            # Check if suggestion context matches user context
            if self._context_matches(context, user_context):
                filtered.append(suggestion)
        
        return filtered if filtered else suggestions
    
    def _context_matches(self, suggestion_context: Dict[str, Any], user_context: Dict[str, Any]) -> bool:
        """Check if suggestion context matches user context"""
        try:
            # Check file-related context
            if 'file_path' in user_context and 'file_path' in suggestion_context:
                if user_context['file_path'] == suggestion_context['file_path']:
                    return True
            
            # Check agent-related context
            if 'agent_used' in user_context and 'agent_used' in suggestion_context:
                if user_context['agent_used'] == suggestion_context['agent_used']:
                    return True
            
            # Check category context
            if 'category' in user_context and 'category' in suggestion_context:
                if user_context['category'] == suggestion_context['category']:
                    return True
            
            return False
            
        except Exception:
            return False
    
    def _rank_suggestions(self, suggestions: List[Dict[str, Any]], current_input: str) -> List[Dict[str, Any]]:
        """Rank suggestions by relevance and quality"""
        try:
            for suggestion in suggestions:
                score = 0.0
                
                # Base similarity score
                similarity_score = suggestion.get('similarity_score', 0.0)
                score += similarity_score * 0.4
                
                # Feedback score
                feedback_score = suggestion.get('feedback_score', 0.5)
                score += feedback_score * 0.3
                
                # Recency bonus
                timestamp = suggestion.get('timestamp', '')
                if timestamp:
                    try:
                        suggestion_time = datetime.fromisoformat(timestamp)
                        time_diff = (datetime.now() - suggestion_time).total_seconds()
                        recency_bonus = max(0, 1.0 - (time_diff / (24 * 60 * 60)))  # 24 hour decay
                        score += recency_bonus * 0.2
                    except:
                        pass
                
                # Input relevance bonus
                input_lower = current_input.lower()
                suggestion_input = suggestion.get('user_input', '').lower()
                if any(word in suggestion_input for word in input_lower.split()):
                    score += 0.1
                
                suggestion['relevance_score'] = score
            
            # Sort by relevance score
            suggestions.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            return suggestions
            
        except Exception as e:
            logger.error(f"Failed to rank suggestions: {str(e)}")
            return suggestions
    
    async def get_contextual_help(self, current_input: str, user_context: Dict[str, Any] = None) -> str:
        """Get contextual help based on current input"""
        try:
            # Get relevant suggestions
            suggestions = await self.get_smart_suggestions(current_input, user_context, top_k=2)
            
            if not suggestions:
                return "I'm here to help! Try asking me about file operations, AI agents, or workflows."
            
            # Build contextual help
            help_text = "Based on similar interactions, here are some helpful suggestions:\n\n"
            
            for i, suggestion in enumerate(suggestions, 1):
                help_text += f"{i}. **{suggestion.get('category', 'General').title()}**: "
                help_text += f"{suggestion.get('ai_response', '')[:100]}...\n\n"
            
            help_text += "You can also try these commands:\n"
            help_text += "• `help` - Show all available commands\n"
            help_text += "• `suggestions` - View your suggestion history\n"
            help_text += "• `export` - Export training data\n"
            
            return help_text
            
        except Exception as e:
            logger.error(f"Failed to get contextual help: {str(e)}")
            return "I'm here to help! Try asking me about file operations, AI agents, or workflows."
    
    async def get_user_suggestions_history(self, user_id: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's suggestion history"""
        try:
            # For now, return all suggestions (in production, filter by user_id)
            suggestions = list(self.suggestion_history)
            suggestions.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get suggestion history: {str(e)}")
            return []
    
    async def update_feedback(self, suggestion_id: str, feedback_score: float) -> bool:
        """Update feedback for a suggestion"""
        try:
            # Update in FAISS engine
            success = await self._get_faiss_engine().update_feedback(suggestion_id, feedback_score)
            
            if success:
                # Update local history
                for suggestion in self.suggestion_history:
                    if suggestion.get('suggestion_id') == suggestion_id:
                        suggestion['feedback_score'] = feedback_score
                        break
                
                logger.info(f"Updated feedback for {suggestion_id}: {feedback_score}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update feedback: {str(e)}")
            return False
    
    async def export_training_data(self, 
                                  output_path: str = None, 
                                  format: str = "json",
                                  include_embeddings: bool = True) -> str:
        """Export training data for model training"""
        try:
            return await self._get_faiss_engine().export_training_data(
                output_path=output_path,
                format=format,
                include_embeddings=include_embeddings
            )
            
        except Exception as e:
            logger.error(f"Failed to export training data: {str(e)}")
            raise
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get suggestion manager statistics"""
        try:
            # Get FAISS engine stats
            faiss_stats = await self._get_faiss_engine().get_statistics()
            
            # Add local stats
            stats = {
                'suggestion_manager': {
                    'total_suggestions': len(self.suggestion_history),
                    'categories': self.categories,
                    'last_updated': datetime.now().isoformat()
                },
                'faiss_engine': faiss_stats
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    async def cleanup_old_suggestions(self, days_old: int = 30) -> int:
        """Clean up old suggestions"""
        try:
            # Clean up FAISS engine
            removed_count = await self._get_faiss_engine().cleanup_old_suggestions(days_old)
            
            # Clean up local history
            cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
            local_removed = 0
            
            self.suggestion_history = [
                suggestion for suggestion in self.suggestion_history
                if datetime.fromisoformat(suggestion.get('timestamp', '')).timestamp() >= cutoff_date
            ]
            
            local_removed = len(self.suggestion_history) - len(self.suggestion_history)
            
            logger.info(f"Cleaned up {removed_count} FAISS suggestions and {local_removed} local suggestions")
            return removed_count + local_removed
            
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return 0
    
    async def get_suggestions_by_category(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get suggestions filtered by category"""
        try:
            return await self._get_faiss_engine().get_suggestions_by_category(category, limit)
            
        except Exception as e:
            logger.error(f"Failed to get suggestions by category: {str(e)}")
            return []
    
    async def search_complex_suggestions(self, 
                                       query: str, 
                                       filters: Dict[str, Any] = None,
                                       top_k: int = 10) -> List[Dict[str, Any]]:
        """Complex suggestion search with advanced filtering"""
        try:
            return await self._get_faiss_engine().search_complex_similarity(
                query=query,
                filters=filters,
                top_k=top_k
            )
            
        except Exception as e:
            logger.error(f"Complex suggestion search failed: {str(e)}")
            return []

# Create global instance
chat_suggestion_manager = ChatSuggestionManager()

# Export for easy access
__all__ = ['ChatSuggestionManager', 'chat_suggestion_manager']
