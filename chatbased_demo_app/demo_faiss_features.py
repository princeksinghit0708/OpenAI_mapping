#!/usr/bin/env python3
"""
FAISS Similarity Engine Demo
Demonstrates advanced similarity search, chat suggestions, and training data export
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime, timedelta
import logging

# Import the FAISS similarity engine and chat suggestion manager
from agents.faiss_similarity_engine import faiss_similarity_engine
from agents.chat_suggestion_manager import chat_suggestion_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FAISSFeaturesDemo:
    """
    Comprehensive demo of FAISS similarity features
    """
    
    def __init__(self):
        self.demo_data = []
        self.setup_demo_data()
    
    def setup_demo_data(self):
        """Setup sample demo data for testing"""
        self.demo_data = [
            {
                'user_input': 'How do I upload an Excel file?',
                'ai_response': 'Use the upload command: upload /path/to/your/file.xlsx',
                'category': 'file_operations',
                'feedback_score': 0.9
            },
            {
                'user_input': 'What agents are available?',
                'ai_response': 'Available agents: Enhanced Orchestrator, Metadata Validator, Code Generator, Test Generator',
                'category': 'ai_agents',
                'feedback_score': 0.8
            },
            {
                'user_input': 'How to run metadata validation?',
                'ai_response': 'Use the validate command after uploading a file. This will run AI-powered metadata analysis.',
                'category': 'validation',
                'feedback_score': 0.95
            },
            {
                'user_input': 'Generate PySpark code for my data',
                'ai_response': 'Use the generate command to create PySpark transformation code with AI agents.',
                'category': 'code_generation',
                'feedback_score': 0.85
            },
            {
                'user_input': 'Run complete workflow',
                'ai_response': 'Use the workflow command to execute the complete end-to-end AI agentic pipeline.',
                'category': 'workflow',
                'feedback_score': 0.9
            },
            {
                'user_input': 'Help with Excel analysis',
                'ai_response': 'Upload your Excel file first, then use analyze to examine the data structure and content.',
                'category': 'file_operations',
                'feedback_score': 0.88
            },
            {
                'user_input': 'Test AI agents functionality',
                'ai_response': 'Use the test command to verify all AI agents are working properly.',
                'category': 'ai_agents',
                'feedback_score': 0.92
            },
            {
                'user_input': 'Export training data',
                'ai_response': 'Use the export command to export chat interactions for model training.',
                'category': 'help',
                'feedback_score': 0.87
            }
        ]
    
    async def demo_basic_functionality(self):
        """Demo basic FAISS functionality"""
        logger.info("=== Demo 1: Basic FAISS Functionality ===")
        
        try:
            # Add sample chat suggestions
            logger.info("Adding sample chat suggestions...")
            suggestion_ids = []
            
            for data in self.demo_data:
                suggestion_id = await faiss_similarity_engine.add_chat_suggestion(
                    user_input=data['user_input'],
                    ai_response=data['ai_response'],
                    context={'demo': True, 'category': data['category']},
                    feedback_score=data['feedback_score'],
                    category=data['category']
                )
                suggestion_ids.append(suggestion_id)
                logger.info(f"Added suggestion: {suggestion_id}")
            
            # Get statistics
            stats = await faiss_similarity_engine.get_statistics()
            logger.info(f"Database statistics: {json.dumps(stats, indent=2)}")
            
            logger.info("Basic functionality demo completed successfully!")
            return suggestion_ids
            
        except Exception as e:
            logger.error(f"Basic functionality demo failed: {str(e)}")
            return []
    
    async def demo_similarity_search(self):
        """Demo similarity search capabilities"""
        logger.info("=== Demo 2: Similarity Search ===")
        
        try:
            # Test queries
            test_queries = [
                "upload Excel file",
                "AI agents help",
                "metadata validation",
                "PySpark code generation",
                "workflow execution",
                "Excel analysis"
            ]
            
            for query in test_queries:
                logger.info(f"\nSearching for: '{query}'")
                
                # Basic similarity search
                results = await faiss_similarity_engine.find_similar_suggestions(
                    query=query,
                    top_k=3,
                    min_similarity=0.3
                )
                
                logger.info(f"Found {len(results)} similar suggestions:")
                for i, result in enumerate(results, 1):
                    logger.info(f"  {i}. Score: {result.get('similarity_score', 0):.3f}")
                    logger.info(f"     Category: {result.get('category', 'Unknown')}")
                    logger.info(f"     User: {result.get('user_input', '')[:60]}...")
                    logger.info(f"     AI: {result.get('ai_response', '')[:60]}...")
            
            logger.info("Similarity search demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Similarity search demo failed: {str(e)}")
    
    async def demo_complex_search(self):
        """Demo complex search with filters"""
        logger.info("=== Demo 3: Complex Search with Filters ===")
        
        try:
            # Test complex search with various filters
            search_scenarios = [
                {
                    'query': 'file operations',
                    'filters': {'category': 'file_operations', 'min_feedback_score': 0.8},
                    'description': 'High-quality file operation suggestions'
                },
                {
                    'query': 'AI agents',
                    'filters': {'category': 'ai_agents'},
                    'description': 'AI agent related suggestions'
                },
                {
                    'query': 'validation',
                    'filters': {'min_feedback_score': 0.9},
                    'description': 'High-feedback validation suggestions'
                }
            ]
            
            for scenario in search_scenarios:
                logger.info(f"\nComplex search: {scenario['description']}")
                logger.info(f"Query: '{scenario['query']}'")
                logger.info(f"Filters: {scenario['filters']}")
                
                results = await faiss_similarity_engine.search_complex_similarity(
                    query=scenario['query'],
                    filters=scenario['filters'],
                    top_k=5
                )
                
                logger.info(f"Found {len(results)} filtered results:")
                for i, result in enumerate(results, 1):
                    logger.info(f"  {i}. Score: {result.get('similarity_score', 0):.3f}")
                    logger.info(f"     Feedback: {result.get('feedback_score', 'N/A')}")
                    logger.info(f"     Category: {result.get('category', 'Unknown')}")
            
            logger.info("Complex search demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Complex search demo failed: {str(e)}")
    
    async def demo_chat_suggestions(self):
        """Demo chat suggestion manager features"""
        logger.info("=== Demo 4: Chat Suggestion Manager ===")
        
        try:
            # Test smart suggestions
            test_inputs = [
                "I need help with Excel files",
                "How do I use AI agents?",
                "Generate code for data transformation"
            ]
            
            for user_input in test_inputs:
                logger.info(f"\nGetting smart suggestions for: '{user_input}'")
                
                suggestions = await chat_suggestion_manager.get_smart_suggestions(
                    current_input=user_input,
                    user_context={'demo': True},
                    top_k=2
                )
                
                logger.info(f"Found {len(suggestions)} smart suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    logger.info(f"  {i}. Relevance: {suggestion.get('relevance_score', 0):.3f}")
                    logger.info(f"     Category: {suggestion.get('category', 'Unknown')}")
                    logger.info(f"     Suggestion: {suggestion.get('ai_response', '')[:80]}...")
            
            # Test contextual help
            logger.info("\nTesting contextual help...")
            contextual_help = await chat_suggestion_manager.get_contextual_help(
                current_input="upload Excel file",
                user_context={'demo': True}
            )
            logger.info(f"Contextual help: {contextual_help[:200]}...")
            
            logger.info("Chat suggestions demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Chat suggestions demo failed: {str(e)}")
    
    async def demo_training_data_export(self):
        """Demo training data export functionality"""
        logger.info("=== Demo 5: Training Data Export ===")
        
        try:
            # Export in different formats
            export_formats = ['json', 'csv']
            
            for format_type in export_formats:
                logger.info(f"Exporting training data in {format_type.upper()} format...")
                
                output_path = await chat_suggestion_manager.export_training_data(
                    format=format_type,
                    include_embeddings=True
                )
                
                logger.info(f"Training data exported to: {output_path}")
                
                # Verify export
                if Path(output_path).exists():
                    file_size = Path(output_path).stat().st_size
                    logger.info(f"Export file size: {file_size} bytes")
                else:
                    logger.warning(f"Export file not found: {output_path}")
            
            logger.info("Training data export demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Training data export demo failed: {str(e)}")
    
    async def demo_advanced_features(self):
        """Demo advanced FAISS features"""
        logger.info("=== Demo 6: Advanced Features ===")
        
        try:
            # Test category-based retrieval
            logger.info("Testing category-based retrieval...")
            categories = ['file_operations', 'ai_agents', 'validation', 'code_generation']
            
            for category in categories:
                suggestions = await faiss_similarity_engine.get_suggestions_by_category(
                    category=category,
                    limit=3
                )
                logger.info(f"Category '{category}': {len(suggestions)} suggestions")
            
            # Test feedback updates
            logger.info("\nTesting feedback updates...")
            # Get a suggestion to update
            results = await faiss_similarity_engine.find_similar_suggestions(
                query="upload file",
                top_k=1
            )
            
            if results:
                suggestion = results[0]
                suggestion_id = suggestion.get('suggestion_id')
                if suggestion_id:
                    # Update feedback
                    success = await faiss_similarity_engine.update_feedback(
                        suggestion_id=suggestion_id,
                        feedback_score=0.95
                    )
                    logger.info(f"Feedback update {'successful' if success else 'failed'}")
            
            # Test cleanup functionality
            logger.info("\nTesting cleanup functionality...")
            removed_count = await faiss_similarity_engine.cleanup_old_suggestions(days_old=365)  # Very old
            logger.info(f"Cleaned up {removed_count} old suggestions")
            
            logger.info("Advanced features demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Advanced features demo failed: {str(e)}")
    
    async def demo_performance_metrics(self):
        """Demo performance and metrics"""
        logger.info("=== Demo 7: Performance Metrics ===")
        
        try:
            # Get comprehensive statistics
            stats = await faiss_similarity_engine.get_statistics()
            suggestion_stats = await chat_suggestion_manager.get_statistics()
            
            logger.info("FAISS Engine Statistics:")
            logger.info(f"  Total suggestions: {stats.get('total_suggestions', 0)}")
            logger.info(f"  Total training examples: {stats.get('total_training_examples', 0)}")
            logger.info(f"  Embedding dimension: {stats.get('embedding_dimension', 0)}")
            logger.info(f"  FAISS index size: {stats.get('faiss_index_size', 0)}")
            
            logger.info("\nCategory Distribution:")
            for category, count in stats.get('categories', {}).items():
                logger.info(f"  {category}: {count}")
            
            logger.info("\nFeedback Distribution:")
            for score_range, count in stats.get('feedback_distribution', {}).items():
                logger.info(f"  {score_range}: {count}")
            
            logger.info("\nSuggestion Manager Statistics:")
            suggestion_mgr_stats = suggestion_stats.get('suggestion_manager', {})
            logger.info(f"  Total suggestions: {suggestion_mgr_stats.get('total_suggestions', 0)}")
            logger.info(f"  Categories: {len(suggestion_mgr_stats.get('categories', {}))}")
            
            logger.info("Performance metrics demo completed successfully!")
            
        except Exception as e:
            logger.error(f"Performance metrics demo failed: {str(e)}")
    
    async def run_complete_demo(self):
        """Run the complete FAISS features demo"""
        logger.info("🚀 Starting Comprehensive FAISS Features Demo")
        logger.info("=" * 60)
        
        try:
            # Run all demo sections
            await self.demo_basic_functionality()
            await asyncio.sleep(1)
            
            await self.demo_similarity_search()
            await asyncio.sleep(1)
            
            await self.demo_complex_search()
            await asyncio.sleep(1)
            
            await self.demo_chat_suggestions()
            await asyncio.sleep(1)
            
            await self.demo_training_data_export()
            await asyncio.sleep(1)
            
            await self.demo_advanced_features()
            await asyncio.sleep(1)
            
            await self.demo_performance_metrics()
            
            logger.info("\n🎉 All FAISS Features Demo Completed Successfully!")
            logger.info("=" * 60)
            logger.info("Key Features Demonstrated:")
            logger.info("✅ FAISS Vector Database Integration")
            logger.info("✅ Advanced Similarity Search")
            logger.info("✅ Complex Filtering and Ranking")
            logger.info("✅ Chat Suggestion Management")
            logger.info("✅ Training Data Export")
            logger.info("✅ Performance Metrics")
            logger.info("✅ Context-Aware Suggestions")
            
        except Exception as e:
            logger.error(f"Demo failed: {str(e)}")
            raise

async def main():
    """Main demo function"""
    try:
        demo = FAISSFeaturesDemo()
        await demo.run_complete_demo()
        
    except Exception as e:
        logger.error(f"Demo execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
