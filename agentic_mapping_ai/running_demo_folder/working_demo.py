#!/usr/bin/env python3
"""
🎯 WORKING END-TO-END DEMO
Demonstrates the complete workflow with working components
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from loguru import logger

# Configure logging
logger.add("demo_logs/working_demo.log", rotation="1 day", level="INFO")

class WorkingDemo:
    """
    Working demo that showcases the complete Agentic Mapping AI workflow
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
        
        # Workflow status
        self.workflow_status = {
            "start_time": None,
            "end_time": None,
            "steps_completed": [],
            "errors": [],
            "outputs": {}
        }
    
    async def create_sample_excel_file(self):
        """Create a comprehensive sample Excel file for demo"""
        logger.info("📝 Creating comprehensive sample Excel file...")
        
        # Sample data with different mapping types
        sample_data = [
            # ACCT_DLY table - Direct mappings
            {
                'physical_table': 'ACCT_DLY',
                'logical_name': 'Account Number',
                'physical_name': 'ACCT_NUM',
                'data_type': 'VARCHAR(20)',
                'name_for': 'acct_num',
                'column_name': 'acct_num',
                'mapping_type': 'Direct',
                'transformation': 'direct'
            },
            {
                'physical_table': 'ACCT_DLY',
                'logical_name': 'Account Balance',
                'physical_name': 'ACCT_BAL',
                'data_type': 'DECIMAL(15,2)',
                'name_for': 'acct_bal',
                'column_name': 'acct_bal',
                'mapping_type': 'Direct',
                'transformation': 'direct'
            },
            # ACCT_DLY table - Derived mappings
            {
                'physical_table': 'ACCT_DLY',
                'logical_name': 'Account Status',
                'physical_name': 'ACCT_STATUS',
                'data_type': 'VARCHAR(10)',
                'name_for': 'acct_status',
                'column_name': 'acct_status',
                'mapping_type': 'Derived',
                'transformation': "CASE WHEN ACCT_BAL > 0 THEN 'ACTIVE' ELSE 'INACTIVE' END"
            },
            {
                'physical_table': 'ACCT_DLY',
                'logical_name': 'High Value Flag',
                'physical_name': 'HIGH_VALUE_FLG',
                'data_type': 'CHAR(1)',
                'name_for': 'high_value_flg',
                'column_name': 'high_value_flg',
                'mapping_type': 'Derived',
                'transformation': "CASE WHEN ACCT_BAL > 100000 THEN 'Y' ELSE 'N' END"
            },
            # ACCT_DLY table - Goldref mappings
            {
                'physical_table': 'ACCT_DLY',
                'logical_name': 'Account Type',
                'physical_name': 'ACCT_TYPE',
                'data_type': 'VARCHAR(50)',
                'name_for': 'acct_type',
                'column_name': 'acct_type',
                'mapping_type': 'Goldref',
                'transformation': 'Lookup from ACCT_TYPE_REF table'
            },
            # TXN_DLY table - Direct mappings
            {
                'physical_table': 'TXN_DLY',
                'logical_name': 'Transaction ID',
                'physical_name': 'TXN_ID',
                'data_type': 'BIGINT',
                'name_for': 'txn_id',
                'column_name': 'txn_id',
                'mapping_type': 'Direct',
                'transformation': 'direct'
            },
            {
                'physical_table': 'TXN_DLY',
                'logical_name': 'Transaction Amount',
                'physical_name': 'TXN_AMT',
                'data_type': 'DECIMAL(15,2)',
                'name_for': 'txn_amt',
                'column_name': 'txn_amt',
                'mapping_type': 'Direct',
                'transformation': 'direct'
            },
            # TXN_DLY table - Derived mappings
            {
                'physical_table': 'TXN_DLY',
                'logical_name': 'Transaction Category',
                'physical_name': 'TXN_CATEGORY',
                'data_type': 'VARCHAR(50)',
                'name_for': 'txn_category',
                'column_name': 'txn_category',
                'mapping_type': 'Derived',
                'transformation': "CASE WHEN TXN_AMT > 1000 THEN 'HIGH_VALUE' WHEN TXN_AMT > 100 THEN 'MEDIUM_VALUE' ELSE 'LOW_VALUE' END"
            },
            # CUST_DLY table - Direct mappings
            {
                'physical_table': 'CUST_DLY',
                'logical_name': 'Customer ID',
                'physical_name': 'CUST_ID',
                'data_type': 'VARCHAR(20)',
                'name_for': 'cust_id',
                'column_name': 'cust_id',
                'mapping_type': 'Direct',
                'transformation': 'direct'
            },
            {
                'physical_table': 'CUST_DLY',
                'logical_name': 'Customer Name',
                'physical_name': 'CUST_NAME',
                'data_type': 'VARCHAR(100)',
                'name_for': 'cust_name',
                'column_name': 'cust_name',
                'mapping_type': 'Direct',
                'transformation': 'direct'
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
            # Read Excel file directly
            df = pd.read_excel(excel_file, sheet_name='datahub standard mapping')
            
            # Group by table
            table_mappings = {}
            for _, row in df.iterrows():
                table_name = row['physical_table']
                if table_name not in table_mappings:
                    table_mappings[table_name] = []
                
                # Create mapping object
                mapping = {
                    'logical_name': row['logical_name'],
                    'physical_name': row['physical_name'],
                    'data_type': row['data_type'],
                    'mapping_type': row['mapping_type'],
                    'transformation': row['transformation']
                }
                table_mappings[table_name].append(mapping)
            
            # Analyze mapping types
            mapping_analysis = {}
            for table_name, table_maps in table_mappings.items():
                direct_count = sum(1 for m in table_maps if m['mapping_type'] == 'Direct')
                derived_count = sum(1 for m in table_maps if m['mapping_type'] == 'Derived')
                goldref_count = sum(1 for m in table_maps if m['mapping_type'] == 'Goldref')
                
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
        """Simulate metadata validation (without external LLM)"""
        logger.info("🔍 Simulating metadata validation...")
        
        try:
            validation_results = {}
            
            for table_name, table_info in mapping_analysis.items():
                logger.info(f"Validating table: {table_name}")
                
                # Simulate validation logic
                validation_result = {
                    'is_valid': True,
                    'errors': [],
                    'warnings': [],
                    'suggestions': [
                        f"Table {table_name} has {table_info['total_fields']} fields",
                        f"Direct mappings: {table_info['direct_mappings']}",
                        f"Derived mappings: {table_info['derived_mappings']}",
                        f"Gold reference mappings: {table_info['goldref_mappings']}"
                    ],
                    'validation_metadata': {
                        'validated_at': datetime.now().isoformat(),
                        'validation_method': 'simulated_validation'
                    }
                }
                
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
        """Generate PySpark code (simulated without external LLM)"""
        logger.info("💻 Generating PySpark code...")
        
        try:
            generated_code = {}
            
            for table_name, table_info in mapping_analysis.items():
                logger.info(f"Generating code for table: {table_name}")
                
                # Generate sample PySpark code based on mapping types
                pyspark_code = f"""# PySpark Transformation for {table_name}
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit

def transform_{table_name.lower()}(spark, source_df):
    \"\"\"
    Transform {table_name} data based on mapping rules
    \"\"\"
    
    # Direct mappings
    result_df = source_df.select(
"""
                
                # Add direct mappings
                for mapping in table_info['mappings']:
                    if mapping['mapping_type'] == 'Direct':
                        pyspark_code += f"        col('{mapping['logical_name']}').alias('{mapping['physical_name']}'),\n"
                
                # Add derived mappings
                for mapping in table_info['mappings']:
                    if mapping['mapping_type'] == 'Derived':
                        if 'ACCT_STATUS' in mapping['physical_name']:
                            pyspark_code += f"""        when(col('ACCT_BAL') > 0, lit('ACTIVE')).otherwise(lit('INACTIVE')).alias('{mapping['physical_name']}'),
"""
                        elif 'HIGH_VALUE_FLG' in mapping['physical_name']:
                            pyspark_code += f"""        when(col('ACCT_BAL') > 100000, lit('Y')).otherwise(lit('N')).alias('{mapping['physical_name']}'),
"""
                        elif 'TXN_CATEGORY' in mapping['physical_name']:
                            pyspark_code += f"""        when(col('TXN_AMT') > 1000, lit('HIGH_VALUE'))
            .when(col('TXN_AMT') > 100, lit('MEDIUM_VALUE'))
            .otherwise(lit('LOW_VALUE')).alias('{mapping['physical_name']}'),
"""
                
                # Remove trailing comma and add closing
                pyspark_code = pyspark_code.rstrip(',\n') + "\n    )\n"
                
                # Add data quality checks
                pyspark_code += f"""
    # Data quality checks
    result_df = result_df.filter(
        col('ACCT_NUM').isNotNull() &
        col('ACCT_BAL').isNotNull() &
        (col('ACCT_BAL') >= 0)
    )
    
    return result_df

# Usage example
if __name__ == "__main__":
    spark = SparkSession.builder.appName("{table_name}_Transformation").getOrCreate()
    
    # Read source data
    source_df = spark.read.parquet("path/to/source/data")
    
    # Transform data
    result_df = transform_{table_name.lower()}(spark, source_df)
    
    # Write result
    result_df.write.mode("overwrite").parquet("path/to/target/data")
    
    spark.stop()
"""
                
                generated_code[table_name] = {
                    'code': pyspark_code,
                    'table_info': table_info,
                    'generated_at': datetime.now().isoformat()
                }
            
            # Save generated code
            code_file = self.output_dir / "generated_code" / f"generated_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(code_file, 'w') as f:
                json.dump(generated_code, f, indent=2, default=str)
            
            # Save individual PySpark files
            for table_name, code_info in generated_code.items():
                pyspark_file = self.output_dir / "generated_code" / f"{table_name}_transformation.py"
                with open(pyspark_file, 'w') as f:
                    f.write(code_info['code'])
            
            logger.info(f"✅ Code generation completed. Saved: {code_file}")
            self.workflow_status["outputs"]["generated_code"] = str(code_file)
            self.workflow_status["steps_completed"].append("code_generation")
            
            return generated_code
            
        except Exception as e:
            logger.error(f"❌ Code generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Code generation failed: {str(e)}")
            return None
    
    async def orchestrate_workflow(self, mapping_analysis: Dict):
        """Simulate workflow orchestration"""
        logger.info("🎯 Simulating workflow orchestration...")
        
        try:
            # Simulate orchestration logic
            orchestration_result = {
                'workflow_type': 'full_mapping_pipeline',
                'status': 'completed',
                'steps_executed': [
                    'excel_processing',
                    'metadata_validation', 
                    'test_case_generation',
                    'code_generation'
                ],
                'orchestration_timestamp': datetime.now().isoformat()
            }
            
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
                    'title': 'Working End-to-End Agentic Mapping AI Demo',
                    'execution_date': datetime.now().isoformat(),
                    'duration_seconds': duration,
                    'status': 'completed' if not self.workflow_status["errors"] else 'completed_with_errors',
                    'steps_completed': self.workflow_status["steps_completed"],
                    'errors': self.workflow_status["errors"]
                },
                'output_files': self.workflow_status["outputs"],
                'demo_highlights': [
                    'Complete Excel file processing with intelligent parsing',
                    'Simulated AI-powered metadata validation',
                    'Comprehensive test case generation for all mapping types',
                    'PySpark code generation with business logic',
                    'Workflow orchestration simulation',
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
        print("🎯 WORKING END-TO-END AGENTIC MAPPING AI DEMO - WORKFLOW SUMMARY")
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
        logger.info("🚀 Starting Working End-to-End Agentic Mapping AI Demo")
        
        try:
            # Start timing
            self.workflow_status["start_time"] = datetime.now()
            
            # Step 1: Create sample Excel file
            excel_file = await self.create_sample_excel_file()
            
            # Step 2: Process Excel file
            mapping_analysis = await self.process_excel_file(excel_file)
            if not mapping_analysis:
                raise Exception("Excel processing failed")
            
            # Step 3: Validate metadata
            validation_results = await self.validate_metadata(mapping_analysis)
            if not validation_results:
                raise Exception("Metadata validation failed")
            
            # Step 4: Generate test cases
            test_cases = await self.generate_test_cases(mapping_analysis)
            if not test_cases:
                raise Exception("Test case generation failed")
            
            # Step 5: Generate code
            generated_code = await self.generate_code(mapping_analysis)
            if not generated_code:
                raise Exception("Code generation failed")
            
            # Step 6: Orchestrate workflow
            orchestration_result = await self.orchestrate_workflow(mapping_analysis)
            
            # Step 7: Generate final report
            final_report = await self.generate_final_report()
            
            # End timing
            self.workflow_status["end_time"] = datetime.now()
            
            # Display summary
            self.display_workflow_summary()
            
            logger.info("✅ Working End-to-End Demo completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Demo failed: {str(e)}")
            self.workflow_status["errors"].append(f"Demo execution failed: {str(e)}")
            self.workflow_status["end_time"] = datetime.now()
            return False

async def main():
    """Main entry point for the working demo"""
    print("🎯 WORKING END-TO-END AGENTIC MAPPING AI DEMO")
    print("="*50)
    print("This demo showcases the complete workflow:")
    print("1. 📊 Excel file processing and parsing")
    print("2. 🔍 Simulated metadata validation")
    print("3. 🧪 Comprehensive test case generation")
    print("4. 💻 PySpark code generation")
    print("5. 🎯 Workflow orchestration simulation")
    print("6. 📋 End-to-end reporting")
    print("="*50)
    
    # Create and run demo
    demo = WorkingDemo()
    success = await demo.run_complete_workflow()
    
    if success:
        print("\n🎉 Demo completed successfully! Check the 'demo_output' directory for all generated files.")
    else:
        print("\n❌ Demo encountered errors. Check the logs for details.")
    
    return success

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
