#!/usr/bin/env python3
"""
Quick Start Example for Agentic Mapping AI Platform
Demonstrates how to use the platform programmatically
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.orchestrator import OrchestratorAgent, WorkflowType
from agents.base_agent import AgentConfig
from knowledge.rag_engine import RAGEngine
from core.models import FieldDefinition, SchemaDefinition, MappingRule, DataType


async def main():
    """Quick start example"""
    print("🚀 Agentic Mapping AI - Quick Start Example")
    print("=" * 50)
    
    # Initialize RAG engine
    print("📚 Initializing RAG engine...")
    rag_engine = RAGEngine()
    await asyncio.sleep(2)  # Give time for initialization
    
    # Initialize orchestrator
    print("🤖 Initializing orchestrator agent...")
    orchestrator_config = AgentConfig(
        name="Example Orchestrator",
        description="Orchestrator for quick start example",
        model="gpt-4",
        temperature=0.1
    )
    
    orchestrator = OrchestratorAgent(
        config=orchestrator_config,
        rag_engine=rag_engine
    )
    
    # Wait for agent initialization
    await asyncio.sleep(3)
    
    # Example 1: Document Validation
    print("\n📄 Example 1: Document Validation")
    print("-" * 30)
    
    sample_document = {
        "dictionary": {
            "providedKey": "PBWM.GCB_AAC_NAM.customer_database_db"
        },
        "fields": [
            {
                "providedKey": "PBWM.GCB_AAC_NAM.customer_database_db.customers.customer_id",
                "displayName": "customer_id",
                "physicalName": "customer_id",
                "dataType": "Integer",
                "isNullable": False,
                "format": "int",
                "description": "Unique identifier for customer"
            },
            {
                "providedKey": "PBWM.GCB_AAC_NAM.customer_database_db.customers.customer_name",
                "displayName": "customer_name", 
                "physicalName": "customer_name",
                "dataType": "Character",
                "isNullable": True,
                "format": "varchar(255)",
                "description": "Full name of the customer"
            },
            {
                "providedKey": "PBWM.GCB_AAC_NAM.customer_database_db.customers.email",
                "displayName": "email",
                "physicalName": "email_address",
                "dataType": "Character", 
                "isNullable": True,
                "format": "varchar(255)",
                "description": "Customer email address"
            }
        ]
    }
    
    try:
        validation_result = await orchestrator._execute_core_logic({
            "workflow_type": WorkflowType.DOCUMENT_PROCESSING.value,
            "workflow_data": {
                "document": sample_document,
                "validation_rules": ["check_required_fields", "validate_data_types"]
            }
        })
        
        if validation_result.get("success"):
            print("✅ Document validation successful!")
            print(f"   Database name: {validation_result.get('database_name')}")
            print(f"   Fields extracted: {validation_result.get('field_count')}")
            
            # Show extracted fields
            fields = validation_result.get('extracted_fields', [])
            if fields:
                print("   Extracted fields:")
                for field in fields[:3]:  # Show first 3 fields
                    print(f"   - {field.get('name')} ({field.get('data_type')})")
        else:
            print("❌ Document validation failed")
            print(f"   Error: {validation_result.get('error')}")
    
    except Exception as e:
        print(f"❌ Validation example failed: {str(e)}")
    
    # Example 2: Code Generation
    print("\n🔧 Example 2: Code Generation")
    print("-" * 30)
    
    try:
        # Define schemas
        source_schema = SchemaDefinition(
            name="customer_source",
            fields=[
                FieldDefinition(
                    name="customer_id",
                    data_type=DataType.INTEGER,
                    is_nullable=False,
                    description="Customer ID"
                ),
                FieldDefinition(
                    name="customer_name", 
                    data_type=DataType.STRING,
                    is_nullable=True,
                    description="Customer name"
                ),
                FieldDefinition(
                    name="email",
                    data_type=DataType.STRING,
                    is_nullable=True,
                    description="Email address"
                )
            ]
        )
        
        target_schema = SchemaDefinition(
            name="customer_target",
            fields=[
                FieldDefinition(
                    name="id",
                    data_type=DataType.INTEGER,
                    is_nullable=False,
                    description="Customer ID"
                ),
                FieldDefinition(
                    name="full_name",
                    data_type=DataType.STRING,
                    is_nullable=True,
                    description="Full customer name"
                ),
                FieldDefinition(
                    name="email_address",
                    data_type=DataType.STRING,
                    is_nullable=True,
                    description="Email address"
                )
            ]
        )
        
        # Define mapping rules
        mapping_rules = [
            MappingRule(
                source_field="customer_id",
                target_field="id",
                description="Direct mapping of customer ID"  
            ),
            MappingRule(
                source_field="customer_name",
                target_field="full_name",
                description="Map customer name to full_name"
            ),
            MappingRule(
                source_field="email",
                target_field="email_address", 
                description="Map email to email_address"
            )
        ]
        
        # Generate code
        code_result = await orchestrator._execute_core_logic({
            "workflow_type": WorkflowType.CODE_GENERATION.value,
            "workflow_data": {
                "code_request": {
                    "source_schema": source_schema.dict(),
                    "target_schema": target_schema.dict(),
                    "mapping_rules": [rule.dict() for rule in mapping_rules],
                    "code_type": "pyspark",
                    "optimization_level": "standard",
                    "include_tests": True
                }
            }
        })
        
        if code_result.get("success"):
            print("✅ Code generation successful!")
            generated_code = code_result.get("generated_code", {})
            
            if generated_code.get("code"):
                print("   Generated PySpark code:")
                code_preview = generated_code["code"][:300]
                print(f"   ```python\n   {code_preview}...\n   ```")
            
            if generated_code.get("dependencies"):
                print(f"   Dependencies: {', '.join(generated_code['dependencies'])}")
        else:
            print("❌ Code generation failed")
            print(f"   Error: {code_result.get('error')}")
    
    except Exception as e:
        print(f"❌ Code generation example failed: {str(e)}")
    
    # Example 3: Full Pipeline
    print("\n🔄 Example 3: Full Pipeline")
    print("-" * 30)
    
    try:
        pipeline_result = await orchestrator._execute_core_logic({
            "workflow_type": WorkflowType.FULL_MAPPING_PIPELINE.value,
            "workflow_data": {
                "document": sample_document,
                "code_type": "pyspark",
                "optimization_level": "standard",
                "include_tests": True
            }
        })
        
        if pipeline_result.get("success"):
            print("✅ Full pipeline successful!")
            
            # Document processing results
            doc_processing = pipeline_result.get("document_processing", {})
            if doc_processing:
                print(f"   Document processing: {doc_processing.get('field_count')} fields extracted")
                print(f"   Database name: {doc_processing.get('database_name')}")
            
            # Code generation results  
            code_generation = pipeline_result.get("code_generation", {})
            if code_generation and code_generation.get("generated_code"):
                print("   Code generation: PySpark transformation code generated")
        else:
            print("❌ Full pipeline failed")
            print(f"   Error: {pipeline_result.get('error')}")
    
    except Exception as e:
        print(f"❌ Full pipeline example failed: {str(e)}")
    
    # Example 4: Knowledge Base Query
    print("\n🧠 Example 4: Knowledge Base Query")
    print("-" * 30)
    
    try:
        # Query knowledge base
        results = await rag_engine.retrieve("PySpark performance optimization", max_results=3)
        
        if results:
            print(f"✅ Found {len(results)} knowledge base results:")
            for i, result in enumerate(results):
                print(f"   {i+1}. {result.metadata.get('title', 'Untitled')} (Score: {result.score:.3f})")
                print(f"      Category: {result.metadata.get('category', 'Unknown')}")
        else:
            print("ℹ️ No knowledge base results found")
    
    except Exception as e:
        print(f"❌ Knowledge base query failed: {str(e)}")
    
    print("\n🎉 Quick start example completed!")
    print("\n📖 Next steps:")
    print("   1. Start the full application: python run_application.py")
    print("   2. Open the API docs: http://localhost:8000/docs")
    print("   3. Use the Streamlit UI: http://localhost:8501")
    print("   4. Explore the examples/ directory for more use cases")


if __name__ == "__main__":
    asyncio.run(main())