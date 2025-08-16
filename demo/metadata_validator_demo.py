#!/usr/bin/env python3
"""
🔍 Metadata Validator Agent Demo
Demonstrates metadata validation capabilities using real table metadata
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# Add the agentic_mapping_ai to path
sys.path.append('./agentic_mapping_ai')
sys.path.append('.')

async def demo_metadata_validator():
    """Demo the MetadataValidator with real metadata files"""
    
    print("🔍 Metadata Validator Agent Demo")
    print("=" * 60)
    
    try:
        # Import required modules with correct paths
        from agentic_mapping_ai.agents.metadata_validator import MetadataValidatorAgent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        from agentic_mapping_ai.core.models import ValidationResult
        
        # Create metadata validator agent
        config = AgentConfig(
            name="Demo Metadata Validator",
            description="Metadata validation demonstration",
            model="gpt-4",
            temperature=0.1
        )
        
        validator_agent = MetadataValidatorAgent(config)
        print("✅ MetadataValidatorAgent initialized")
        
        # Load real metadata files
        metadata_files = list(Path("results").glob("*_metadata.json"))
        if not metadata_files:
            print("❌ No metadata files found in results/ directory")
            return False
        
        print(f"\n📁 Found {len(metadata_files)} metadata files:")
        for file in metadata_files:
            print(f"   📄 {file.name}")
        
        print("\n" + "=" * 60)
        
        # Demo each metadata file
        for metadata_file in metadata_files:
            print(f"\n🔍 Validating: {metadata_file.name}")
            print("-" * 40)
            
            try:
                # Load metadata
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                print(f"📊 Table: {metadata.get('table_name', 'Unknown')}")
                print(f"🗄️  Database: {metadata.get('database_name', 'Unknown')}")
                print(f"📈 Rows: {metadata.get('row_count', 'Unknown'):,}")
                print(f"🔄 Refresh: {metadata.get('data_refresh', 'Unknown')}")
                
                # Prepare validation input
                validation_input = {
                    "document": metadata,
                    "validation_type": "schema_validation",
                    "strict_mode": True
                }
                
                # Execute validation
                result = await validator_agent._execute_core_logic(validation_input)
                
                if result.get("success"):
                    validation_data = result.get("validation_result", {})
                    print(f"\n✅ Validation Status: {validation_data.get('status', 'UNKNOWN')}")
                    print(f"📋 Total Checks: {validation_data.get('total_checks', 0)}")
                    print(f"✅ Passed: {validation_data.get('passed_checks', 0)}")
                    print(f"❌ Failed: {validation_data.get('failed_checks', 0)}")
                    
                    # Show validation details
                    details = validation_data.get('validation_details', [])
                    if details:
                        print(f"\n📝 Validation Details:")
                        for detail in details[:3]:  # Show first 3
                            status_icon = "✅" if detail.get('status') == 'PASS' else "❌"
                            print(f"   {status_icon} {detail.get('check_type', 'Unknown')}: {detail.get('message', 'No message')}")
                        
                        if len(details) > 3:
                            print(f"   ... and {len(details) - 3} more checks")
                    
                    # Show column analysis
                    columns = metadata.get('columns', [])
                    if columns:
                        print(f"\n🔍 Column Analysis ({len(columns)} columns):")
                        
                        # Data type distribution
                        data_types = {}
                        for col in columns:
                            dtype = col.get('data_type', 'unknown')
                            data_types[dtype] = data_types.get(dtype, 0) + 1
                        
                        for dtype, count in data_types.items():
                            print(f"   📊 {dtype}: {count} columns")
                        
                        # Sample columns
                        print(f"\n📋 Sample Columns:")
                        for col in columns[:5]:  # Show first 5
                            col_name = col.get('col_name', 'unknown')
                            col_type = col.get('data_type', 'unknown')
                            comment = col.get('comment', 'No comment')[:50]
                            print(f"   🔹 {col_name} ({col_type}): {comment}")
                        
                        if len(columns) > 5:
                            print(f"   ... and {len(columns) - 5} more columns")
                    
                else:
                    print(f"❌ Validation failed: {result.get('error', 'Unknown error')}")
                
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON format in {metadata_file.name}")
            except Exception as e:
                print(f"❌ Error validating {metadata_file.name}: {e}")
            
            print("\n" + "-" * 40)
        
        # Summary
        print(f"\n" + "=" * 60)
        print("🎉 Metadata Validation Demo Complete!")
        print(f"\n💡 The MetadataValidator can:")
        print("   • Validate table schema structures")
        print("   • Check column definitions and data types")
        print("   • Verify naming conventions")
        print("   • Validate referential integrity")
        print("   • Check data quality constraints")
        print("   • Generate validation reports")
        print("   • Suggest schema improvements")
        
        print(f"\n📊 Banking-Specific Validations:")
        print("   • Account number format validation")
        print("   • Currency code compliance") 
        print("   • Date range validation")
        print("   • Regulatory field requirements")
        print("   • PII data classification")
        
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
    if not Path("agentic_mapping_ai/agents/metadata_validator.py").exists():
        print("❌ MetadataValidatorAgent not found!")
        print("💡 Please run this from the demo directory")
        return 1
    
    if not Path("results").exists() or not list(Path("results").glob("*_metadata.json")):
        print("❌ No metadata files found!")
        print("💡 Make sure the results/ directory contains *_metadata.json files")
        return 1
    
    try:
        result = asyncio.run(demo_metadata_validator())
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
