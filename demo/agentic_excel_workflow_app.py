#!/usr/bin/env python3
"""
🚀 Agentic Excel Workflow Application
Complete end-to-end workflow: Excel → Validation → Testing → Code Generation
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# Add the agentic_mapping_ai to path
sys.path.append('./agentic_mapping_ai')
sys.path.append('.')

class AgenticExcelWorkflowApp:
    """
    Comprehensive agentic application that orchestrates the entire workflow:
    1. Excel Reading & Parsing
    2. Metadata Validation
    3. Testing & Quality Assurance
    4. Code Generation
    5. Workflow Orchestration
    """
    
    def __init__(self):
        """Initialize the agentic workflow application"""
        self.workflow_status = {
            'current_step': 'initialized',
            'start_time': datetime.now(),
            'steps_completed': [],
            'errors': [],
            'warnings': []
        }
        
        # Initialize agents
        self.agents = {}
        self.workflow_results = {}
        
        # Excel processing
        self.excel_data = None
        self.parsed_mappings = None
        
        # Output directories
        self.output_dirs = self._setup_output_directories()
        
        print("🚀 Agentic Excel Workflow Application Initialized")
        print("=" * 60)
    
    def _setup_output_directories(self):
        """Setup output directory structure"""
        output_dirs = {
            'excel_parsed': Path('output/excel_parsed'),
            'validation_reports': Path('output/validation_reports'),
            'test_cases': Path('output/test_cases'),
            'generated_code': Path('output/generated_code'),
            'workflow_logs': Path('output/workflow_logs'),
            'final_reports': Path('output/final_reports')
        }
        
        for dir_path in output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        return output_dirs
    
    async def initialize_agents(self):
        """Initialize all required agents"""
        print("🔧 Initializing AI Agents...")
        print("-" * 40)
        
        try:
            # Import required modules
            from agentic_mapping_ai.agents.base_agent import AgentConfig
            from agentic_mapping_ai.agents.metadata_validator import MetadataValidatorAgent
            from agentic_mapping_ai.agents.code_generator import CodeGeneratorAgent
            from agentic_mapping_ai.agents.orchestrator import OrchestratorAgent
            
            print("✅ Successfully imported agent modules")
            
            # Initialize Metadata Validator Agent
            metadata_config = AgentConfig(
                name="Excel Metadata Validator",
                description="Validates Excel mapping metadata and schemas",
                model="gpt-4",
                temperature=0.1
            )
            self.agents['metadata_validator'] = MetadataValidatorAgent(metadata_config)
            print("✅ Metadata Validator Agent initialized")
            
            # Initialize Code Generator Agent
            code_config = AgentConfig(
                name="PySpark Code Generator",
                description="Generates PySpark transformation code from Excel mappings",
                model="gpt-4",
                temperature=0.2
            )
            self.agents['code_generator'] = CodeGeneratorAgent(code_config)
            print("✅ Code Generator Agent initialized")
            
            # Initialize Orchestrator Agent
            orchestrator_config = AgentConfig(
                name="Workflow Orchestrator",
                description="Coordinates the entire Excel-to-Code workflow",
                model="gpt-4",
                temperature=0.1
            )
            self.agents['orchestrator'] = OrchestratorAgent(orchestrator_config)
            print("✅ Orchestrator Agent initialized")
            
            self.workflow_status['steps_completed'].append('agents_initialized')
            print("🎉 All agents initialized successfully!")
            
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            self.workflow_status['errors'].append(f"Agent initialization: {str(e)}")
            raise
    
    async def process_excel_file(self, excel_file_path: str):
        """Step 1: Process Excel file and extract mappings"""
        print(f"\n📊 Step 1: Processing Excel File")
        print("=" * 50)
        
        try:
            if not Path(excel_file_path).exists():
                raise FileNotFoundError(f"Excel file not found: {excel_file_path}")
            
            print(f"📁 Reading Excel file: {excel_file_path}")
            
            # Read Excel file
            excel_file = pd.ExcelFile(excel_file_path)
            print(f"📋 Found sheets: {excel_file.sheet_names}")
            
            # Read main mapping sheet
            mapping_sheet = None
            for sheet_name in excel_file.sheet_names:
                if 'mapping' in sheet_name.lower() or 'datahub' in sheet_name.lower():
                    mapping_sheet = sheet_name
                    break
            
            if not mapping_sheet:
                mapping_sheet = excel_file.sheet_names[0]
                print(f"⚠️  Using first sheet as mapping sheet: {mapping_sheet}")
            
            # Read mapping data
            mapping_df = pd.read_excel(excel_file_path, sheet_name=mapping_sheet)
            print(f"📊 Loaded {len(mapping_df)} rows from '{mapping_sheet}' sheet")
            
            # Read gold reference sheet if available
            goldref_df = None
            for sheet_name in excel_file.sheet_names:
                if 'goldref' in sheet_name.lower() or 'gold' in sheet_name.lower():
                    goldref_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
                    print(f"🥇 Loaded {len(goldref_df)} gold reference rows from '{sheet_name}' sheet")
                    break
            
            # Store Excel data
            self.excel_data = {
                'mapping_data': mapping_df,
                'goldref_data': goldref_df,
                'sheet_names': excel_file.sheet_names,
                'mapping_sheet': mapping_sheet,
                'source_file': excel_file_path
            }
            
            # Parse mappings
            self.parsed_mappings = self._parse_excel_mappings(mapping_df)
            
            # Save parsed data
            self._save_excel_parsed_data()
            
            self.workflow_status['steps_completed'].append('excel_processed')
            print("✅ Excel file processed successfully!")
            
        except Exception as e:
            print(f"❌ Excel processing failed: {e}")
            self.workflow_status['errors'].append(f"Excel processing: {str(e)}")
            raise
    
    def _parse_excel_mappings(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Parse Excel mappings into structured format"""
        print("🔍 Parsing Excel mappings...")
        
        # Detect column structure
        column_mapping = self._detect_column_structure(df)
        print(f"📋 Detected column mapping: {column_mapping}")
        
        # Parse field mappings
        field_mappings = []
        for idx, row in df.iterrows():
            mapping = {
                'row_index': idx + 1,
                'physical_table': row.get(column_mapping.get('physical_table', ''), ''),
                'logical_name': row.get(column_mapping.get('logical_name', ''), ''),
                'physical_name': row.get(column_mapping.get('physical_name', ''), ''),
                'data_type': row.get(column_mapping.get('data_type', ''), ''),
                'source_table': row.get(column_mapping.get('source_table', ''), ''),
                'source_column': row.get(column_mapping.get('source_column', ''), ''),
                'mapping_type': row.get(column_mapping.get('mapping_type', ''), ''),
                'transformation_logic': row.get(column_mapping.get('transformation_logic', ''), ''),
                'description': row.get(column_mapping.get('description', ''), '')
            }
            field_mappings.append(mapping)
        
        # Group by table
        tables = {}
        for mapping in field_mappings:
            table_name = mapping['physical_table']
            if table_name not in tables:
                tables[table_name] = []
            tables[table_name].append(mapping)
        
        parsed_data = {
            'total_mappings': len(field_mappings),
            'tables': tables,
            'column_mapping': column_mapping,
            'mapping_types': self._analyze_mapping_types(field_mappings),
            'data_types': self._analyze_data_types(field_mappings)
        }
        
        print(f"✅ Parsed {len(field_mappings)} field mappings across {len(tables)} tables")
        return parsed_data
    
    def _detect_column_structure(self, df: pd.DataFrame) -> Dict[str, str]:
        """Intelligently detect Excel column structure"""
        column_mapping = {}
        
        # Define possible column name patterns
        patterns = {
            'physical_table': ['physical table', 'table name', 'target table', 'staging table'],
            'logical_name': ['logical name', 'business name', 'description', 'field description'],
            'physical_name': ['physical name', 'column name', 'field name', 'target column'],
            'data_type': ['data type', 'type', 'datatype', 'field type'],
            'source_table': ['source table', 'source', 'from table'],
            'source_column': ['source column', 'source field', 'from column'],
            'mapping_type': ['mapping type', 'type', 'mapping', 'transformation type'],
            'transformation_logic': ['transformation', 'logic', 'formula', 'derivation'],
            'description': ['description', 'comment', 'notes', 'business description']
        }
        
        for standard_name, possible_names in patterns.items():
            for col in df.columns:
                if any(name in col.lower() for name in possible_names):
                    column_mapping[standard_name] = col
                    break
        
        return column_mapping
    
    def _analyze_mapping_types(self, mappings: List[Dict]) -> Dict[str, int]:
        """Analyze distribution of mapping types"""
        mapping_types = {}
        for mapping in mappings:
            mtype = mapping.get('mapping_type', 'Unknown')
            mapping_types[mtype] = mapping_types.get(mtype, 0) + 1
        return mapping_types
    
    def _analyze_data_types(self, mappings: List[Dict]) -> Dict[str, int]:
        """Analyze distribution of data types"""
        data_types = {}
        for mapping in mappings:
            dtype = mapping.get('data_type', 'Unknown')
            data_types[dtype] = data_types.get(dtype, 0) + 1
        return data_types
    
    def _save_excel_parsed_data(self):
        """Save parsed Excel data to output directory"""
        output_file = self.output_dirs['excel_parsed'] / 'parsed_mappings.json'
        
        with open(output_file, 'w') as f:
            json.dump(self.parsed_mappings, f, indent=2, default=str)
        
        print(f"💾 Saved parsed mappings to: {output_file}")
    
    async def validate_metadata(self):
        """Step 2: Validate metadata using the Metadata Validator Agent"""
        print(f"\n🔍 Step 2: Metadata Validation")
        print("=" * 50)
        
        try:
            if not self.parsed_mappings:
                raise ValueError("No parsed mappings available for validation")
            
            print("🤖 Metadata Validator Agent is analyzing the mappings...")
            
            # Prepare validation input
            validation_input = {
                "document": self.parsed_mappings,
                "validation_type": "excel_mapping_validation",
                "strict_mode": True,
                "context": "EBS IM DataHub Excel mapping validation"
            }
            
            # Execute validation using the agent
            metadata_agent = self.agents['metadata_validator']
            validation_result = await metadata_agent._execute_core_logic(validation_input)
            
            if validation_result and validation_result.get("validation_result"):
                validation_data = validation_result.get("validation_result", {})
                
                print("✅ Metadata validation completed!")
                print(f"📊 Validation Status: {validation_result.get('status', 'VALIDATED')}")
                
                # Save validation report
                self._save_validation_report(validation_result)
                
                # Store results
                self.workflow_results['metadata_validation'] = validation_result
                
                self.workflow_status['steps_completed'].append('metadata_validated')
                print("✅ Metadata validation step completed!")
                
            else:
                raise Exception("Metadata validation returned no results")
                
        except Exception as e:
            print(f"❌ Metadata validation failed: {e}")
            self.workflow_status['errors'].append(f"Metadata validation: {str(e)}")
            raise
    
    def _save_validation_report(self, validation_result: Dict):
        """Save validation report to output directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dirs['validation_reports'] / f'validation_report_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(validation_result, f, indent=2, default=str)
        
        print(f"💾 Saved validation report to: {output_file}")
    
    async def generate_test_cases(self):
        """Step 3: Generate test cases using AI agents"""
        print(f"\n🧪 Step 3: Test Case Generation")
        print("=" * 50)
        
        try:
            print("🤖 Generating comprehensive test cases...")
            
            # Create test cases for each table
            test_cases = {}
            
            for table_name, mappings in self.parsed_mappings['tables'].items():
                print(f"📊 Generating tests for table: {table_name}")
                
                table_test_cases = self._generate_table_test_cases(table_name, mappings)
                test_cases[table_name] = table_test_cases
            
            # Save test cases
            self._save_test_cases(test_cases)
            
            # Store results
            self.workflow_results['test_cases'] = test_cases
            
            self.workflow_status['steps_completed'].append('test_cases_generated')
            print("✅ Test case generation completed!")
            
        except Exception as e:
            print(f"❌ Test case generation failed: {e}")
            self.workflow_status['errors'].append(f"Test case generation: {str(e)}")
            raise
    
    def _generate_table_test_cases(self, table_name: str, mappings: List[Dict]) -> Dict[str, Any]:
        """Generate test cases for a specific table"""
        test_cases = {
            'table_name': table_name,
            'total_fields': len(mappings),
            'test_scenarios': [],
            'data_quality_tests': [],
            'business_rule_tests': []
        }
        
        # Generate test scenarios for each mapping type
        for mapping in mappings:
            mapping_type = mapping.get('mapping_type', 'Direct')
            
            if mapping_type == 'Direct':
                test_cases['test_scenarios'].append({
                    'field': mapping['physical_name'],
                    'test_type': 'direct_mapping',
                    'description': f"Test direct mapping from {mapping['source_column']} to {mapping['physical_name']}",
                    'expected_result': f"Value should be identical to source field {mapping['source_column']}"
                })
            
            elif mapping_type == 'Derived':
                test_cases['test_scenarios'].append({
                    'field': mapping['physical_name'],
                    'test_type': 'derived_mapping',
                    'description': f"Test derived mapping with logic: {mapping['transformation_logic']}",
                    'expected_result': "Value should match transformation logic"
                })
            
            elif mapping_type == 'Goldref':
                test_cases['test_scenarios'].append({
                    'field': mapping['physical_name'],
                    'test_type': 'goldref_lookup',
                    'description': f"Test gold reference lookup for {mapping['physical_name']}",
                    'expected_result': "Value should be found in gold reference table"
                })
        
        # Generate data quality tests
        test_cases['data_quality_tests'] = [
            {
                'test_name': 'null_check',
                'description': 'Check for unexpected null values in required fields',
                'sql_query': f"SELECT COUNT(*) FROM {table_name} WHERE required_field IS NULL"
            },
            {
                'test_name': 'data_type_validation',
                'description': 'Validate data types match expected schema',
                'sql_query': f"SELECT * FROM {table_name} WHERE CAST(field AS expected_type) IS NULL"
            }
        ]
        
        # Generate business rule tests
        test_cases['business_rule_tests'] = [
            {
                'test_name': 'account_number_format',
                'description': 'Validate account number format compliance',
                'sql_query': f"SELECT * FROM {table_name} WHERE acct_nbr NOT REGEXP '^[0-9]{{8,12}}$'"
            },
            {
                'test_name': 'currency_code_validation',
                'description': 'Validate currency codes are standard',
                'sql_query': f"SELECT * FROM {table_name} WHERE curr_cd NOT IN ('USD', 'EUR', 'GBP')"
            }
        ]
        
        return test_cases
    
    def _save_test_cases(self, test_cases: Dict):
        """Save test cases to output directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dirs['test_cases'] / f'test_cases_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(test_cases, f, indent=2, default=str)
        
        print(f"💾 Saved test cases to: {output_file}")
    
    async def generate_code(self):
        """Step 4: Generate PySpark transformation code"""
        print(f"\n💻 Step 4: Code Generation")
        print("=" * 50)
        
        try:
            print("🤖 Code Generator Agent is creating PySpark transformations...")
            
            # Generate code for each table
            generated_code = {}
            
            for table_name, mappings in self.parsed_mappings['tables'].items():
                print(f"📊 Generating code for table: {table_name}")
                
                table_code = await self._generate_table_code(table_name, mappings)
                generated_code[table_name] = table_code
            
            # Save generated code
            self._save_generated_code(generated_code)
            
            # Store results
            self.workflow_results['generated_code'] = generated_code
            
            self.workflow_status['steps_completed'].append('code_generated')
            print("✅ Code generation completed!")
            
        except Exception as e:
            print(f"❌ Code generation failed: {e}")
            self.workflow_status['errors'].append(f"Code generation: {str(e)}")
            raise
    
    async def _generate_table_code(self, table_name: str, mappings: List[Dict]) -> Dict[str, Any]:
        """Generate PySpark code for a specific table"""
        code_generator = self.agents['code_generator']
        
        # Prepare code generation request
        code_request = {
            "table_name": table_name,
            "mappings": mappings,
            "code_type": "pyspark",
            "include_tests": True,
            "optimization_level": "production"
        }
        
        # Generate code using the agent
        code_result = await code_generator._execute_core_logic(code_request)
        
        if code_result and code_result.get("generated_code"):
            return {
                'table_name': table_name,
                'pyspark_code': code_result.get("generated_code", {}),
                'transformation_logic': code_result.get("transformation_logic", {}),
                'dependencies': code_result.get("dependencies", []),
                'configuration': code_result.get("configuration", {})
            }
        else:
            # Fallback: generate basic code structure
            return self._generate_fallback_code(table_name, mappings)
    
    def _generate_fallback_code(self, table_name: str, mappings: List[Dict]) -> Dict[str, Any]:
        """Generate fallback code if agent fails"""
        pyspark_code = f"""
# PySpark Transformation for {table_name}
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def transform_{table_name.lower()}(spark: SparkSession, source_df):
    \"\"\"
    Transform source data for {table_name} table
    \"\"\"
    
    # Apply field mappings
    transformed_df = source_df.select(
"""
        
        # Add field mappings
        for mapping in mappings:
            physical_name = mapping.get('physical_name', '')
            source_column = mapping.get('source_column', '')
            mapping_type = mapping.get('mapping_type', 'Direct')
            
            if mapping_type == 'Direct' and source_column:
                pyspark_code += f"        col('{source_column}').alias('{physical_name}'),\n"
            elif mapping_type == 'Derived':
                pyspark_code += f"        expr('{mapping.get('transformation_logic', '')}').alias('{physical_name}'),\n"
            else:
                pyspark_code += f"        lit(None).alias('{physical_name}'),\n"
        
        pyspark_code += """    )
    
    return transformed_df
"""
        
        return {
            'table_name': table_name,
            'pyspark_code': pyspark_code,
            'transformation_logic': 'Fallback code generation',
            'dependencies': ['pyspark'],
            'configuration': {'fallback_generated': True}
        }
    
    def _save_generated_code(self, generated_code: Dict):
        """Save generated code to output directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_file = self.output_dirs['generated_code'] / f'generated_code_{timestamp}.json'
        with open(json_file, 'w') as f:
            json.dump(generated_code, f, indent=2, default=str)
        
        # Save individual PySpark files
        for table_name, code_data in generated_code.items():
            if 'pyspark_code' in code_data:
                py_file = self.output_dirs['generated_code'] / f'{table_name.lower()}_transformation.py'
                with open(py_file, 'w') as f:
                    f.write(code_data['pyspark_code'])
        
        print(f"💾 Saved generated code to: {self.output_dirs['generated_code']}")
    
    async def orchestrate_workflow(self):
        """Step 5: Orchestrate the entire workflow using the Orchestrator Agent"""
        print(f"\n🎯 Step 5: Workflow Orchestration")
        print("=" * 50)
        
        try:
            print("🤖 Orchestrator Agent is coordinating the workflow...")
            
            orchestrator = self.agents['orchestrator']
            
            # Prepare workflow data
            workflow_data = {
                "workflow_type": "full_mapping_pipeline",
                "excel_data": self.excel_data,
                "parsed_mappings": self.parsed_mappings,
                "validation_results": self.workflow_results.get('metadata_validation'),
                "test_cases": self.workflow_results.get('test_cases'),
                "generated_code": self.workflow_results.get('generated_code')
            }
            
            # Execute orchestration
            orchestration_result = await orchestrator._execute_core_logic(workflow_data)
            
            if orchestration_result and orchestration_result.get("success"):
                print("✅ Workflow orchestration completed!")
                
                # Store orchestration results
                self.workflow_results['orchestration'] = orchestration_result
                
                self.workflow_status['steps_completed'].append('workflow_orchestrated')
                print("✅ Workflow orchestration step completed!")
                
            else:
                print("⚠️  Workflow orchestration completed with warnings")
                
        except Exception as e:
            print(f"❌ Workflow orchestration failed: {e}")
            self.workflow_status['errors'].append(f"Workflow orchestration: {str(e)}")
            # Don't raise here as this is the final step
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print(f"\n📊 Generating Final Report")
        print("=" * 50)
        
        try:
            # Prepare report data
            report_data = {
                'workflow_summary': {
                    'start_time': self.workflow_status['start_time'].isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'total_steps': 5,
                    'completed_steps': len(self.workflow_status['steps_completed']),
                    'errors': self.workflow_status['errors'],
                    'warnings': self.workflow_status['warnings']
                },
                'excel_processing': {
                    'source_file': self.excel_data.get('source_file') if self.excel_data else None,
                    'total_mappings': self.parsed_mappings.get('total_mappings') if self.parsed_mappings else 0,
                    'tables_processed': len(self.parsed_mappings.get('tables', {})) if self.parsed_mappings else 0
                },
                'agent_performance': {
                    'agents_initialized': len(self.agents),
                    'workflow_results': list(self.workflow_results.keys())
                },
                'output_files': {
                    'excel_parsed': str(self.output_dirs['excel_parsed']),
                    'validation_reports': str(self.output_dirs['validation_reports']),
                    'test_cases': str(self.output_dirs['test_cases']),
                    'generated_code': str(self.output_dirs['generated_code'])
                }
            }
            
            # Save final report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = self.output_dirs['final_reports'] / f'workflow_report_{timestamp}.json'
            
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            print(f"💾 Final report saved to: {report_file}")
            
            # Display summary
            self._display_workflow_summary(report_data)
            
        except Exception as e:
            print(f"❌ Final report generation failed: {e}")
    
    def _display_workflow_summary(self, report_data: Dict):
        """Display workflow summary"""
        print("\n" + "=" * 60)
        print("🎉 WORKFLOW EXECUTION SUMMARY")
        print("=" * 60)
        
        summary = report_data['workflow_summary']
        print(f"⏱️  Duration: {summary['start_time']} → {summary['end_time']}")
        print(f"📊 Steps: {summary['completed_steps']}/{summary['total_steps']} completed")
        
        if summary['errors']:
            print(f"❌ Errors: {len(summary['errors'])}")
            for error in summary['errors']:
                print(f"   • {error}")
        
        if summary['warnings']:
            print(f"⚠️  Warnings: {len(summary['warnings'])}")
            for warning in summary['warnings']:
                print(f"   • {warning}")
        
        excel_info = report_data['excel_processing']
        print(f"\n📊 Excel Processing:")
        print(f"   • Source: {excel_info['source_file']}")
        print(f"   • Mappings: {excel_info['total_mappings']}")
        print(f"   • Tables: {excel_info['tables_processed']}")
        
        agent_info = report_data['agent_performance']
        print(f"\n🤖 Agent Performance:")
        print(f"   • Agents: {agent_info['agents_initialized']}")
        print(f"   • Results: {', '.join(agent_info['workflow_results'])}")
        
        print(f"\n📁 Output Files:")
        for output_type, path in report_data['output_files'].items():
            print(f"   • {output_type}: {path}")
        
        print("\n🎯 Next Steps:")
        print("   • Review generated code in output/generated_code/")
        print("   • Check validation reports in output/validation_reports/")
        print("   • Run test cases from output/test_cases/")
        print("   • Deploy PySpark transformations to your cluster")
    
    async def run_complete_workflow(self, excel_file_path: str):
        """Run the complete agentic workflow"""
        print("🚀 Starting Complete Agentic Excel Workflow")
        print("=" * 60)
        
        try:
            # Step 1: Initialize agents
            await self.initialize_agents()
            
            # Step 2: Process Excel file
            await self.process_excel_file(excel_file_path)
            
            # Step 3: Validate metadata
            await self.validate_metadata()
            
            # Step 4: Generate test cases
            await self.generate_test_cases()
            
            # Step 5: Generate code
            await self.generate_code()
            
            # Step 6: Orchestrate workflow
            await self.orchestrate_workflow()
            
            # Step 7: Generate final report
            self.generate_final_report()
            
            print("\n🎉 Complete workflow executed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Workflow execution failed: {e}")
            self.workflow_status['errors'].append(f"Workflow execution: {str(e)}")
            
            # Generate error report
            self.generate_final_report()
            return False

async def main():
    """Main entry point"""
    print("🚀 Agentic Excel Workflow Application")
    print("=" * 50)
    
    # Check prerequisites
    if not Path("agentic_mapping_ai/agents/metadata_validator.py").exists():
        print("❌ agentic_mapping_ai not found!")
        print("💡 Please run this from the demo directory")
        return 1
    
    # Get Excel file path
    excel_file = input("Enter path to Excel file (or press Enter for sample): ").strip()
    
    if not excel_file:
        # Create sample Excel file
        print("📊 Creating sample Excel file...")
        try:
            from create_sample_excel import create_sample_excel
            excel_file = str(create_sample_excel())
        except Exception as e:
            print(f"❌ Failed to create sample Excel: {e}")
            return 1
    
    if not Path(excel_file).exists():
        print(f"❌ Excel file not found: {excel_file}")
        return 1
    
    print(f"📁 Using Excel file: {excel_file}")
    
    # Initialize and run workflow
    app = AgenticExcelWorkflowApp()
    
    try:
        success = await app.run_complete_workflow(excel_file)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n👋 Workflow interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except Exception as e:
        print(f"❌ Failed to run workflow: {e}")
        sys.exit(1)
