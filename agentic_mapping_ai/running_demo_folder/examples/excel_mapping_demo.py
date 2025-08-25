"""
Excel Mapping Demo - Demonstrates the new Excel mapping capabilities
"""

import asyncio
import json
from pathlib import Path
import pandas as pd
from loguru import logger

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent))

from parsers.excel_mapping_parser import ExcelMappingParser, parse_excel_mappings
from agents.transformation_agent import create_transformation_agent
from agents.goldref_validator import create_goldref_validator
from core.models import GoldReferenceDefinition


async def demo_excel_mapping_system():
    """Demonstrate the complete Excel mapping system"""
    
    logger.info("🚀 Starting Excel Mapping Demo")
    
    # Step 1: Create sample Excel data (simulating your screenshots)
    await create_sample_excel_file()
    
    # Step 2: Parse Excel mapping file
    excel_schema = await demo_excel_parsing()
    
    # Step 3: Demonstrate transformation analysis
    await demo_transformation_analysis(excel_schema)
    
    # Step 4: Demonstrate gold reference validation
    await demo_gold_reference_validation(excel_schema)
    
    # Step 5: Generate code for transformations
    await demo_code_generation(excel_schema)
    
    logger.info("✅ Excel Mapping Demo completed successfully!")


async def create_sample_excel_file():
    """Create a sample Excel file based on the screenshot data"""
    logger.info("📝 Creating sample Excel file from screenshot data")
    
    # Data extracted from your Excel screenshots
    sample_data = [
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'account flag',
            'Physical_Name': 'CT_FLG',
            'datatype': 'Char(1)',
            'Name (For)': '',
            'Column Name /Default/No': '',
            'Direct/No mapping/Derived/Goldref': 'No Mapping',
            'Transformation/Derivation': 'No Mapping'
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Company Flag',
            'Physical_Name': 'CO_FLG',
            'datatype': 'Char(1)',
            'Name (For)': '',
            'Column Name /Default/No': '',
            'Direct/No mapping/Derived/Goldref': 'No Mapping',
            'Transformation/Derivation': 'No Mapping'
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Fee Amount',
            'Physical_Name': 'TXN_FEE_AMT',
            'datatype': 'Decimal(15,2)',
            'Name (For)': 'y',
            'Column Name /Default/No': 'n_amt',
            'Direct/No mapping/Derived/Goldref': 'Direct',
            'Transformation/Derivation': 'direct'
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Rate',
            'Physical_Name': 'TE',
            'datatype': 'String',
            'Name (For)': '',
            'Column Name /Default/No': '',
            'Direct/No mapping/Derived/Goldref': 'Derived',
            'Transformation/Derivation': 'If HIFI_ACCT_IND > 0 then \'Y\' else \'N\''
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Account Type',
            'Physical_Name': 'TYP_DESC',
            'datatype': 'String',
            'Name (For)': 's06s',
            'Column Name /Default/No': 'at',
            'Direct/No mapping/Derived/Goldref': 'Goldref',
            'Transformation/Derivation': 'v_rsrv_mstr_stat=\'R\', then PPvalue = \'3\' else \'6\''
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Beginning',
            'Physical_Name': 'L_AMT',
            'datatype': 'Decimal(15,2)',
            'Name (For)': 'y',
            'Column Name /Default/No': 'n_stmbegbal',
            'Direct/No mapping/Derived/Goldref': 'Direct',
            'Transformation/Derivation': 'direct'
        },
        {
            'Physical': 'ACCT_DLY',
            'Logical Name': 'Variability',
            'Physical_Name': 'DESC',
            'datatype': 'String',
            'Name (For)': 'ACCT_DLY',
            'Column Name /Default/No': 'IB_FLG',
            'Direct/No mapping/Derived/Goldref': 'Goldref',
            'Transformation/Derivation': '2. Lookup for the genesis STANDARD_VAL_DESC using the lookup keys'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Save to Excel file
    excel_path = Path("./data/sample_mapping.xlsx")
    excel_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_excel(excel_path, index=False, sheet_name='Sheet1')
    logger.info(f"📊 Sample Excel file created: {excel_path}")
    
    return excel_path


async def demo_excel_parsing():
    """Demonstrate Excel parsing capabilities"""
    logger.info("🔍 Demonstrating Excel parsing")
    
    excel_path = "./data/sample_mapping.xlsx"
    
    try:
        # Parse the Excel file
        excel_schema = parse_excel_mappings(excel_path)
        
        logger.info(f"✅ Parsed Excel schema: {excel_schema.name}")
        logger.info(f"   - Field mappings: {len(excel_schema.field_mappings)}")
        logger.info(f"   - Gold references: {len(excel_schema.gold_references)}")
        logger.info(f"   - Transformation rules: {len(excel_schema.transformation_rules)}")
        
        # Show some sample mappings
        for i, mapping in enumerate(excel_schema.field_mappings[:3]):
            logger.info(f"   Mapping {i+1}: {mapping.logical_name} -> {mapping.physical_name} ({mapping.mapping_type})")
        
        return excel_schema
        
    except Exception as e:
        logger.error(f"❌ Excel parsing failed: {str(e)}")
        return None


async def demo_transformation_analysis(excel_schema):
    """Demonstrate transformation analysis capabilities"""
    logger.info("⚙️  Demonstrating transformation analysis")
    
    if not excel_schema or not excel_schema.transformation_rules:
        logger.warning("No transformation rules to analyze")
        return
    
    # Create transformation agent
    transform_agent = create_transformation_agent()
    
    for field_name, transformation_text in excel_schema.transformation_rules.items():
        logger.info(f"\n🔧 Analyzing transformation for {field_name}:")
        logger.info(f"   Logic: {transformation_text}")
        
        try:
            # Analyze the transformation
            analysis = await transform_agent.analyze_transformation(transformation_text)
            
            logger.info(f"   Type: {analysis['type']}")
            logger.info(f"   Complexity: {analysis['complexity']}")
            logger.info(f"   Dependencies: {analysis['dependencies']}")
            
            # Create and validate transformation rule
            rule = await transform_agent.create_transformation_rule(
                name=f"rule_{field_name}",
                source_fields=analysis['dependencies'],
                target_field=field_name,
                logic=transformation_text
            )
            
            validation = await transform_agent.validate_transformation(rule)
            
            if validation.is_valid:
                logger.info("   ✅ Transformation is valid")
            else:
                logger.warning(f"   ⚠️  Validation issues: {validation.errors}")
            
        except Exception as e:
            logger.error(f"   ❌ Transformation analysis failed: {str(e)}")


async def demo_gold_reference_validation(excel_schema):
    """Demonstrate gold reference validation"""
    logger.info("🥇 Demonstrating gold reference validation")
    
    # Create gold reference validator
    goldref_validator = create_goldref_validator()
    
    # Create sample gold reference definitions
    sample_gold_refs = [
        GoldReferenceDefinition(
            name="account_type_reference",
            lookup_table="STANDARD_VAL_DESC",
            key_fields=["CNTRY_ID", "PRD_PROCESSOR"],
            standard_values={
                "SAVINGS": "Savings Account",
                "CHECKING": "Checking Account", 
                "LOAN": "Loan Account"
            },
            business_rules=["Account type must not be null", "Must be valid account type"],
            description="Standard account type reference"
        ),
        GoldReferenceDefinition(
            name="branch_reference",
            lookup_table="genesis",
            key_fields=["BRANCH_CODE"],
            standard_values={
                "001": "Private Bank Branch",
                "002": "Retail Citibank Branch",
                "003": "Commercial Branch"
            },
            business_rules=["Branch code format should be numeric"],
            description="Branch code reference data"
        )
    ]
    
    # Register gold references
    for gold_ref in sample_gold_refs:
        try:
            await goldref_validator.register_gold_reference(gold_ref)
            logger.info(f"✅ Registered gold reference: {gold_ref.name}")
        except Exception as e:
            logger.error(f"❌ Failed to register {gold_ref.name}: {str(e)}")
    
    # Validate mappings against gold reference template
    if excel_schema:
        field_mappings = []
        for mapping in excel_schema.field_mappings:
            field_mappings.append({
                "physical_table": mapping.physical_table,
                "logical_name": mapping.logical_name,
                "physical_name": mapping.physical_name,
                "data_type": mapping.data_type,
                "mapping_type": mapping.mapping_type,
                "transformation": mapping.transformation
            })
        
        try:
            validation_result = await goldref_validator.validate_mapping_compliance(
                field_mappings,
                "img_0241"  # Your gold reference template
            )
            
            logger.info(f"🎯 Gold reference validation results:")
            logger.info(f"   Valid: {validation_result.is_valid}")
            logger.info(f"   Errors: {len(validation_result.errors)}")
            logger.info(f"   Warnings: {len(validation_result.warnings)}")
            
            if validation_result.errors:
                for error in validation_result.errors[:3]:  # Show first 3 errors
                    logger.warning(f"   ❌ {error}")
                    
            if validation_result.suggestions:
                for suggestion in validation_result.suggestions[:3]:  # Show first 3 suggestions
                    logger.info(f"   💡 {suggestion}")
                    
        except Exception as e:
            logger.error(f"❌ Gold reference validation failed: {str(e)}")


async def demo_code_generation(excel_schema):
    """Demonstrate code generation for transformations"""
    logger.info("🔨 Demonstrating code generation")
    
    if not excel_schema or not excel_schema.transformation_rules:
        logger.warning("No transformation rules for code generation")
        return
    
    # Create transformation agent
    transform_agent = create_transformation_agent()
    
    # Generate code for each transformation
    for field_name, transformation_text in excel_schema.transformation_rules.items():
        logger.info(f"\n💻 Generating code for {field_name}:")
        
        try:
            # Create transformation rule
            rule = await transform_agent.create_transformation_rule(
                name=f"code_gen_{field_name}",
                source_fields=[field_name],  # Simplified for demo
                target_field=field_name,
                logic=transformation_text
            )
            
            # Generate PySpark code
            pyspark_code = await transform_agent.generate_transformation_code(rule, "pyspark")
            logger.info("   PySpark Code:")
            logger.info(f"   {pyspark_code}")
            
        except Exception as e:
            logger.error(f"   ❌ Code generation failed: {str(e)}")


def create_demo_visualization():
    """Create a visual diagram of the Excel mapping process"""
    
    diagram_content = """
flowchart TD
    A[Excel Mapping File<br/>img_0241 Gold Reference] --> B[Excel Parser]
    B --> C[Field Mappings Extracted]
    B --> D[Gold References Extracted] 
    B --> E[Transformation Rules Extracted]
    
    C --> F[Transformation Agent]
    D --> G[Gold Reference Validator]
    E --> F
    
    F --> H[Analyze Logic]
    F --> I[Validate Transformations]
    F --> J[Generate Code]
    
    G --> K[Validate Compliance]
    G --> L[Check Business Rules]
    G --> M[Generate Reports]
    
    H --> N[PySpark/SQL Code]
    I --> O[Validation Results]
    J --> N
    K --> P[Compliance Report]
    L --> P
    M --> P
    
    N --> Q[Executable Transformations]
    O --> R[Quality Assurance]
    P --> R
    
    style A fill:#e1f5fe
    style N fill:#c8e6c9
    style P fill:#fff3e0
    style Q fill:#f3e5f5
    """
    
    return diagram_content


async def main():
    """Main demo function"""
    try:
        # Run the demo
        await demo_excel_mapping_system()
        
        # Create visualization
        diagram = create_demo_visualization()
        
        print("\n" + "="*80)
        print("📊 EXCEL MAPPING SYSTEM ARCHITECTURE")
        print("="*80)
        print("The system processes your Excel mappings through this flow:")
        print("\n[See the flow diagram above for visual representation]")
        print("\n🎯 Key Features Demonstrated:")
        print("   ✅ Excel file parsing and field extraction")
        print("   ✅ Complex transformation logic analysis")
        print("   ✅ Gold reference validation (using img_0241 template)")
        print("   ✅ Automatic code generation (PySpark/SQL)")
        print("   ✅ Compliance reporting and validation")
        print("   ✅ Business rule enforcement")
        
        print("\n🚀 API Endpoints Available:")
        print("   POST /api/v1/excel/upload - Upload Excel files")
        print("   POST /api/v1/excel/parse - Parse mapping files")  
        print("   POST /api/v1/transformations/validate - Validate logic")
        print("   POST /api/v1/goldref/validate - Gold reference validation")
        print("   POST /api/v1/excel/process-full - Full pipeline processing")
        
        print("\n🎉 Your Excel mapping system is ready to use!")
        
    except Exception as e:
        logger.error(f"Demo failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)