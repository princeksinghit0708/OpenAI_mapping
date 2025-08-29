"""
Enhanced Orchestrator v2 - Production Ready with LangChain + LiteLLM
Coordinates multi-agent workflows with advanced AI capabilities
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum

from ..core.enhanced_base_agent import EnhancedBaseAgent, EnhancedAgentConfig
from .enhanced_metadata_validator_v2 import create_enhanced_metadata_validator
from .enhanced_code_generator_v2 import create_enhanced_code_generator
from ...core.models import (
    AgentType, AgentTask, TaskStatus, WorkflowDefinition,
    CodeGenerationRequest, ValidationResult, SchemaDefinition, MappingRule, FieldDefinition, DataType
)


class WorkflowType(str, Enum):
    """Types of workflows"""
    DOCUMENT_PROCESSING = "document_processing"
    CODE_GENERATION = "code_generation"
    FULL_MAPPING_PIPELINE = "full_mapping_pipeline"
    VALIDATION_ONLY = "validation_only"


class EnhancedOrchestrator(EnhancedBaseAgent):
    """
    Production-ready orchestrator with advanced AI capabilities
    
    Features:
    - Intelligent workflow planning
    - Multi-agent coordination with LangChain + LiteLLM
    - Advanced error recovery
    - Performance optimization
    - Resource management
    """
    
    def __init__(self, config: EnhancedAgentConfig, rag_engine=None, tools=None):
        # Ensure this is configured as an orchestrator
        config.agent_type = "orchestrator"
        
        super().__init__(config, rag_engine, tools)
        
        # Orchestrator-specific state
        self.agents: Dict[AgentType, EnhancedBaseAgent] = {}
        self.active_workflows: Dict[str, WorkflowDefinition] = {}
        self.task_results: Dict[str, Any] = {}
        self.workflow_stats = {
            "total_workflows": 0,
            "successful_workflows": 0,
            "average_execution_time": 0.0,
            "workflow_types": {}
        }
        
        # Initialize specialized agents
        asyncio.create_task(self._initialize_enhanced_agents())
        
        self.logger.info("Enhanced Orchestrator initialized")
    
    async def _initialize_enhanced_agents(self):
        """Initialize enhanced specialized agents"""
        try:
            # Create enhanced metadata validator
            self.agents[AgentType.METADATA_VALIDATOR] = create_enhanced_metadata_validator(
                enable_multi_provider=self.config.enable_multi_provider,
                rag_engine=self.rag_engine
            )
            
            # Create enhanced code generator
            self.agents[AgentType.CODE_GENERATOR] = create_enhanced_code_generator(
                enable_multi_provider=self.config.enable_multi_provider,
                rag_engine=self.rag_engine
            )
            
            self.logger.info(f"Enhanced orchestrator initialized with {len(self.agents)} agents")
            
        except Exception as e:
            self.logger.error("Failed to initialize enhanced agents", error=str(e))
    
    def _get_system_prompt(self) -> str:
        return """
        You are an Enhanced Orchestrator Agent responsible for coordinating complex multi-agent workflows.
        
        Your advanced responsibilities:
        1. **Intelligent Workflow Planning**: Create optimal execution plans for complex tasks
        2. **Multi-Agent Coordination**: Manage specialized AI agents with LangChain + LiteLLM
        3. **Advanced Error Recovery**: Handle failures gracefully with intelligent retries
        4. **Performance Optimization**: Optimize resource usage and execution time
        5. **Quality Assurance**: Ensure high-quality outputs through validation and review
        
        Enhanced capabilities:
        - Context-aware task scheduling and dependency management
        - AI-powered workflow optimization and adaptation
        - Real-time performance monitoring and adjustment
        - Intelligent resource allocation across agents
        - Advanced error prediction and prevention
        - Learning from workflow patterns for continuous improvement
        
        Specialized agents you coordinate:
        - **Enhanced Metadata Validator**: Advanced document validation with multi-strategy extraction
        - **Enhanced Code Generator**: Production-ready code generation with optimization
        
        Workflow management principles:
        - Always validate inputs before starting workflows
        - Create optimal execution plans considering dependencies and resources
        - Monitor progress in real-time and adapt as needed
        - Handle errors gracefully with context-aware recovery
        - Provide comprehensive status updates and progress tracking
        - Learn from each workflow to improve future performance
        
        Focus on reliability, efficiency, and continuous improvement.
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.ORCHESTRATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """Enhanced orchestration logic"""
        try:
            workflow_type = WorkflowType(input_data.get("workflow_type", "document_processing"))
            workflow_data = input_data.get("workflow_data", {})
            workflow_id = input_data.get("workflow_id", f"workflow_{datetime.utcnow().timestamp()}")
            
            self.logger.info("Starting enhanced workflow", 
                           workflow_id=workflow_id,
                           workflow_type=workflow_type.value)
            
            # Create intelligent execution plan
            execution_plan = await self._create_intelligent_execution_plan(
                workflow_type, workflow_data, context
            )
            
            # Execute workflow based on plan
            if workflow_type == WorkflowType.DOCUMENT_PROCESSING:
                result = await self._execute_document_processing_enhanced(
                    workflow_id, workflow_data, context, execution_plan
                )
            elif workflow_type == WorkflowType.CODE_GENERATION:
                result = await self._execute_code_generation_enhanced(
                    workflow_id, workflow_data, context, execution_plan
                )
            elif workflow_type == WorkflowType.FULL_MAPPING_PIPELINE:
                result = await self._execute_full_pipeline_enhanced(
                    workflow_id, workflow_data, context, execution_plan
                )
            elif workflow_type == WorkflowType.VALIDATION_ONLY:
                result = await self._execute_validation_enhanced(
                    workflow_id, workflow_data, context, execution_plan
                )
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            # Update statistics
            self.workflow_stats["total_workflows"] += 1
            if result.get("success"):
                self.workflow_stats["successful_workflows"] += 1
            
            self.workflow_stats["workflow_types"][workflow_type.value] = \
                self.workflow_stats["workflow_types"].get(workflow_type.value, 0) + 1
            
            self.logger.info("Enhanced workflow completed", 
                           workflow_id=workflow_id,
                           success=result.get("success"))
            
            return result
            
        except Exception as e:
            self.logger.error("Enhanced workflow execution failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "workflow_id": input_data.get("workflow_id"),
                "timestamp": datetime.utcnow().isoformat(),
                "orchestrator_enhancement": "error_occurred"
            }
    
    async def _create_intelligent_execution_plan(
        self, 
        workflow_type: WorkflowType, 
        workflow_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Create intelligent execution plan using AI"""
        
        try:
            planning_prompt = f"""
            Create an optimal execution plan for this workflow:
            
            Type: {workflow_type.value}
            Data: {json.dumps(workflow_data, indent=2)[:500]}
            Context: {context[:300]}
            
            Consider:
            1. Task dependencies and optimal ordering
            2. Resource requirements and allocation
            3. Potential bottlenecks and mitigation
            4. Error scenarios and recovery strategies
            5. Performance optimization opportunities
            
            Return a JSON execution plan with steps, dependencies, and optimizations.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a workflow planning expert. Create optimal execution plans."
                },
                {
                    "role": "user",
                    "content": planning_prompt
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=800)
            
            try:
                plan = json.loads(response["content"])
                self.logger.info("AI execution plan created", plan_steps=len(plan.get("steps", [])))
                return plan
            except json.JSONDecodeError:
                # Fallback to basic plan
                return self._create_basic_execution_plan(workflow_type)
                
        except Exception as e:
            self.logger.warning("AI planning failed, using basic plan", error=str(e))
            return self._create_basic_execution_plan(workflow_type)
    
    def _create_basic_execution_plan(self, workflow_type: WorkflowType) -> Dict[str, Any]:
        """Create basic execution plan"""
        if workflow_type == WorkflowType.DOCUMENT_PROCESSING:
            return {
                "steps": ["validate_document", "extract_fields", "analyze_structure"],
                "dependencies": {},
                "optimizations": ["parallel_validation"]
            }
        elif workflow_type == WorkflowType.CODE_GENERATION:
            return {
                "steps": ["analyze_schemas", "generate_code", "optimize_code", "generate_tests"],
                "dependencies": {"generate_code": ["analyze_schemas"]},
                "optimizations": ["cache_analysis", "parallel_generation"]
            }
        else:
            return {
                "steps": ["sequential_execution"],
                "dependencies": {},
                "optimizations": []
            }
    
    async def _execute_document_processing_enhanced(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str,
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute enhanced document processing workflow"""
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Enhanced Document Processing",
            description="Advanced document processing with AI validation",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Enhanced validation task
            validation_task = AgentTask(
                agent_type=AgentType.METADATA_VALIDATOR,
                input_data={
                    "document": workflow_data.get("document"),
                    "validation_rules": workflow_data.get("validation_rules", [])
                }
            )
            
            workflow.tasks.append(validation_task)
            
            # Execute with enhanced metadata validator
            if AgentType.METADATA_VALIDATOR in self.agents:
                validation_result = await self.agents[AgentType.METADATA_VALIDATOR].execute_task(
                    validation_task
                )
                self.task_results[validation_task.id] = validation_result
            else:
                raise Exception("Enhanced Metadata Validator not available")
            
            # Check validation success
            if validation_result.status != TaskStatus.COMPLETED:
                return {
                    "success": False,
                    "error": "Enhanced metadata validation failed",
                    "validation_result": validation_result.dict(),
                    "workflow_id": workflow_id,
                    "orchestrator_enhancement": "validation_failed"
                }
            
            # Extract enhanced results
            validation_data = validation_result.output_data
            extracted_fields = validation_data.get("extracted_fields", [])
            database_name = validation_data.get("database_name")
            extraction_method = validation_data.get("extraction_method")
            confidence_scores = validation_data.get("confidence_scores", {})
            
            self.active_workflows[workflow_id] = workflow
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "workflow_type": "enhanced_document_processing",
                "validation_result": validation_data.get("validation_result"),
                "extracted_fields": extracted_fields,
                "database_name": database_name,
                "extraction_method": extraction_method,
                "confidence_scores": confidence_scores,
                "field_count": len(extracted_fields),
                "orchestrator_enhancement": "enhanced_extraction",
                "ai_insights": validation_data.get("ai_insights", ""),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error("Enhanced document processing failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id,
                "orchestrator_enhancement": "error_recovery"
            }
    
    async def _execute_code_generation_enhanced(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str,
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute enhanced code generation workflow"""
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Enhanced Code Generation",
            description="Advanced code generation with AI optimization",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Parse enhanced code generation request
            request_data = workflow_data.get("code_request", {})
            
            # Enhanced code generation task
            code_gen_task = AgentTask(
                agent_type=AgentType.CODE_GENERATOR,
                input_data=request_data
            )
            
            workflow.tasks.append(code_gen_task)
            
            # Execute with enhanced code generator
            if AgentType.CODE_GENERATOR in self.agents:
                code_result = await self.agents[AgentType.CODE_GENERATOR].execute_task(
                    code_gen_task
                )
                self.task_results[code_gen_task.id] = code_result
            else:
                raise Exception("Enhanced Code Generator not available")
            
            if code_result.status != TaskStatus.COMPLETED:
                return {
                    "success": False,
                    "error": "Enhanced code generation failed",
                    "task_result": code_result.dict(),
                    "workflow_id": workflow_id,
                    "orchestrator_enhancement": "code_generation_failed"
                }
            
            self.active_workflows[workflow_id] = workflow
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "workflow_type": "enhanced_code_generation",
                "generated_code": code_result.output_data.get("generated_code"),
                "request": code_result.output_data.get("request"),
                "generation_stats": code_result.output_data.get("generation_stats", {}),
                "orchestrator_enhancement": "ai_optimized_code",
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error("Enhanced code generation failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id,
                "orchestrator_enhancement": "error_recovery"
            }
    
    async def _execute_full_pipeline_enhanced(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str,
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute enhanced full mapping pipeline"""
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Enhanced Full Mapping Pipeline",
            description="Complete enhanced document processing and code generation pipeline",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Step 1: Enhanced Document Processing
            self.logger.info("Pipeline Step 1: Enhanced document processing")
            doc_processing_result = await self._execute_document_processing_enhanced(
                f"{workflow_id}_doc_processing",
                {"document": workflow_data.get("document")},
                context,
                execution_plan
            )
            
            if not doc_processing_result.get("success"):
                return doc_processing_result
            
            # Extract enhanced schema from document processing
            extracted_fields = doc_processing_result.get("extracted_fields", [])
            database_name = doc_processing_result.get("database_name")
            extraction_method = doc_processing_result.get("extraction_method")
            
            # Step 2: Build enhanced schemas for code generation
            self.logger.info("Pipeline Step 2: Building enhanced schemas")
            source_schema = await self._build_enhanced_schema_from_fields(
                extracted_fields, 
                f"{database_name}_source" if database_name else "source_schema"
            )
            
            target_schema = workflow_data.get("target_schema")
            if not target_schema:
                target_schema = await self._generate_intelligent_target_schema(source_schema, context)
            
            mapping_rules = workflow_data.get("mapping_rules", [])
            if not mapping_rules:
                mapping_rules = await self._generate_intelligent_mapping_rules(source_schema, target_schema, context)
            
            # Step 3: Enhanced Code Generation
            self.logger.info("Pipeline Step 3: Enhanced code generation")
            code_gen_request = CodeGenerationRequest(
                source_schema=source_schema,
                target_schema=target_schema,
                mapping_rules=mapping_rules,
                code_type=workflow_data.get("code_type", "pyspark"),
                optimization_level=workflow_data.get("optimization_level", "standard"),
                include_tests=workflow_data.get("include_tests", True)
            )
            
            code_generation_result = await self._execute_code_generation_enhanced(
                f"{workflow_id}_code_generation",
                {"code_request": code_gen_request.dict()},
                context,
                execution_plan
            )
            
            if not code_generation_result.get("success"):
                return code_generation_result
            
            # Combine enhanced results
            return {
                "success": True,
                "workflow_id": workflow_id,
                "pipeline_type": "enhanced_full_mapping",
                "document_processing": doc_processing_result,
                "code_generation": code_generation_result,
                "database_name": database_name,
                "extraction_method": extraction_method,
                "field_count": len(extracted_fields),
                "orchestrator_enhancement": "full_ai_pipeline",
                "pipeline_stats": {
                    "total_steps": 3,
                    "ai_enhancements_used": ["metadata_validation", "code_generation", "schema_mapping"],
                    "confidence_scores": doc_processing_result.get("confidence_scores", {})
                },
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error("Enhanced full pipeline failed", error=str(e))
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id,
                "orchestrator_enhancement": "pipeline_error_recovery"
            }
    
    async def _execute_validation_enhanced(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str,
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute enhanced validation workflow"""
        return await self._execute_document_processing_enhanced(
            workflow_id, workflow_data, context, execution_plan
        )
    
    async def _build_enhanced_schema_from_fields(
        self, 
        fields: List[Dict], 
        schema_name: str
    ) -> SchemaDefinition:
        """Build enhanced SchemaDefinition from extracted fields"""
        
        field_definitions = []
        
        for field_data in fields:
            try:
                field_def = FieldDefinition(
                    name=field_data.get("name", "unknown"),
                    data_type=DataType(field_data.get("data_type", "string")),
                    is_nullable=field_data.get("is_nullable", True),
                    description=field_data.get("description"),
                    provided_key=field_data.get("provided_key"),
                    physical_name=field_data.get("physical_name"),
                    format=field_data.get("format"),
                    constraints=field_data.get("constraints", {})
                )
                field_definitions.append(field_def)
            except Exception as e:
                self.logger.warning("Failed to create enhanced field definition", error=str(e))
        
        return SchemaDefinition(
            name=schema_name,
            fields=field_definitions,
            metadata={
                "generated_by": "enhanced_orchestrator",
                "timestamp": datetime.utcnow().isoformat(),
                "enhancement_level": "ai_assisted"
            }
        )
    
    async def _generate_intelligent_target_schema(
        self, 
        source_schema: SchemaDefinition,
        context: str
    ) -> SchemaDefinition:
        """Generate intelligent target schema using AI"""
        
        try:
            schema_prompt = f"""
            Generate an optimized target schema based on this source schema:
            
            Source Schema: {source_schema.name}
            Fields: {len(source_schema.fields)} fields
            
            Sample fields:
            {json.dumps([field.dict() for field in source_schema.fields[:5]], indent=2)}
            
            Context: {context[:300]}
            
            Create an improved target schema with:
            1. Optimized field names and types
            2. Better organization and structure
            3. Added indexes and constraints where appropriate
            4. Performance considerations
            
            Return the schema structure as JSON.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a database schema design expert."
                },
                {
                    "role": "user",
                    "content": schema_prompt
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=1000)
            
            # For now, return optimized version of source schema
            # In full implementation, would parse AI response
            return SchemaDefinition(
                name=f"{source_schema.name}_optimized",
                fields=source_schema.fields,
                metadata={
                    "generated": True,
                    "ai_optimized": True,
                    "source": source_schema.name
                }
            )
            
        except Exception as e:
            self.logger.warning("AI target schema generation failed", error=str(e))
            # Fallback to basic target schema
            return SchemaDefinition(
                name=f"{source_schema.name}_target",
                fields=source_schema.fields,
                metadata={"generated": True, "fallback": True}
            )
    
    async def _generate_intelligent_mapping_rules(
        self, 
        source_schema: SchemaDefinition, 
        target_schema: SchemaDefinition,
        context: str
    ) -> List[MappingRule]:
        """Generate intelligent mapping rules using AI"""
        
        try:
            mapping_prompt = f"""
            Generate intelligent mapping rules between these schemas:
            
            Source: {source_schema.name} ({len(source_schema.fields)} fields)
            Target: {target_schema.name} ({len(target_schema.fields)} fields)
            
            Context: {context[:300]}
            
            Create mapping rules that:
            1. Map semantically similar fields
            2. Handle data type conversions
            3. Include necessary transformations
            4. Consider data quality and validation
            
            Return mapping rules as JSON array.
            """
            
            messages = [
                {
                    "role": "system",
                    "content": "You are a data mapping expert."
                },
                {
                    "role": "user",
                    "content": mapping_prompt
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=800)
            
            # For now, create basic field-to-field mapping
            # In full implementation, would parse AI response
            mapping_rules = []
            
            for source_field in source_schema.fields:
                for target_field in target_schema.fields:
                    if (source_field.name == target_field.name or 
                        source_field.physical_name == target_field.physical_name):
                        mapping_rules.append(MappingRule(
                            source_field=source_field.name,
                            target_field=target_field.name,
                            description=f"AI-generated mapping from {source_field.name} to {target_field.name}"
                        ))
                        break
            
            return mapping_rules
            
        except Exception as e:
            self.logger.warning("AI mapping rules generation failed", error=str(e))
            # Fallback to basic mapping
            return []
    
    async def get_enhanced_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get enhanced status of a specific workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            
            # Collect enhanced task statuses
            task_statuses = []
            for task in workflow.tasks:
                if task.id in self.task_results:
                    result = self.task_results[task.id]
                    task_statuses.append({
                        "task_id": task.id,
                        "agent_type": task.agent_type.value,
                        "status": result.status.value,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": result.updated_at.isoformat() if result.updated_at else None,
                        "enhanced_metadata": result.output_data.get("enhanced_metadata", {}) if result.output_data else {}
                    })
            
            return {
                "workflow_id": workflow_id,
                "name": workflow.name,
                "description": workflow.description,
                "enhancement_level": "ai_powered",
                "task_count": len(workflow.tasks),
                "task_statuses": task_statuses,
                "created_at": workflow.created_at.isoformat(),
                "orchestrator_stats": self.workflow_stats.copy()
            }
        else:
            return {"error": f"Workflow {workflow_id} not found"}
    
    async def list_enhanced_workflows(self) -> List[Dict[str, Any]]:
        """List all enhanced workflows"""
        workflows = []
        
        for workflow_id, workflow in self.active_workflows.items():
            status = await self.get_enhanced_workflow_status(workflow_id)
            workflows.append(status)
        
        return workflows


# Factory function for easy creation
def create_enhanced_orchestrator(
    enable_multi_provider: bool = None,
    rag_engine=None,
    **kwargs
) -> EnhancedOrchestrator:
    """Create enhanced orchestrator with smart defaults"""
    
    config = create_enhanced_agent(
        agent_type="orchestrator",
        name="Enhanced Orchestrator v2",
        description="Production-ready orchestrator with LangChain + LiteLLM",
        enable_multi_provider=enable_multi_provider,
        primary_model="claude-3-sonnet",  # Good for planning and coordination
        fallback_models=["gpt-4", "gpt-3.5-turbo"],
        **kwargs
    )
    
    return EnhancedOrchestrator(config, rag_engine)