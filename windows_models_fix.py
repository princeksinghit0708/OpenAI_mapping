#!/usr/bin/env python3
"""
Alternative Windows fix: Replace problematic imports with safe versions
"""

import os
import sys

def create_safe_models_import():
    """Create a safe models import that avoids SQLAlchemy conflicts"""
    
    safe_models_content = '''"""
Safe models import for Windows - avoids SQLAlchemy metadata conflicts
"""

# Import only what we need, avoiding SQLAlchemy declarative issues
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field as PydanticField
import uuid

# Enums
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AgentType(str, Enum):
    METADATA_VALIDATOR = "metadata_validator"
    SCHEMA_MAPPER = "schema_mapper"
    CODE_GENERATOR = "code_generator"
    TEST_GENERATOR = "test_generator"
    ORCHESTRATOR = "orchestrator"

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    TIMESTAMP = "timestamp"
    ARRAY = "array"
    OBJECT = "object"

# Pydantic Models (safe - no SQLAlchemy conflicts)
class FieldDefinition(BaseModel):
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
    name: str
    fields: List[FieldDefinition]
    schema_metadata: Optional[Dict[str, Any]] = None  # Safe name
    version: str = "1.0"

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []
    validation_metadata: Optional[Dict[str, Any]] = None  # Safe name

class MappingRule(BaseModel):
    source_field: str
    target_field: str
    transformation: Optional[str] = None
    validation_rules: Optional[List[str]] = None
    description: Optional[str] = None
    mapping_type: str = "Direct"
    transformation_category: Optional[str] = None
    dependency_fields: List[str] = []
    gold_reference_key: Optional[str] = None

class AgentTask(BaseModel):
    id: str = PydanticField(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType
    status: TaskStatus = TaskStatus.PENDING
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime = PydanticField(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    parent_task_id: Optional[str] = None

# Skip SQLAlchemy models for Windows compatibility
# These would normally be defined with SQLAlchemy but cause conflicts on Windows

print("✅ Safe models loaded successfully (Windows compatible)")
'''
    
    # Write the safe models file
    safe_models_path = 'safe_models.py'
    with open(safe_models_path, 'w', encoding='utf-8') as f:
        f.write(safe_models_content)
    
    print(f"✅ Created safe models file: {safe_models_path}")
    return safe_models_path

def patch_imports():
    """Patch imports to use safe models"""
    print("🔧 Patching imports to use safe models...")
    
    # Files that might need patching
    files_to_patch = [
        'chatbased_demo_app/agents/agent_manager.py',
        'chatbased_demo_app/main.py'
    ]
    
    for file_path in files_to_patch:
        if os.path.exists(file_path):
            print(f"   Checking: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add safe import at the top
            if 'from safe_models import' not in content:
                # Add safe import after existing imports
                lines = content.split('\n')
                import_end = 0
                for i, line in enumerate(lines):
                    if line.startswith('import ') or line.startswith('from '):
                        import_end = i + 1
                
                # Insert safe import
                safe_import = 'from safe_models import AgentTask, AgentType, TaskStatus, ValidationResult'
                lines.insert(import_end, safe_import)
                
                content = '\n'.join(lines)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Patched: {file_path}")
            else:
                print(f"   Already patched: {file_path}")

def main():
    print("🔧 Windows Models Fix - Alternative Approach")
    print("=" * 50)
    
    # Create safe models
    safe_models_path = create_safe_models_import()
    
    # Patch imports
    patch_imports()
    
    print("\n🎉 Alternative fix applied!")
    print("This creates a Windows-compatible version that avoids SQLAlchemy conflicts.")
    print("You can now try running the chatbased demo app.")

if __name__ == "__main__":
    main()
