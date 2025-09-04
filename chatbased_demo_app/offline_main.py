#!/usr/bin/env python3
"""
Offline Chat-Based Agentic AI Demo Application
No Internet Required - Uses Local Processing Only
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

# Add the parent directory to path for imports
sys.path.append('..')
sys.path.append('../agentic_mapping_ai')
sys.path.append('../demo')

# Import offline components
from agents.offline_faiss_engine import OfflineFAISSSimilarityEngine
from agents.offline_chat_suggestion_manager import OfflineChatSuggestionManager

class OfflineChatBasedAgenticDemo:
    """
    Offline chat-based interface for the agentic AI mapping system
    No internet required - uses local processing only
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
        
        # Initialize offline components
        self._initialize_offline_system()
    
    def _initialize_offline_system(self):
        """Initialize offline components"""
        print("🔧 Initializing Offline AI System...")
        
        # Initialize offline FAISS engine
        self.faiss_engine = OfflineFAISSSimilarityEngine()
        
        # Initialize offline chat suggestion manager
        self.suggestion_manager = OfflineChatSuggestionManager()
        
        # Load sample training data
        self._load_sample_training_data()
        
        print("✅ Offline AI System initialized successfully!")
        print("📊 System Statistics:")
        stats = self.faiss_engine.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
    
    def _load_sample_training_data(self):
        """Load sample training data for the offline system"""
        sample_data = [
            {
                "user_input": "Hello, I need help with data processing",
                "ai_response": "Hello! I can help you with data processing tasks. What type of data are you working with?",
                "category": "greeting"
            },
            {
                "user_input": "How do I process an Excel file?",
                "ai_response": "I can help you process Excel files. Please upload your Excel file and I'll analyze its structure and help you with mapping or transformation tasks.",
                "category": "help"
            },
            {
                "user_input": "I have a CSV file with customer data",
                "ai_response": "Great! I can help you process CSV files. I can analyze the data structure, validate the data, and help you create mapping rules for transformation.",
                "category": "data"
            },
            {
                "user_input": "I need to map fields between two schemas",
                "ai_response": "I can help you create field mappings between different schemas. Please provide the source and target schema definitions, and I'll help you create the mapping rules.",
                "category": "mapping"
            },
            {
                "user_input": "Can you validate my data?",
                "ai_response": "Absolutely! I can help you validate your data for completeness, accuracy, and consistency. What validation rules would you like to apply?",
                "category": "validation"
            },
            {
                "user_input": "Generate code for data transformation",
                "ai_response": "I can generate code for data transformation tasks. What programming language would you prefer (Python, SQL, PySpark) and what type of transformation do you need?",
                "category": "code"
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
        """Process user input and generate response"""
        try:
            # Add to chat history
            self.chat_history.append({
                "user": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # Get suggestions from offline system
            suggestions = self.suggestion_manager.get_suggestions(user_input, max_suggestions=3)
            
            # Generate response based on input analysis
            response = await self._generate_offline_response(user_input, suggestions)
            
            # Add AI response to chat history
            self.chat_history.append({
                "ai": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Store interaction in offline systems
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
    
    async def _generate_offline_response(self, user_input: str, suggestions: List[str]) -> str:
        """Generate response using offline processing"""
        user_input_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return "Hello! I'm your offline AI assistant. I can help you with data processing, mapping, validation, and code generation tasks. What would you like to work on today?"
        
        # Help requests
        if any(word in user_input_lower for word in ["help", "assist", "support", "how to"]):
            return "I'm here to help! I can assist you with:\n• Data processing (Excel, CSV, JSON)\n• Schema mapping and transformation\n• Data validation and quality checks\n• Code generation for data tasks\n• Workflow automation\n\nWhat specific task would you like help with?"
        
        # Data processing requests
        if any(word in user_input_lower for word in ["data", "file", "excel", "csv", "json", "process"]):
            return "I can help you process your data files! I can:\n• Analyze file structure and content\n• Validate data quality\n• Create mapping rules\n• Generate transformation code\n• Provide data insights\n\nPlease upload your file or describe what you need to do with your data."
        
        # Mapping requests
        if any(word in user_input_lower for word in ["map", "mapping", "transform", "convert", "schema"]):
            return "I can help you with data mapping! I can:\n• Create field mappings between schemas\n• Generate transformation rules\n• Validate mapping logic\n• Generate code for transformations\n\nPlease provide your source and target schema information."
        
        # Validation requests
        if any(word in user_input_lower for word in ["validate", "check", "verify", "test", "error"]):
            return "I can help you validate your data! I can:\n• Check data completeness and accuracy\n• Validate against business rules\n• Identify data quality issues\n• Generate validation reports\n• Suggest data improvements\n\nWhat validation rules would you like to apply?"
        
        # Code generation requests
        if any(word in user_input_lower for word in ["code", "generate", "create", "build", "script", "function"]):
            return "I can help you generate code! I can create:\n• Python scripts for data processing\n• SQL queries for data transformation\n• PySpark code for big data tasks\n• Data validation scripts\n• Mapping and transformation functions\n\nWhat type of code do you need and for what purpose?"
        
        # Use suggestions if available
        if suggestions:
            return f"Based on similar requests, here are some suggestions:\n\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions[:2])
        
        # Default response
        return "I understand you're looking for assistance. I can help you with data processing, mapping, validation, and code generation tasks. Could you please provide more details about what you'd like to accomplish?"
    
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
🤖 OFFLINE AI ASSISTANT - HELP MENU

AVAILABLE COMMANDS:
• help, h - Show this help menu
• history - Show chat history
• stats - Show system statistics
• clear - Clear chat history
• quit, exit, q - Exit the application

CAPABILITIES:
• Data Processing: Excel, CSV, JSON file analysis and processing
• Schema Mapping: Create mappings between different data schemas
• Data Validation: Check data quality and completeness
• Code Generation: Generate Python, SQL, PySpark code
• Workflow Automation: Create automated data processing workflows

EXAMPLES:
• "Help me process an Excel file"
• "I need to map fields between two schemas"
• "Validate my customer data"
• "Generate Python code for data transformation"
• "Create a workflow for data processing"

PRIVACY: This system works completely offline - no data is sent to external services.
        """
        print(help_text)
    
    def display_stats(self):
        """Display system statistics"""
        print("\n" + "="*50)
        print("SYSTEM STATISTICS")
        print("="*50)
        
        faiss_stats = self.faiss_engine.get_stats()
        suggestion_stats = self.suggestion_manager.get_stats()
        
        print(f"📊 FAISS Engine:")
        for key, value in faiss_stats.items():
            print(f"   • {key}: {value}")
        
        print(f"\n📊 Suggestion Manager:")
        for key, value in suggestion_stats.items():
            print(f"   • {key}: {value}")
        
        print(f"\n💬 Chat History: {len(self.chat_history)} messages")
    
    async def run_interactive_chat(self):
        """Run interactive chat session"""
        print("🤖 OFFLINE AI ASSISTANT")
        print("="*50)
        print("Welcome! I'm your offline AI assistant for data processing tasks.")
        print("Type 'help' for available commands or 'quit' to exit.")
        print("="*50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using the Offline AI Assistant.")
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
                print("\n\n👋 Goodbye! Thanks for using the Offline AI Assistant.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main function"""
    print("🚀 Starting Offline Chat-Based Agentic AI Demo...")
    
    # Create and run the demo
    demo = OfflineChatBasedAgenticDemo()
    
    # Run interactive chat
    asyncio.run(demo.run_interactive_chat())

if __name__ == "__main__":
    main()
