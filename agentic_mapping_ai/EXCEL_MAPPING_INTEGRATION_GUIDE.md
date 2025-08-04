# Excel Mapping Integration Guide

## Overview

This guide demonstrates how to integrate Excel-based field mappings (like your `img_0241` gold reference) with the Agentic Mapping AI platform. The system now supports parsing complex Excel mapping files, validating transformations, and generating code automatically.

## Key Features Added

### 🔍 Excel Mapping Parser
- **Purpose**: Extract field mappings, transformations, and reference data from Excel files
- **Supports**: Complex transformation logic, conditional statements, lookup operations
- **Input**: Excel files with structured mapping data (like your screenshots)
- **Output**: Structured field definitions and mapping rules

### ⚙️ Transformation Agent
- **Purpose**: Analyze and process complex transformation logic
- **Capabilities**:
  - Parse conditional statements (`If HIFI_ACCT_IND > 0 then 'Y' else 'N'`)
  - Handle lookup operations (`Lookup for genesis STANDARD_VAL_DESC`)
  - Generate executable code (PySpark, SQL, Python)
  - Validate transformation syntax and logic

### 🥇 Gold Reference Validator
- **Purpose**: Ensure compliance with data standards and business rules
- **Features**:
  - Validate against gold reference templates (img_0241)
  - Check data consistency and completeness
  - Generate compliance reports
  - Enforce business rules and constraints

## Excel File Structure Expected

Based on your screenshots, the system expects Excel files with these columns:

| Column | Purpose | Example |
|--------|---------|---------|
| A | Physical Table | `ACCT_DLY` |
| B | Logical Name | `Fee Amount`, `Account Type` |
| C | Physical Name | `TXN_FEE_AMT`, `TYP_DESC` |
| D | Data Type | `Decimal(15,2)`, `String`, `Char(1)` |
| G | Source Name/Context | Field context information |
| H | Column Name/Default | Target column specifications |
| I | Mapping Type | `Direct`, `Derived`, `Goldref`, `No Mapping` |
| J | Transformation Logic | Complex transformation rules |

## API Endpoints

### 1. Upload Excel File
```http
POST /api/v1/excel/upload
Content-Type: multipart/form-data

# Upload your Excel mapping file
```

### 2. Parse Excel Mappings
```http
POST /api/v1/excel/parse
Content-Type: application/json

{
    "file_path": "./data/uploads/your_mapping.xlsx",
    "sheet_name": "Sheet1",
    "gold_reference_template": "img_0241"
}
```

### 3. Validate Transformations
```http
POST /api/v1/transformations/validate
Content-Type: application/json

{
    "transformation_logic": "If HIFI_ACCT_IND > 0 then 'Y' else 'N'",
    "source_fields": ["HIFI_ACCT_IND"],
    "target_field": "account_indicator"
}
```

### 4. Generate Code
```http
POST /api/v1/transformations/generate-code?language=pyspark
Content-Type: application/json

{
    "transformation_logic": "If HIFI_ACCT_IND > 0 then 'Y' else 'N'",
    "source_fields": ["HIFI_ACCT_IND"],
    "target_field": "account_indicator"
}
```

### 5. Gold Reference Validation
```http
POST /api/v1/goldref/validate
Content-Type: application/json

{
    "field_mappings": [
        {
            "physical_table": "ACCT_DLY",
            "logical_name": "Account Type",
            "physical_name": "TYP_DESC",
            "data_type": "String",
            "mapping_type": "Goldref",
            "transformation": "Lookup for genesis STANDARD_VAL"
        }
    ],
    "gold_reference_template": "img_0241"
}
```

### 6. Full Pipeline Processing
```http
POST /api/v1/excel/process-full
Content-Type: application/json

{
    "file_path": "./data/uploads/your_mapping.xlsx",
    "sheet_name": "Sheet1",
    "gold_reference_template": "img_0241"
}
```

## Usage Examples

### Python SDK Usage

```python
import asyncio
from parsers.excel_mapping_parser import parse_excel_mappings
from agents.transformation_agent import create_transformation_agent
from agents.goldref_validator import create_goldref_validator

async def process_excel_mapping():
    # 1. Parse Excel file
    excel_schema = parse_excel_mappings("your_mapping.xlsx")
    
    # 2. Analyze transformations
    transform_agent = create_transformation_agent()
    for field, logic in excel_schema.transformation_rules.items():
        analysis = await transform_agent.analyze_transformation(logic)
        print(f"Field: {field}, Type: {analysis['type']}, Complexity: {analysis['complexity']}")
    
    # 3. Validate against gold reference
    goldref_validator = create_goldref_validator()
    validation = await goldref_validator.validate_mapping_compliance(
        excel_schema.field_mappings, 
        "img_0241"
    )
    
    print(f"Validation passed: {validation.is_valid}")
    return excel_schema

# Run the processing
asyncio.run(process_excel_mapping())
```

### REST API Usage (cURL)

```bash
# Upload Excel file
curl -X POST "http://localhost:8000/api/v1/excel/upload" \
     -F "file=@your_mapping.xlsx"

# Parse the uploaded file
curl -X POST "http://localhost:8000/api/v1/excel/parse" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "./data/uploads/your_mapping.xlsx",
       "sheet_name": "Sheet1",
       "gold_reference_template": "img_0241"
     }'

# Process full pipeline
curl -X POST "http://localhost:8000/api/v1/excel/process-full" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "./data/uploads/your_mapping.xlsx",
       "generate_code": true,
       "validate_goldref": true
     }'
```

## Transformation Types Supported

### 1. Conditional Transformations
```
If HIFI_ACCT_IND > 0 then 'Y' else 'N'
```
**Generated PySpark:**
```python
df = df.withColumn(
    'account_indicator',
    when(col('HIFI_ACCT_IND') > 0, lit('Y'))
    .otherwise(lit('N'))
)
```

### 2. Lookup Transformations
```
Lookup for the genesis STANDARD_VAL_DESC using the lookup keys (CNTRY_ID, PRD_PROCESSOR)
```
**Generated PySpark:**
```python
lookup_df = spark.table('STANDARD_VAL_DESC')
df = df.join(
    lookup_df.select('CNTRY_ID', 'PRD_PROCESSOR', 'standard_value'),
    ['CNTRY_ID', 'PRD_PROCESSOR'],
    'left'
).withColumnRenamed('standard_value', 'target_field')
```

### 3. Date Format Transformations
```
Date format should be 'YYYYMMDD'
```
**Generated PySpark:**
```python
df = df.withColumn(
    'formatted_date',
    date_format(col('source_date'), 'yyyyMMdd')
)
```

## Gold Reference Template (img_0241)

The system uses your `img_0241` as the gold reference template with these validation rules:

### Required Fields
- `physical_table` - Must be present
- `logical_name` - Must be descriptive
- `physical_name` - Must follow naming conventions
- `data_type` - Must be valid SQL data type
- `mapping_type` - Must be one of: Direct, Derived, Goldref, No Mapping

### Mapping Type Rules
- **Direct**: Simple one-to-one mapping
- **Derived**: Requires transformation logic
- **Goldref**: Requires lookup table reference
- **No Mapping**: Field is not mapped

### Data Quality Checks
- No duplicate physical names
- Consistent data types for same logical names
- Valid transformation syntax
- Proper lookup table references

## Integration with Existing Workflows

### Enhanced Orchestrator Integration
```python
from agents.enhanced_orchestrator_v2 import create_enhanced_orchestrator

# Create enhanced orchestrator with Excel capabilities
orchestrator = create_enhanced_orchestrator()

# Add Excel processing workflow
workflow_data = {
    "excel_file_path": "your_mapping.xlsx",
    "gold_reference_template": "img_0241",
    "generate_code": True,
    "validate_compliance": True
}

result = await orchestrator.execute_workflow(
    "excel_mapping_pipeline",
    workflow_data
)
```

### RAG Engine Knowledge Integration
```python
from knowledge.rag_engine import RAGEngine

# Initialize RAG engine
rag_engine = RAGEngine()

# Add Excel mapping patterns to knowledge base
await rag_engine.add_knowledge(
    content="Excel mapping transformation patterns",
    metadata={
        "category": "excel_mappings",
        "source": "img_0241",
        "type": "gold_reference"
    }
)
```

## Running the Demo

To see the Excel mapping system in action:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
cd agentic_mapping_ai
python examples/excel_mapping_demo.py
```

## Monitoring and Logging

The system provides comprehensive logging:

```python
from loguru import logger

# All Excel processing is logged
# Transformation analysis results
# Validation outcomes
# Code generation success/failures
# Gold reference compliance reports
```

## Error Handling

Common issues and solutions:

### Excel File Format Issues
- **Issue**: Unsupported file format
- **Solution**: Use `.xlsx` or `.xls` files only

### Transformation Syntax Errors
- **Issue**: Invalid transformation logic
- **Solution**: Check conditional syntax and field references

### Gold Reference Validation Failures
- **Issue**: Non-compliant mappings
- **Solution**: Review mapping types and required fields

### Missing Dependencies
- **Issue**: Missing pandas or openpyxl
- **Solution**: `pip install pandas openpyxl`

## Best Practices

1. **Excel File Preparation**
   - Use consistent column headers
   - Provide clear transformation logic
   - Include all required mapping information

2. **Transformation Logic**
   - Use clear conditional statements
   - Reference valid field names
   - Include proper data type specifications

3. **Gold Reference Compliance**
   - Follow img_0241 template structure
   - Ensure required fields are populated
   - Validate mapping types are appropriate

4. **Code Generation**
   - Review generated code before deployment
   - Test with sample data
   - Optimize for performance when needed

## Next Steps

1. Upload your Excel mapping files using the API
2. Run validation against the img_0241 template
3. Generate and review transformation code
4. Integrate with your existing data pipelines
5. Monitor compliance and quality metrics

The system is now ready to process your Excel mappings and integrate them seamlessly with your agentic AI platform!