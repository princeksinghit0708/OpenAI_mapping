"""
Production-Ready Data Mapping Application
Leverages GPT-4 with advanced prompt engineering for intelligent code generation
"""
import pandas as pd
import json
import openai
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich import print as rprint
from dotenv import load_dotenv

# Import our custom modules
from gpt4_prompt_engine import GPT4PromptEngine
from faiss_integration import FAISSIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mapping_application.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rich console for beautiful output
console = Console()

class DataMappingApplication:
    """Production-ready application for intelligent data mapping and code generation"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the application with configuration"""
        self.config = config
        self.openai_api_key = config.get('openai_api_key')
        self.excel_file = config.get('excel_file', 'Testing1.xlsx')
        self.results_dir = Path(config.get('results_dir', 'results'))
        self.output_dir = Path(config.get('output_dir', 'output'))
        
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / 'pyspark_code').mkdir(exist_ok=True)
        (self.output_dir / 'test_cases').mkdir(exist_ok=True)
        (self.output_dir / 'validation_rules').mkdir(exist_ok=True)
        (self.output_dir / 'reports').mkdir(exist_ok=True)
        
        # Initialize components
        self.prompt_engine = GPT4PromptEngine()
        self.faiss_db = FAISSIntegration(self.openai_api_key)
        self.gpt_client = None
        
        # Data storage
        self.mapping_data = None
        self.goldref_data = None
        self.table_metadata = {}
        
        logger.info("Data Mapping Application initialized successfully")
    
    def setup_openai(self) -> bool:
        """Setup OpenAI client"""
        try:
            openai.api_key = self.openai_api_key
            self.gpt_client = openai
            
            # Test connection
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            
            console.print("[green]✓ OpenAI GPT-4 connection established[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Failed to setup OpenAI: {e}[/red]")
            return False
    
    def load_excel_data(self) -> bool:
        """Load and parse Excel mapping data"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Loading Excel data...", total=None)
                
                # Read Excel file
                excel_data = pd.read_excel(self.excel_file, sheet_name=None)
                
                # Identify mapping sheet (Sheet 1)
                mapping_sheet = None
                goldref_sheet = None
                
                for sheet_name, df in excel_data.items():
                    # Check if this is the mapping sheet
                    columns_lower = [col.lower() for col in df.columns]
                    if any('standard physical table name' in col for col in columns_lower):
                        mapping_sheet = df
                        console.print(f"[green]✓ Found mapping sheet: {sheet_name}[/green]")
                    elif mapping_sheet is not None and goldref_sheet is None:
                        goldref_sheet = df
                        console.print(f"[green]✓ Found goldref sheet: {sheet_name}[/green]")
                
                if mapping_sheet is None:
                    raise ValueError("Could not identify mapping sheet in Excel file")
                
                # Standardize column names for mapping sheet
                mapping_sheet.columns = [
                    'staging_table', 'logical_name', 'column_name', 'data_type',
                    'source_table', 'source_column', 'mapping_type', 'transformation_logic'
                ]
                
                self.mapping_data = mapping_sheet
                self.goldref_data = goldref_sheet
                
                progress.update(task, completed=True)
                
            console.print(f"[cyan]Loaded {len(self.mapping_data)} mapping rules[/cyan]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Failed to load Excel data: {e}[/red]")
            logger.error(f"Excel loading error: {e}")
            return False
    
    def load_table_metadata(self) -> bool:
        """Load table metadata from JSON files in results directory"""
        try:
            if not self.results_dir.exists():
                console.print(f"[yellow]⚠ Results directory does not exist: {self.results_dir}[/yellow]")
                console.print("[yellow]Creating sample metadata files...[/yellow]")
                self._create_sample_metadata()
                
            metadata_files = list(self.results_dir.glob("*_metadata.json"))
            
            if not metadata_files:
                console.print("[yellow]⚠ No metadata files found[/yellow]")
                return True
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Loading metadata files...", total=len(metadata_files))
                
                for file_path in metadata_files:
                    try:
                        with open(file_path, 'r') as f:
                            metadata = json.load(f)
                        
                        table_name = file_path.stem.replace('_metadata', '')
                        self.table_metadata[table_name] = metadata
                        
                        progress.advance(task)
                        
                    except Exception as e:
                        console.print(f"[yellow]⚠ Error loading {file_path}: {e}[/yellow]")
            
            console.print(f"[cyan]Loaded metadata for {len(self.table_metadata)} tables[/cyan]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Failed to load metadata: {e}[/red]")
            return False
    
    def _create_sample_metadata(self) -> None:
        """Create sample metadata files for demonstration"""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample metadata for ACCT_DLY table
        acct_dly_metadata = {
            "table_name": "ACCT_DLY",
            "database": "prod_db",
            "columns": [
                {"name": "LAST_PYMT_DT", "type": "string", "nullable": True},
                {"name": "TIER_DEPST_FLG", "type": "char(1)", "nullable": False},
                {"name": "STAT_CHDT", "type": "string", "nullable": True},
                {"name": "SAL_CR_IND", "type": "char(1)", "nullable": True},
                {"name": "PROD_DESC", "type": "string", "nullable": True},
                {"name": "PROD_CDE", "type": "string", "nullable": True},
                {"name": "PRD_CTGRY_TYP_CDE", "type": "string", "nullable": True},
                {"name": "v_status", "type": "string", "nullable": True},
                {"name": "cntrycd", "type": "string", "nullable": False},
                {"name": "SRC_SYS_ID", "type": "string", "nullable": False},
                {"name": "PRD_CDE_LCL", "type": "string", "nullable": True},
                {"name": "IB_FLG", "type": "char(1)", "nullable": True},
                {"name": "HIFI_ACCT_IND", "type": "integer", "nullable": True}
            ],
            "partitions": ["biz_dt"],
            "file_format": "parquet",
            "location": "hdfs://prod/data/ACCT_DLY"
        }
        
        # Sample metadata for source tables
        im_s061_metadata = {
            "table_name": "im_s061_static_dly",
            "database": "source_db",
            "columns": [
                {"name": "d_date_last_stmt", "type": "string", "nullable": True},
                {"name": "n_mtd_salary_amt", "type": "decimal(15,2)", "nullable": True}
            ]
        }
        
        im_dynamic_metadata = {
            "table_name": "im_dynamic_dly",
            "database": "source_db", 
            "columns": [
                {"name": "n_rate_ptr", "type": "integer", "nullable": True},
                {"name": "v_hifi_indicator", "type": "integer", "nullable": True}
            ]
        }
        
        # Save metadata files
        with open(self.results_dir / 'ACCT_DLY_metadata.json', 'w') as f:
            json.dump(acct_dly_metadata, f, indent=2)
        
        with open(self.results_dir / 'im_s061_static_dly_metadata.json', 'w') as f:
            json.dump(im_s061_metadata, f, indent=2)
            
        with open(self.results_dir / 'im_dynamic_dly_metadata.json', 'w') as f:
            json.dump(im_dynamic_metadata, f, indent=2)
    
    def build_vector_database(self) -> bool:
        """Build FAISS vector database from mapping data"""
        try:
            with console.status("[bold green]Building vector database...") as status:
                # Convert DataFrame to list of dictionaries
                mappings = self.mapping_data.to_dict('records')
                
                # Add mappings to FAISS
                self.faiss_db.add_mappings(mappings)
                
                # Save index
                self.faiss_db.save('indexes/mapping_index.faiss')
                
            console.print("[green]✓ Vector database built successfully[/green]")
            console.print(f"[cyan]Statistics: {json.dumps(self.faiss_db.get_statistics(), indent=2)}[/cyan]")
            return True
            
        except Exception as e:
            console.print(f"[red]✗ Failed to build vector database: {e}[/red]")
            return False
    
    def call_gpt4(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Call GPT-4 with retry logic and error handling"""
        for attempt in range(max_retries):
            try:
                # Optimize prompt for token limit
                optimized_prompt = self.prompt_engine.optimize_prompt_for_tokens(prompt)
                
                response = self.gpt_client.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert data engineer specializing in PySpark, data validation, and ETL processes. Always provide production-ready code with comprehensive error handling."},
                        {"role": "user", "content": optimized_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=2000
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                logger.error(f"GPT-4 call failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    console.print(f"[red]✗ GPT-4 call failed after {max_retries} attempts[/red]")
                    return None
        
        return None
    
    def generate_pyspark_code(self, mapping_row: pd.Series) -> Optional[str]:
        """Generate PySpark code for a mapping using GPT-4"""
        try:
            # Convert row to dictionary
            mapping_info = mapping_row.to_dict()
            
            # Get table metadata if available
            table_meta = self.table_metadata.get(mapping_info['staging_table'], {})
            
            # Search for similar patterns
            similar_patterns = self.faiss_db.find_similar_patterns(mapping_info, top_k=3)
            
            # Build context
            context = {
                'data_volume': 'Large scale (millions of records)',
                'performance': 'Optimized for speed and memory efficiency',
                'table_metadata': table_meta,
                'similar_patterns': similar_patterns
            }
            
            # Generate prompt
            prompt = self.prompt_engine.get_pyspark_generator_prompt(mapping_info, context)
            
            # Call GPT-4
            code = self.call_gpt4(prompt)
            
            if code:
                # Save generated code
                filename = f"{mapping_info['staging_table']}_{mapping_info['column_name']}_transform.py"
                filepath = self.output_dir / 'pyspark_code' / filename
                
                with open(filepath, 'w') as f:
                    f.write(code)
                
                console.print(f"[green]✓ Generated PySpark code for {mapping_info['column_name']}[/green]")
                return code
            
        except Exception as e:
            logger.error(f"Failed to generate PySpark code: {e}")
            return None
    
    def generate_test_cases(self, mapping_row: pd.Series) -> Optional[Dict]:
        """Generate test cases for a mapping"""
        try:
            mapping_info = mapping_row.to_dict()
            
            # Generate prompt
            prompt = self.prompt_engine.get_test_generator_prompt(mapping_info)
            
            # Call GPT-4
            response = self.call_gpt4(prompt)
            
            if response:
                # Parse JSON response
                try:
                    test_cases = json.loads(response)
                except:
                    # If not valid JSON, wrap it
                    test_cases = {"raw_response": response}
                
                # Save test cases
                filename = f"{mapping_info['staging_table']}_{mapping_info['column_name']}_tests.json"
                filepath = self.output_dir / 'test_cases' / filename
                
                with open(filepath, 'w') as f:
                    json.dump(test_cases, f, indent=2)
                
                console.print(f"[green]✓ Generated test cases for {mapping_info['column_name']}[/green]")
                return test_cases
                
        except Exception as e:
            logger.error(f"Failed to generate test cases: {e}")
            return None
    
    def generate_validation_rules(self, mapping_row: pd.Series) -> Optional[Dict]:
        """Generate validation rules for a mapping"""
        try:
            mapping_info = mapping_row.to_dict()
            
            # Create mock profile data
            column_profile = {
                "column_name": mapping_info['column_name'],
                "data_type": mapping_info['data_type'],
                "null_percentage": 5.2,
                "distinct_count": 1000,
                "patterns_detected": ["standard_format"]
            }
            
            # Generate prompt
            prompt = self.prompt_engine.get_validation_prompt(column_profile, mapping_info)
            
            # Call GPT-4
            response = self.call_gpt4(prompt)
            
            if response:
                # Parse response
                try:
                    validation_rules = json.loads(response)
                except:
                    validation_rules = {"raw_response": response}
                
                # Save validation rules
                filename = f"{mapping_info['staging_table']}_{mapping_info['column_name']}_validation.json"
                filepath = self.output_dir / 'validation_rules' / filename
                
                with open(filepath, 'w') as f:
                    json.dump(validation_rules, f, indent=2)
                
                return validation_rules
                
        except Exception as e:
            logger.error(f"Failed to generate validation rules: {e}")
            return None
    
    def process_all_mappings(self) -> None:
        """Process all mappings and generate outputs"""
        if self.mapping_data is None:
            console.print("[red]No mapping data loaded[/red]")
            return
        
        # Create progress table
        progress_table = Table(title="Processing Progress")
        progress_table.add_column("Column", style="cyan")
        progress_table.add_column("PySpark Code", style="green")
        progress_table.add_column("Test Cases", style="yellow")
        progress_table.add_column("Validation", style="magenta")
        
        results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing mappings...", total=len(self.mapping_data))
            
            for idx, row in self.mapping_data.iterrows():
                column_name = row['column_name']
                
                # Generate PySpark code
                code_status = "✓" if self.generate_pyspark_code(row) else "✗"
                
                # Generate test cases
                test_status = "✓" if self.generate_test_cases(row) else "✗"
                
                # Generate validation rules
                validation_status = "✓" if self.generate_validation_rules(row) else "✗"
                
                results.append([column_name, code_status, test_status, validation_status])
                progress.advance(task)
        
        # Show results
        for result in results:
            progress_table.add_row(*result)
        
        console.print(progress_table)
    
    def generate_comprehensive_report(self) -> None:
        """Generate comprehensive analysis report"""
        try:
            # Prepare analysis data
            excel_data = {
                "mapping_sheet": self.mapping_data.to_dict('records') if self.mapping_data is not None else [],
                "goldref_sheet": self.goldref_data.to_dict('records') if self.goldref_data is not None else [],
                "table_metadata": self.table_metadata
            }
            
            # Get analysis prompt
            prompt = self.prompt_engine.get_mapping_analyzer_prompt(excel_data)
            
            console.print("[bold]Generating comprehensive analysis report...[/bold]")
            
            # Call GPT-4
            analysis = self.call_gpt4(prompt)
            
            if analysis:
                # Save analysis report
                report_path = self.output_dir / 'reports' / 'comprehensive_analysis.json'
                
                try:
                    analysis_dict = json.loads(analysis)
                except:
                    analysis_dict = {"analysis": analysis}
                
                with open(report_path, 'w') as f:
                    json.dump(analysis_dict, f, indent=2)
                
                # Generate recommendations
                rec_prompt = self.prompt_engine.get_recommendation_prompt(analysis_dict)
                recommendations = self.call_gpt4(rec_prompt)
                
                if recommendations:
                    rec_path = self.output_dir / 'reports' / 'recommendations.json'
                    
                    try:
                        rec_dict = json.loads(recommendations)
                    except:
                        rec_dict = {"recommendations": recommendations}
                    
                    with open(rec_path, 'w') as f:
                        json.dump(rec_dict, f, indent=2)
                
                console.print("[green]✓ Analysis report generated successfully[/green]")
                
        except Exception as e:
            console.print(f"[red]✗ Failed to generate report: {e}[/red]")
            logger.error(f"Report generation error: {e}")
    
    def run(self) -> None:
        """Main execution flow"""
        console.print(Panel.fit("🚀 Data Mapping Application", style="bold blue"))
        
        # Setup OpenAI
        if not self.setup_openai():
            return
        
        # Load Excel data
        if not self.load_excel_data():
            return
        
        # Load table metadata
        if not self.load_table_metadata():
            return
        
        # Build vector database
        if not self.build_vector_database():
            return
        
        # Process all mappings
        self.process_all_mappings()
        
        # Generate comprehensive report
        self.generate_comprehensive_report()
        
        console.print(Panel.fit("✅ Processing Complete!", style="bold green"))
        console.print(f"[cyan]Output directory: {self.output_dir}[/cyan]")


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    # Configuration
    config = {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'excel_file': 'Testing1 copy.xlsx',  # Using the non-empty Excel file
        'results_dir': 'results',
        'output_dir': 'output'
    }
    
    # Validate configuration
    if not config['openai_api_key']:
        console.print("[red]Error: OPENAI_API_KEY not found in environment variables[/red]")
        console.print("Please create a .env file with: OPENAI_API_KEY=your_api_key_here")
        return
    
    # Create and run application
    app = DataMappingApplication(config)
    app.run()


if __name__ == "__main__":
    main() 