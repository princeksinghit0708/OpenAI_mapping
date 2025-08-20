# 🚀 Agentic Excel Workflow Application

A **comprehensive AI-powered application** that orchestrates the entire data mapping workflow from Excel files to production-ready PySpark code, using multiple intelligent agents working together.

## 🎯 What This Application Does

This is a **unified agentic application** that brings together all the components we've built into a single, intelligent workflow:

### 🔄 **Complete Workflow Pipeline**

```
Excel File → AI Agents → Validation → Testing → Code Generation → Orchestration
    ↓              ↓           ↓         ↓           ↓              ↓
📊 Read Excel  🤖 Validate  🧪 Generate  💻 Generate  🎯 Coordinate  📋 Final Report
   Mappings     Metadata     Test Cases   PySpark     Workflow      & Outputs
```

### 🎭 **AI Agents Working Together**

1. **📊 Excel Processor**: Intelligently reads and parses Excel mapping files
2. **🔍 Metadata Validator Agent**: AI-powered validation of field mappings and schemas
3. **🧪 Test Generator**: Creates comprehensive test cases for data quality and business rules
4. **💻 Code Generator Agent**: Generates production-ready PySpark transformation code
5. **🎯 Orchestrator Agent**: Coordinates all agents and manages workflow dependencies

## 🚀 How to Use

### **Option 1: Easy Launcher (Recommended)**
```bash
cd demo
python run_agentic_workflow.py
```

This gives you an interactive menu to:
- Select existing Excel files
- Create sample Excel files
- Enter custom file paths
- Confirm workflow execution

### **Option 2: Direct Application**
```bash
cd demo
python agentic_excel_workflow_app.py
```

### **Option 3: Programmatic Usage**
```python
from agentic_excel_workflow_app import AgenticExcelWorkflowApp
import asyncio

app = AgenticExcelWorkflowApp()
success = await app.run_complete_workflow("path/to/excel/file.xlsx")
```

## 📁 Application Structure

### **Core Application Files**
- `agentic_excel_workflow_app.py` - Main application with all workflow logic
- `run_agentic_workflow.py` - Interactive launcher script
- `create_sample_excel.py` - Creates sample Excel files for testing

### **Output Directory Structure**
```
output/
├── excel_parsed/          # Parsed Excel mappings
├── validation_reports/     # Metadata validation results
├── test_cases/            # Generated test scenarios
├── generated_code/         # PySpark transformation code
├── workflow_logs/          # Workflow execution logs
└── final_reports/          # Comprehensive workflow reports
```

## 🔧 Prerequisites

1. **Python Environment**: Python 3.7+ with required packages
2. **agentic_mapping_ai**: The AI framework must be installed
3. **LLM Access**: OpenAI API key or other LLM provider configured
4. **Excel Files**: Your mapping files or use the sample generator

## 📊 What the Application Processes

### **Excel File Structure Expected**
The application intelligently detects columns in your Excel files:

| Standard Column | Excel Column Patterns |
|----------------|----------------------|
| `physical_table` | "Physical Table", "Table Name", "Target Table" |
| `logical_name` | "Logical Name", "Business Name", "Description" |
| `physical_name` | "Physical Name", "Column Name", "Field Name" |
| `data_type` | "Data Type", "Type", "Field Type" |
| `source_table` | "Source Table", "Source", "From Table" |
| `source_column` | "Source Column", "Source Field", "From Column" |
| `mapping_type` | "Mapping Type", "Type", "Transformation Type" |
| `transformation_logic` | "Transformation", "Logic", "Formula" |
| `description` | "Description", "Comment", "Notes" |

### **Mapping Types Supported**
- **Direct**: Simple field-to-field mapping
- **Derived**: Calculated fields with transformation logic
- **Goldref**: Lookup-based mappings from reference tables
- **No Mapping**: Fields that don't require transformation

## 🤖 AI Agent Capabilities

### **Metadata Validator Agent**
- ✅ **Intelligent Analysis**: Uses AI to understand your mapping structure
- ✅ **Banking-Specific Rules**: Validates against financial data standards
- ✅ **Automated Issue Detection**: Finds problems without manual rule definition
- ✅ **Actionable Insights**: Provides specific recommendations for fixes

### **Code Generator Agent**
- ✅ **PySpark Generation**: Creates production-ready transformation code
- ✅ **Business Logic Integration**: Incorporates your transformation rules
- ✅ **Error Handling**: Adds robust error handling and logging
- ✅ **Performance Optimization**: Optimizes for production environments

### **Test Generator**
- ✅ **Comprehensive Testing**: Covers all mapping scenarios
- ✅ **Data Quality Tests**: Validates data integrity and consistency
- ✅ **Business Rule Tests**: Ensures compliance with business logic
- ✅ **SQL Test Queries**: Ready-to-run validation queries

### **Orchestrator Agent**
- ✅ **Workflow Management**: Coordinates all agents and steps
- ✅ **Dependency Handling**: Manages task dependencies and order
- ✅ **Error Recovery**: Handles failures gracefully
- ✅ **Progress Tracking**: Monitors workflow execution

## 📈 Workflow Execution Steps

### **Step 1: Agent Initialization**
```
🔧 Initializing AI Agents...
✅ Metadata Validator Agent initialized
✅ Code Generator Agent initialized  
✅ Orchestrator Agent initialized
🎉 All agents initialized successfully!
```

### **Step 2: Excel Processing**
```
📊 Step 1: Processing Excel File
📁 Reading Excel file: mapping_file.xlsx
📋 Found sheets: ['datahub standard mapping', 'goldref']
📊 Loaded 25 rows from 'datahub standard mapping' sheet
🥇 Loaded 15 gold reference rows from 'goldref' sheet
✅ Excel file processed successfully!
```

### **Step 3: Metadata Validation**
```
🔍 Step 2: Metadata Validation
🤖 Metadata Validator Agent is analyzing the mappings...
✅ Metadata validation completed!
📊 Validation Status: VALIDATED
✅ Metadata validation step completed!
```

### **Step 4: Test Case Generation**
```
🧪 Step 3: Test Case Generation
🤖 Generating comprehensive test cases...
📊 Generating tests for table: ACCT_DLY
📊 Generating tests for table: CUST_DLY
📊 Generating tests for table: TXN_DLY
✅ Test case generation completed!
```

### **Step 5: Code Generation**
```
💻 Step 4: Code Generation
🤖 Code Generator Agent is creating PySpark transformations...
📊 Generating code for table: ACCT_DLY
📊 Generating code for table: CUST_DLY
📊 Generating code for table: TXN_DLY
✅ Code generation completed!
```

### **Step 6: Workflow Orchestration**
```
🎯 Step 5: Workflow Orchestration
🤖 Orchestrator Agent is coordinating the workflow...
✅ Workflow orchestration completed!
✅ Workflow orchestration step completed!
```

### **Step 7: Final Report**
```
📊 Generating Final Report
💾 Final report saved to: output/final_reports/workflow_report_20241220_143022.json

🎉 WORKFLOW EXECUTION SUMMARY
⏱️  Duration: 2024-12-20T14:30:22 → 2024-12-20T14:35:45
📊 Steps: 5/5 completed
📊 Excel Processing:
   • Source: mapping_file.xlsx
   • Mappings: 25
   • Tables: 3
🤖 Agent Performance:
   • Agents: 3
   • Results: metadata_validation, test_cases, generated_code, orchestration
```

## 🎯 Sample Outputs

### **Generated PySpark Code**
```python
# PySpark Transformation for ACCT_DLY
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def transform_acct_dly(spark: SparkSession, source_df):
    """
    Transform source data for ACCT_DLY table
    """
    
    # Apply field mappings
    transformed_df = source_df.select(
        col('ACCOUNT_NUMBER').alias('acct_nbr'),
        col('BALANCE').alias('acct_bal'),
        col('CURRENCY').alias('curr_cd'),
        expr('If ACCT_TYP_CD = "01" then "Savings" else "Checking"').alias('acct_typ_desc'),
        # ... more mappings
    )
    
    return transformed_df
```

### **Generated Test Cases**
```json
{
  "table_name": "ACCT_DLY",
  "total_fields": 8,
  "test_scenarios": [
    {
      "field": "acct_nbr",
      "test_type": "direct_mapping",
      "description": "Test direct mapping from ACCOUNT_NUMBER to acct_nbr",
      "expected_result": "Value should be identical to source field ACCOUNT_NUMBER"
    }
  ],
  "data_quality_tests": [
    {
      "test_name": "null_check",
      "description": "Check for unexpected null values in required fields",
      "sql_query": "SELECT COUNT(*) FROM ACCT_DLY WHERE required_field IS NULL"
    }
  ]
}
```

## 🚀 Next Steps After Execution

1. **Review Generated Code**: Check `output/generated_code/` for PySpark transformations
2. **Validate Test Cases**: Review `output/test_cases/` for testing scenarios
3. **Check Validation Reports**: Review `output/validation_reports/` for any issues
4. **Deploy Code**: Use generated PySpark code in your data pipeline
5. **Run Tests**: Execute generated test cases to validate data quality

## 🆘 Troubleshooting

### **Common Issues**

**Agent Initialization Failed**
```bash
❌ Agent initialization failed: ImportError
```
**Solution**: Ensure `agentic_mapping_ai` is properly installed and accessible

**Excel Processing Failed**
```bash
❌ Excel processing failed: File not found
```
**Solution**: Check file path and ensure Excel file exists

**Validation Failed**
```bash
❌ Metadata validation failed: No validation results returned
```
**Solution**: Check LLM service configuration and API keys

### **Getting Help**

1. **Run the launcher**: `python run_agentic_workflow.py`
2. **Check prerequisites**: Ensure all dependencies are installed
3. **Verify Excel files**: Ensure your mapping files are properly formatted
4. **Check LLM access**: Verify your AI service configuration

## 🎉 Success Indicators

You'll know the application is working when you see:

- ✅ "All agents initialized successfully"
- ✅ "Excel file processed successfully"
- ✅ "Metadata validation step completed"
- ✅ "Test case generation completed"
- ✅ "Code generation completed"
- ✅ "Workflow orchestration step completed"
- 📊 Comprehensive final report with all outputs

## 🔗 Related Components

- **Metadata Validation Demo**: `hive_metadata_validation_demo.py`
- **Agent Testing**: `test_metadata_agent.py`
- **Sample Excel Creation**: `create_sample_excel.py`
- **Enhanced Main App**: `enhanced_main.py`

## 🚀 Why This is Powerful

- **🎯 End-to-End**: Complete workflow from Excel to production code
- **🤖 AI-Powered**: Multiple intelligent agents working together
- **🔄 Automated**: No manual intervention required
- **📊 Comprehensive**: Covers validation, testing, and code generation
- **🏗️ Production-Ready**: Generates deployable PySpark code
- **📈 Scalable**: Handles any number of tables and mappings

---

**Ready to see AI agents orchestrate your entire data mapping workflow? Run the application now!** 🚀

```bash
cd demo
python run_agentic_workflow.py
```
