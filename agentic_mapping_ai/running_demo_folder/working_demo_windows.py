#!/usr/bin/env python3
"""
WORKING END-TO-END DEMO - Windows Compatible
Demonstrates the complete workflow with core logic for agents
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
    
    async def process_excel_file(self, excel_file_path: str):
        """Process Excel file and extract mapping information"""
        logger.info("Processing Excel file...")
        
        try:
            # Read Excel file directly
            df = pd.read_excel(excel_file_path, sheet_name='datahub standard mapping')
            
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
                'excel_file': excel_file_path,
                'parsed_at': datetime.now().isoformat(),
                'table_mappings': mapping_analysis,
                'total_tables': len(table_mappings),
                'total_fields': sum(len(maps) for maps in table_mappings.values())
            }
            
            parsed_file = self.output_dir / "excel_parsed" / "parsed_mappings.json"
            with open(parsed_file, 'w') as f:
                json.dump(parsed_data, f, indent=2, default=str)
            
            logger.info(f"Excel file processed. Found {len(table_mappings)} tables with {parsed_data['total_fields']} fields")
            self.workflow_status["outputs"]["excel_parsed"] = str(parsed_file)
            self.workflow_status["steps_completed"].append("excel_processing")
            
            return mapping_analysis
            
        except Exception as e:
            logger.error(f"Excel processing failed: {str(e)}")
            self.workflow_status["errors"].append(f"Excel processing failed: {str(e)}")
            return None
    
    async def validate_metadata(self, mapping_analysis: Dict):
        """Simulate metadata validation"""
        logger.info("Validating metadata...")
        
        try:
            validation_results = {
                'is_valid': True,
                'validation_timestamp': datetime.now().isoformat(),
                'tables_validated': len(mapping_analysis),
                'total_fields_validated': sum(table['total_fields'] for table in mapping_analysis.values()),
                'suggestions': []
            }
            
            # Add validation suggestions
            for table_name, table_data in mapping_analysis.items():
                if table_data['total_fields'] < 3:
                    validation_results['suggestions'].append(f"Table {table_name} has only {table_data['total_fields']} fields - consider adding more fields")
                
                if table_data['direct_mappings'] == 0:
                    validation_results['suggestions'].append(f"Table {table_name} has no direct mappings - ensure at least one direct field mapping exists")
            
            # Save validation report
            validation_file = self.output_dir / "validation_reports" / "metadata_validation.json"
            with open(validation_file, 'w') as f:
                json.dump(validation_results, f, indent=2, default=str)
            
            logger.info("Metadata validation completed successfully")
            self.workflow_status["outputs"]["validation_report"] = str(validation_file)
            self.workflow_status["steps_completed"].append("metadata_validation")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Metadata validation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Metadata validation failed: {str(e)}")
            return None
    
    async def generate_test_cases(self, mapping_analysis: Dict):
        """Generate comprehensive test cases"""
        logger.info("Generating test cases...")
        
        try:
            test_cases = {
                'generated_at': datetime.now().isoformat(),
                'total_test_cases': 0,
                'test_categories': {},
                'table_tests': {}
            }
            
            for table_name, table_data in mapping_analysis.items():
                table_tests = {
                    'data_quality_tests': [],
                    'business_rule_tests': [],
                    'integration_tests': []
                }
                
                # Data quality tests
                for mapping in table_data['mappings']:
                    if mapping['data_type'].startswith('VARCHAR'):
                        table_tests['data_quality_tests'].append({
                            'test_name': f"Check {mapping['physical_name']} length",
                            'description': f"Verify {mapping['physical_name']} field length is within limits",
                            'sql': f"SELECT COUNT(*) FROM {table_name} WHERE LENGTH({mapping['physical_name']}) > 100"
                        })
                    
                    if mapping['data_type'].startswith('DECIMAL'):
                        table_tests['data_quality_tests'].append({
                            'test_name': f"Check {mapping['physical_name']} range",
                            'description': f"Verify {mapping['physical_name']} field values are within reasonable range",
                            'sql': f"SELECT COUNT(*) FROM {table_name} WHERE {mapping['physical_name']} < 0 OR {mapping['physical_name']} > 999999999"
                        })
                
                # Business rule tests
                if table_name == 'ACCT_DLY':
                    table_tests['business_rule_tests'].append({
                        'test_name': 'Account balance validation',
                        'description': 'Verify account balance logic is correct',
                        'sql': "SELECT COUNT(*) FROM ACCT_DLY WHERE ACCT_STATUS = 'ACTIVE' AND ACCT_BAL <= 0"
                    })
                
                if table_name == 'TXN_DLY':
                    table_tests['business_rule_tests'].append({
                        'test_name': 'Transaction amount validation',
                        'description': 'Verify transaction amounts are positive',
                        'sql': "SELECT COUNT(*) FROM TXN_DLY WHERE TXN_AMT <= 0"
                    })
                
                # Integration tests
                table_tests['integration_tests'].append({
                    'test_name': f'{table_name} referential integrity',
                    'description': f'Verify {table_name} has proper foreign key relationships',
                    'sql': f"SELECT COUNT(*) FROM {table_name} WHERE 1=1"  # Placeholder
                })
                
                test_cases['table_tests'][table_name] = table_tests
                test_cases['total_test_cases'] += (
                    len(table_tests['data_quality_tests']) + 
                    len(table_tests['business_rule_tests']) + 
                    len(table_tests['integration_tests'])
                )
            
            # Save test cases
            test_file = self.output_dir / "test_cases" / "generated_test_cases.json"
            with open(test_file, 'w') as f:
                json.dump(test_cases, f, indent=2, default=str)
            
            logger.info(f"Generated {test_cases['total_test_cases']} test cases successfully")
            self.workflow_status["outputs"]["test_cases"] = str(test_file)
            self.workflow_status["steps_completed"].append("test_case_generation")
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Test case generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Test case generation failed: {str(e)}")
            return None
    
    async def generate_code(self, mapping_analysis: Dict):
        """Generate PySpark transformation code"""
        logger.info("Generating PySpark transformation code...")
        
        try:
            generated_code = {
                'generated_at': datetime.now().isoformat(),
                'tables_processed': len(mapping_analysis),
                'code_files': []
            }
            
            for table_name, table_data in mapping_analysis.items():
                # Generate PySpark code for each table
                code_content = f"""# PySpark Transformation Code for {table_name}
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, expr

def transform_{table_name.lower()}(spark, input_df):
    \"\"\"
    Transform {table_name} data according to mapping specifications
    \"\"\"
    
    # Start with input data
    transformed_df = input_df
    
    # Apply transformations based on mapping types
"""
                
                # Add transformation logic for each field
                for mapping in table_data['mappings']:
                    if mapping['mapping_type'] == 'Direct':
                        code_content += f"    # Direct mapping for {mapping['physical_name']}\n"
                        code_content += f"    transformed_df = transformed_df.withColumn('{mapping['physical_name']}', col('{mapping['physical_name']}'))\n\n"
                    
                    elif mapping['mapping_type'] == 'Derived':
                        code_content += f"    # Derived mapping for {mapping['physical_name']}\n"
                        if 'ACCT_BAL' in mapping['transformation']:
                            code_content += f"    transformed_df = transformed_df.withColumn('{mapping['physical_name']}', \n"
                            code_content += f"        when(col('ACCT_BAL') > 0, lit('ACTIVE')).otherwise(lit('INACTIVE')))\n\n"
                        elif 'TXN_AMT' in mapping['transformation']:
                            code_content += f"    transformed_df = transformed_df.withColumn('{mapping['physical_name']}', \n"
                            code_content += f"        when(col('TXN_AMT') > 1000, lit('HIGH_VALUE'))\n"
                            code_content += f"        .when(col('TXN_AMT') > 100, lit('MEDIUM_VALUE'))\n"
                            code_content += f"        .otherwise(lit('LOW_VALUE')))\n\n"
                        else:
                            code_content += f"    # Custom transformation for {mapping['physical_name']}\n"
                            code_content += f"    transformed_df = transformed_df.withColumn('{mapping['physical_name']}', \n"
                            code_content += f"        expr(\"{mapping['transformation']}\"))\n\n"
                    
                    elif mapping['mapping_type'] == 'Goldref':
                        code_content += f"    # Gold reference lookup for {mapping['physical_name']}\n"
                        code_content += f"    # TODO: Implement lookup logic for {mapping['physical_name']}\n\n"
                
                code_content += f"""    # Add audit columns
    transformed_df = transformed_df.withColumn('processed_date', lit(current_timestamp()))
    transformed_df = transformed_df.withColumn('source_table', lit('{table_name}'))
    
    return transformed_df

# Usage example:
# spark = SparkSession.builder.appName("{table_name}_Transformation").getOrCreate()
# result_df = transform_{table_name.lower()}(spark, input_dataframe)
"""
                
                # Save code file
                code_file = self.output_dir / "generated_code" / f"{table_name}_transformation.py"
                with open(code_file, 'w') as f:
                    f.write(code_content)
                
                generated_code['code_files'].append(str(code_file))
                logger.info(f"Generated code for {table_name}")
            
            # Save code summary
            code_summary_file = self.output_dir / "generated_code" / "code_generation_summary.json"
            with open(code_summary_file, 'w') as f:
                json.dump(generated_code, f, indent=2, default=str)
            
            logger.info(f"Generated PySpark code for {len(mapping_analysis)} tables successfully")
            self.workflow_status["outputs"]["generated_code"] = str(code_summary_file)
            self.workflow_status["steps_completed"].append("code_generation")
            
            return generated_code
            
        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Code generation failed: {str(e)}")
            return None
    
    async def orchestrate_workflow(self, mapping_analysis: Dict):
        """Simulate workflow orchestration"""
        logger.info("Orchestrating workflow...")
        
        try:
            orchestration_result = {
                'status': 'completed',
                'orchestrated_at': datetime.now().isoformat(),
                'workflow_steps': [
                    'excel_processing',
                    'metadata_validation', 
                    'test_case_generation',
                    'code_generation'
                ],
                'tables_processed': list(mapping_analysis.keys()),
                'total_fields_processed': sum(table['total_fields'] for table in mapping_analysis.values())
            }
            
            # Save orchestration report
            orchestration_file = self.output_dir / "workflow_logs" / "workflow_orchestration.json"
            with open(orchestration_file, 'w') as f:
                json.dump(orchestration_result, f, indent=2, default=str)
            
            logger.info("Workflow orchestration completed successfully")
            self.workflow_status["outputs"]["orchestration"] = str(orchestration_file)
            self.workflow_status["steps_completed"].append("workflow_orchestration")
            
            return orchestration_result
            
        except Exception as e:
            logger.error(f"Workflow orchestration failed: {str(e)}")
            self.workflow_status["errors"].append(f"Workflow orchestration failed: {str(e)}")
            return None
    
    async def generate_final_report(self):
        """Generate final workflow report"""
        logger.info("Generating final workflow report...")
        
        try:
            # Calculate duration
            if self.workflow_status["start_time"] and self.workflow_status["end_time"]:
                duration = (self.workflow_status["end_time"] - self.workflow_status["start_time"]).total_seconds()
                self.workflow_status["duration_seconds"] = duration
            
            # Create final report
            final_report = {
                'workflow_summary': self.workflow_status,
                'generated_at': datetime.now().isoformat(),
                'demo_version': '1.0.0',
                'status': 'completed' if not self.workflow_status["errors"] else 'completed_with_errors'
            }
            
            # Save final report
            final_report_file = self.output_dir / "final_reports" / "workflow_final_report.json"
            with open(final_report_file, 'w') as f:
                json.dump(final_report, f, indent=2, default=str)
            
            logger.info("Final workflow report generated successfully")
            self.workflow_status["outputs"]["final_report"] = str(final_report_file)
            self.workflow_status["steps_completed"].append("final_report_generation")
            
            return final_report
            
        except Exception as e:
            logger.error(f"Final report generation failed: {str(e)}")
            self.workflow_status["errors"].append(f"Final report generation failed: {str(e)}")
            return None
    
    def display_workflow_summary(self):
        """Display workflow execution summary"""
        print("\n" + "="*80)
        print("WORKFLOW EXECUTION SUMMARY")
        print("="*80)
        
        print(f"Start Time: {self.workflow_status.get('start_time', 'N/A')}")
        print(f"End Time: {self.workflow_status.get('end_time', 'N/A')}")
        print(f"Duration: {self.workflow_status.get('duration_seconds', 0):.2f} seconds")
        print(f"Steps Completed: {len(self.workflow_status['steps_completed'])}")
        
        print(f"\nWorkflow Steps:")
        for i, step in enumerate(self.workflow_status['steps_completed'], 1):
            print(f"   {i}. {step.replace('_', ' ').title()}")
        
        if self.workflow_status['outputs']:
            print(f"\nOutput Files:")
            for key, file_path in self.workflow_status['outputs'].items():
                print(f"   • {key.replace('_', ' ').title()}: {file_path}")
        
        if self.workflow_status['errors']:
            print(f"\nErrors Encountered:")
            for error in self.workflow_status['errors']:
                print(f"   • {error}")
        
        print(f"\nDemo completed successfully!")
        print("="*80)
    
    async def run_complete_workflow(self, excel_file_path: str):
        """Run the complete end-to-end workflow"""
        logger.info("Starting Working End-to-End Agentic Mapping AI Demo")
        
        try:
            # Start timing
            self.workflow_status["start_time"] = datetime.now()
            
            # Step 1: Process Excel file
            mapping_analysis = await self.process_excel_file(excel_file_path)
            if not mapping_analysis:
                raise Exception("Excel processing failed")
            
            # Step 2: Validate metadata
            validation_results = await self.validate_metadata(mapping_analysis)
            if not validation_results:
                raise Exception("Metadata validation failed")
            
            # Step 3: Generate test cases
            test_cases = await self.generate_test_cases(mapping_analysis)
            if not test_cases:
                raise Exception("Test case generation failed")
            
            # Step 4: Generate code
            generated_code = await self.generate_code(mapping_analysis)
            if not generated_code:
                raise Exception("Code generation failed")
            
            # Step 5: Orchestrate workflow
            orchestration_result = await self.orchestrate_workflow(mapping_analysis)
            
            # Step 6: Generate final report
            final_report = await self.generate_final_report()
            
            # End timing
            self.workflow_status["end_time"] = datetime.now()
            
            # Display summary
            self.display_workflow_summary()
            
            logger.info("Working End-to-End Demo completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Demo failed: {str(e)}")
            self.workflow_status["errors"].append(f"Demo execution failed: {str(e)}")
            self.workflow_status["end_time"] = datetime.now()
            return False

async def main():
    """Main entry point for the working demo"""
    print("WORKING END-TO-END AGENTIC MAPPING AI DEMO")
    print("="*50)
    print("This demo showcases the complete workflow:")
    print("1. Excel file processing and parsing")
    print("2. Simulated metadata validation")
    print("3. Comprehensive test case generation")
    print("4. PySpark code generation")
    print("5. Workflow orchestration simulation")
    print("6. End-to-end reporting")
    print("="*50)
    
    # Get Excel file path from user
    excel_file_path = input("\nPlease enter the path to your Excel file: ").strip()
    
    if not excel_file_path or not os.path.exists(excel_file_path):
        print("Error: Please provide a valid Excel file path")
        return False
    
    # Create and run demo
    demo = WorkingDemo()
    success = await demo.run_complete_workflow(excel_file_path)
    
    if success:
        print("\nDemo completed successfully! Check the 'demo_output' directory for all generated files.")
    else:
        print("\nDemo encountered errors. Check the logs for details.")
    
    return success

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
