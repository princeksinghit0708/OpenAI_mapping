#!/usr/bin/env python3
"""
Hybrid Agentic Chat-Based AI Demo Application
Uses llm_service.py for online LLM responses but removes Hugging Face dependencies
Maintains agentic approach with online LLM integration
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

# Import hybrid agentic components
from agents.hybrid_agent_manager import HybridAgentManager, AgentType, hybrid_agent_manager
from agents.pure_offline_faiss_engine import PureOfflineFAISSSimilarityEngine
from agents.offline_chat_suggestion_manager import OfflineChatSuggestionManager

class HybridAgenticChatDemo:
    """
    Hybrid agentic chat-based interface using specialized agents with LLM integration
    Uses llm_service.py for online responses but removes Hugging Face dependencies
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
        
        # Initialize hybrid agentic system
        self._initialize_hybrid_agentic_system()
    
    def _initialize_hybrid_agentic_system(self):
        """Initialize hybrid agentic system with LLM integration"""
        print("🤖 Initializing Hybrid Agentic AI System...")
        print("   🔗 Using llm_service.py for online LLM responses")
        print("   🚫 Removed Hugging Face dependencies")
        print("   📦 Using specialized agents with LLM integration")
        
        # Initialize hybrid agent manager
        self.agent_manager = hybrid_agent_manager
        
        # Initialize offline FAISS engine for suggestions
        self.faiss_engine = PureOfflineFAISSSimilarityEngine()
        
        # Initialize offline chat suggestion manager
        self.suggestion_manager = OfflineChatSuggestionManager()
        
        # Load sample training data
        self._load_sample_training_data()
        
        print("✅ Hybrid Agentic AI System initialized successfully!")
        print("📊 Available Agents:")
        agents = self.agent_manager.get_available_agents()
        for agent in agents:
            llm_status = "with LLM" if agent.get('use_llm', False) else "offline only"
            print(f"   • {agent['name']}: {agent['status']} ({llm_status})")
        
        print("\n📊 System Statistics:")
        stats = self.faiss_engine.get_stats()
        for key, value in stats.items():
            print(f"   • {key}: {value}")
    
    def _load_sample_training_data(self):
        """Load sample training data for the hybrid system"""
        sample_data = [
            {
                "user_input": "Hello, I need help with data processing",
                "ai_response": "Hello! I can help you with data processing using my specialized agents with LLM integration. I have a Hybrid Data Processor Agent that can analyze Excel, CSV, and JSON files with intelligent insights. What type of data are you working with?",
                "category": "greeting"
            },
            {
                "user_input": "How do I process an Excel file?",
                "ai_response": "I'll use my Hybrid Data Processor Agent to help you with Excel files. It can analyze file structure, detect data types, identify missing values, and provide detailed insights using LLM-powered analysis. Please provide the file path or upload your Excel file.",
                "category": "help"
            },
            {
                "user_input": "I need to map fields between two schemas",
                "ai_response": "I'll use my Hybrid Schema Mapper Agent to help you create intelligent field mappings. It can analyze both schemas, suggest mappings based on field names and types, and generate mapping rules with LLM-enhanced recommendations. Please provide your source and target schema definitions.",
                "category": "mapping"
            },
            {
                "user_input": "Can you validate my data?",
                "ai_response": "I'll use my Hybrid Validator Agent to help you validate your data with intelligent insights. It can check data quality, validate against business rules, detect errors, and generate validation reports with LLM-powered analysis and recommendations. What validation rules would you like to apply?",
                "category": "validation"
            },
            {
                "user_input": "Generate code for data transformation",
                "ai_response": "I'll use my Hybrid Code Generator Agent to help you create intelligent transformation code. It can generate Python scripts, SQL queries, and data processing code with LLM-enhanced best practices and optimization suggestions. What type of code do you need?",
                "category": "code"
            },
            {
                "user_input": "What agents do you have?",
                "ai_response": "I have several specialized hybrid agents: Data Processor (Excel/CSV/JSON analysis with LLM insights), Schema Mapper (intelligent field mapping), Validator (data quality with AI recommendations), and Code Generator (enhanced code creation). Each agent uses LLM integration for better results.",
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
        """Process user input using hybrid agentic approach with LLM integration"""
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
                response = await self._process_with_hybrid_agent(agent_type, user_input, suggestions)
            else:
                response = await self._generate_hybrid_general_response(user_input, suggestions)
            
            # Add AI response to chat history
            self.chat_history.append({
                "ai": response,
                "timestamp": datetime.now().isoformat(),
                "agent_used": agent_type.value if agent_type else "general",
                "llm_enhanced": agent_type is not None
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
                "agent_used": "error",
                "llm_enhanced": False
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
    
    async def _process_with_hybrid_agent(self, agent_type: AgentType, user_input: str, suggestions: List[str]) -> str:
        """Process user input with specific hybrid agent using LLM integration"""
        try:
            # Prepare input data for agent
            input_data = self._prepare_agent_input(agent_type, user_input)
            
            # Process with hybrid agent (includes LLM integration)
            result = await self.agent_manager.process_with_agent(agent_type, input_data, self.user_context)
            
            if result.get("success", False):
                return self._format_hybrid_agent_response(agent_type, result, user_input)
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
    
    def _format_hybrid_agent_response(self, agent_type: AgentType, result: Dict[str, Any], user_input: str) -> str:
        """Format hybrid agent response for user"""
        agent_name = agent_type.value.replace('_', ' ').title()
        result_data = result.get("result", {})
        
        if agent_type == AgentType.DATA_PROCESSOR:
            if "file_type" in result_data:
                llm_insights = result_data.get("llm_insights", "")
                analysis_method = result_data.get("analysis_method", "unknown")
                
                response = f"""I've analyzed your {result_data['file_type']} file using my Hybrid Data Processor Agent:

📊 **File Analysis:**
• Rows: {result_data.get('rows', 'N/A')}
• Columns: {result_data.get('columns', 'N/A')}
• File Type: {result_data.get('file_type', 'N/A')}

📋 **Columns:** {', '.join(result_data.get('column_names', []))}

⚠️ **Missing Values:** {sum(result_data.get('missing_values', {}).values())} total

🔗 **Analysis Method:** {analysis_method.replace('_', ' ').title()}"""
                
                if llm_insights:
                    response += f"\n\n🤖 **LLM Insights:**\n{llm_insights}"
                
                response += "\n\nThe analysis is complete! Would you like me to help you with data transformation, validation, or mapping next?"
                
                return response
        
        elif agent_type == AgentType.SCHEMA_MAPPER:
            if "basic_mappings" in result_data:
                basic_mappings = result_data.get("basic_mappings", [])[:5]  # Show first 5
                llm_mappings = result_data.get("llm_mappings", [])
                mapping_method = result_data.get("mapping_method", "unknown")
                
                response = f"I've analyzed your schemas using my Hybrid Schema Mapper Agent:\n\n"
                response += f"🔗 **Mapping Method:** {mapping_method.replace('_', ' ').title()}\n\n"
                
                response += "📋 **Basic Mappings:**\n"
                for mapping in basic_mappings:
                    response += f"• **{mapping['source_field']}** → "
                    if mapping['exact_matches']:
                        response += f"**{mapping['exact_matches'][0]}** (exact match)\n"
                    elif mapping['partial_matches']:
                        response += f"**{mapping['partial_matches'][0]}** (partial match)\n"
                    else:
                        response += "No clear match found\n"
                
                if llm_mappings:
                    response += f"\n🤖 **LLM-Enhanced Mappings:**\n"
                    for mapping in llm_mappings[:3]:  # Show first 3
                        if isinstance(mapping, dict) and 'source_field' in mapping:
                            response += f"• **{mapping['source_field']}** → **{mapping.get('target_field', 'N/A')}** (confidence: {mapping.get('confidence', 'N/A')})\n"
                        elif isinstance(mapping, dict) and 'llm_insights' in mapping:
                            response += f"• {mapping['llm_insights']}\n"
                
                response += "\nWould you like me to generate mapping code or create transformation rules?"
                return response
        
        elif agent_type == AgentType.VALIDATOR:
            if "total_records" in result_data:
                llm_insights = result_data.get("llm_insights", "")
                validation_method = result_data.get("validation_method", "unknown")
                
                response = f"""I've validated your data using my Hybrid Validator Agent:

📊 **Validation Results:**
• Total Records: {result_data.get('total_records', 0)}
• Valid Records: {result_data.get('valid_records', 0)}
• Invalid Records: {result_data.get('invalid_records', 0)}
• Validity Rate: {result_data.get('validation_summary', {}).get('validity_rate', 0):.2%}

⚠️ **Errors:** {result_data.get('validation_summary', {}).get('total_errors', 0)}
⚠️ **Warnings:** {result_data.get('validation_summary', {}).get('total_warnings', 0)}

🔗 **Validation Method:** {validation_method.replace('_', ' ').title()}"""
                
                if llm_insights:
                    response += f"\n\n🤖 **LLM Insights:**\n{llm_insights}"
                
                response += "\n\nThe validation is complete! Would you like me to help you fix the errors or generate a validation report?"
                
                return response
        
        elif agent_type == AgentType.CODE_GENERATOR:
            if "code" in result_data:
                code = result_data.get("code", "")
                basic_code = result_data.get("basic_code", "")
                generation_method = result_data.get("generation_method", "unknown")
                
                response = f"""I've generated {result_data.get('code_type', 'Python')} code using my Hybrid Code Generator Agent:

🔗 **Generation Method:** {generation_method.replace('_', ' ').title()}

```{result_data.get('code_type', 'python')}
{code}
```"""
                
                if generation_method == "hybrid_llm" and basic_code != code:
                    response += f"\n📝 **Basic Template (for comparison):**\n```{result_data.get('code_type', 'python')}\n{basic_code}\n```"
                
                response += f"\n\nThe code is ready! You can copy and use it for your {result_data.get('task', 'data processing')} task. Would you like me to explain the code or generate additional functionality?"
                
                return response
        
        # Fallback response
        return f"I've processed your request using my {agent_name} agent with LLM integration. The task has been completed successfully!"
    
    async def _generate_hybrid_general_response(self, user_input: str, suggestions: List[str]) -> str:
        """Generate general response when no specific agent is needed"""
        user_input_lower = user_input.lower()
        
        # Greeting responses
        if any(word in user_input_lower for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return """Hello! I'm your hybrid agentic AI assistant with LLM integration. I have several specialized agents ready to help you:

🤖 **Available Hybrid Agents:**
• **Data Processor** - Excel, CSV, JSON file analysis with LLM insights
• **Schema Mapper** - Intelligent field mapping with AI recommendations
• **Validator** - Data quality validation with smart suggestions
• **Code Generator** - Enhanced code creation with best practices

🔗 **LLM Integration:** Each agent uses your llm_service.py for intelligent responses
🚫 **No Hugging Face:** Removed problematic dependencies while keeping LLM functionality

What would you like to work on today? Just describe your task and I'll use the appropriate agent to help you!"""
        
        # Help requests
        if any(word in user_input_lower for word in ["help", "assist", "support", "what can you do", "agents"]):
            return """I'm here to help using my specialized hybrid agents with LLM integration! Here's what I can do:

🔧 **Hybrid Data Processor Agent:**
• Analyze Excel, CSV, JSON files with LLM-powered insights
• Detect data types and missing values with intelligent recommendations
• Provide detailed file structure analysis with AI suggestions

🗺️ **Hybrid Schema Mapper Agent:**
• Create intelligent field mappings between schemas
• Suggest mapping rules with LLM-enhanced recommendations
• Generate transformation logic with best practices

✅ **Hybrid Validator Agent:**
• Check data quality with AI-powered analysis
• Validate against business rules with smart suggestions
• Generate comprehensive validation reports

💻 **Hybrid Code Generator Agent:**
• Create enhanced Python scripts with LLM assistance
• Generate optimized SQL queries with best practices
• Build validation and mapping code with intelligent suggestions

🔗 **LLM Integration:** All agents use your llm_service.py for intelligent responses
🚫 **No Hugging Face:** Removed problematic dependencies while maintaining LLM functionality

What specific task would you like help with?"""
        
        # Use suggestions if available
        if suggestions:
            return f"Based on similar requests, here are some suggestions:\n\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions[:2])
        
        # Default response
        return "I understand you're looking for assistance. I have several specialized hybrid agents that can help with data processing, mapping, validation, and code generation using LLM integration. Could you please describe what you'd like to accomplish?"
    
    def display_chat_history(self):
        """Display chat history with agent and LLM information"""
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
                llm_info = " [LLM Enhanced]" if message.get('llm_enhanced', False) else ""
                print(f"🤖 AI{agent_info}{llm_info}: {message['ai']}")
    
    def display_help(self):
        """Display help information"""
        help_text = """
🤖 HYBRID AGENTIC AI ASSISTANT - HELP MENU

AVAILABLE COMMANDS:
• help, h - Show this help menu
• history - Show chat history
• stats - Show system statistics
• agents - Show available agents
• clear - Clear chat history
• quit, exit, q - Exit the application

HYBRID AGENTS (with LLM Integration):
• Data Processor - Excel, CSV, JSON analysis with LLM insights
• Schema Mapper - Intelligent field mapping with AI recommendations
• Validator - Data quality validation with smart suggestions
• Code Generator - Enhanced code creation with best practices

HYBRID FEATURES:
• Automatic agent selection based on your request
• LLM integration using your llm_service.py
• Specialized processing for different task types
• Workflow orchestration between agents
• No Hugging Face dependencies (removed problematic libraries)

EXAMPLES:
• "Analyze my Excel file" → Hybrid Data Processor Agent (with LLM)
• "Map fields between schemas" → Hybrid Schema Mapper Agent (with LLM)
• "Validate my data" → Hybrid Validator Agent (with LLM)
• "Generate Python code" → Hybrid Code Generator Agent (with LLM)

PRIVACY: Uses your llm_service.py for intelligent responses while maintaining privacy.
        """
        print(help_text)
    
    def display_stats(self):
        """Display system statistics"""
        print("\n" + "="*60)
        print("HYBRID AGENTIC SYSTEM STATISTICS")
        print("="*60)
        
        # Agent statistics
        agents = self.agent_manager.get_available_agents()
        print(f"🤖 Available Hybrid Agents: {len(agents)}")
        for agent in agents:
            llm_status = "with LLM" if agent.get('use_llm', False) else "offline only"
            print(f"   • {agent['name']}: {agent['status']} ({llm_status})")
        
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
        print(f"🔗 LLM Integration: Using llm_service.py")
        print(f"🚫 Hugging Face: Dependencies removed")
        print(f"📦 Libraries: Built-in Python + minimal dependencies")
    
    def display_agents(self):
        """Display detailed agent information"""
        print("\n" + "="*60)
        print("AVAILABLE HYBRID AGENTS")
        print("="*60)
        
        agents = self.agent_manager.get_available_agents()
        capabilities = self.agent_manager.get_agent_capabilities()
        
        for agent in agents:
            print(f"\n🤖 {agent['name']}")
            print(f"   Type: {agent['type']}")
            print(f"   Status: {agent['status']}")
            print(f"   LLM Integration: {'Yes' if agent.get('use_llm', False) else 'No'}")
            print(f"   Capabilities:")
            for capability in capabilities.get(agent['type'], []):
                print(f"     • {capability}")
    
    async def run_interactive_chat(self):
        """Run interactive chat session"""
        print("🤖 HYBRID AGENTIC AI ASSISTANT")
        print("="*60)
        print("Welcome! I'm your hybrid agentic AI assistant.")
        print("I use specialized agents with LLM integration - no Hugging Face dependencies!")
        print("Type 'help' for available commands or 'quit' to exit.")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye! Thanks for using the Hybrid Agentic AI Assistant.")
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
                
                # Process user input with hybrid agentic approach
                print("🤖 AI: ", end="", flush=True)
                response = await self.process_user_input(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Hybrid Agentic AI Assistant.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main function"""
    print("🚀 Starting Hybrid Agentic Chat-Based AI Demo...")
    print("🤖 Using specialized agents with LLM integration")
    print("🔗 Using llm_service.py for online responses")
    print("🚫 Removed Hugging Face dependencies")
    
    # Create and run the demo
    demo = HybridAgenticChatDemo()
    
    # Run interactive chat
    asyncio.run(demo.run_interactive_chat())

if __name__ == "__main__":
    main()
