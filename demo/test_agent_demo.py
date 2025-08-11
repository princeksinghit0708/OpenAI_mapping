#!/usr/bin/env python3
"""
🧪 Test Generator Agent Demo
Demonstrates the standalone TestGeneratorAgent capabilities
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the agentic_mapping_ai to path
sys.path.append('./agentic_mapping_ai')

async def demo_test_generator():
    """Demo the TestGeneratorAgent standalone"""
    
    print("🧪 Test Generator Agent Demo")
    print("=" * 50)
    
    try:
        # Import required modules
        from agents.test_generator import TestGeneratorAgent
        from agents.base_agent import AgentConfig
        from core.models import (
            CodeGenerationRequest, GeneratedCode, 
            SchemaDefinition, FieldDefinition, DataType
        )
        
        # Create test generator agent
        config = AgentConfig(
            name="Demo Test Generator",
            description="Test generation demonstration",
            model="gpt-4",
            temperature=0.1
        )
        
        test_agent = TestGeneratorAgent(config)
        print("✅ TestGeneratorAgent initialized")
        
        # Create sample schema definitions
        source_schema = SchemaDefinition(
            name="account_source",
            description="EBS IM Account source schema",
            fields=[
                FieldDefinition(
                    name="account_id",
                    physical_name="ACCOUNT_ID",
                    data_type=DataType.STRING,
                    is_nullable=False,
                    description="Unique account identifier"
                ),
                FieldDefinition(
                    name="account_balance",
                    physical_name="ACCOUNT_BALANCE",
                    data_type=DataType.FLOAT,
                    is_nullable=True,
                    description="Current account balance"
                ),
                FieldDefinition(
                    name="account_status",
                    physical_name="ACCOUNT_STATUS",
                    data_type=DataType.STRING,
                    is_nullable=False,
                    description="Account status code"
                )
            ]
        )
        
        target_schema = SchemaDefinition(
            name="account_target",
            description="DataHub account target schema",
            fields=[
                FieldDefinition(
                    name="account_number",
                    physical_name="ACCOUNT_NUMBER",
                    data_type=DataType.STRING,
                    is_nullable=False,
                    description="Standardized account number"
                ),
                FieldDefinition(
                    name="balance_amount",
                    physical_name="BALANCE_AMOUNT",
                    data_type=DataType.FLOAT,
                    is_nullable=True,
                    description="Account balance in standard format"
                ),
                FieldDefinition(
                    name="status_code",
                    physical_name="STATUS_CODE",
                    data_type=DataType.STRING,
                    is_nullable=False,
                    description="Standardized status code"
                )
            ]
        )
        
        # Sample generated code
        sample_code = """
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, when, regexp_replace, coalesce
from pyspark.sql.types import StringType, FloatType

def transform_account_data(spark: SparkSession, source_df: DataFrame) -> DataFrame:
    \"\"\"Transform EBS IM Account data to DataHub standard format\"\"\"
    
    transformed_df = source_df.select(
        # Account ID transformation
        col("ACCOUNT_ID").alias("account_number"),
        
        # Balance transformation with validation
        when(col("ACCOUNT_BALANCE").isNull(), 0.0)
        .otherwise(col("ACCOUNT_BALANCE")).alias("balance_amount"),
        
        # Status code standardization
        when(col("ACCOUNT_STATUS") == "A", "ACTIVE")
        .when(col("ACCOUNT_STATUS") == "I", "INACTIVE")
        .when(col("ACCOUNT_STATUS") == "C", "CLOSED")
        .otherwise("UNKNOWN").alias("status_code")
    )
    
    return transformed_df
"""
        
        generated_code = GeneratedCode(
            code=sample_code,
            language="pyspark",
            framework="pyspark",
            generated_at="2024-01-01T00:00:00Z",
            performance_notes="Optimized for large datasets"
        )
        
        # Create code generation request
        code_request = CodeGenerationRequest(
            source_schema=source_schema,
            target_schema=target_schema,
            mapping_rules=[],
            code_type="pyspark",
            optimization_level="standard",
            include_tests=True
        )
        
        print("\n🎯 Demo Scenarios:")
        
        # Demo 1: Unit Tests
        print("\n1. 🧪 Generating Unit Tests...")
        unit_test_input = {
            "code_generation_request": code_request.dict(),
            "generated_code": generated_code.dict(),
            "test_type": "unit"
        }
        
        unit_result = await test_agent._execute_core_logic(unit_test_input)
        if unit_result.get("success"):
            print("✅ Unit tests generated successfully!")
            print(f"   Coverage estimate: {unit_result.get('coverage_estimate', 'N/A')}%")
        else:
            print(f"❌ Unit test generation failed: {unit_result.get('error')}")
        
        # Demo 2: Integration Tests
        print("\n2. 🔗 Generating Integration Tests...")
        integration_test_input = {
            "code_generation_request": code_request.dict(),
            "generated_code": generated_code.dict(),
            "test_type": "integration"
        }
        
        integration_result = await test_agent._execute_core_logic(integration_test_input)
        if integration_result.get("success"):
            print("✅ Integration tests generated successfully!")
        else:
            print(f"❌ Integration test generation failed: {integration_result.get('error')}")
        
        # Demo 3: Comprehensive Test Suite
        print("\n3. 📋 Generating Comprehensive Test Suite...")
        comprehensive_test_input = {
            "code_generation_request": code_request.dict(),
            "generated_code": generated_code.dict(),
            "test_type": "comprehensive"
        }
        
        comprehensive_result = await test_agent._execute_core_logic(comprehensive_test_input)
        if comprehensive_result.get("success"):
            print("✅ Comprehensive test suite generated successfully!")
            test_results = comprehensive_result.get("test_results", {})
            print(f"   📊 Test components generated:")
            for component, _ in test_results.items():
                if component != "test_documentation":
                    print(f"      ✓ {component.replace('_', ' ').title()}")
            print(f"   📈 Estimated coverage: {comprehensive_result.get('coverage_estimate', 'N/A')}%")
        else:
            print(f"❌ Comprehensive test generation failed: {comprehensive_result.get('error')}")
        
        print("\n" + "=" * 50)
        print("🎉 Test Generator Agent Demo Complete!")
        print("\n💡 The TestGeneratorAgent can generate:")
        print("   • Unit tests for individual transformations")
        print("   • Integration tests for end-to-end pipelines") 
        print("   • Performance tests for scalability")
        print("   • Data quality validation tests")
        print("   • Mock data for realistic testing")
        print("   • Comprehensive test documentation")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the demo directory")
        return False
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Main demo entry point"""
    if not Path("agentic_mapping_ai/agents/test_generator.py").exists():
        print("❌ TestGeneratorAgent not found!")
        print("💡 Please run this from the demo directory")
        return 1
    
    try:
        result = asyncio.run(demo_test_generator())
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
