# 🚀 Agentic Mapping AI - Setup Instructions

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
# Navigate to the project directory
cd agentic_mapping_ai

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp env_template.txt .env

# Edit .env file with your API keys (optional for basic usage)
# nano .env
```

**Required API Keys (at least one):**
- `OPENAI_API_KEY` - For GPT-4 (recommended)
- `ANTHROPIC_API_KEY` - For Claude (alternative)

### 3. Start the Application
```bash
# Option 1: Run everything (API + UI)
python run_application.py

# Option 2: API server only
python run_application.py --api-only

# Option 3: Check dependencies first
python run_application.py --check-deps
```

### 4. Access the Platform
- **API Documentation**: http://localhost:8000/docs
- **Streamlit UI**: http://localhost:8501  
- **Health Check**: http://localhost:8000/health

---

## 📋 Detailed Setup

### Prerequisites
- Python 3.8+
- 4GB+ RAM (for vector embeddings)
- 2GB+ disk space

### Environment Variables

Create a `.env` file with these settings:

```bash
# Required: At least one LLM API key
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here

# Database (optional - uses SQLite by default)
DATABASE_URL=postgresql://username:password@localhost:5432/agentic_mapping

# Vector Database (uses Chroma by default)
VECTOR_DB_TYPE=chroma
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# Application Settings
DEBUG=true
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# UI Configuration  
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost
```

### Optional: PostgreSQL Setup
```bash
# Install PostgreSQL (optional)
# macOS
brew install postgresql

# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# Create database
createdb agentic_mapping

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/agentic_mapping
```

---

## 🧪 Testing the Setup

### 1. Run Quick Start Example
```bash
python examples/quick_start_example.py
```

### 2. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Validate document (with API running)
curl -X POST "http://localhost:8000/api/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{"document": {"dictionary": {"providedKey": "test.schema.db"}}, "validation_rules": []}'
```

### 3. Test UI
1. Open http://localhost:8501
2. Navigate to "Document Validation"
3. Paste sample JSON and validate

---

## 🛠️ Development Setup

### Code Quality Tools
```bash
# Install development dependencies
pip install black isort pylint pytest pre-commit

# Format code
black .
isort .

# Lint code  
pylint agents/ core/ knowledge/ api/

# Run tests
pytest tests/
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## 📁 Project Structure

```
agentic_mapping_ai/
├── agents/                 # AI Agents
│   ├── base_agent.py      # Base agent class
│   ├── metadata_validator.py
│   ├── code_generator.py
│   └── orchestrator.py
├── api/                   # REST API
│   └── main.py           # FastAPI application
├── core/                  # Core models
│   └── models.py         # Data models
├── knowledge/             # RAG & Vector DB
│   └── rag_engine.py     # RAG implementation
├── ui/                    # User Interface
│   └── streamlit_app.py  # Streamlit dashboard
├── config/               # Configuration
│   └── settings.py       # App settings
├── templates/            # Code templates
├── examples/             # Usage examples
├── data/                 # Data storage
├── output/               # Generated output
├── requirements.txt      # Dependencies
└── run_application.py    # Application runner
```

---

## 🔧 Common Issues & Solutions

### Issue: Missing API Keys
**Error:** `API key not found`
**Solution:** Add your OpenAI or Anthropic API key to `.env` file

### Issue: Port Already in Use
**Error:** `Port 8000/8501 already in use`
**Solution:** Change ports in `.env` file or kill existing processes

### Issue: Vector DB Initialization Failed
**Error:** `ChromaDB initialization failed`
**Solution:** Ensure write permissions for `./data/chroma_db` directory

### Issue: Memory Error
**Error:** `Out of memory` when loading embeddings
**Solution:** Increase available RAM or use a smaller embedding model

### Issue: Import Errors
**Error:** `ModuleNotFoundError`
**Solution:** Ensure you're in the `agentic_mapping_ai` directory and run `pip install -r requirements.txt`

---

## 🎯 Usage Examples

### 1. Document Validation
```python
import requests

response = requests.post("http://localhost:8000/api/v1/validate", json={
    "document": {
        "dictionary": {"providedKey": "PBWM.GCB_AAC_NAM.database_name"},
        "fields": [...]
    },
    "validation_rules": ["check_required_fields"]
})
```

### 2. Code Generation
```python
response = requests.post("http://localhost:8000/api/v1/generate/code", json={
    "source_schema": {...},
    "target_schema": {...},
    "mapping_rules": [...],
    "code_type": "pyspark"
})
```

### 3. Full Pipeline
```python
response = requests.post("http://localhost:8000/api/v1/pipeline/full", json={
    "document": {...},
    "code_type": "pyspark",
    "optimization_level": "standard"
})
```

---

## 📞 Support

### Getting Help
1. Check the [README.md](README.md) for detailed documentation
2. Review the [API Documentation](http://localhost:8000/docs) 
3. Run the health check: `curl http://localhost:8000/health`
4. Check logs in `./logs/` directory

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

---

## 🎉 You're Ready!

Your Agentic Mapping AI platform is now set up and ready to use. Start with the Streamlit UI at http://localhost:8501 or explore the API at http://localhost:8000/docs.

**Next Steps:**
1. Try the Document Validation feature
2. Generate some PySpark code  
3. Explore the Knowledge Base
4. Run the full mapping pipeline
5. Customize agents for your specific use cases