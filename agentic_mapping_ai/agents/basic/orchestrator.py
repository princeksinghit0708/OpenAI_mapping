"""
Orchestrator Agent - Coordinates multi-agent workflows and task dependencies
"""

import asyncio
import json
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
from enum import Enum

from loguru import logger

from ..core.base_agent import BaseAgent, AgentConfig, AgentFactory
from .metadata_validator import MetadataValidatorAgent
from .code_generator import CodeGeneratorAgent
from ...core.models import (
    AgentType, AgentTask, TaskStatus, WorkflowDefinition,
    CodeGenerationRequest, ValidationResult
)


class WorkflowType(str, Enum):
    """Types of workflows"""
    DOCUMENT_PROCESSING = "document_processing"
    CODE_GENERATION = "code_generation"
    FULL_MAPPING_PIPELINE = "full_mapping_pipeline"
    VALIDATION_ONLY = "validation_only"


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent responsible for coordinating multi-agent workflows
    
    Capabilities:
    - Manage task dependencies and execution order
    - Coordinate between specialized agents
    - Handle error recovery and retries
    - Monitor workflow progress
    - Optimize resource utilization
    - Provide workflow status and reporting
    """
    
    def __init__(self, config: AgentConfig, rag_engine=None, tools=None):
        super().__init__(config, rag_engine, tools)
        
        # Agent registry
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.active_workflows: Dict[str, WorkflowDefinition] = {}
        self.task_results: Dict[str, Any] = {}
        
        # Initialize specialized agents
        asyncio.create_task(self._initialize_agents())
    
    async def _initialize_agents(self):
        """Initialize all specialized agents"""
        try:
            # Agent configurations
            agent_configs = {
                AgentType.METADATA_VALIDATOR: AgentConfig(
                    name="Metadata Validator",
                    description="Validates document metadata and schemas",
                    model="gpt-4",
                    temperature=0.1
                ),
                AgentType.CODE_GENERATOR: AgentConfig(
                    name="Code Generator", 
                    description="Generates PySpark and SQL code",
                    model="gpt-4",
                    temperature=0.2
                )
            }
            
            # Create agents
            for agent_type, config in agent_configs.items():
                try:
                    agent = AgentFactory.create_agent(
                        agent_type=agent_type,
                        config=config,
                        rag_engine=self.rag_engine
                    )
                    self.agents[agent_type] = agent
                    logger.info(f"Initialized {agent_type.value} agent")
                except Exception as e:
                    logger.error(f"Failed to initialize {agent_type.value} agent: {str(e)}")
            
            logger.info(f"Orchestrator initialized with {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        return """
        You are an Orchestrator Agent responsible for coordinating complex multi-agent workflows.
        
        Your responsibilities:
        1. Plan and execute multi-step workflows
        2. Coordinate between specialized agents
        3. Manage task dependencies and execution order
        4. Handle error recovery and retry mechanisms
        5. Monitor workflow progress and performance
        6. Optimize resource utilization
        7. Provide status updates and reporting
        
        Workflow management principles:
        - Always validate inputs before starting workflows
        - Execute tasks in optimal order considering dependencies
        - Handle errors gracefully with appropriate retries
        - Provide clear status updates and progress tracking
        - Optimize for both speed and resource efficiency
        - Maintain detailed logs for debugging and monitoring
        
        You coordinate specialized agents:
        - Metadata Validator: Validates schemas and documents
        - Code Generator: Creates PySpark/SQL transformation code
        - Test Generator: Creates comprehensive test suites
        - Schema Mapper: Handles schema mapping and transformations
        
        Always consider the entire pipeline and optimize for end-to-end success.
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.ORCHESTRATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute orchestration logic
        
        Args:
            input_data: Should contain workflow_type and workflow_data
            context: RAG context for workflow patterns
            
        Returns:
            Workflow execution results
        """
        try:
            workflow_type = WorkflowType(input_data.get("workflow_type", "document_processing"))
            workflow_data = input_data.get("workflow_data", {})
            workflow_id = input_data.get("workflow_id", f"workflow_{datetime.utcnow().timestamp()}")
            
            logger.info(f"Starting workflow {workflow_id} of type {workflow_type.value}")
            
            # Execute workflow based on type
            if workflow_type == WorkflowType.DOCUMENT_PROCESSING:
                result = await self._execute_document_processing_workflow(
                    workflow_id, workflow_data, context
                )
            elif workflow_type == WorkflowType.CODE_GENERATION:
                result = await self._execute_code_generation_workflow(
                    workflow_id, workflow_data, context
                )
            elif workflow_type == WorkflowType.FULL_MAPPING_PIPELINE:
                result = await self._execute_full_mapping_pipeline(
                    workflow_id, workflow_data, context
                )
            elif workflow_type == WorkflowType.VALIDATION_ONLY:
                result = await self._execute_validation_workflow(
                    workflow_id, workflow_data, context
                )
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            logger.info(f"Completed workflow {workflow_id}")
            return result
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "workflow_id": input_data.get("workflow_id"),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _execute_document_processing_workflow(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute document processing workflow"""
        
        # Create workflow definition
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Document Processing Workflow",
            description="Validate and process document metadata",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Task 1: Metadata Validation
            validation_task = AgentTask(
                agent_type=AgentType.METADATA_VALIDATOR,
                input_data={
                    "document": workflow_data.get("document"),
                    "validation_rules": workflow_data.get("validation_rules", [])
                }
            )
            
            workflow.tasks.append(validation_task)
            
            # Execute validation
            if AgentType.METADATA_VALIDATOR in self.agents:
                validation_result = await self.agents[AgentType.METADATA_VALIDATOR].execute_task(
                    validation_task
                )
                self.task_results[validation_task.id] = validation_result
            else:
                raise Exception("Metadata Validator agent not available")
            
            # Check validation success
            if validation_result.status != TaskStatus.COMPLETED:
                return {
                    "success": False,
                    "error": "Metadata validation failed",
                    "validation_result": validation_result.dict(),
                    "workflow_id": workflow_id
                }
            
            # Extract results
            validation_data = validation_result.output_data
            extracted_fields = validation_data.get("extracted_fields", [])
            database_name = validation_data.get("database_name")
            
            self.active_workflows[workflow_id] = workflow
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "validation_result": validation_data.get("validation_result"),
                "extracted_fields": extracted_fields,
                "database_name": database_name,
                "field_count": len(extracted_fields),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Document processing workflow {workflow_id} failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id
            }
    
    async def _execute_code_generation_workflow(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute code generation workflow"""
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Code Generation Workflow", 
            description="Generate transformation code from schemas",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Parse code generation request
            request_data = workflow_data.get("code_request", {})
            code_generation_request = CodeGenerationRequest(**request_data)
            
            # Task 1: Code Generation
            code_gen_task = AgentTask(
                agent_type=AgentType.CODE_GENERATOR,
                input_data=code_generation_request.dict()
            )
            
            workflow.tasks.append(code_gen_task)
            
            # Execute code generation
            if AgentType.CODE_GENERATOR in self.agents:
                code_result = await self.agents[AgentType.CODE_GENERATOR].execute_task(
                    code_gen_task
                )
                self.task_results[code_gen_task.id] = code_result
            else:
                raise Exception("Code Generator agent not available")
            
            if code_result.status != TaskStatus.COMPLETED:
                return {
                    "success": False,
                    "error": "Code generation failed",
                    "task_result": code_result.dict(),
                    "workflow_id": workflow_id
                }
            
            self.active_workflows[workflow_id] = workflow
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "generated_code": code_result.output_data.get("generated_code"),
                "request": code_result.output_data.get("request"),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Code generation workflow {workflow_id} failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id
            }
    
    async def _execute_full_mapping_pipeline(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute full end-to-end mapping pipeline"""
        
        workflow = WorkflowDefinition(
            id=workflow_id,
            name="Full Mapping Pipeline",
            description="Complete document processing and code generation pipeline",
            tasks=[],
            dependencies={}
        )
        
        try:
            # Step 1: Document Processing
            doc_processing_result = await self._execute_document_processing_workflow(
                f"{workflow_id}_doc_processing",
                {"document": workflow_data.get("document")},
                context
            )
            
            if not doc_processing_result.get("success"):
                return doc_processing_result
            
            # Extract schema from document processing
            extracted_fields = doc_processing_result.get("extracted_fields", [])
            database_name = doc_processing_result.get("database_name")
            
            # Step 2: Build schemas for code generation
            source_schema = self._build_schema_from_fields(
                extracted_fields, 
                f"{database_name}_source" if database_name else "source_schema"
            )
            
            target_schema = workflow_data.get("target_schema")
            if not target_schema:
                # Generate a simple target schema if not provided
                target_schema = self._generate_default_target_schema(source_schema)
            
            mapping_rules = workflow_data.get("mapping_rules", [])
            if not mapping_rules:
                # Generate default mapping rules
                mapping_rules = self._generate_default_mapping_rules(source_schema, target_schema)
            
            # Step 3: Code Generation
            code_gen_request = CodeGenerationRequest(
                source_schema=source_schema,
                target_schema=target_schema,
                mapping_rules=mapping_rules,
                code_type=workflow_data.get("code_type", "pyspark"),
                optimization_level=workflow_data.get("optimization_level", "standard"),
                include_tests=workflow_data.get("include_tests", True)
            )
            
            code_generation_result = await self._execute_code_generation_workflow(
                f"{workflow_id}_code_generation",
                {"code_request": code_gen_request.dict()},
                context
            )
            
            if not code_generation_result.get("success"):
                return code_generation_result
            
            # Combine results
            return {
                "success": True,
                "workflow_id": workflow_id,
                "pipeline_type": "full_mapping",
                "document_processing": doc_processing_result,
                "code_generation": code_generation_result,
                "database_name": database_name,
                "field_count": len(extracted_fields),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Full mapping pipeline {workflow_id} failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id
            }
    
    async def _execute_validation_workflow(
        self, 
        workflow_id: str, 
        workflow_data: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """Execute validation-only workflow"""
        return await self._execute_document_processing_workflow(
            workflow_id, workflow_data, context
        )
    
    def _build_schema_from_fields(self, fields: List[Dict], schema_name: str):
        """Build SchemaDefinition from extracted fields"""
        from core.models import SchemaDefinition, FieldDefinition, DataType
        
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
                    format=field_data.get("format")
                )
                field_definitions.append(field_def)
            except Exception as e:
                logger.warning(f"Failed to create field definition: {str(e)}")
        
        return SchemaDefinition(
            name=schema_name,
            fields=field_definitions,
            metadata={"generated_by": "orchestrator", "timestamp": datetime.utcnow().isoformat()}
        )
    
    def _generate_default_target_schema(self, source_schema):
        """Generate a default target schema based on source schema"""
        from core.models import SchemaDefinition
        
        # For now, use the same schema as target
        # In a real implementation, this would involve more sophisticated logic
        return SchemaDefinition(
            name=f"{source_schema.name}_target",
            fields=source_schema.fields,  # Copy fields
            metadata={"generated": True, "source": source_schema.name}
        )
    
    def _generate_default_mapping_rules(self, source_schema, target_schema):
        """Generate default mapping rules"""
        from core.models import MappingRule
        
        mapping_rules = []
        
        # Simple field-to-field mapping
        for source_field in source_schema.fields:
            # Find matching target field (by name or physical name)
            matching_target = None
            for target_field in target_schema.fields:
                if (source_field.name == target_field.name or 
                    source_field.physical_name == target_field.physical_name):
                    matching_target = target_field
                    break
            
            if matching_target:
                mapping_rules.append(MappingRule(
                    source_field=source_field.name,
                    target_field=matching_target.name,
                    description=f"Direct mapping from {source_field.name} to {matching_target.name}"
                ))
        
        return mapping_rules
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get status of a specific workflow"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            
            # Collect task statuses
            task_statuses = []
            for task in workflow.tasks:
                if task.id in self.task_results:
                    result = self.task_results[task.id]
                    task_statuses.append({
                        "task_id": task.id,
                        "agent_type": task.agent_type.value,
                        "status": result.status.value,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": result.updated_at.isoformat() if result.updated_at else None
                    })
            
            return {
                "workflow_id": workflow_id,
                "name": workflow.name,
                "description": workflow.description,
                "task_count": len(workflow.tasks),
                "task_statuses": task_statuses,
                "created_at": workflow.created_at.isoformat()
            }
        else:
            return {"error": f"Workflow {workflow_id} not found"}
    
    async def list_active_workflows(self) -> List[Dict[str, Any]]:
        """List all active workflows"""
        workflows = []
        
        for workflow_id, workflow in self.active_workflows.items():
            status = await self.get_workflow_status(workflow_id)
            workflows.append(status)
        
        return workflows
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a workflow"""
        if workflow_id in self.active_workflows:
            # Mark all tasks as cancelled
            workflow = self.active_workflows[workflow_id]
            for task in workflow.tasks:
                if task.id in self.task_results:
                    self.task_results[task.id].status = TaskStatus.CANCELLED
            
            # Remove from active workflows
            del self.active_workflows[workflow_id]
            logger.info(f"Cancelled workflow {workflow_id}")
            return True
        
        return False


# Register the agent
AgentFactory.register_agent(AgentType.ORCHESTRATOR, OrchestratorAgent)