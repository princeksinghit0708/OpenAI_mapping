"""
🎯 END-TO-END AGENTIC MAPPING AI DEMO
Complete workflow demonstration from document processing to code generation
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from loguru import logger

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from agents.metadata_validator import MetadataValidatorAgent
from agents.code_generator import CodeGeneratorAgent
from agents.orchestrator import OrchestratorAgent
from agents.base_agent import AgentConfig
from core.models import (
    FieldDefinition, SchemaDefinition, MappingRule, 
    ValidationResult, CodeGenerationRequest, GeneratedCode
)
from parsers.excel_mapping_parser import ExcelMappingParser

# Configure logging
logger.add("demo_logs/end_to_end_demo.log", rotation="1 day", level="INFO")

class EndToEndDemoApp:
    """
    Comprehensive demo application showcasing the complete Agentic Mapping AI workflow
    """
    
    def __init__(self):
        self.output_dir = Path("demo_output")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "excel_parsed").mkdir(exist_ok=True)
        (self.output_dir / "validation_reports").mkdir(exist_ok=True)
        (self.output_dir / "test_cases").mkdir(exist_ok=True)
        (self.output_dir / "generated_code").mkdir(exist_ok=True)
        (self.output_dir / "workflow_logs").mkdir(exist_ok=True)
        (self.output_dir / "final_reports").mkdir(exist_ok=True)
        
        # Initialize agents
        self.metadata_agent = None
        self.code_generator_agent = None
        self.orchestrator_agent = None
        
        # Workflow status
        self.workflow_status = {
            "start_time": None,
            "end_time": None,
            "steps_completed": [],
            "errors": [],
            "outputs": {}
        }
    
    async def initialize_agents(self):
        """Initialize all AI agents"""
        logger.info("🤖 Initializing AI Agents...")
        
        try:
            # Metadata Validator Agent
            metadata_config = AgentConfig(
                name="Metadata Validator",
                description="Validates document metadata and schemas",
                model="gpt-4",
                temperature=0.1
            )
            self.metadata_agent = MetadataValidatorAgent(metadata_config)
            logger.info("✅ Metadata Validator Agent initialized")
            
            # Code Generator Agent
            code_config = AgentConfig(
                name="Code Generator",
                description="Generates PySpark and SQL code",
                model="gpt-4",
                temperature=0.2
            )
            self.code_generator_agent = CodeGeneratorAgent(code_config)
            logger.info("✅ Code Generator Agent initialized")
            
            # Orchestrator Agent
            orchestrator_config = AgentConfig(
                name="Orchestrator",
                description="Coordinates multi-agent workflows",
                model="gpt-4",
                temperature=0.1
            )
            self.orchestrator_agent = OrchestratorAgent(orchestrator_config)
            logger.info("✅ Orchestrator Agent initialized")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize agents: {str(e)}")
            self.workflow_status["errors"].append(f"Agent initialization failed: {str(e)}")
            return False
    
    async def create_sample_excel_file(self):
        """Create a comprehensive sample Excel file for demo"""
        logger.info("📝 Creating comprehensive sample Excel file...")
        
        # Sample data with different mapping types
        sample_data = [
            # ACCT_DLY table - Direct mappings
            {
                'Physical_Table': 'ACCT_DLY',
                'Logical_Name': 'Account Number',
                'Physical_Name': 'ACCT_NUM',
                'datatype': 'VARCHAR(20)',
                'Name_For': 'acct_num',
                'Column_Name': 'acct_num',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            },
            {
                'Physical_Table': 'ACCT_DLY',
                'Logical_Name': 'Account Balance',
                'Physical_Name': 'ACCT_BAL',
                'datatype': 'DECIMAL(15,2)',
                'Name_For': 'acct_bal',
                'Column_Name': 'acct_bal',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            },
            # ACCT_DLY table - Derived mappings
            {
                'Physical_Table': 'ACCT_DLY',
                'Logical_Name': 'Account Status',
                'Physical_Name': 'ACCT_STATUS',
                'datatype': 'VARCHAR(10)',
                'Name_For': 'acct_status',
                'Column_Name': 'acct_status',
                'Mapping_Type': 'Derived',
                'Transformation': "CASE WHEN ACCT_BAL > 0 THEN 'ACTIVE' ELSE 'INACTIVE' END"
            },
            {
                'Physical_Table': 'ACCT_DLY',
                'Logical_Name': 'High Value Flag',
                'Physical_Name': 'HIGH_VALUE_FLG',
                'datatype': 'CHAR(1)',
                'Name_For': 'high_value_flg',
                'Column_Name': 'high_value_flg',
                'Mapping_Type': 'Derived',
                'Transformation': "CASE WHEN ACCT_BAL > 100000 THEN 'Y' ELSE 'N' END"
            },
            # ACCT_DLY table - Goldref mappings
            {
                'Physical_Table': 'ACCT_DLY',
                'Logical_Name': 'Account Type',
                'Physical_Name': 'ACCT_TYPE',
                'datatype': 'VARCHAR(50)',
                'Name_For': 'acct_type',
                'Column_Name': 'acct_type',
                'Mapping_Type': 'Goldref',
                'Transformation': 'Lookup from ACCT_TYPE_REF table'
            },
            # TXN_DLY table - Direct mappings
            {
                'Physical_Table': 'TXN_DLY',
                'Logical_Name': 'Transaction ID',
                'Physical_Name': 'TXN_ID',
                'datatype': 'BIGINT',
                'Name_For': 'txn_id',
                'Column_Name': 'txn_id',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            },
            {
                'Physical_Table': 'TXN_DLY',
                'Logical_Name': 'Transaction Amount',
                'Physical_Name': 'TXN_AMT',
                'datatype': 'DECIMAL(15,2)',
                'Name_For': 'txn_amt',
                'Column_Name': 'txn_amt',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            },
            # TXN_DLY table - Derived mappings
            {
                'Physical_Table': 'TXN_DLY',
                'Logical_Name': 'Transaction Category',
                'Physical_Name': 'TXN_CATEGORY',
                'datatype': 'VARCHAR(50)',
                'Name_For': 'txn_category',
                'Column_Name': 'txn_category',
                'Mapping_Type': 'Derived',
                'Transformation': "CASE WHEN TXN_AMT > 1000 THEN 'HIGH_VALUE' WHEN TXN_AMT > 100 THEN 'MEDIUM_VALUE' ELSE 'LOW_VALUE' END"
            },
            # CUST_DLY table - Direct mappings
            {
                'Physical_Table': 'CUST_DLY',
                'Logical_Name': 'Customer ID',
                'Physical_Name': 'CUST_ID',
                'datatype': 'VARCHAR(20)',
                'Name_For': 'cust_id',
                'Column_Name': 'cust_id',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            },
            {
                'Physical_Table': 'CUST_DLY',
                'Logical_Name': 'Customer Name',
                'Physical_Name': 'CUST_NAME',
                'datatype': 'VARCHAR(100)',
                'Name_For': 'cust_name',
                'Column_Name': 'cust_name',
                'Mapping_Type': 'Direct',
                'Transformation': 'direct'
            }
        ]
        
        # Create DataFrame
        df = pd.DataFrame(sample_data)
        
        # Save to Excel with multiple sheets
        excel_file = self.output_dir / "sample_mapping_data.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Main mapping sheet
            df.to_excel(writer, sheet_name='datahub standard mapping', index=False)
            
            # Gold reference sheet
            goldref_data = [
                {
                    'Reference_Table': 'ACCT_TYPE_REF',
                    'Reference_Key': 'ACCT_TYPE_CODE',
                    'Reference_Value': 'ACCT_TYPE_DESC',
                    'Description': 'Account Type Reference'
                },
                {
                    'Reference_Table': 'CUST_STATUS_REF',
                    'Reference_Key': 'STATUS_CODE',
                    'Reference_Value': 'STATUS_DESC',
                    'Description': 'Customer Status Reference'
                }
            ]
            goldref_df = pd.DataFrame(goldref_data)
            goldref_df.to_excel(writer, sheet_name='goldref', index=False)
        
        logger.info(f"✅ Sample Excel file created: {excel_file}")
        return excel_file
    
    async def process_excel_file(self, excel_file: Path):
        """Process Excel file and extract mapping information"""
        logger.info("📊 Processing Excel file...")
        
        try:
            # Parse Excel file
            parser = ExcelMappingParser()
            mappings = parser.parse_excel_file(str(excel_file))
            
            # Group by table
            table_mappings = {}
            for mapping in mappings:
                table_name = mapping.physical_table
                if table_name not in table_mappings:
                    table_mappings[table_name] = []
                table_mappings[table_name].append(mapping)
            
            # Analyze mapping types
            mapping_analysis = {}
            for table_name, table_maps in table_mappings.items():
                direct_count = sum(1 for m in table_maps if m.mapping_type == 'Direct')
                derived_count = sum(1 for m in table_maps if m.mapping_type == 'Derived')
                goldref_count = sum(1 for m in table_maps if m.mapping_type == 'Goldref')
                
                mapping_analysis[table_name] = {
                    'total_fields': len(table_maps),
                    'direct_mappings': direct_count,
                    'derived_mappings': derived_count,
                    'goldref_mappings': goldref_count,
                    'mappings': table_maps
                }
            
            # Save parsed data
            parsed_data = {
                'excel_file': str(excel_file),
                'parsed_at': datetime.now().isoformat(),
                'table_mappings': mapping_analysis,
                'total_tables': len(table_mappings),
                'total_fields': sum(len(maps) for maps in table_mappings.values())
            }
            
            parsed_file = self.output_dir / "excel_parsed" / "parsed_mappings.json"
            with open(parsed_file, 'w') as f:
                json.dump(parsed_data, f, indent=2, default=str)
            
            logger.info(f"✅ Excel file processed. Found {len(table_mappings)} tables with {parsed_data['total_fields']} fields")
            self.workflow_status["outputs"]["excel_parsed"] = str(parsed_file)
            self.workflow_status["steps_completed"].append("excel_processing")
            
            return mapping_analysis
            
        except Exception as e:
            logger.error(f"❌ Excel processing failed: {str(e)}")
            self.workflow_status["errors"].append(f"Excel processing failed: {str(e)}")
            return None
    
    async def validate_metadata(self, mapping_analysis: Dict):
        """Validate metadata using the MetadataValidatorAgent"""
        logger.info("🔍 Validating metadata with AI agent...")
        
        try:
            validation_results = {}
            
            for table_name, table_info in mapping_analysis.items():
                logger.info(f"Validating table: {table_name}")
                
                # Prepare validation input
                validation_input = {
                    'document': {
                        'table_name': table_name,
                        'fields': [
                            {
                                'name': mapping.logical_name,
                                'physical_name': mapping.physical_name,
                                'data_type': mapping.datatype,
                                'mapping_type': mapping.mapping_type,
                                'transformation': mapping.transformation
                            }
                            for mapping in table_info['mappings']
                        ]
                    }
                }
                
                # Execute validation
                validation_result = await self.metadata_agent.execute(validation_input)
                
                validation_results[table_name] = {
                    'validation_result': validation_result,
                    'field_count': table_info['total_fields'],
                    'mapping_types': {
                        'direct': table_info['direct_mappings'],
                        'derived': table_info['derived_mappings'],
                        'goldref': table_info['goldref_mappings']
                    }
                }
            
            # Save validation report
            validation_report = {
                'validation_timestamp': datetime.now().isoformat(),
                'tables_validated': len(validation_results),
                'validation_results': validation_results,
                'summary': {
                    'total_tables': len(validation_results),
                    'total_fields': sum(r['field_count'] for r in validation_results.values()),
                    'validation_status': 'completed'
                }
            }
            
            validation_file = self.output_dir / "validation_reports" / f"metadata_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(validation_file, 'w') as f:
                json.dump(validation_report, f, indent=2, default=str)
            
            logger.info(f"✅ Metadata validation completed. Report saved: {validation_file}")
            self.workflow_status["outputs"]["validation_report"] = str(validation_file)
            self.workflow_status["steps_completed"].append("metadata_validation")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Metadata validation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Metadata validation failed: {str(e)}")
            return None
    
    async def generate_test_cases(self, mapping_analysis: Dict):
        """Generate comprehensive test cases for each table"""
        logger.info("🧪 Generating test cases...")
        
        try:
            test_cases = {}
            
            for table_name, table_info in mapping_analysis.items():
                logger.info(f"Generating test cases for table: {table_name}")
                
                table_test_cases = {
                    'table_name': table_name,
                    'test_scenarios': [],
                    'data_quality_tests': [],
                    'business_rule_tests': []
                }
                
                # Test scenarios based on mapping types
                if table_info['direct_mappings'] > 0:
                    table_test_cases['test_scenarios'].append({
                        'scenario': 'Direct Mapping Validation',
                        'description': 'Verify direct field mappings work correctly',
                        'test_type': 'data_integrity',
                        'priority': 'high'
                    })
                
                if table_info['derived_mappings'] > 0:
                    table_test_cases['test_scenarios'].append({
                        'scenario': 'Derived Field Calculation',
                        'description': 'Verify derived field calculations are accurate',
                        'test_type': 'business_logic',
                        'priority': 'high'
                    })
                
                if table_info['goldref_mappings'] > 0:
                    table_test_cases['test_scenarios'].append({
                        'scenario': 'Gold Reference Lookup',
                        'description': 'Verify gold reference lookups return correct values',
                        'test_type': 'data_quality',
                        'priority': 'medium'
                    })
                
                # Data quality tests
                table_test_cases['data_quality_tests'] = [
                    {
                        'test_name': 'Null Value Check',
                        'description': 'Check for unexpected null values in required fields',
                        'sql_query': f"SELECT COUNT(*) FROM {table_name} WHERE ACCT_NUM IS NULL"
                    },
                    {
                        'test_name': 'Data Type Validation',
                        'description': 'Verify data types match expected schema',
                        'sql_query': f"SELECT * FROM {table_name} WHERE ACCT_BAL NOT REGEXP '^[0-9]+(\\.[0-9]{2})?$'"
                    }
                ]
                
                # Business rule tests
                table_test_cases['business_rule_tests'] = [
                    {
                        'test_name': 'Account Balance Validation',
                        'description': 'Verify account balances are within valid range',
                        'sql_query': f"SELECT * FROM {table_name} WHERE ACCT_BAL < 0 OR ACCT_BAL > 999999999.99"
                    },
                    {
                        'test_name': 'Transaction Amount Validation',
                        'description': 'Verify transaction amounts are reasonable',
                        'sql_query': f"SELECT * FROM {table_name} WHERE TXN_AMT < 0 OR TXN_AMT > 1000000.00"
                    }
                ]
                
                test_cases[table_name] = table_test_cases
            
            # Save test cases
            test_cases_file = self.output_dir / "test_cases" / f"test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(test_cases_file, 'w') as f:
                json.dump(test_cases, f, indent=2, default=str)
            
            logger.info(f"✅ Test cases generated. Saved: {test_cases_file}")
            self.workflow_status["outputs"]["test_cases"] = str(test_cases_file)
            self.workflow_status["steps_completed"].append("test_case_generation")
            
            return test_cases
            
        except Exception as e:
            logger.error(f"❌ Test case generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Test case generation failed: {str(e)}")
            return None
    
    async def generate_code(self, mapping_analysis: Dict):
        """Generate PySpark code using the CodeGeneratorAgent"""
        logger.info("💻 Generating PySpark code...")
        
        try:
            generated_code = {}
            
            for table_name, table_info in mapping_analysis.items():
                logger.info(f"Generating code for table: {table_name}")
                
                # Prepare code generation request
                code_request = {
                    'source_schema': {
                        'name': f'{table_name}_SOURCE',
                        'fields': [
                            {
                                'name': mapping.logical_name,
                                'data_type': mapping.datatype,
                                'is_nullable': True
                            }
                            for mapping in table_info['mappings']
                        ]
                    },
                    'target_schema': {
                        'name': table_name,
                        'fields': [
                            {
                                'name': mapping.physical_name,
                                'data_type': mapping.datatype,
                                'is_nullable': True
                            }
                            for mapping in table_info['mappings']
                        ]
                    },
                    'mapping_rules': [
                        {
                            'source_field': mapping.logical_name,
                            'target_field': mapping.physical_name,
                            'transformation': mapping.transformation,
                            'mapping_type': mapping.mapping_type
                        }
                        for mapping in table_info['mappings']
                    ],
                    'code_type': 'pyspark',
                    'include_tests': True
                }
                
                # Execute code generation
                code_result = await self.code_generator_agent.execute(code_request)
                
                generated_code[table_name] = {
                    'code_result': code_result,
                    'table_info': table_info,
                    'generated_at': datetime.now().isoformat()
                }
            
            # Save generated code
            code_file = self.output_dir / "generated_code" / f"generated_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(code_file, 'w') as f:
                json.dump(generated_code, f, indent=2, default=str)
            
            # Save individual PySpark files
            for table_name, code_info in generated_code.items():
                if 'code' in code_info['code_result']:
                    pyspark_file = self.output_dir / "generated_code" / f"{table_name}_transformation.py"
                    with open(pyspark_file, 'w') as f:
                        f.write(code_info['code_result']['code'])
            
            logger.info(f"✅ Code generation completed. Saved: {code_file}")
            self.workflow_status["outputs"]["generated_code"] = str(code_file)
            self.workflow_status["steps_completed"].append("code_generation")
            
            return generated_code
            
        except Exception as e:
            logger.error(f"❌ Code generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Code generation failed: {str(e)}")
            return None
    
    async def orchestrate_workflow(self, mapping_analysis: Dict):
        """Use OrchestratorAgent to coordinate the workflow"""
        logger.info("🎯 Orchestrating complete workflow...")
        
        try:
            # Prepare workflow data
            workflow_data = {
                'workflow_type': 'full_mapping_pipeline',
                'input_data': mapping_analysis,
                'workflow_steps': [
                    'excel_processing',
                    'metadata_validation',
                    'test_case_generation',
                    'code_generation'
                ],
                'status': 'completed'
            }
            
            # Execute orchestration
            orchestration_result = await self.orchestrator_agent.execute(workflow_data)
            
            logger.info("✅ Workflow orchestration completed")
            self.workflow_status["steps_completed"].append("workflow_orchestration")
            
            return orchestration_result
            
        except Exception as e:
            logger.error(f"❌ Workflow orchestration failed: {str(e)}")
            self.workflow_status["errors"].append(f"Workflow orchestration failed: {str(e)}")
            return None
    
    async def generate_final_report(self):
        """Generate comprehensive final report"""
        logger.info("📋 Generating final report...")
        
        try:
            # Calculate workflow duration
            if self.workflow_status["start_time"] and self.workflow_status["end_time"]:
                duration = (self.workflow_status["end_time"] - self.workflow_status["start_time"]).total_seconds()
            else:
                duration = 0
            
            final_report = {
                'workflow_summary': {
                    'title': 'End-to-End Agentic Mapping AI Demo',
                    'execution_date': datetime.now().isoformat(),
                    'duration_seconds': duration,
                    'status': 'completed' if not self.workflow_status["errors"] else 'completed_with_errors',
                    'steps_completed': self.workflow_status["steps_completed"],
                    'errors': self.workflow_status["errors"]
                },
                'output_files': self.workflow_status["outputs"],
                'demo_highlights': [
                    'Complete Excel file processing with intelligent parsing',
                    'AI-powered metadata validation using MetadataValidatorAgent',
                    'Comprehensive test case generation for all mapping types',
                    'PySpark code generation with CodeGeneratorAgent',
                    'Workflow orchestration using OrchestratorAgent',
                    'End-to-end data lineage tracking'
                ],
                'next_steps': [
                    'Review generated code and test cases',
                    'Execute test cases against sample data',
                    'Customize transformations based on business requirements',
                    'Deploy to development environment',
                    'Set up monitoring and alerting'
                ]
            }
            
            # Save final report
            report_file = self.output_dir / "final_reports" / f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(final_report, f, indent=2, default=str)
            
            logger.info(f"✅ Final report generated: {report_file}")
            self.workflow_status["outputs"]["final_report"] = str(report_file)
            
            return final_report
            
        except Exception as e:
            logger.error(f"❌ Final report generation failed: {str(e)}")
            return None
    
    def display_workflow_summary(self):
        """Display workflow execution summary"""
        print("\n" + "="*80)
        print("🎯 END-TO-END AGENTIC MAPPING AI DEMO - WORKFLOW SUMMARY")
        print("="*80)
        
        print(f"\n📊 Workflow Status: {'✅ COMPLETED' if not self.workflow_status['errors'] else '⚠️ COMPLETED WITH ERRORS'}")
        print(f"⏱️  Duration: {self.workflow_status.get('duration_seconds', 0):.2f} seconds")
        print(f"📋 Steps Completed: {len(self.workflow_status['steps_completed'])}")
        
        print(f"\n🔄 Workflow Steps:")
        for i, step in enumerate(self.workflow_status['steps_completed'], 1):
            print(f"   {i}. {step.replace('_', ' ').title()}")
        
        if self.workflow_status['outputs']:
            print(f"\n📁 Output Files:")
            for key, file_path in self.workflow_status['outputs'].items():
                print(f"   • {key.replace('_', ' ').title()}: {file_path}")
        
        if self.workflow_status['errors']:
            print(f"\n❌ Errors Encountered:")
            for error in self.workflow_status['errors']:
                print(f"   • {error}")
        
        print(f"\n🎉 Demo completed successfully!")
        print("="*80)
    
    async def run_complete_workflow(self):
        """Run the complete end-to-end workflow"""
        logger.info("🚀 Starting End-to-End Agentic Mapping AI Demo")
        
        try:
            # Start timing
            self.workflow_status["start_time"] = datetime.now()
            
            # Step 1: Initialize agents
            if not await self.initialize_agents():
                raise Exception("Failed to initialize agents")
            
            # Step 2: Create sample Excel file
            excel_file = await self.create_sample_excel_file()
            
            # Step 3: Process Excel file
            mapping_analysis = await self.process_excel_file(excel_file)
            if not mapping_analysis:
                raise Exception("Excel processing failed")
            
            # Step 4: Validate metadata
            validation_results = await self.validate_metadata(mapping_analysis)
            if not validation_results:
                raise Exception("Metadata validation failed")
            
            # Step 5: Generate test cases
            test_cases = await self.generate_test_cases(mapping_analysis)
            if not test_cases:
                raise Exception("Test case generation failed")
            
            # Step 6: Generate code
            generated_code = await self.generate_code(mapping_analysis)
            if not generated_code:
                raise Exception("Code generation failed")
            
            # Step 7: Orchestrate workflow
            orchestration_result = await self.orchestrate_workflow(mapping_analysis)
            
            # Step 8: Generate final report
            final_report = await self.generate_final_report()
            
            # End timing
            self.workflow_status["end_time"] = datetime.now()
            
            # Display summary
            self.display_workflow_summary()
            
            logger.info("✅ End-to-End Demo completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {str(e)}")
            self.workflow_status["errors"].append(f"Demo execution failed: {str(e)}")
            self.workflow_status["end_time"] = datetime.now()
            return False

async def main():
    """Main entry point for the demo"""
    print("🎯 END-TO-END AGENTIC MAPPING AI DEMO")
    print("="*50)
    print("This demo showcases the complete workflow:")
    print("1. 📊 Excel file processing and parsing")
    print("2. 🔍 AI-powered metadata validation")
    print("3. 🧪 Comprehensive test case generation")
    print("4. 💻 PySpark code generation")
    print("5. 🎯 Workflow orchestration")
    print("6. 📋 End-to-end reporting")
    print("="*50)
    
    # Create and run demo
    demo_app = EndToEndDemoApp()
    success = await demo_app.run_complete_workflow()
    
    if success:
        print("\n🎉 Demo completed successfully! Check the 'demo_output' directory for all generated files.")
    else:
        print("\n❌ Demo encountered errors. Check the logs for details.")
    
    return success

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
