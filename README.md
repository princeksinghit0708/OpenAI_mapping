# 🤖 Agentic Mapping AI Platform

A comprehensive AI-powered data mapping and transformation platform with advanced Excel integration capabilities.

## 🚀 Features

### Core Platform
- **Enhanced Orchestrator**: Multi-agent coordination and workflow management
- **RAG Knowledge Engine**: Intelligent context retrieval and learning
- **Streamlit UI**: Interactive web interface for system management
- **FastAPI Backend**: RESTful API for all platform operations

### Excel Mapping Integration
- **Excel Parser**: Extract complex field mappings from Excel files
- **Transformation Agent**: Analyze and process conditional logic, lookups, and derivations
- **Gold Reference Validator**: Ensure compliance with data standards (img_0241 template)
- **PySpark Code Generator**: Automatic production-ready code generation

### Advanced Capabilities
- **Multi-Agent Architecture**: Specialized agents for different transformation types
- **Code Generation**: PySpark, SQL, and Python code generation
- **Validation & Compliance**: Comprehensive data quality checks
- **Knowledge Management**: Learning from transformation patterns

## 📊 Excel Mapping Support

The platform supports complex Excel mapping structures including:
- **Conditional Transformations**: `If HIFI_ACCT_IND > 0 then 'Y' else 'N'`
- **Lookup Operations**: `Lookup for genesis STANDARD_VAL_DESC using keys`
- **Date Formatting**: `Date format should be 'YYYYMMDD'`
- **Direct Mappings**: Simple field-to-field mappings
- **Gold Reference Validation**: Against img_0241 template standards

## 🛠️ Quick Start

### 1. Install Dependencies
```bash
cd agentic_mapping_ai
pip install -r requirements.txt
```

### 2. Start the Platform
```bash
python run_application.py
```

### 3. Access the Interface
- **API Documentation**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501
- **Health Check**: http://localhost:8000/health

### 4. Upload Excel Mappings
```bash
# Upload Excel file
curl -X POST "http://localhost:8000/api/v1/excel/upload" -F "file=@your_mapping.xlsx"

# Process full pipeline
curl -X POST "http://localhost:8000/api/v1/excel/process-full" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "./data/uploads/your_mapping.xlsx"}'
```

## 📁 Project Structure

```
agentic_mapping_ai/
├── agents/                 # AI agents for different tasks
│   ├── transformation_agent.py
│   ├── goldref_validator.py
│   └── pyspark_code_generator.py
├── parsers/               # Excel and data parsers
├── api/                   # FastAPI backend
├── core/                  # Core models and utilities
├── knowledge/             # RAG engine and knowledge base
├── examples/              # Demo scripts and examples
└── ui/                    # Streamlit interface
```

## 🔧 API Endpoints

### Excel Processing
- `POST /api/v1/excel/upload` - Upload Excel files
- `POST /api/v1/excel/parse` - Parse mapping files
- `POST /api/v1/excel/process-full` - Full pipeline processing

### Transformations
- `POST /api/v1/transformations/validate` - Validate transformation logic
- `POST /api/v1/transformations/generate-code` - Generate PySpark/SQL code

### Gold Reference
- `POST /api/v1/goldref/validate` - Validate against standards
- `GET /api/v1/goldref/compliance-report` - Generate compliance reports

## 📚 Documentation

- [Excel Mapping Integration Guide](agentic_mapping_ai/EXCEL_MAPPING_INTEGRATION_GUIDE.md)
- [Enhanced Implementation Guide](agentic_mapping_ai/ENHANCED_IMPLEMENTATION_GUIDE.md)
- [Setup Instructions](agentic_mapping_ai/SETUP_INSTRUCTIONS.md)

## 🎯 Use Cases

1. **Data Migration Projects**: Automate complex field transformations
2. **ETL Pipeline Generation**: Generate production-ready PySpark code
3. **Compliance Validation**: Ensure mappings meet business standards
4. **Knowledge Management**: Learn from transformation patterns
5. **Code Automation**: Reduce manual coding for data transformations

## 🤝 Contributing

This is an AI-generated platform. Contributions and improvements are welcome!

## 📄 License

Open source - see LICENSE file for details.

---

**Built with AI-powered agents for intelligent data transformation** 🚀