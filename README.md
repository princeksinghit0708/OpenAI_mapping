# 🚀 Production-Ready Data Mapping Application

An intelligent data mapping application that leverages GPT-4 with advanced prompt engineering to automate PySpark code generation, test case creation, and data validation.

## 🌟 Features

- **AI-Powered Code Generation**: Uses GPT-4 to generate production-ready PySpark transformation code
- **Intelligent Mapping Analysis**: Analyzes Excel mapping specifications and provides recommendations
- **FAISS Vector Database**: Enables similarity search to find and reuse similar mapping patterns
- **Comprehensive Test Generation**: Automatically creates test cases for all mapping scenarios
- **Data Quality Validation**: Generates validation rules based on data profiling
- **Beautiful CLI Interface**: Rich terminal UI with progress tracking and status updates
- **Production-Ready**: Includes error handling, logging, and performance optimizations

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key with GPT-4 access
- Excel file with mapping specifications
- (Optional) Table metadata JSON files in `results/` directory

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   cd /Applications/Mapping
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env and add your OpenAI API key
   ```

## 📁 Project Structure

```
Mapping/
├── main.py                 # Main application orchestrator
├── gpt4_prompt_engine.py   # Advanced prompt engineering system
├── faiss_integration.py    # Vector database for similarity search
├── data_profiler.py        # Data quality profiling module
├── run_application.py      # Interactive runner script
├── requirements.txt        # Python dependencies
├── env_example.txt         # Environment configuration template
├── Testing1 copy.xlsx      # Your mapping Excel file
├── results/               # Directory for table metadata JSON files
├── output/                # Generated outputs
│   ├── pyspark_code/     # Generated PySpark transformations
│   ├── test_cases/       # Generated test cases
│   ├── validation_rules/ # Data validation rules
│   └── reports/          # Analysis reports
└── indexes/              # FAISS vector database indexes
```

## 🚀 Quick Start

### Option 1: Using the Interactive Runner (Recommended)
```bash
python run_application.py
```

The runner will:
- Check all requirements
- Guide you through setup if needed
- Let you select which Excel file to process
- Run the application with proper configuration

### Option 2: Direct Execution
```bash
python main.py
```

## 📊 Excel File Format

Your Excel file should have two sheets:

### Sheet 1: Mapping Logic
Required columns:
- `standard physical table name`: Target table name
- `Logical name`: Business description
- `Standard physical column name`: Target column name
- `Datatype`: Data type (String, char(1), etc.)
- `Source table name`: Source table(s)
- `source column name`: Source column(s)
- `Direct/derived/Default/no mapping`: Mapping type
- `Transformation/Derivation`: Transformation logic

### Sheet 2: Gold Reference Data
Contains lookup/reference data for mappings

## 📝 Table Metadata Format

Create JSON files in the `results/` directory with naming pattern: `{table_name}_metadata.json`

Example structure:
```json
{
  "table_name": "ACCT_DLY",
  "database": "prod_db",
  "columns": [
    {
      "name": "LAST_PYMT_DT",
      "type": "string",
      "nullable": true
    }
  ],
  "partitions": ["biz_dt"],
  "file_format": "parquet",
  "location": "hdfs://prod/data/ACCT_DLY"
}
```

## 🎯 Supported Mapping Types

1. **derived**: Complex transformations with business logic
2. **derived_goldref**: Derived with gold reference lookups
3. **direct**: Simple column-to-column mapping
4. **direct_map**: Direct mapping with value transformation
5. **no_mapping**: Columns to exclude or pass through
6. **blanks**: Special handling for null/blank values

## 📤 Output Files

The application generates:

1. **PySpark Code** (`output/pyspark_code/`)
   - Production-ready transformation functions
   - Error handling and logging included
   - Performance optimizations applied

2. **Test Cases** (`output/test_cases/`)
   - Positive, negative, edge, and performance tests
   - Test data generators
   - PySpark test code

3. **Validation Rules** (`output/validation_rules/`)
   - Data quality checks
   - Business rule validations
   - Monitoring metrics

4. **Reports** (`output/reports/`)
   - Comprehensive analysis
   - Recommendations
   - Data quality assessments

## 🔧 Configuration

Edit `.env` file to customize:
```bash
OPENAI_API_KEY=your_key_here
EXCEL_FILE=Testing1 copy.xlsx
RESULTS_DIR=results
OUTPUT_DIR=output
GPT_MODEL=gpt-4
MAX_TOKENS=8000
TEMPERATURE=0.1
```

## 📊 Monitoring & Logs

- Application logs: `mapping_application.log`
- FAISS index statistics available in the application output
- Progress tracking shown in real-time during execution

## 🤝 Best Practices

1. **Excel Data Quality**
   - Ensure mapping logic is clear and complete
   - Use consistent naming conventions
   - Document complex transformations clearly

2. **Performance**
   - For large datasets, the application automatically optimizes prompts
   - FAISS index enables fast similarity searches
   - Caching reduces redundant API calls

3. **Cost Management**
   - Monitor OpenAI API usage
   - Application optimizes prompts to fit within token limits
   - Batch processing reduces API calls

## 🐛 Troubleshooting

1. **OpenAI API Issues**
   - Verify API key has GPT-4 access
   - Check API rate limits
   - Ensure sufficient credits

2. **Excel Reading Errors**
   - Verify Excel file format
   - Check column names match expected format
   - Ensure file is not corrupted

3. **Memory Issues**
   - For large mappings, increase available memory
   - Process in batches if needed

## 📈 Performance Tips

1. Use the FAISS similarity search to find existing patterns
2. Keep transformation logic clear and well-documented
3. Provide complete table metadata for better code generation
4. Review and optimize generated code before production use

## 🔐 Security

- API keys are stored in `.env` file (not committed to version control)
- No sensitive data is sent to external APIs
- All outputs are stored locally

## 📞 Support

For issues or questions:
1. Check the application logs
2. Review generated reports for insights
3. Ensure all prerequisites are met
4. Verify Excel format matches requirements

## 🎉 Getting Started Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python run_application.py

# 3. Follow the interactive prompts
# 4. Check the output directory for results
```

---

Built with ❤️ using GPT-4, FAISS, and PySpark 