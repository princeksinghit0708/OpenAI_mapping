"""
Conversational AI Agent for Natural Language Interaction
Processes user queries and provides intelligent responses with context awareness
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel

from .base_agent import BaseAgent, AgentConfig
from agentic_mapping_ai.core.models import (
    AgentTask, AgentType, TaskStatus, ChatMessage, ChatSession
)


class ChatContext(BaseModel):
    """Context for chat conversations"""
    session_id: str
    user_intent: str
    current_task: Optional[str] = None
    uploaded_files: List[str] = []
    workflow_status: str = "idle"
    last_action: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = []


class ChatResponse(BaseModel):
    """Response from chat agent"""
    message: str
    intent: str
    confidence: float
    suggested_actions: List[Dict[str, str]] = []
    context_update: Optional[Dict[str, Any]] = None
    requires_action: bool = False


class ConversationalAgent(BaseAgent):
    """
    AI Agent that processes natural language queries and provides intelligent responses
    with context awareness for data mapping and transformation tasks
    """
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.agent_type = AgentType.CONVERSATIONAL
        self.intent_patterns = self._load_intent_patterns()
        self.context_memory = {}
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this conversational agent"""
        return """You are a conversational AI agent specialized in data mapping and transformation tasks.

Your role is to:
1. Understand user queries about data mapping, validation, and code generation
2. Provide helpful, accurate responses about EBS IM Account DataHub operations
3. Guide users through complex data transformation workflows
4. Assist with Excel file processing and PySpark code generation
5. Help with metadata validation and quality checks

Always be helpful, professional, and focused on data engineering tasks."""
    
    def get_agent_type(self) -> AgentType:
        """Get the agent type"""
        return AgentType.CONVERSATIONAL
        
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent recognition patterns"""
        return {
            "upload": [
                r"\b(upload|load|import|add)\b.*\b(file|excel|xlsx|data)\b",
                r"\b(file|excel|xlsx)\b.*\b(upload|load|import)\b",
                r"i (have|want to|need to) (upload|load|import)",
                r"how (do i|to) (upload|load|import)",
                r"where (do i|to) (upload|load|import)",
            ],
            "generate": [
                r"\b(generate|create|build|make)\b.*\b(code|pyspark|sql|transformation)\b",
                r"\b(code|pyspark|sql)\b.*\b(generate|create|build|make)\b",
                r"i (want|need) (code|pyspark|sql|transformation)",
                r"how (do i|to) (generate|create|build|make).*\b(code|pyspark|sql)\b",
                r"can you (generate|create|build|make).*\b(code|pyspark|sql)\b",
            ],
            "validate": [
                r"\b(validate|check|verify|test)\b.*\b(data|metadata|quality|schema)\b",
                r"\b(data|metadata|quality|schema)\b.*\b(validate|check|verify|test)\b",
                r"i (want|need) to (validate|check|verify|test)",
                r"how (do i|to) (validate|check|verify|test)",
                r"is (my|the) (data|metadata|quality|schema) (valid|correct|good)",
            ],
            "workflow": [
                r"\b(run|start|execute)\b.*\b(workflow|pipeline|process|all)\b",
                r"\b(workflow|pipeline|process)\b.*\b(run|start|execute)\b",
                r"i (want|need) to (run|start|execute) (everything|all|complete|full)",
                r"how (do i|to) (run|start|execute).*\b(workflow|pipeline|process)\b",
                r"can you (run|start|execute).*\b(workflow|pipeline|process)\b",
            ],
            "test": [
                r"\b(test|testing|unit test|test case)\b",
                r"i (want|need) (test|testing|unit test|test case)",
                r"how (do i|to) (test|testing|create test)",
                r"can you (create|generate|make).*\b(test|testing)\b",
            ],
            "help": [
                r"\b(help|how|what|guide|tutorial|explain|show)\b",
                r"i (don't know|need help|am confused|don't understand)",
                r"what (is|are|does|can)",
                r"how (do i|to|does|can)",
                r"where (is|are|do i|to)",
                r"when (do i|to|should i)",
                r"why (do i|should i)",
            ],
            "status": [
                r"\b(status|progress|what happened|result|how did it go)\b",
                r"what (is|are) the (status|progress|result)",
                r"how (is|are) (it|things|everything) (going|doing)",
                r"did (it|everything) (work|finish|complete)",
                r"what (happened|went wrong)",
            ],
            "greeting": [
                r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b",
                r"how are you",
                r"what's up",
                r"nice to meet you",
            ],
            "thanks": [
                r"\b(thank|thanks|appreciate|grateful)\b",
                r"thank you",
                r"thanks for",
                r"i appreciate",
            ],
        }
    
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """
        Detect user intent from natural language message
        Returns intent and confidence score
        """
        message_lower = message.lower().strip()
        
        # Score each intent based on pattern matches
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            
            if score > 0:
                # Normalize score
                intent_scores[intent] = score / len(patterns)
        
        # Return intent with highest score
        if intent_scores:
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return best_intent[0], best_intent[1]
        
        return "general", 0.5
    
    def extract_entities(self, message: str, intent: str) -> Dict[str, Any]:
        """Extract relevant entities from the message based on intent"""
        entities = {}
        message_lower = message.lower()
        
        # File-related entities
        if intent in ["upload", "generate", "validate"]:
            # File extensions
            file_extensions = re.findall(r'\.(xlsx?|csv|json|py|sql)', message_lower)
            if file_extensions:
                entities["file_types"] = file_extensions
            
            # File names
            file_names = re.findall(r'\b[\w\-_]+\.(xlsx?|csv|json|py|sql)\b', message)
            if file_names:
                entities["file_names"] = file_names
        
        # Code types
        if intent == "generate":
            code_types = []
            if re.search(r'\b(pyspark|spark)\b', message_lower):
                code_types.append("pyspark")
            if re.search(r'\bsql\b', message_lower):
                code_types.append("sql")
            if re.search(r'\bpython\b', message_lower):
                code_types.append("python")
            
            if code_types:
                entities["code_types"] = code_types
        
        # Urgency indicators
        urgency_words = ["urgent", "asap", "quickly", "fast", "immediately", "now"]
        if any(word in message_lower for word in urgency_words):
            entities["urgency"] = "high"
        
        return entities
    
    def generate_response(self, message: str, context: ChatContext) -> ChatResponse:
        """Generate intelligent response based on message and context"""
        intent, confidence = self.detect_intent(message)
        entities = self.extract_entities(message, intent)
        
        # Generate appropriate response based on intent
        if intent == "upload":
            return self._handle_upload_intent(message, context, entities, confidence)
        elif intent == "generate":
            return self._handle_generate_intent(message, context, entities, confidence)
        elif intent == "validate":
            return self._handle_validate_intent(message, context, entities, confidence)
        elif intent == "workflow":
            return self._handle_workflow_intent(message, context, entities, confidence)
        elif intent == "test":
            return self._handle_test_intent(message, context, entities, confidence)
        elif intent == "status":
            return self._handle_status_intent(message, context, entities, confidence)
        elif intent == "help":
            return self._handle_help_intent(message, context, entities, confidence)
        elif intent == "greeting":
            return self._handle_greeting_intent(message, context, entities, confidence)
        elif intent == "thanks":
            return self._handle_thanks_intent(message, context, entities, confidence)
        else:
            return self._handle_general_intent(message, context, entities, confidence)
    
    def _handle_upload_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle file upload related queries"""
        if context.uploaded_files:
            response_text = f"I see you already have {len(context.uploaded_files)} file(s) uploaded. " \
                           f"Would you like to upload another file or work with the existing ones?\n\n" \
                           f"Current files: {', '.join(context.uploaded_files)}"
            actions = [
                {"label": "Upload New File", "action": "navigate", "target": "/upload"},
                {"label": "Generate Code", "action": "generate", "target": "pyspark"},
                {"label": "Run Workflow", "action": "workflow", "target": "full_pipeline"}
            ]
        else:
            response_text = "I'll help you upload your Excel mapping file! Here's what you need to know:\n\n" \
                           "📁 **File Requirements:**\n" \
                           "• Name: `ebs_IM_account_DATAhub_mapping_v8.0.xlsx`\n" \
                           "• Sheets: `datahub standard mapping` and `goldref`\n" \
                           "• Format: Excel (.xlsx)\n\n" \
                           "You can drag and drop your file or use the file browser. " \
                           "I'll automatically validate the structure and guide you through any issues."
            
            actions = [
                {"label": "Go to Upload Page", "action": "navigate", "target": "/upload"},
                {"label": "File Requirements", "action": "help", "target": "file_requirements"},
                {"label": "Setup Guide", "action": "help", "target": "setup_guide"}
            ]
        
        return ChatResponse(
            message=response_text,
            intent="upload",
            confidence=confidence,
            suggested_actions=actions,
            requires_action=True
        )
    
    def _handle_generate_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle code generation queries"""
        if not context.uploaded_files:
            response_text = "I'd love to generate code for you! However, I need an Excel mapping file first.\n\n" \
                           "Once you upload your file, I can create:\n" \
                           "• 🐍 **PySpark transformations** - For big data processing\n" \
                           "• 🗄️ **SQL scripts** - For database transformations\n" \
                           "• 🐍 **Python code** - For data manipulation\n\n" \
                           "All generated code includes error handling, optimization, and comprehensive documentation."
            
            actions = [
                {"label": "Upload File First", "action": "navigate", "target": "/upload"},
                {"label": "See Examples", "action": "help", "target": "code_examples"}
            ]
        else:
            code_types = entities.get("code_types", ["pyspark"])
            primary_type = code_types[0] if code_types else "pyspark"
            
            response_text = f"Perfect! I'll generate {primary_type.upper()} code for your mappings.\n\n" \
                           f"🔧 **What I'll Create:**\n" \
                           f"• Optimized {primary_type} transformations\n" \
                           f"• Error handling and validation\n" \
                           f"• Performance optimizations\n" \
                           f"• Comprehensive documentation\n" \
                           f"• Best practices implementation\n\n" \
                           f"Ready to start generating code?"
            
            actions = [
                {"label": f"Generate {primary_type.capitalize()}", "action": "generate", "target": primary_type},
                {"label": "Full Workflow", "action": "workflow", "target": "full_pipeline"},
                {"label": "Customize Options", "action": "navigate", "target": "/mapping"}
            ]
        
        return ChatResponse(
            message=response_text,
            intent="generate",
            confidence=confidence,
            suggested_actions=actions,
            requires_action=True
        )
    
    def _handle_validate_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle validation queries"""
        response_text = "I'll help you validate your data comprehensively!\n\n" \
                       "🔍 **Validation Types:**\n" \
                       "• **Metadata Validation** - Schema structure, data types, constraints\n" \
                       "• **Data Quality** - Null values, formats, distributions\n" \
                       "• **Business Rules** - Domain-specific validations\n" \
                       "• **Referential Integrity** - Relationships and dependencies\n\n" \
                       "I'll provide detailed reports with issues and recommendations for improvement."
        
        actions = [
            {"label": "Validate Metadata", "action": "validate", "target": "metadata"},
            {"label": "Data Quality Check", "action": "validate", "target": "quality"},
            {"label": "Full Validation", "action": "workflow", "target": "validation_only"},
            {"label": "Validation Guide", "action": "help", "target": "validation_help"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="validate",
            confidence=confidence,
            suggested_actions=actions,
            requires_action=True
        )
    
    def _handle_workflow_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle workflow execution queries"""
        urgency = entities.get("urgency", "normal")
        
        if urgency == "high":
            response_text = "I understand this is urgent! I'll start the complete workflow immediately.\n\n"
        else:
            response_text = "Excellent! I'll run the complete end-to-end workflow for you.\n\n"
        
        response_text += "🔄 **Complete Pipeline:**\n" \
                        "1. 📊 **Metadata Extraction** - Analyze Excel structure\n" \
                        "2. 🔧 **Code Generation** - Create PySpark transformations\n" \
                        "3. 🧪 **Test Creation** - Generate comprehensive test suites\n" \
                        "4. ✅ **Validation** - Quality checks and verification\n\n" \
                        "⏱️ **Estimated Time:** 3-5 minutes\n" \
                        "📁 **Output:** Generated code, tests, and documentation"
        
        actions = [
            {"label": "Start Full Pipeline", "action": "workflow", "target": "full_mapping_pipeline"},
            {"label": "Code Only", "action": "workflow", "target": "code_generation_only"},
            {"label": "Customize Workflow", "action": "navigate", "target": "/agents"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="workflow",
            confidence=confidence,
            suggested_actions=actions,
            requires_action=True
        )
    
    def _handle_test_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle test generation queries"""
        response_text = "I'll create comprehensive test suites for your transformations!\n\n" \
                       "🧪 **Test Types:**\n" \
                       "• **Unit Tests** - Individual transformation validation\n" \
                       "• **Integration Tests** - End-to-end workflow verification\n" \
                       "• **Data Quality Tests** - Assertions and validations\n" \
                       "• **Performance Tests** - Large dataset handling\n" \
                       "• **Mock Data** - Realistic test datasets\n\n" \
                       "All tests are ready-to-run with clear documentation and examples."
        
        actions = [
            {"label": "Generate All Tests", "action": "test", "target": "comprehensive"},
            {"label": "Unit Tests Only", "action": "test", "target": "unit"},
            {"label": "Mock Data Only", "action": "test", "target": "mock_data"},
            {"label": "Test Examples", "action": "help", "target": "test_examples"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="test",
            confidence=confidence,
            suggested_actions=actions,
            requires_action=True
        )
    
    def _handle_status_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle status and progress queries"""
        status_text = f"📊 **Current Status:**\n" \
                     f"• Workflow: {context.workflow_status.title()}\n" \
                     f"• Files: {len(context.uploaded_files)} uploaded\n" \
                     f"• Last Action: {context.last_action or 'None'}\n\n"
        
        if context.workflow_status == "running":
            status_text += "🔄 A workflow is currently running. I'll keep you updated on progress!"
        elif context.workflow_status == "completed":
            status_text += "✅ Last workflow completed successfully! Check the results in the output directory."
        elif context.workflow_status == "failed":
            status_text += "❌ Last workflow encountered an error. Would you like me to help troubleshoot?"
        else:
            status_text += "Ready for your next request! What would you like me to help you with?"
        
        actions = [
            {"label": "View Dashboard", "action": "navigate", "target": "/"},
            {"label": "Check Workflows", "action": "navigate", "target": "/agents"}
        ]
        
        return ChatResponse(
            message=status_text,
            intent="status",
            confidence=confidence,
            suggested_actions=actions
        )
    
    def _handle_help_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle help and guidance queries"""
        response_text = "I'm here to help! 🤝\n\n" \
                       "🎯 **What I Can Do:**\n" \
                       "• 📁 **File Upload & Processing** - Excel mapping files\n" \
                       "• 🔧 **Code Generation** - PySpark, SQL, Python transformations\n" \
                       "• 🧪 **Test Creation** - Comprehensive test suites\n" \
                       "• ✅ **Data Validation** - Quality checks and metadata validation\n" \
                       "• 🔄 **Workflow Management** - End-to-end processing pipelines\n\n" \
                       "💡 **Pro Tips:**\n" \
                       "• Ask me anything in plain English\n" \
                       "• I remember our conversation context\n" \
                       "• I can guide you step-by-step through any process"
        
        actions = [
            {"label": "Getting Started", "action": "help", "target": "getting_started"},
            {"label": "File Requirements", "action": "help", "target": "file_requirements"},
            {"label": "View Examples", "action": "help", "target": "examples"},
            {"label": "Best Practices", "action": "help", "target": "best_practices"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="help",
            confidence=confidence,
            suggested_actions=actions
        )
    
    def _handle_greeting_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle greetings and social interactions"""
        greetings = [
            "Hello! 👋 I'm your AI mapping assistant, ready to help with data transformation tasks!",
            "Hi there! 🤖 Great to see you! What data mapping challenge can I help you solve today?",
            "Hey! 🚀 I'm excited to help you with your mapping and transformation needs!",
        ]
        
        import random
        greeting = random.choice(greetings)
        
        response_text = f"{greeting}\n\n" \
                       "I can help you with:\n" \
                       "• Upload and process Excel mapping files\n" \
                       "• Generate PySpark transformation code\n" \
                       "• Create comprehensive test suites\n" \
                       "• Validate data quality and metadata\n" \
                       "• Run complete automation workflows\n\n" \
                       "What would you like to start with?"
        
        actions = [
            {"label": "Upload File", "action": "navigate", "target": "/upload"},
            {"label": "Generate Code", "action": "help", "target": "generate"},
            {"label": "Run Workflow", "action": "navigate", "target": "/agents"},
            {"label": "Get Help", "action": "help", "target": "help"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="greeting",
            confidence=confidence,
            suggested_actions=actions
        )
    
    def _handle_thanks_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle thanks and appreciation"""
        thanks_responses = [
            "You're very welcome! 😊 I'm here whenever you need help with data mapping!",
            "Happy to help! 🎉 Feel free to ask me anything else about your transformations!",
            "My pleasure! 🚀 Let me know if you need assistance with anything else!",
        ]
        
        import random
        thanks_response = random.choice(thanks_responses)
        
        actions = [
            {"label": "Upload Another File", "action": "navigate", "target": "/upload"},
            {"label": "Run More Workflows", "action": "navigate", "target": "/agents"},
            {"label": "View Dashboard", "action": "navigate", "target": "/"}
        ]
        
        return ChatResponse(
            message=thanks_response,
            intent="thanks",
            confidence=confidence,
            suggested_actions=actions
        )
    
    def _handle_general_intent(self, message: str, context: ChatContext, entities: Dict, confidence: float) -> ChatResponse:
        """Handle general queries that don't fit specific intents"""
        response_text = "I understand you're asking about data mapping and transformation. " \
                       "Let me help you clarify what you need!\n\n" \
                       "🤔 **Common Tasks I Help With:**\n" \
                       "• 📁 Upload Excel mapping files\n" \
                       "• 🔧 Generate transformation code\n" \
                       "• 🧪 Create test suites\n" \
                       "• ✅ Validate data quality\n" \
                       "• 🔄 Run complete workflows\n\n" \
                       "Could you tell me more specifically what you'd like to accomplish?"
        
        actions = [
            {"label": "Upload File", "action": "navigate", "target": "/upload"},
            {"label": "Generate Code", "action": "help", "target": "generate"},
            {"label": "Run Workflow", "action": "navigate", "target": "/agents"},
            {"label": "Get Help", "action": "help", "target": "help"}
        ]
        
        return ChatResponse(
            message=response_text,
            intent="general",
            confidence=confidence,
            suggested_actions=actions
        )
    
    async def process_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a chat message and return response"""
        try:
            # Convert context to ChatContext
            chat_context = ChatContext(
                session_id=context.get("session_id", "default"),
                user_intent=context.get("user_intent", "unknown"),
                current_task=context.get("current_task"),
                uploaded_files=context.get("uploaded_files", []),
                workflow_status=context.get("workflow_status", "idle"),
                last_action=context.get("last_action"),
                conversation_history=context.get("conversation_history", [])
            )
            
            # Generate response
            response = self.generate_response(message, chat_context)
            
            # Update conversation history
            chat_context.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "user_message": message,
                "bot_response": response.message,
                "intent": response.intent,
                "confidence": response.confidence
            })
            
            # Return response with updated context
            return {
                "message": response.message,
                "intent": response.intent,
                "confidence": response.confidence,
                "suggested_actions": response.suggested_actions,
                "requires_action": response.requires_action,
                "context": chat_context.dict()
            }
            
        except Exception as e:
            self.logger.error(f"Error processing chat message: {e}")
            return {
                "message": "I apologize, but I encountered an error processing your message. Please try again or rephrase your question.",
                "intent": "error",
                "confidence": 0.0,
                "suggested_actions": [
                    {"label": "Try Again", "action": "retry"},
                    {"label": "Get Help", "action": "help", "target": "help"}
                ],
                "requires_action": False,
                "context": context
            }
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute the core logic of the conversational agent
        
        Args:
            input_data: Input data containing the message and context
            context: RAG context if available
            
        Returns:
            Chat response data
        """
        try:
            message = input_data.get("message", "")
            chat_context = input_data.get("context", {})
            
            # Process the message
            result = await self.process_message(message, chat_context)
            
            return {
                "success": True,
                "response": result,
                "agent_type": self.get_agent_type().value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent_type": self.get_agent_type().value,
                "timestamp": datetime.now().isoformat()
            }
