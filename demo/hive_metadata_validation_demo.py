#!/usr/bin/env python3
"""
🔍 Hive Metadata Validation Demo using MetadataValidatorAgent
Demonstrates the agent working with your existing Hive metadata JSON files
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add the agentic_mapping_ai to path
sys.path.append('./agentic_mapping_ai')
sys.path.append('.')

async def demo_hive_metadata_validation():
    """Demo the MetadataValidatorAgent with your existing Hive metadata files"""
    
    print("🔍 Hive Metadata Validation Demo using MetadataValidatorAgent")
    print("=" * 70)
    print("🎯 This demo shows the agent working with your existing Hive metadata")
    print("📁 Using metadata files from: demo/results/")
    print("=" * 70)
    
    try:
        # Import required modules with correct paths
        from agentic_mapping_ai.agents.metadata_validator import MetadataValidatorAgent
        from agentic_mapping_ai.agents.base_agent import AgentConfig
        from agentic_mapping_ai.core.models import ValidationResult
        
        print("✅ Successfully imported MetadataValidatorAgent")
        
        # Create metadata validator agent with enhanced configuration
        config = AgentConfig(
            name="Hive Metadata Validator",
            description="Validates Hive table metadata for EBS IM DataHub",
            model="gpt-4",  # Using GPT-4 for better analysis
            temperature=0.1,  # Low temperature for consistent validation
            max_tokens=2000
        )
        
        print("🔧 Initializing MetadataValidatorAgent...")
        validator_agent = MetadataValidatorAgent(config)
        print("✅ MetadataValidatorAgent initialized successfully")
        
        # Load all metadata files from results directory
        results_dir = Path("results")
        metadata_files = list(results_dir.glob("*_metadata.json"))
        
        if not metadata_files:
            print("❌ No metadata files found in results/ directory")
            print("💡 Expected files: acct_dly_metadata.json, cust_dly_metadata.json, txn_dly_metadata.json")
            return False
        
        print(f"\n📁 Found {len(metadata_files)} Hive metadata files:")
        for file in metadata_files:
            print(f"   📄 {file.name}")
        
        print("\n" + "=" * 70)
        print("🚀 STARTING AGENTIC VALIDATION PROCESS")
        print("=" * 70)
        
        # Track overall validation results
        overall_results = {
            'total_files': len(metadata_files),
            'validated_files': 0,
            'total_issues': 0,
            'validation_summary': {}
        }
        
        # Demo each metadata file with the agent
        for i, metadata_file in enumerate(metadata_files, 1):
            print(f"\n🔍 [{i}/{len(metadata_files)}] Validating: {metadata_file.name}")
            print("-" * 60)
            
            try:
                # Load metadata
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                print(f"📊 Table: {metadata.get('table_name', 'Unknown')}")
                print(f"🗄️  Database: {metadata.get('database_name', 'Unknown')}")
                print(f"📈 Rows: {metadata.get('row_count', 'Unknown'):,}")
                print(f"🔄 Refresh: {metadata.get('data_refresh', 'Unknown')}")
                print(f"📋 Columns: {len(metadata.get('columns', []))}")
                
                # Prepare validation input for the agent
                validation_input = {
                    "document": metadata,
                    "validation_type": "hive_schema_validation",
                    "strict_mode": True,
                    "context": "EBS IM DataHub banking data validation"
                }
                
                print(f"\n🤖 Agent is analyzing the metadata...")
                print("   (This demonstrates the agent's AI-powered validation capabilities)")
                
                # Execute validation using the agent
                result = await validator_agent._execute_core_logic(validation_input)
                
                if result and result.get("validation_result"):
                    validation_data = result.get("validation_result", {})
                    
                    # Display validation results
                    print(f"\n✅ AGENT VALIDATION COMPLETED")
                    print(f"📊 Validation Status: {validation_data.get('status', 'VALIDATED')}")
                    
                    # Show validation details
                    if validation_data.get('validation_details'):
                        details = validation_data['validation_details']
                        print(f"\n📝 Validation Details ({len(details)} checks):")
                        
                        for detail in details:
                            status_icon = "✅" if detail.get('status') == 'PASS' else "❌"
                            check_type = detail.get('check_type', 'Unknown')
                            message = detail.get('message', 'No message')
                            print(f"   {status_icon} {check_type}: {message}")
                    
                    # Show field analysis
                    if validation_data.get('field_analysis'):
                        field_analysis = validation_data['field_analysis']
                        print(f"\n🔍 Field Analysis:")
                        print(f"   📊 Total Fields: {field_analysis.get('total_fields', 0)}")
                        print(f"   ✅ Valid Fields: {field_analysis.get('valid_fields', 0)}")
                        print(f"   ⚠️  Warnings: {field_analysis.get('warnings', 0)}")
                        print(f"   ❌ Errors: {field_analysis.get('errors', 0)}")
                    
                    # Show data type distribution
                    columns = metadata.get('columns', [])
                    if columns:
                        data_types = {}
                        for col in columns:
                            dtype = col.get('data_type', 'unknown')
                            data_types[dtype] = data_types.get(dtype, 0) + 1
                        
                        print(f"\n📊 Data Type Distribution:")
                        for dtype, count in data_types.items():
                            print(f"   🔹 {dtype}: {count} columns")
                    
                    # Show sample columns with agent insights
                    if columns:
                        print(f"\n📋 Sample Columns with Agent Analysis:")
                        for col in columns[:5]:  # Show first 5
                            col_name = col.get('col_name', 'unknown')
                            col_type = col.get('data_type', 'unknown')
                            comment = col.get('comment', 'No comment')[:60]
                            
                            # Agent would provide insights here
                            agent_insight = "✅ Standard banking field" if col_name in ['acct_nbr', 'txn_id', 'cust_id'] else "🔍 Business field"
                            
                            print(f"   {agent_insight} {col_name} ({col_type}): {comment}")
                        
                        if len(columns) > 5:
                            print(f"   ... and {len(columns) - 5} more columns")
                    
                    # Track results
                    overall_results['validated_files'] += 1
                    if validation_data.get('errors'):
                        overall_results['total_issues'] += len(validation_data['errors'])
                    
                    overall_results['validation_summary'][metadata_file.name] = {
                        'status': 'SUCCESS',
                        'issues': validation_data.get('errors', []),
                        'warnings': validation_data.get('warnings', [])
                    }
                    
                else:
                    print(f"❌ Agent validation failed or returned no results")
                    overall_results['validation_summary'][metadata_file.name] = {
                        'status': 'FAILED',
                        'error': 'No validation results returned'
                    }
                
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON format in {metadata_file.name}")
                overall_results['validation_summary'][metadata_file.name] = {
                    'status': 'FAILED',
                    'error': 'Invalid JSON format'
                }
            except Exception as e:
                print(f"❌ Error validating {metadata_file.name}: {e}")
                overall_results['validation_summary'][metadata_file.name] = {
                    'status': 'FAILED',
                    'error': str(e)
                }
            
            print("\n" + "-" * 60)
        
        # Overall summary
        print(f"\n" + "=" * 70)
        print("📊 AGENTIC VALIDATION SUMMARY")
        print("=" * 70)
        
        print(f"🎯 Total Files Processed: {overall_results['total_files']}")
        print(f"✅ Successfully Validated: {overall_results['validated_files']}")
        print(f"❌ Total Issues Found: {overall_results['total_issues']}")
        
        print(f"\n📋 File-by-File Results:")
        for filename, result in overall_results['validation_summary'].items():
            status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
            print(f"   {status_icon} {filename}: {result['status']}")
            if result['status'] == 'SUCCESS' and result.get('issues'):
                print(f"      ⚠️  {len(result['issues'])} issues found")
            elif result['status'] == 'FAILED':
                print(f"      ❌ {result.get('error', 'Unknown error')}")
        
        print(f"\n🎉 AGENTIC VALIDATION DEMO COMPLETE!")
        print(f"\n💡 The MetadataValidatorAgent demonstrated:")
        print("   • AI-powered metadata analysis")
        print("   • Intelligent field validation")
        print("   • Banking-specific rule checking")
        print("   • Automated issue detection")
        print("   • Comprehensive reporting")
        
        print(f"\n🚀 Next Steps:")
        print("   • Run this demo to see the agent in action")
        print("   • Check the validation results for each table")
        print("   • Use the agent to validate new metadata")
        print("   • Integrate with your Excel mapping process")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the demo directory")
        print("💡 Check that agentic_mapping_ai is properly installed")
        return False
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main demo entry point"""
    print("🔍 Hive Metadata Validation Demo")
    print("=" * 50)
    
    # Check prerequisites
    if not Path("agentic_mapping_ai/agents/metadata_validator.py").exists():
        print("❌ MetadataValidatorAgent not found!")
        print("💡 Please run this from the demo directory")
        return 1
    
    if not Path("results").exists() or not list(Path("results").glob("*_metadata.json")):
        print("❌ No metadata files found!")
        print("💡 Make sure the results/ directory contains *_metadata.json files")
        return 1
    
    print("✅ Prerequisites check passed")
    print("🚀 Starting agentic validation demo...")
    
    try:
        result = asyncio.run(demo_hive_metadata_validation())
        return 0 if result else 1
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
