#!/usr/bin/env python3
"""
Offline Agentic Chat-Based AI Demo Application
Uses agentic approach with specialized offline agents
No external dependencies - Only built-in Python libraries + minimal requirements
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

# Import offline agentic components
from agents.offline_agent_manager import OfflineAgentManager, AgentType, offline_agent_manager
from agents.pure_offline_faiss_engine import PureOfflineFAISSSimilarityEngine
from agents.offline_chat_suggestion_manager import OfflineChatSuggestionManager

class OfflineAgenticChatDemo:
    """
    Offline agentic chat-based interface using specialized agents
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
        
        # Initialize offline agentic system
        self._initialize_offline_agentic_system()
    
    def _initialize_offline_agentic_system(self):
        """Initialize offline agentic system with specialized agents"""
        print("🤖 Initializing Offline Agentic AI System...")
        print("   📦 Using specialized agents with built-in Python libraries")
        print("   🚫 No external model downloads required")
        
        # Initialize agent manager
        self.agent_manager = offline_agent_manager
        
        # Initialize offline FAISS engine
        self.faiss_engine = PureOfflineFAISSSimilarityEngine()
        
        # Initialize offline chat suggestion manager
        self.suggestion_manager = OfflineChatSuggestionManager()
        
        # Load sample training data
        self._load_sample_training_data()
        
        print("✅ Offline Agentic AI System initialized successfully!")
        print("📊 Available Agents:")
        agents = self.agent_manager.get_available_agents()
        for agent in agents:
            print(f"   • {agent['name']}: {agent['status']}")
        
        print("\n📊 System Statistics:")
        stats = self.faiss_engine.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
    
    def _load_sample_training_data(self):
        """Load sample training data for the offline agentic system"""
        sample_data = [
            {
                "user_input": "Hello, I need help with data processing",
                "ai_response": "Hello! I can help you with data processing using my specialized agents. I have a Data Processor Agent that can analyze Excel, CSV, and JSON files. What type of data are you working with?",
                "category": "greeting"
            },
            {
                "user_input": "How do I process an Excel file?",
                "ai_response": "I'll use my Data Processor Agent to help you with Excel files. It can analyze file structure, detect data types, identify missing values, and provide detailed insights. Please provide the file path or upload your Excel file.",
                "category": "help"
            },
            {
                "user_input": "I need to map fields between two schemas",
                "ai_response": "I'll use my Schema Mapper Agent to help you create field mappings. It can analyze both schemas, suggest mappings based on field names and types, and generate mapping rules. Please provide your source and target schema definitions.",
                "category": "mapping"
            },
            {
                "user_input": "Can you validate my data?",
                "ai_response": "I'll use my Validator Agent to help you validate your data. It can check data quality, validate against business rules, detect errors, and generate validation reports. What validation rules would you like to apply?",
                "category": "validation"
            },
            {
                "user_input": "Generate code for data transformation",
                "ai_response": "I'll use my Code Generator Agent to help you create transformation code. It can generate Python scripts, SQL queries, and data processing code based on your requirements. What type of code do you need?",
                "category": "code"
            },
            {
                "user_input": "What agents do you have?",
                "ai_response": "I have several specialized agents: Data Processor (Excel/CSV/JSON analysis), Schema Mapper (field mapping), Validator (data quality), and Code Generator (Python/SQL code). Each agent is designed for specific tasks and works completely offline.",
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
        """Process user input using agentic approach"""
        try:
            # Add to chat history
            self.chat_history.append({
                "user": user_input,
                "timestamp": datetime.now().isoformat()
            })
            
            # Determine which agent to use based on input analysis
            agent_type = self._determine_agent_type(user_input)
            
            # Get suggestions from offline system
            suggestions = self.suggestion_manager.get_suggestions(user_input, max_suggestions=3)
            
            # Process with appropriate agent
            if agent_type:
                response = await self._process_with_agent(agent_type, user_input, suggestions)
            else:
                response = await self._generate_general_response(user_input, suggestions)
            
            # Add AI response to chat history
            self.chat_history.append({
                "ai": response,
                "timestamp": datetime.now().isoformat(),
                "agent_used": agent_type.value if agent_type else "general"
            })
            
            # Store interaction in offline systems
            await self.faiss_engine.add_chat_interaction(user_input, response)
            await self.suggestion_manager.add_chat_interaction(user_input, response)
            
            return response
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}. Please try again."
            self.chat_history.append({
                "ai": error_response,
                "timestamp": datetime.now().isoformat(),
                "agent_used": "error"
            })
            return error_response
    
    def _determine_agent_type(self, user_input: str) -> Optional[AgentType]:
        """Determine which agent to use based on user input"""
        user_input_lower = user_input.lower()
        
        # Data processing keywords
        if any(word in user_input_lower for word in ["data", "file", "excel", "csv", "json", "process", "analyze", "upload"]):
            return AgentType.DATA_PROCESSOR
        
        # Schema mapping keywords
        if any(word in user_input_lower for word in ["map", "mapping", "schema", "field", "transform", "convert", "mapping rules"]):
            return AgentType.SCHEMA_MAPPER
        
        # Validation keywords
        if any(word in user_input_lower for word in ["validate", "check", "verify", "test", "error", "quality", "validation"]):
            return AgentType.VALIDATOR
        
        # Code generation keywords
        if any(word in user_input_lower for word in ["code", "generate", "create", "build", "script", "function", "program", "sql", "python"]):
            return AgentType.CODE_GENERATOR
        
        return None
    
    async def _process_with_agent(self, agent_type: AgentType, user_input: str, suggestions: List[str]) -> str:
        """Process user input with specific agent"""
        try:
            # Prepare input data for agent
            input_data = self._prepare_agent_input(agent_type, user_input)
            
            # Process with agent
            result = await self.agent_manager.process_with_agent(agent_type, input_data, self.user_context)
            
            if result.get("success", False):
                return self._format_agent_response(agent_type, result, user_input)
            else:
                error_msg = result.get("error", "Unknown error")
                return f"I encountered an issue with my {agent_type.value.replace('_', ' ')} agent: {error_msg}. Please try rephrasing your request or provide more details."
                
        except Exception as e:
            return f"I had trouble processing your request with my {agent_type.value.replace('_', ' ')} agent: {str(e)}. Let me try a different approach."
    
    def _prepare_agent_input(self, agent_type: AgentType, user_input: str) -> Dict[str, Any]:
        """Prepare input data for specific agent"""
        if agent_type == AgentType.DATA_PROCESSOR:
            # Extract file path if mentioned
            file_path = self._extract_file_path(user_input)
            return {
                "file_path": file_path,
                "task": "analyze",
                "user_input": user_input
            }
        
        elif agent_type == AgentType.SCHEMA_MAPPER:
            return {
                "source_schema": self.user_context.get("source_schema"),
                "target_schema": self.user_context.get("target_schema"),
                "mapping_rules": self.user_context.get("mapping_rules", []),
                "user_input": user_input
            }
        
        elif agent_type == AgentType.VALIDATOR:
            return {
                "data": self.user_context.get("data"),
                "validation_rules": self.user_context.get("validation_rules", []),
                "user_input": user_input
            }
        
        elif agent_type == AgentType.CODE_GENERATOR:
            return {
                "code_type": self._extract_code_type(user_input),
                "task": self._extract_task_type(user_input),
                "parameters": self._extract_parameters(user_input),
                "user_input": user_input
            }
        
        return {"user_input": user_input}
    
    def _extract_file_path(self, user_input: str) -> Optional[str]:
        """Extract file path from user input"""
        # Simple file path extraction
        words = user_input.split()
        for word in words:
            if any(ext in word.lower() for ext in ['.xlsx', '.xls', '.csv', '.json']):
                return word
        return None
    
    def _extract_code_type(self, user_input: str) -> str:
        """Extract code type from user input"""
        user_input_lower = user_input.lower()
        if "sql" in user_input_lower:
            return "sql"
        elif "python" in user_input_lower:
            return "python"
        else:
            return "python"  # Default
    
    def _extract_task_type(self, user_input: str) -> str:
        """Extract task type from user input"""
        user_input_lower = user_input.lower()
        if "validation" in user_input_lower or "validate" in user_input_lower:
            return "data_validation"
        elif "mapping" in user_input_lower or "map" in user_input_lower:
            return "schema_mapping"
        else:
            return "data_processing"
    
    def _extract_parameters(self, user_input: str) -> Dict[str, Any]:
        """Extract parameters from user input"""
        return {
            "description": user_input,
            "timestamp": datetime.now().isoformat()
        }
    
    def _format_agent_response(self, agent_type: AgentType, result: Dict[str, Any], user_input: str) -> str:
        """Format agent response for user"""
        agent_name = agent_type.value.replace('_', ' ').title()
        result_data = result.get("result", {})
        
        if agent_type == AgentType.DATA_PROCESSOR:
            if "file_type" in result_data:
                return f"""I've analyzed your {result_data['file_type']} file using my Data Processor Agent:

📊 **File Analysis:**
• Rows: {result_data.get('rows', 'N/A')}
• Columns: {result_data.get('columns', 'N/A')}
• File Type: {result_data.get('file_type', 'N/A')}

📋 **Columns:** {', '.join(result_data.get('column_names', []))}

⚠️ **Missing Values:** {sum(result_data.get('missing_values', {}).values())} total

The analysis is complete! Would you like me to help you with data transformation, validation, or mapping next?"""
        
        elif agent_type == AgentType.SCHEMA_MAPPER:
            if "mapping_suggestions" in result_data:
                suggestions = result_data["mapping_suggestions"][:5]  # Show first 5
                response = f"I've analyzed your schemas using my Schema Mapper Agent:\n\n"
                for suggestion in suggestions:
                    response += f"• **{suggestion['source_field']}** → "
                    if suggestion['exact_matches']:
                        response += f"**{suggestion['exact_matches'][0]}** (exact match)\n"
                    elif suggestion['partial_matches']:
                        response += f"**{suggestion['partial_matches'][0]}** (partial match)\n"
                    elif suggestion['similar_matches']:
                        response += f"**{suggestion['similar_matches'][0][0]}** (similar: {suggestion['similar_matches'][0][1]:.2f})\n"
                    else:
                        response += "No clear match found\n"
                
                response += "\nWould you like me to generate mapping code or create transformation rules?"
                return response
        
        elif agent_type == AgentType.VALIDATOR:
            if "total_records" in result_data:
                return f"""I've validated your data using my Validator Agent:

📊 **Validation Results:**
• Total Records: {result_data.get('total_records', 0)}
• Valid Records: {result_data.get('valid_records', 0)}
• Invalid Records: {result_data.get('invalid_records', 0)}
• Validity Rate: {result_data.get('validation_summary', {}).get('validity_rate', 0):.2%}

⚠️ **Errors:** {result_data.get('validation_summary', {}).get('total_errors', 0)}
⚠️ **Warnings:** {result_data.get('validation_summary', {}).get('total_warnings', 0)}

The validation is complete! Would you like me to help you fix the errors or generate a validation report?"""
        
        elif agent_type == AgentType.CODE_GENERATOR:
            if "code" in result_data:
                return f"""I've generated {result_data.get('code_type', 'Python')} code using my Code Generator Agent:

```{result_data.get('code_type', 'python')}
{result_data.get('code', '')}
```

The code is ready! You can copy and use it for your {result_data.get('task', 'data processing')} task. Would you like me to explain the code or generate additional functionality?"""
        
        # Fallback response
        return f"I've processed your request using my {agent_name} agent. The task has been completed successfully!"
    
    async def _generate_general_response(self, user_input: str, suggestions: List[str]) -> str:
        """Generate general response when no specific agent is needed"""
        user_input_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return """Hello! I'm your offline agentic AI assistant. I have several specialized agents ready to help you:

🤖 **Available Agents:**
• **Data Processor** - Excel, CSV, JSON file analysis
• **Schema Mapper** - Field mapping and transformation rules
• **Validator** - Data quality and validation checks
• **Code Generator** - Python and SQL code creation

What would you like to work on today? Just describe your task and I'll use the appropriate agent to help you!"""
        
        # Help requests
        if any(word in user_input_lower for word in ["help", "assist", "support", "what can you do", "agents"]):
            return """I'm here to help using my specialized offline agents! Here's what I can do:

🔧 **Data Processing Agent:**
• Analyze Excel, CSV, JSON files
• Detect data types and missing values
• Provide file structure insights

🗺️ **Schema Mapper Agent:**
• Create field mappings between schemas
• Suggest mapping rules based on field names
• Generate transformation logic

✅ **Validator Agent:**
• Check data quality and completeness
• Validate against business rules
• Generate validation reports

💻 **Code Generator Agent:**
• Create Python scripts for data processing
• Generate SQL queries for transformations
• Build validation and mapping code

All agents work completely offline using built-in Python libraries. What specific task would you like help with?"""
        
        # Use suggestions if available
        if suggestions:
            return f"Based on similar requests, here are some suggestions:\n\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions[:2])
        
        # Default response
        return "I understand you're looking for assistance. I have several specialized agents that can help with data processing, mapping, validation, and code generation. Could you please describe what you'd like to accomplish?"
    
    def display_chat_history(self):
        """Display chat history with agent information"""
        if not self.chat_history:
            print("No chat history available.")
            return
        
        print("\n" + "="*60)
        print("CHAT HISTORY")
        print("="*60)
        
        for i, message in enumerate(self.chat_history, 1):
            if "user" in message:
                print(f"\n👤 User: {message['user']}")
            elif "ai" in message:
                agent_info = f" (Agent: {message.get('agent_used', 'general')})" if 'agent_used' in message else ""
                print(f"🤖 AI{agent_info}: {message['ai']}")
    
    def display_help(self):
        """Display help information"""
        help_text = """
🤖 OFFLINE AGENTIC AI ASSISTANT - HELP MENU

AVAILABLE COMMANDS:
• help, h - Show this help menu
• history - Show chat history
• stats - Show system statistics
• agents - Show available agents
• clear - Clear chat history
• quit, exit, q - Exit the application

SPECIALIZED AGENTS:
• Data Processor - Excel, CSV, JSON file analysis
• Schema Mapper - Field mapping and transformation rules
• Validator - Data quality and validation checks
• Code Generator - Python and SQL code creation

AGENTIC FEATURES:
• Automatic agent selection based on your request
• Specialized processing for different task types
• Workflow orchestration between agents
• Complete offline operation using built-in libraries

EXAMPLES:
• "Analyze my Excel file" → Data Processor Agent
• "Map fields between schemas" → Schema Mapper Agent
• "Validate my data" → Validator Agent
• "Generate Python code" → Code Generator Agent

PRIVACY: All agents work completely offline - no data transmission.
        """
        print(help_text)
    
    def display_stats(self):
        """Display system statistics"""
        print("\n" + "="*60)
        print("OFFLINE AGENTIC SYSTEM STATISTICS")
        print("="*60)
        
        # Agent statistics
        agents = self.agent_manager.get_available_agents()
        print(f"🤖 Available Agents: {len(agents)}")
        for agent in agents:
            print(f"   • {agent['name']}: {agent['status']}")
        
        # FAISS engine statistics
        faiss_stats = self.faiss_engine.get_stats()
        print(f"\n📊 FAISS Engine:")
        for key, value in faiss_stats.items():
            print(f"   • {key}: {value}")
        
        # Suggestion manager statistics
        suggestion_stats = self.suggestion_manager.get_stats()
        print(f"\n📊 Suggestion Manager:")
        for key, value in suggestion_stats.items():
            print(f"   • {key}: {value}")
        
        print(f"\n💬 Chat History: {len(self.chat_history)} messages")
        print(f"🔒 Privacy: Complete offline operation")
        print(f"📦 Libraries: Built-in Python + minimal dependencies")
    
    def display_agents(self):
        """Display detailed agent information"""
        print("\n" + "="*60)
        print("AVAILABLE AGENTS")
        print("="*60)
        
        agents = self.agent_manager.get_available_agents()
        capabilities = self.agent_manager.get_agent_capabilities()
        
        for agent in agents:
            print(f"\n🤖 {agent['name']}")
            print(f"   Type: {agent['type']}")
            print(f"   Status: {agent['status']}")
            print(f"   Capabilities:")
            for capability in capabilities.get(agent['type'], []):
                print(f"     • {capability}")
    
    async def run_interactive_chat(self):
        """Run interactive chat session"""
        print("🤖 OFFLINE AGENTIC AI ASSISTANT")
        print("="*60)
        print("Welcome! I'm your offline agentic AI assistant.")
        print("I have specialized agents for different tasks - no internet required!")
        print("Type 'help' for available commands or 'quit' to exit.")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using the Offline Agentic AI Assistant.")
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
                elif user_input.lower() == 'agents':
                    self.display_agents()
                    continue
                elif user_input.lower() == 'clear':
                    self.chat_history = []
                    print("✅ Chat history cleared.")
                    continue
                
                # Process user input with agentic approach
                print("🤖 AI: ", end="", flush=True)
                response = await self.process_user_input(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Offline Agentic AI Assistant.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main function"""
    print("🚀 Starting Offline Agentic Chat-Based AI Demo...")
    print("🤖 Using specialized agents with built-in Python libraries")
    print("🔒 Complete privacy - no internet required")
    
    # Create and run the demo
    demo = OfflineAgenticChatDemo()
    
    # Run interactive chat
    asyncio.run(demo.run_interactive_chat())

if __name__ == "__main__":
    main()
