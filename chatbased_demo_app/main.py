#!/usr/bin/env python3
"""
Chat-Based Agentic AI Demo Application
Interactive chat interface for the agentic mapping AI system
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# Add the parent directory to path for imports
sys.path.append('..')
sys.path.append('../agentic_mapping_ai')
sys.path.append('../demo')

# Import the agent manager and suggestion manager
from agents.agent_manager import agent_manager
from agents.chat_suggestion_manager import chat_suggestion_manager

class ChatBasedAgenticDemo:
    """
    Chat-based interface for the agentic AI mapping system
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
        
        # Initialize the system with agent manager and suggestion manager
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the chat-based system with AI agents and FAISS suggestions"""
        print("Chat-Based Agentic AI Demo System")
        print("=" * 60)
        print("Initializing AI agents and FAISS similarity engine...")
        
        # Get agent status
        agent_status = agent_manager.get_agent_status()
        print(f"Agent Source: {agent_status['agents_source']}")
        print(f"Total Agents: {agent_status['total_agents']}")
        print(f"Available Agents: {', '.join(agent_status['available_agent_types'])}")
        
        print("System ready for interactive chat with intelligent suggestions!")
        print("=" * 60)
        print("\nYou can now chat with the AI agents!")
        print("Available commands:")
        print("   • 'help' - Show available commands")
        print("   • 'agents' - Show AI agent status")
        print("   • 'test' - Test all AI agents")
        print("   • 'upload <file_path>' - Upload Excel file")
        print("   • 'analyze' - Analyze uploaded file")
        print("   • 'validate' - Run metadata validation")
        print("   • 'generate' - Generate PySpark code")
        print("   • 'workflow' - Run complete workflow")
        print("   • 'suggestions' - View suggestion history")
        print("   • 'export' - Export training data")
        print("   • 'status' - Show current status")
        print("   • 'quit' - Exit the application")
        print("=" * 60)
    
    async def process_chat_input(self, user_input: str) -> str:
        """Process user chat input and return AI response with intelligent suggestions"""
        try:
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_input,
                'type': 'user_input'
            })
            
            # Process commands
            if user_input.lower().startswith('help'):
                return await self._get_help_response(user_input)
            
            elif user_input.lower() == 'agents':
                return agent_manager.get_agent_info()
            
            elif user_input.lower() == 'test':
                return await self._handle_agent_testing()
            
            elif user_input.lower() == 'suggestions':
                return await self._handle_suggestions_command()
            
            elif user_input.lower() == 'export':
                return await self._handle_export_command()
            
            elif user_input.lower().startswith('upload'):
                return await self._handle_file_upload(user_input)
            
            elif user_input.lower() == 'analyze':
                return await self._handle_analyze()
            
            elif user_input.lower() == 'validate':
                return await self._handle_validation()
            
            elif user_input.lower() == 'generate':
                return await self._handle_code_generation()
            
            elif user_input.lower() == 'workflow':
                return await self._handle_complete_workflow()
            
            elif user_input.lower() == 'status':
                return self._get_status_response()
            
            elif user_input.lower() in ['quit', 'exit', 'bye']:
                return "Goodbye! Thanks for using the Chat-Based Agentic AI Demo!"
            
            else:
                return await self._get_general_response(user_input)
                
        except Exception as e:
            error_msg = f"Error processing input: {str(e)}"
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'error': error_msg,
                'type': 'error'
            })
            return error_msg
    
    async def _get_help_response(self, user_input: str) -> str:
        """Get contextual help based on user input"""
        try:
            # Get contextual help from suggestion manager
            contextual_help = await chat_suggestion_manager.get_contextual_help(
                current_input=user_input,
                user_context=self.user_context
            )
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input=user_input,
                ai_response=contextual_help,
                context=self.user_context,
                category='help'
            )
            
            return contextual_help
            
        except Exception as e:
            # Fallback to basic help
            return self._get_basic_help_response()
    
    def _get_basic_help_response(self) -> str:
        """Get basic help response"""
        return """Available Commands:

AI Agent Operations:
   • `agents` - Show AI agent status and capabilities
   • `test` - Test all AI agents functionality

File Operations:
   • `upload <file_path>` - Upload Excel file for processing
   • `analyze` - Analyze uploaded Excel file

AI Agent Operations:
   • `validate` - Run AI-powered metadata validation
   • `generate` - Generate PySpark code with AI agents

Workflow Operations:
   • `workflow` - Run complete end-to-end workflow
   • `status` - Show current system status

Learning & Suggestions:
   • `suggestions` - View your suggestion history
   • `export` - Export training data for model training

General:
   • `help` - Show this help message
   • `quit` - Exit the application

Example Usage:
   ```
   agents                    # Check AI agent status
   test                     # Test all AI agents
   upload /path/to/file.xlsx
   analyze
   validate
   generate
   workflow
   suggestions              # View learning history
   export                   # Export training data
   ```

AI Agents Available:
   • Enhanced Orchestrator Agent
   • Enhanced Metadata Validator Agent
   • Enhanced Code Generator Agent
   • Test Generator Agent"""
    
    async def _handle_suggestions_command(self) -> str:
        """Handle suggestions command"""
        try:
            # Get user's suggestion history
            suggestions = await chat_suggestion_manager.get_user_suggestions_history(limit=10)
            
            if not suggestions:
                return "No suggestions found yet. Start chatting to build your suggestion history!"
            
            response = "Your Chat Suggestion History:\n\n"
            
            for i, suggestion in enumerate(suggestions, 1):
                response += f"{i}. **{suggestion.get('category', 'General').title()}**\n"
                response += f"   User: {suggestion.get('user_input', '')[:80]}...\n"
                response += f"   AI: {suggestion.get('ai_response', '')[:80]}...\n"
                response += f"   Feedback: {suggestion.get('feedback_score', 'N/A')}\n"
                response += f"   Time: {suggestion.get('timestamp', '')[:19]}\n\n"
            
            response += "These suggestions help improve the AI's responses over time!"
            
            return response
            
        except Exception as e:
            return f"Error getting suggestions: {str(e)}"
    
    async def _handle_export_command(self) -> str:
        """Handle export command for training data"""
        try:
            # Export training data
            output_path = await chat_suggestion_manager.export_training_data(
                format="json",
                include_embeddings=True
            )
            
            response = f"Training data exported successfully!\n\n"
            response += f"Output file: {output_path}\n"
            response += "This data can be used for:\n"
            response += "• Fine-tuning language models\n"
            response += "• Training custom AI agents\n"
            response += "• Improving response quality\n"
            response += "• Pattern analysis and insights"
            
            return response
            
        except Exception as e:
            return f"Error exporting training data: {str(e)}"
    
    async def _handle_agent_testing(self) -> str:
        """Handle AI agent testing"""
        try:
            print("Testing AI agents...")
            test_results = await agent_manager.test_agents()
            
            response = "AI Agent Testing Results\n\n"
            
            for agent_type, result in test_results.items():
                status = result['status']
                if status == 'success':
                    response += f"[OK] {agent_type}: Test passed\n"
                elif status == 'no_execute_method':
                    response += f"[WARN] {agent_type}: No execute method\n"
                else:
                    response += f"[ERROR] {agent_type}: Test failed - {result.get('error', 'Unknown error')}\n"
            
            response += f"\nOverall Status: {len([r for r in test_results.values() if r['status'] == 'success'])}/{len(test_results)} agents working"
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input="test",
                ai_response=response,
                context={'agent_used': 'test', 'test_results': test_results},
                category='ai_agents'
            )
            
            return response
            
        except Exception as e:
            return f"Error testing agents: {str(e)}"
    
    async def _handle_file_upload(self, user_input: str) -> str:
        """Handle file upload command"""
        try:
            # Extract file path
            parts = user_input.split()
            if len(parts) < 2:
                return "Please provide a file path: `upload <file_path>`"
            
            file_path = ' '.join(parts[1:])
            file_path = Path(file_path)
            
            if not file_path.exists():
                return f"File not found: {file_path}"
            
            if not file_path.suffix.lower() in ['.xlsx', '.xls']:
                return f"Please provide an Excel file (.xlsx or .xls): {file_path}"
            
            # Store file path
            self.excel_file_path = str(file_path)
            
            # Update user context
            self.user_context['file_path'] = str(file_path)
            self.user_context['file_name'] = file_path.name
            
            # Get file info
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            response = f"""File Uploaded Successfully!

File Details:
   • Name: {file_path.name}
   • Path: {file_path}
   • Size: {file_size_mb:.2f} MB
   • Type: Excel file

Next Steps:
   • Use `analyze` to examine the file
   • Use `validate` to run metadata validation
   • Use `generate` to create PySpark code
   • Use `workflow` to run complete pipeline

Ready for AI agent processing!"""
            
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'system': 'File uploaded',
                'file_path': str(file_path),
                'file_size_mb': file_size_mb,
                'type': 'file_upload'
            })
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input=user_input,
                ai_response=response,
                context=self.user_context,
                category='file_operations'
            )
            
            return response
            
        except Exception as e:
            return f"Error uploading file: {str(e)}"
    
    async def _handle_analyze(self) -> str:
        """Handle file analysis"""
        if not self.excel_file_path:
            return "No file uploaded. Please use `upload <file_path>` first."
        
        try:
            # Read Excel file
            df = pd.read_excel(self.excel_file_path, sheet_name='datahub standard mapping')
            
            # Basic analysis
            total_rows = len(df)
            total_columns = len(df.columns)
            
            # Get unique tables
            if 'physical_table' in df.columns:
                tables = df['physical_table'].unique()
                table_count = len(tables)
            else:
                tables = ['Unknown']
                table_count = 1
            
            response = f"""File Analysis Complete!

Excel File Analysis:
   • Total Rows: {total_rows}
   • Total Columns: {total_columns}
   • Tables Found: {table_count}
   • Table Names: {', '.join(tables)}

Columns Detected:
   {', '.join(df.columns.tolist())}

Ready for AI agent processing!
   • Use `validate` for metadata validation
   • Use `generate` for code generation
   • Use `workflow` for complete pipeline"""
            
            # Update user context
            self.user_context['analysis_results'] = {
                'total_rows': total_rows,
                'total_columns': total_columns,
                'tables': tables.tolist() if hasattr(tables, 'tolist') else tables,
                'columns': df.columns.tolist()
            }
            
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'system': 'File analyzed',
                'analysis': self.user_context['analysis_results'],
                'type': 'file_analysis'
            })
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input="analyze",
                ai_response=response,
                context=self.user_context,
                category='file_operations'
            )
            
            return response
            
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
    
    async def _handle_validation(self) -> str:
        """Handle metadata validation using AI agents"""
        if not self.excel_file_path:
            return "No file uploaded. Please use `upload <file_path>` first."
        
        try:
            # Get the metadata validator agent
            validator_agent = agent_manager.get_agent('metadata_validator')
            
            if not validator_agent:
                return "Metadata validator agent not available. Use `agents` to check agent status."
            
            # Create validation task
            validation_task = {
                'task_id': f'validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'task_type': 'metadata_validation',
                'input_data': {
                    'excel_file_path': self.excel_file_path,
                    'validation_rules': [
                        'field_count_validation',
                        'mapping_type_validation', 
                        'data_type_validation',
                        'complexity_analysis'
                    ]
                },
                'status': 'pending'
            }
            
            response = """AI-Powered Metadata Validation Started!

AI Agents Working:
   • Enhanced Metadata Validator Agent: Analyzing field mappings
   • Enhanced Orchestrator Agent: Coordinating validation process
   • AI Intelligence: Understanding data patterns and relationships

Validation Process:
   • Field mapping analysis
   • Data type validation
   • Business rule validation
   • Complexity scoring
   • Quality assessment

Please wait while AI agents process your data...
   (This would normally take a few minutes for large files)"""
            
            # Update user context
            self.user_context['agent_used'] = 'metadata_validator'
            self.user_context['current_task'] = 'validation'
            
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'system': 'Validation started',
                'agent_used': 'metadata_validator',
                'type': 'validation_started'
            })
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input="validate",
                ai_response=response,
                context=self.user_context,
                category='validation'
            )
            
            return response
            
        except Exception as e:
            return f"Error starting validation: {str(e)}"
    
    async def _handle_code_generation(self) -> str:
        """Handle code generation using AI agents"""
        if not self.excel_file_path:
            return "No file uploaded. Please use `upload <file_path>` first."
        
        try:
            # Get the code generator agent
            code_agent = agent_manager.get_agent('code_generator')
            
            if not code_agent:
                return "Code generator agent not available. Use `agents` to check agent status."
            
            response = """AI-Powered Code Generation Started!

AI Agents Working:
   • Enhanced Code Generator Agent: Creating PySpark transformations
   • Enhanced Orchestrator Agent: Coordinating generation process
   • AI Intelligence: Optimizing code for performance and scalability

Code Generation Process:
   • PySpark transformation code
   • Error handling and logging
   • Performance optimization
   • Best practices integration
   • Documentation and comments

Please wait while AI agents generate your code...
   (This would normally take a few minutes for complex mappings)"""
            
            # Update user context
            self.user_context['agent_used'] = 'code_generator'
            self.user_context['current_task'] = 'code_generation'
            
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'system': 'Code generation started',
                'agent_used': 'code_generator',
                'type': 'code_generation_started'
            })
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input="generate",
                ai_response=response,
                context=self.user_context,
                category='code_generation'
            )
            
            return response
            
        except Exception as e:
            return f"Error starting code generation: {str(e)}"
    
    async def _handle_complete_workflow(self) -> str:
        """Handle complete workflow execution using AI agents"""
        if not self.excel_file_path:
            return "No file uploaded. Please use `upload <file_path>` first."
        
        try:
            # Get the orchestrator agent
            orchestrator_agent = agent_manager.get_agent('orchestrator')
            
            if not orchestrator_agent:
                return "Orchestrator agent not available. Use `agents` to check agent status."
            
            response = """Complete AI Agentic Workflow Started!

AI Agents Orchestrating Complete Pipeline:

1. Excel Processing Agent
   • Reading and parsing your file
   • Chunked processing for large datasets
   • Intelligent field mapping detection

2. Metadata Validation Agent
   • AI-powered field analysis
   • Business rule validation
   • Quality scoring and recommendations

3. Code Generation Agent
   • PySpark transformation code
   • Performance optimization
   • Production-ready implementations

4. Orchestrator Agent
   • Coordinating all agents
   • Workflow management
   • Error handling and recovery

Please wait while AI agents process your complete workflow...
   (This would normally take 5-10 minutes for large files)"""
            
            # Update user context
            self.user_context['agent_used'] = 'orchestrator'
            self.user_context['current_task'] = 'complete_workflow'
            
            # Add to chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'system': 'Complete workflow started',
                'agent_used': 'orchestrator',
                'type': 'workflow_started'
            })
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input="workflow",
                ai_response=response,
                context=self.user_context,
                category='workflow'
            )
            
            return response
            
        except Exception as e:
            return f"Error starting workflow: {str(e)}"
    
    async def _get_general_response(self, user_input: str) -> str:
        """Get intelligent response with suggestions"""
        try:
            # Get smart suggestions based on current input
            suggestions = await chat_suggestion_manager.get_smart_suggestions(
                current_input=user_input,
                user_context=self.user_context,
                top_k=2
            )
            
            response = f"""AI Agent Response:

I understand you said: "{user_input}"

How I can help you:

• Check AI agents with `agents` command
• Test AI agents with `test` command
• Upload Excel files for AI processing
• Run metadata validation with AI agents
• Generate PySpark code using AI intelligence
• Execute complete workflows with AI orchestration

Try these commands:
   • `help` - See all available commands
   • `agents` - Check AI agent status
   • `upload <file_path>` - Upload your Excel file
   • `analyze` - Analyze your data
   • `workflow` - Run complete AI pipeline
   • `suggestions` - View your learning history
   • `export` - Export training data

I'm ready to help you with your data mapping needs!"""
            
            # Add contextual suggestions if available
            if suggestions:
                response += "\n\nBased on similar interactions, you might also want to try:\n"
                for i, suggestion in enumerate(suggestions, 1):
                    response += f"{i}. {suggestion.get('ai_response', '')[:80]}...\n"
            
            # Add to chat suggestions for learning
            await chat_suggestion_manager.add_chat_interaction(
                user_input=user_input,
                ai_response=response,
                context=self.user_context,
                category='general'
            )
            
            return response
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _get_status_response(self) -> str:
        """Get current system status"""
        # Get agent status
        agent_status = agent_manager.get_agent_status()
        
        status = f"""Current System Status:

Session Info:
   • Chat Messages: {len(self.chat_history)}
   • Session Duration: {self._get_session_duration()}

File Status:
   • Excel File: {'Uploaded' if self.excel_file_path else 'Not uploaded'}
   • File Path: {self.excel_file_path or 'None'}

AI Agent Status:
   • Agent Source: {agent_status['agents_source']}
   • Total Agents: {agent_status['total_agents']}
   • Available Agents: {', '.join(agent_status['available_agent_types'])}

Learning & Suggestions:
   • FAISS Similarity Engine: Active
   • Chat Suggestion Manager: Active
   • Training Data Collection: Enabled

Output Directories:
   • Excel Parsed: Ready
   • Validation Reports: Ready
   • Test Cases: Ready
   • Generated Code: Ready
   • Workflow Logs: Ready
   • Final Reports: Ready

Ready for AI agent processing and learning!"""
        
        return status
    
    def _get_session_duration(self) -> str:
        """Get session duration"""
        if not self.chat_history:
            return "0 minutes"
        
        start_time = datetime.fromisoformat(self.chat_history[0]['timestamp'])
        current_time = datetime.now()
        duration = current_time - start_time
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    async def run_chat_interface(self):
        """Run the interactive chat interface"""
        print("\nChat Interface Active - Type your messages below:")
        print("Type 'help' for available commands")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Process input
                response = await self.process_chat_input(user_input)
                
                # Display response
                print(f"\nAI: {response}")
                
                # Check for quit
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\nChat session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
        
        # Save chat history
        self._save_chat_history()
    
    def _save_chat_history(self):
        """Save chat history to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            history_file = self.output_dir / "workflow_logs" / f"chat_history_{timestamp}.json"
            
            with open(history_file, 'w') as f:
                json.dump(self.chat_history, f, indent=2, default=str)
            
            print(f"\nChat history saved to: {history_file}")
            
        except Exception as e:
            print(f"\nError saving chat history: {str(e)}")

async def main():
    """Main entry point"""
    print("Starting Chat-Based Agentic AI Demo...")
    
    # Create and run the demo
    demo = ChatBasedAgenticDemo()
    await demo.run_chat_interface()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nDemo failed: {str(e)}")
