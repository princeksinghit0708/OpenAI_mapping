"""
Core data models for Agentic Mapping AI Platform
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field as PydanticField
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentType(str, Enum):
    """Types of agents in the system"""
    METADATA_VALIDATOR = "metadata_validator"
    SCHEMA_MAPPER = "schema_mapper"
    CODE_GENERATOR = "code_generator"
    TEST_GENERATOR = "test_generator"
    ORCHESTRATOR = "orchestrator"


class DataType(str, Enum):
    """Data types for schema mapping"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIMESTAMP = "timestamp"
    ARRAY = "array"
    OBJECT = "object"


# Pydantic Models for API

class FieldDefinition(BaseModel):
    """Field definition model"""
    name: str
    data_type: DataType
    is_nullable: bool = True
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None
    provided_key: Optional[str] = None
    physical_name: Optional[str] = None
    format: Optional[str] = None
    logical_name: Optional[str] = None
    physical_table: Optional[str] = None
    source_system: Optional[str] = None
    business_rules: List[str] = []


class SchemaDefinition(BaseModel):
    """Schema definition model"""
    name: str
    fields: List[FieldDefinition]
    schema_metadata: Optional[Dict[str, Any]] = None
    version: str = "1.0"


class MappingRule(BaseModel):
    """Mapping rule between source and target schemas"""
    source_field: str
    target_field: str
    transformation: Optional[str] = None
    validation_rules: Optional[List[str]] = None
    description: Optional[str] = None
    mapping_type: str = "Direct"  # Direct, Derived, Goldref, No Mapping
    transformation_category: Optional[str] = None  # lookup, conditional, calculation, etc.
    dependency_fields: List[str] = []  # Fields this transformation depends on
    gold_reference_key: Optional[str] = None  # For Goldref mappings


class ValidationResult(BaseModel):
    """Validation result model"""
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []
    validation_metadata: Optional[Dict[str, Any]] = None


class CodeGenerationRequest(BaseModel):
    """Code generation request model"""
    source_schema: SchemaDefinition
    target_schema: SchemaDefinition
    mapping_rules: List[MappingRule]
    code_type: str = "pyspark"  # pyspark, sql, python
    optimization_level: str = "standard"  # basic, standard, advanced
    include_tests: bool = True


class GeneratedCode(BaseModel):
    """Generated code model"""
    code: str
    language: str
    test_code: Optional[str] = None
    documentation: Optional[str] = None
    dependencies: List[str] = []
    performance_notes: Optional[str] = None


class AgentTask(BaseModel):
    """Agent task model"""
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime = PydanticField(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    parent_task_id: Optional[str] = None


class WorkflowDefinition(BaseModel):
    """Workflow definition model"""
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    tasks: List[AgentTask]
    dependencies: Dict[str, List[str]] = {}  # task_id -> [dependency_task_ids]
    created_at: datetime = PydanticField(default_factory=datetime.now)


class GoldReferenceDefinition(BaseModel):
    """Gold reference data definition"""
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    name: str
    lookup_table: str
    key_fields: List[str]
    standard_values: Dict[str, Any]
    business_rules: List[str] = []
    description: Optional[str] = None
    created_at: datetime = PydanticField(default_factory=datetime.now)


class TransformationRule(BaseModel):
    """Complex transformation rule definition"""
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    name: str
    rule_type: str  # conditional, lookup, calculation, derivation
    source_fields: List[str]
    target_field: str
    logic: str  # The actual transformation logic
    conditions: List[str] = []  # Conditional statements
    parameters: Dict[str, Any] = {}
    description: Optional[str] = None
    created_at: datetime = PydanticField(default_factory=datetime.now)


class ExcelMappingProject(BaseModel):
    """Excel-based mapping project"""
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    name: str
    source_file: str
    field_mappings: List[MappingRule]
    gold_references: List[GoldReferenceDefinition]
    transformation_rules: List[TransformationRule]
    validation_results: Optional[ValidationResult] = None
    project_metadata: Dict[str, Any] = {}
    created_at: datetime = PydanticField(default_factory=datetime.now)


# SQLAlchemy Models for Database

class Document(Base):
    """Document table for storing processed documents"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    content_hash = Column(String(64), nullable=False)
    doc_metadata = Column(JSON)
    schema_extracted = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class MappingProject(Base):
    """Mapping project table"""
    __tablename__ = "mapping_projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    source_schema = Column(JSON)
    target_schema = Column(JSON)
    mapping_rules = Column(JSON)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class GeneratedArtifact(Base):
    """Generated artifacts table"""
    __tablename__ = "generated_artifacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    artifact_type = Column(String(50), nullable=False)  # code, test, documentation
    content = Column(Text, nullable=False)
    language = Column(String(50))
    file_path = Column(String(500))
    artifact_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


class AgentExecution(Base):
    """Agent execution history table"""
    __tablename__ = "agent_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_type = Column(String(100), nullable=False)
    task_id = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    input_data = Column(JSON)
    output_data = Column(JSON)
    error_message = Column(Text)
    execution_time_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)


class KnowledgeBase(Base):
    """Knowledge base table for storing learned patterns"""
    __tablename__ = "knowledge_base"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String(100), nullable=False)  # schema_pattern, code_pattern, etc.
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    embedding_id = Column(String(100))  # Reference to vector store
    tags = Column(JSON)
    usage_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Response Models

class APIResponse(BaseModel):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = PydanticField(default_factory=datetime.now)


class ValidationResponse(APIResponse):
    """Validation API response"""
    data: Optional[ValidationResult] = None


class CodeGenerationResponse(APIResponse):
    """Code generation API response"""
    data: Optional[GeneratedCode] = None


class WorkflowResponse(APIResponse):
    """Workflow API response"""
    data: Optional[WorkflowDefinition] = None