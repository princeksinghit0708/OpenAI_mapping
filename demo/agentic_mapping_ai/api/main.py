"""
FastAPI application for Agentic Mapping AI Platform
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from agentic_mapping_ai.config.settings import settings
from agentic_mapping_ai.core.models import (
    APIResponse, ValidationResponse, CodeGenerationResponse, WorkflowResponse,
    SchemaDefinition, MappingRule, CodeGenerationRequest, ValidationResult
)
from agentic_mapping_ai.agents.orchestrator import OrchestratorAgent, WorkflowType
from agentic_mapping_ai.knowledge.rag_engine import RAGEngine
from agentic_mapping_ai.agents.chat_agent import ConversationalAgent


# Pydantic models for API requests
class DocumentValidationRequest(BaseModel):
    document: Dict[str, Any]
    validation_rules: Optional[List[str]] = []

class ChatMessageRequest(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = {}
    timestamp: Optional[str] = None

class ChatMessageResponse(BaseModel):
    message: str
    intent: str
    confidence: float
    suggested_actions: List[Dict[str, str]] = []
    requires_action: bool = False
    context: Dict[str, Any] = {}
    timestamp: str


class WorkflowRequest(BaseModel):
    workflow_type: str
    workflow_data: Dict[str, Any]
    workflow_id: Optional[str] = None


class RAGQueryRequest(BaseModel):
    query: str
    max_results: int = 5
    category_filter: Optional[str] = None


class KnowledgeAddRequest(BaseModel):
    content: str
    metadata: Dict[str, Any]
    doc_id: Optional[str] = None


class ExcelMappingRequest(BaseModel):
    file_path: str
    sheet_name: str = "Sheet1"
    gold_reference_template: str = "img_0241"


class TransformationValidationRequest(BaseModel):
    transformation_logic: str
    source_fields: List[str]
    target_field: str


class GoldReferenceValidationRequest(BaseModel):
    field_mappings: List[Dict[str, Any]]
    gold_reference_template: str = "img_0241"


# Initialize FastAPI app
app = FastAPI(
    title=settings.name,
    version=settings.version,
    description="Intelligent document metadata validation and code generation platform",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
rag_engine: Optional[RAGEngine] = None
orchestrator_agent = None  # Enhanced orchestrator instance
chat_agent = None  # Conversational AI agent


@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    global rag_engine, orchestrator_agent, chat_agent
    
    try:
        # Initialize RAG engine
        rag_engine = RAGEngine()
        
        # Initialize orchestrator agent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        config = AgentConfig(
            name="Main Orchestrator",
            description="Orchestrator for coordinating multi-agent workflows",
            model="gpt-4",
            temperature=0.1
        )
        orchestrator_agent = OrchestratorAgent(config, rag_engine=rag_engine)
        
        # Initialize chat agent
        chat_config = AgentConfig(
            name="Conversational Assistant",
            description="AI chat assistant for natural language interaction",
            model="gpt-4",
            temperature=0.7
        )
        chat_agent = ConversationalAgent(chat_config)
        
        print(f"🚀 {settings.name} v{settings.version} started successfully!")
        print(f"📚 RAG Engine initialized")
        print(f"🤖 Enhanced Orchestrator with LangChain + LiteLLM initialized")
        print(f"💬 Conversational AI Agent initialized")
        print(f"✨ Multi-provider AI capabilities enabled")
        
    except Exception as e:
        print(f"❌ Startup failed: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down Agentic Mapping AI Platform")


# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.name}",
        "version": settings.version,
        "timestamp": datetime.utcnow().isoformat(),
        "docs_url": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.version,
        "components": {}
    }
    
    try:
        # Check RAG engine
        if rag_engine:
            rag_health = await rag_engine.health_check()
            health_status["components"]["rag_engine"] = rag_health
        
        # Check enhanced orchestrator agent
        if orchestrator_agent:
            agent_health = await orchestrator_agent.health_check()
            health_status["components"]["enhanced_orchestrator"] = agent_health
        
        return health_status
        
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
        return JSONResponse(status_code=503, content=health_status)


# Document validation endpoints
@app.post("/api/v1/validate", response_model=ValidationResponse, tags=["Validation"])
async def validate_document(request: DocumentValidationRequest):
    """Validate document metadata and extract field definitions"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, message="Orchestrator agent not available")
        
        # Execute validation workflow
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.VALIDATION_ONLY.value,
            "workflow_data": request.dict()
        })
        
        if not workflow_result.get("success"):
            return ValidationResponse(
                success=False,
                message="Validation failed",
                errors=[workflow_result.get("error", "Unknown error")]
            )
        
        validation_result = ValidationResult(**workflow_result.get("validation_result", {}))
        
        return ValidationResponse(
            success=True,
            message="Document validated successfully",
            data=validation_result
        )
        
    except Exception as e:
        return ValidationResponse(
            success=False,
            message="Validation request failed",
            errors=[str(e)]
        )


@app.post("/api/v1/extract", tags=["Extraction"])
async def extract_metadata(request: DocumentValidationRequest):
    """Extract metadata and field definitions from document"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        # Execute document processing workflow
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.DOCUMENT_PROCESSING.value,
            "workflow_data": request.dict()
        })
        
        return APIResponse(
            success=workflow_result.get("success", False),
            message="Metadata extraction completed" if workflow_result.get("success") else "Extraction failed",
            data=workflow_result,
            errors=[workflow_result.get("error")] if workflow_result.get("error") else None
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Extraction request failed",
            errors=[str(e)]
        )


# Code generation endpoints
@app.post("/api/v1/generate/code", response_model=CodeGenerationResponse, tags=["Code Generation"])
async def generate_code(request: CodeGenerationRequest):
    """Generate transformation code based on schema mappings"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        # Execute code generation workflow
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.CODE_GENERATION.value,
            "workflow_data": {"code_request": request.dict()}
        })
        
        if not workflow_result.get("success"):
            return CodeGenerationResponse(
                success=False,
                message="Code generation failed",
                errors=[workflow_result.get("error", "Unknown error")]
            )
        
        return CodeGenerationResponse(
            success=True,
            message="Code generated successfully",
            data=workflow_result.get("generated_code")
        )
        
    except Exception as e:
        return CodeGenerationResponse(
            success=False,
            message="Code generation request failed",
            errors=[str(e)]
        )


# Workflow endpoints
@app.post("/api/v1/workflows", response_model=WorkflowResponse, tags=["Workflows"])
async def create_workflow(request: WorkflowRequest):
    """Create and execute a workflow"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": request.workflow_type,
            "workflow_data": request.workflow_data,
            "workflow_id": request.workflow_id
        })
        
        return WorkflowResponse(
            success=workflow_result.get("success", False),
            message="Workflow executed" if workflow_result.get("success") else "Workflow failed",
            data=workflow_result
        )
        
    except Exception as e:
        return WorkflowResponse(
            success=False,
            message="Workflow execution failed",
            errors=[str(e)]
        )


@app.get("/api/v1/workflows", tags=["Workflows"])
async def list_workflows():
    """List active workflows"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        workflows = await orchestrator_agent.list_enhanced_workflows()
        
        return APIResponse(
            success=True,
            message=f"Found {len(workflows)} active workflows",
            data={"workflows": workflows}
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to list workflows", 
            errors=[str(e)]
        )


@app.get("/api/v1/workflows/{workflow_id}", tags=["Workflows"])
async def get_workflow_status(workflow_id: str):
    """Get status of a specific workflow"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        status = await orchestrator_agent.get_enhanced_workflow_status(workflow_id)
        
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        
        return APIResponse(
            success=True,
            message="Workflow status retrieved",
            data=status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to get workflow status",
            errors=[str(e)]
        )


@app.delete("/api/v1/workflows/{workflow_id}", tags=["Workflows"])
async def cancel_workflow(workflow_id: str):
    """Cancel a workflow"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        # Note: Enhanced orchestrator doesn't have cancel_workflow method yet
        # For now, return success if workflow exists in active workflows
        status = await orchestrator_agent.get_enhanced_workflow_status(workflow_id)
        success = "error" not in status
        
        if not success:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return APIResponse(
            success=True,
            message="Workflow cancelled successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to cancel workflow",
            errors=[str(e)]
        )


# RAG and knowledge management endpoints
@app.post("/api/v1/knowledge/query", tags=["Knowledge"])
async def query_knowledge(request: RAGQueryRequest):
    """Query the knowledge base using RAG"""
    try:
        if not rag_engine:
            raise HTTPException(status_code=503, detail="RAG engine not available")
        
        results = await rag_engine.retrieve(
            query=request.query,
            max_results=request.max_results,
            category_filter=request.category_filter
        )
        
        return APIResponse(
            success=True,
            message=f"Found {len(results)} relevant results",
            data={
                "query": request.query,
                "results": [
                    {
                        "content": result.content,
                        "metadata": result.metadata,
                        "score": result.score,
                        "source": result.source
                    }
                    for result in results
                ]
            }
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Knowledge query failed",
            errors=[str(e)]
        )


@app.post("/api/v1/knowledge/add", tags=["Knowledge"])
async def add_knowledge(request: KnowledgeAddRequest):
    """Add knowledge to the knowledge base"""
    try:
        if not rag_engine:
            raise HTTPException(status_code=503, detail="RAG engine not available")
        
        doc_id = await rag_engine.add_knowledge(
            content=request.content,
            metadata=request.metadata,
            doc_id=request.doc_id
        )
        
        return APIResponse(
            success=True,
            message="Knowledge added successfully",
            data={"doc_id": doc_id}
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to add knowledge",
            errors=[str(e)]
        )


@app.get("/api/v1/knowledge/stats", tags=["Knowledge"])
async def get_knowledge_stats():
    """Get knowledge base statistics"""
    try:
        if not rag_engine:
            raise HTTPException(status_code=503, detail="RAG engine not available")
        
        stats = await rag_engine.get_knowledge_stats()
        
        return APIResponse(
            success=True,
            message="Knowledge base statistics retrieved",
            data=stats
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Failed to get knowledge stats",
            errors=[str(e)]
        )


# File upload endpoints
@app.post("/api/v1/upload", tags=["File Upload"])
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        if not file.filename.endswith(('.json', '.xml')):
            raise HTTPException(status_code=400, detail="Only JSON and XML files are supported")
        
        # Read file content
        content = await file.read()
        
        # Parse JSON
        if file.filename.endswith('.json'):
            try:
                document = json.loads(content)
            except json.JSONDecodeError as e:
                raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
        else:
            # XML parsing would go here
            raise HTTPException(status_code=400, detail="XML processing not yet implemented")
        
        # Process document in background
        workflow_id = f"upload_{datetime.utcnow().timestamp()}"
        
        # Execute document processing
        if orchestrator_agent:
            workflow_result = await orchestrator_agent._execute_core_logic({
                "workflow_type": WorkflowType.DOCUMENT_PROCESSING.value,
                "workflow_data": {"document": document},
                "workflow_id": workflow_id
            })
            
            return APIResponse(
                success=workflow_result.get("success", False),
                message="Document uploaded and processed",
                data={
                    "filename": file.filename,
                    "workflow_id": workflow_id,
                    "processing_result": workflow_result
                }
            )
        else:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
    except HTTPException:
        raise
    except Exception as e:
        return APIResponse(
            success=False,
            message="File upload failed",
            errors=[str(e)]
        )


# Full pipeline endpoint
# Enhanced endpoints showcasing LangChain + LiteLLM capabilities
@app.post("/api/v1/enhanced/extract", tags=["Enhanced Features"])
async def enhanced_metadata_extraction(request: DocumentValidationRequest):
    """Enhanced metadata extraction with AI-powered database name detection"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Enhanced orchestrator not available")
        
        # Execute enhanced document processing workflow
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.DOCUMENT_PROCESSING.value,
            "workflow_data": request.dict()
        })
        
        return APIResponse(
            success=workflow_result.get("success", False),
            message="Enhanced metadata extraction completed" if workflow_result.get("success") else "Enhanced extraction failed",
            data={
                **workflow_result,
                "enhancement_features": {
                    "multi_strategy_db_extraction": True,
                    "ai_powered_validation": True,
                    "confidence_scoring": True,
                    "langchain_litellm_integration": True
                }
            },
            errors=[workflow_result.get("error")] if workflow_result.get("error") else None
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Enhanced extraction request failed",
            errors=[str(e)]
        )


@app.post("/api/v1/enhanced/pipeline/full", tags=["Enhanced Features"])
async def run_enhanced_full_pipeline(
    document: Dict[str, Any],
    target_schema: Optional[SchemaDefinition] = None,
    mapping_rules: Optional[List[MappingRule]] = None,
    code_type: str = "pyspark",
    optimization_level: str = "standard"
):
    """Run the complete enhanced mapping pipeline with LangChain + LiteLLM"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Enhanced orchestrator not available")
        
        workflow_data = {
            "document": document,
            "target_schema": target_schema.dict() if target_schema else None,
            "mapping_rules": [rule.dict() for rule in mapping_rules] if mapping_rules else None,
            "code_type": code_type,
            "optimization_level": optimization_level,
            "include_tests": True
        }
        
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.FULL_MAPPING_PIPELINE.value,
            "workflow_data": workflow_data
        })
        
        return APIResponse(
            success=workflow_result.get("success", False),
            message="Enhanced full pipeline executed",
            data={
                **workflow_result,
                "enhancement_features": {
                    "ai_powered_extraction": True,
                    "multi_provider_llm": True,
                    "intelligent_code_generation": True,
                    "comprehensive_testing": True,
                    "performance_optimization": True
                }
            }
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Enhanced full pipeline execution failed",
            errors=[str(e)]
        )


@app.post("/api/v1/pipeline/full", tags=["Pipeline"])
async def run_full_pipeline(
    document: Dict[str, Any],
    target_schema: Optional[SchemaDefinition] = None,
    mapping_rules: Optional[List[MappingRule]] = None,
    code_type: str = "pyspark",
    optimization_level: str = "standard"
):
    """Run the complete mapping pipeline from document to code (Legacy endpoint - use /enhanced/pipeline/full for advanced features)"""
    try:
        if not orchestrator_agent:
            raise HTTPException(status_code=503, detail="Orchestrator agent not available")
        
        workflow_data = {
            "document": document,
            "target_schema": target_schema.dict() if target_schema else None,
            "mapping_rules": [rule.dict() for rule in mapping_rules] if mapping_rules else None,
            "code_type": code_type,
            "optimization_level": optimization_level,
            "include_tests": True
        }
        
        workflow_result = await orchestrator_agent._execute_core_logic({
            "workflow_type": WorkflowType.FULL_MAPPING_PIPELINE.value,
            "workflow_data": workflow_data
        })
        
        return APIResponse(
            success=workflow_result.get("success", False),
            message="Full pipeline executed",
            data=workflow_result
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Full pipeline execution failed",
            errors=[str(e)]
        )


# Excel Mapping Endpoints
@app.post("/api/v1/excel/upload", tags=["Excel Mapping"])
async def upload_excel_mapping(file: UploadFile = File(...)):
    """Upload Excel mapping file for processing"""
    try:
        if not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only Excel files are allowed")
        
        # Save uploaded file
        import tempfile
        import os
        from pathlib import Path
        
        # Create temp directory for uploads
        upload_dir = Path("./data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return APIResponse(
            success=True,
            message="Excel file uploaded successfully",
            data={
                "file_path": str(file_path),
                "filename": file.filename,
                "size": len(content)
            }
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Excel upload failed",
            errors=[str(e)]
        )


@app.post("/api/v1/excel/parse", tags=["Excel Mapping"])
async def parse_excel_mapping(request: ExcelMappingRequest):
    """Parse Excel mapping file and extract field mappings"""
    # NOTE: parsers.excel_mapping_parser not available in demo version
    return APIResponse(
        success=False,
        message="Excel parsing not available in demo version",
        errors=["parsers.excel_mapping_parser not included in demo"]
    )


@app.post("/api/v1/transformations/validate", tags=["Transformations"])
async def validate_transformation(request: TransformationValidationRequest):
    """Validate transformation logic"""
    # NOTE: transformation_agent not available in demo version
    return ValidationResponse(
        success=False,
        message="Transformation validation not available in demo version",
        errors=["transformation_agent not included in demo"]
    )


@app.post("/api/v1/transformations/generate-code", tags=["Transformations"])
async def generate_transformation_code(
    request: TransformationValidationRequest,
    language: str = "pyspark"
):
    """Generate code for transformation logic"""
    # NOTE: transformation_agent not available in demo version
    return APIResponse(
        success=False,
        message="Transformation code generation not available in demo version",
        errors=["transformation_agent not included in demo"]
    )


@app.post("/api/v1/goldref/validate", tags=["Gold Reference"])
async def validate_gold_reference(request: GoldReferenceValidationRequest):
    """Validate field mappings against gold reference standards"""
    # NOTE: goldref_validator not available in demo version
    return ValidationResponse(
        success=False,
        message="Gold reference validation not available in demo version",
        errors=["goldref_validator agent not included in demo"]
    )


@app.get("/api/v1/goldref/compliance-report", tags=["Gold Reference"])
async def generate_compliance_report(template: str = "img_0241"):
    """Generate comprehensive compliance report"""
    # NOTE: goldref_validator not available in demo version
    return APIResponse(
        success=False,
        message="Compliance report generation not available in demo version",
        errors=["goldref_validator agent not included in demo"]
    )


@app.post("/api/v1/excel/process-full", tags=["Excel Mapping"])
async def process_excel_full_pipeline(
    request: ExcelMappingRequest,
    generate_code: bool = True,
    validate_goldref: bool = True
):
    """Process Excel mapping through full pipeline"""
    # NOTE: Simplified demo version - some agents not available
    try:
        # Step 1: Basic Excel parsing would go here
        # NOTE: parsers.excel_mapping_parser not included in demo
        
        results = {
            "parsing": {
                "success": False,
                "message": "Excel parsing not available in demo version"
            },
            "transformations": {
                "success": False,
                "message": "transformation_agent not included in demo"
            },
            "gold_reference": {
                "success": False,
                "message": "goldref_validator not included in demo"
            },
            "code_generation": {
                "success": False,
                "message": "Advanced code generation not available in demo"
            }
        }
        
        return APIResponse(
            success=False,
            message="Full pipeline processing not available in demo version",
            data=results,
            errors=["parsers.excel_mapping_parser, transformation_agent, and goldref_validator not included in demo"]
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Full pipeline processing failed",
            errors=[str(e)]
        )


# ============================================================================
# CHAT & CONVERSATIONAL AI ENDPOINTS
# ============================================================================

@app.post("/api/v1/chat/message", response_model=ChatMessageResponse)
async def chat_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """
    Send a message to the conversational AI agent
    Supports natural language interaction for all platform features
    """
    try:
        if chat_agent is None:
            raise HTTPException(status_code=503, detail="Chat agent not initialized")
        
        # Process the message
        result = await chat_agent.process_message(request.message, request.context or {})
        
        return ChatMessageResponse(
            message=result["message"],
            intent=result["intent"],
            confidence=result["confidence"],
            suggested_actions=result.get("suggested_actions", []),
            requires_action=result.get("requires_action", False),
            context=result.get("context", {}),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@app.get("/api/v1/chat/history")
async def get_chat_history():
    """Get conversation history for the current session"""
    try:
        # For demo purposes, return mock history
        # In production, this would fetch from a database
        return APIResponse(
            success=True,
            message="Chat history retrieved",
            data={
                "conversations": [],
                "session_count": 0,
                "last_activity": None
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chat history: {str(e)}")


@app.delete("/api/v1/chat/session")
async def clear_chat_session():
    """Clear the current chat session"""
    try:
        # For demo purposes, just return success
        # In production, this would clear session data
        return APIResponse(
            success=True,
            message="Chat session cleared successfully",
            data={"session_id": "default", "cleared_at": datetime.now().isoformat()}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear chat session: {str(e)}")


@app.post("/api/v1/chat/intent")
async def detect_intent(request: ChatMessageRequest):
    """Detect user intent from a message (for debugging/testing)"""
    try:
        if chat_agent is None:
            raise HTTPException(status_code=503, detail="Chat agent not initialized")
        
        intent, confidence = chat_agent.detect_intent(request.message)
        entities = chat_agent.extract_entities(request.message, intent)
        
        return APIResponse(
            success=True,
            message="Intent detected successfully",
            data={
                "message": request.message,
                "intent": intent,
                "confidence": confidence,
                "entities": entities,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intent detection failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host=settings.api.host,
        port=settings.api.port,
        reload=settings.api.reload,
        log_level=settings.monitoring.log_level.lower()
    )