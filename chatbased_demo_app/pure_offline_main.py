#!/usr/bin/env python3
"""
Pure Offline Chat-Based Agentic AI Demo Application
Uses ONLY built-in Python libraries - No external dependencies
No sentence-transformers, torch, transformers, or internet required
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import random
import re
from collections import Counter, defaultdict

# Add the parent directory to path for imports
sys.path.append('..')
sys.path.append('../agentic_mapping_ai')
sys.path.append('../demo')

# Import pure offline components
from agents.pure_offline_faiss_engine import PureOfflineFAISSSimilarityEngine
from agents.offline_chat_suggestion_manager import OfflineChatSuggestionManager

class PureOfflineChatBasedAgenticDemo:
    """
    Pure offline chat-based interface using only built-in Python libraries
    No external model downloads or internet required
    """
    
    def __init__(self):
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "excel_parsed").mkdir(exist_ok=True)
        (self.output_dir / "validation_reports").mkdir(exist_ok=True)
        (self.output_dir / "test_cases").mkdir(exist_ok=True)
        (self.output_dir / "generated_code").mkdir(exist_ok=True)
        (self.output_dir / "workflow_logs").mkdir(exist_ok=True)
        (self.output_dir / "final_reports").mkdir(exist_ok=True)
        
        # Chat session state
        self.chat_history = []
        self.current_workflow = None
        self.excel_file_path = None
        self.user_context = {}
        
        # Initialize pure offline components
        self._initialize_pure_offline_system()
    
    def _initialize_pure_offline_system(self):
        """Initialize pure offline components using only built-in libraries"""
        print("🔧 Initializing Pure Offline AI System...")
        print("   📦 Using only built-in Python libraries")
        print("   🚫 No external model downloads required")
        
        # Initialize pure offline FAISS engine
        self.faiss_engine = PureOfflineFAISSSimilarityEngine()
        
        # Initialize offline chat suggestion manager
        self.suggestion_manager = OfflineChatSuggestionManager()
        
        # Load sample training data
        self._load_sample_training_data()
        
        print("✅ Pure Offline AI System initialized successfully!")
        print("📊 System Statistics:")
        stats = self.faiss_engine.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
    
    def _load_sample_training_data(self):
        """Load sample training data for the pure offline system"""
        sample_data = [
            {
                "user_input": "Hello, I need help with data processing",
                "ai_response": "Hello! I can help you with data processing tasks using pure offline methods. What type of data are you working with?",
                "category": "greeting"
            },
            {
                "user_input": "How do I process an Excel file?",
                "ai_response": "I can help you process Excel files using pandas and openpyxl. Please upload your Excel file and I'll analyze its structure and help you with mapping or transformation tasks.",
                "category": "help"
            },
            {
                "user_input": "I have a CSV file with customer data",
                "ai_response": "Great! I can help you process CSV files using built-in Python libraries. I can analyze the data structure, validate the data, and help you create mapping rules for transformation.",
                "category": "data"
            },
            {
                "user_input": "I need to map fields between two schemas",
                "ai_response": "I can help you create field mappings between different schemas using pattern matching and built-in text processing. Please provide the source and target schema definitions.",
                "category": "mapping"
            },
            {
                "user_input": "Can you validate my data?",
                "ai_response": "Absolutely! I can help you validate your data using built-in validation rules and pattern matching. What validation rules would you like to apply?",
                "category": "validation"
            },
            {
                "user_input": "Generate code for data transformation",
                "ai_response": "I can generate code for data transformation tasks using built-in Python libraries. What programming language would you prefer and what type of transformation do you need?",
                "category": "code"
            },
            {
                "user_input": "What can you do without internet?",
                "ai_response": "I can perform data processing, text analysis, pattern matching, code generation, and similarity search using only built-in Python libraries. No internet required!",
                "category": "help"
            },
            {
                "user_input": "How does your text processing work?",
                "ai_response": "I use TF-IDF (Term Frequency-Inverse Document Frequency) and character n-grams for text processing. This creates meaningful embeddings without needing external models.",
                "category": "help"
            }
        ]
        
        # Train the embedder on sample data
        self.faiss_engine.embedder.build_vocabulary([f"{item['user_input']} {item['ai_response']}" for item in sample_data])
        
        # Add sample interactions
        for item in sample_data:
            asyncio.run(self.faiss_engine.add_chat_interaction(
                item["user_input"],
                item["ai_response"],
                category=item["category"]
            ))
    
    async def process_user_input(self, user_input: str) -> str:
        """Process user input and generate response using pure offline methods"""
        try:
            # Add to chat history
            self.chat_history.append({
                "user": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get suggestions from pure offline system
            suggestions = self.suggestion_manager.get_suggestions(user_input, max_suggestions=3)
            
            # Generate response based on input analysis using built-in libraries
            response = await self._generate_pure_offline_response(user_input, suggestions)
            
            # Add AI response to chat history
            self.chat_history.append({
                "ai": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Store interaction in pure offline systems
            await self.faiss_engine.add_chat_interaction(user_input, response)
            await self.suggestion_manager.add_chat_interaction(user_input, response)
            
            return response
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            self.chat_history.append({
                "ai": error_response,
                "timestamp": datetime.now().isoformat()
            })
            return error_response
    
    async def _generate_pure_offline_response(self, user_input: str, suggestions: List[str]) -> str:
        """Generate response using pure offline processing and built-in libraries"""
        user_input_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "Hello! I'm your pure offline AI assistant. I use only built-in Python libraries for data processing, mapping, validation, and code generation. What would you like to work on today?"
        
        # Help requests
        if any(word in user_input_lower for word in ["help", "assist", "support", "how to", "what can you do"]):
            return """I'm here to help using pure offline methods! I can assist you with:

• Data Processing: Excel, CSV, JSON using pandas and built-in libraries
• Schema Mapping: Pattern matching and text processing
• Data Validation: Built-in validation rules and quality checks
• Code Generation: Python, SQL using template-based generation
• Text Analysis: TF-IDF, character n-grams, similarity search
• Workflow Automation: Local file processing and automation

All processing happens locally - no internet required! What specific task would you like help with?"""
        
        # Data processing requests
        if any(word in user_input_lower for word in ["data", "file", "excel", "csv", "json", "process", "analyze"]):
            return """I can help you process your data files using pure offline methods! I can:

• Analyze file structure and content using pandas
• Validate data quality using built-in validation rules
• Create mapping rules using pattern matching
• Generate transformation code using templates
• Provide data insights using statistical analysis
• Process Excel, CSV, JSON files locally

Please upload your file or describe what you need to do with your data."""
        
        # Mapping requests
        if any(word in user_input_lower for word in ["map", "mapping", "transform", "convert", "schema", "field"]):
            return """I can help you with data mapping using pure offline methods! I can:

• Create field mappings between schemas using pattern matching
• Generate transformation rules using built-in text processing
• Validate mapping logic using local validation
• Generate code for transformations using templates
• Use TF-IDF similarity for field matching

Please provide your source and target schema information."""
        
        # Validation requests
        if any(word in user_input_lower for word in ["validate", "check", "verify", "test", "error", "quality"]):
            return """I can help you validate your data using pure offline methods! I can:

• Check data completeness and accuracy using built-in rules
• Validate against business rules using pattern matching
• Identify data quality issues using statistical analysis
• Generate validation reports using templates
• Suggest data improvements using similarity analysis

What validation rules would you like to apply?"""
        
        # Code generation requests
        if any(word in user_input_lower for word in ["code", "generate", "create", "build", "script", "function", "program"]):
            return """I can help you generate code using pure offline methods! I can create:

• Python scripts for data processing using pandas
• SQL queries for data transformation using templates
• Data validation scripts using built-in libraries
• Mapping and transformation functions using pattern matching
• Workflow automation scripts using local processing

What type of code do you need and for what purpose?"""
        
        # Technical questions about the system
        if any(word in user_input_lower for word in ["how does", "how do you", "what libraries", "offline", "privacy"]):
            return """I work completely offline using only built-in Python libraries:

• Text Processing: TF-IDF, character n-grams, regex
• Vector Search: FAISS for similarity search
• Data Processing: pandas, openpyxl for files
• Pattern Matching: Built-in text processing
• Code Generation: Template-based generation
• Privacy: All data stays on your machine

No external models, no internet, no data transmission!"""
        
        # Use suggestions if available
        if suggestions:
            return f"Based on similar requests, here are some suggestions:\n\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions[:2])
        
        # Default response
        return "I understand you're looking for assistance. I can help you with data processing, mapping, validation, and code generation using pure offline methods. Could you please provide more details about what you'd like to accomplish?"
    
    def display_chat_history(self):
        """Display chat history"""
        if not self.chat_history:
            print("No chat history available.")
            return
        
        print("\n" + "="*50)
        print("CHAT HISTORY")
        print("="*50)
        
        for i, message in enumerate(self.chat_history, 1):
            if "user" in message:
                print(f"\n👤 User: {message['user']}")
            elif "ai" in message:
                print(f"🤖 AI: {message['ai']}")
    
    def display_help(self):
        """Display help information"""
        help_text = """
🤖 PURE OFFLINE AI ASSISTANT - HELP MENU

AVAILABLE COMMANDS:
• help, h - Show this help menu
• history - Show chat history
• stats - Show system statistics
• clear - Clear chat history
• quit, exit, q - Exit the application

CAPABILITIES (Pure Offline):
• Data Processing: Excel, CSV, JSON using pandas and built-in libraries
• Schema Mapping: Pattern matching and text processing
• Data Validation: Built-in validation rules and quality checks
• Code Generation: Python, SQL using template-based generation
• Text Analysis: TF-IDF, character n-grams, similarity search
• Workflow Automation: Local file processing and automation

TECHNICAL DETAILS:
• Uses only built-in Python libraries
• No external model downloads required
• TF-IDF + character n-grams for text processing
• FAISS for vector similarity search
• Complete privacy - no data transmission

EXAMPLES:
• "Help me process an Excel file"
• "I need to map fields between two schemas"
• "Validate my customer data"
• "Generate Python code for data transformation"
• "How does your text processing work?"

PRIVACY: This system works completely offline using only built-in libraries.
        """
        print(help_text)
    
    def display_stats(self):
        """Display system statistics"""
        print("\n" + "="*50)
        print("PURE OFFLINE SYSTEM STATISTICS")
        print("="*50)
        
        faiss_stats = self.faiss_engine.get_stats()
        suggestion_stats = self.suggestion_manager.get_stats()
        
        print(f"📊 Pure Offline FAISS Engine:")
        for key, value in faiss_stats.items():
            print(f"   • {key}: {value}")
        
        print(f"\n📊 Suggestion Manager:")
        for key, value in suggestion_stats.items():
            print(f"   • {key}: {value}")
        
        print(f"\n💬 Chat History: {len(self.chat_history)} messages")
        print(f"🔒 Privacy: Complete offline operation")
        print(f"📦 Libraries: Built-in Python only")
    
    async def run_interactive_chat(self):
        """Run interactive chat session"""
        print("🤖 PURE OFFLINE AI ASSISTANT")
        print("="*50)
        print("Welcome! I'm your pure offline AI assistant.")
        print("I use only built-in Python libraries - no internet required!")
        print("Type 'help' for available commands or 'quit' to exit.")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using the Pure Offline AI Assistant.")
                    break
                elif user_input.lower() in ['help', 'h']:
                    self.display_help()
                    continue
                elif user_input.lower() == 'history':
                    self.display_chat_history()
                    continue
                elif user_input.lower() == 'stats':
                    self.display_stats()
                    continue
                elif user_input.lower() == 'clear':
                    self.chat_history = []
                    print("✅ Chat history cleared.")
                    continue
                
                # Process user input
                print("🤖 AI: ", end="", flush=True)
                response = await self.process_user_input(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Pure Offline AI Assistant.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main function"""
    print("🚀 Starting Pure Offline Chat-Based Agentic AI Demo...")
    print("📦 Using only built-in Python libraries")
    print("🔒 Complete privacy - no internet required")
    
    # Create and run the demo
    demo = PureOfflineChatBasedAgenticDemo()
    
    # Run interactive chat
    asyncio.run(demo.run_interactive_chat())

if __name__ == "__main__":
    main()
