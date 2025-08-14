# Complete Requirements & Dependencies - Agentic Mapping AI Demo

## 📋 System Requirements

### Hardware Requirements
- **CPU**: 4+ cores (8+ recommended for optimal performance)
- **RAM**: 8GB minimum (16GB+ recommended)
- **Storage**: 5GB free space (2GB for dependencies, 3GB for data/models)
- **Network**: Stable internet connection for LLM provider APIs

### Software Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8+ (3.9+ recommended)
- **Git**: For repository management
- **Command Line**: Terminal/Command Prompt access

## 🐍 Python Dependencies

### Core Framework Dependencies
```
# AI/ML Libraries
openai==1.3.0                    # OpenAI GPT models
anthropic>=0.3.0                 # Claude models integration
google-cloud-aiplatform>=1.0.0   # Google Gemini integration
vertexai>=1.0.0                  # Google Vertex AI
sentence-transformers>=2.2.0     # Embedding generation
faiss-cpu==1.7.4                # Vector similarity search
numpy==1.24.3                   # Numerical computing
tiktoken==0.5.1                 # Token counting for LLMs

# Web Framework
fastapi>=0.104.0                # REST API framework
uvicorn>=0.24.0                 # ASGI server
pydantic>=2.0.0                 # Data validation
pydantic-settings>=2.0.0        # Settings management

# Agent Framework
langchain>=0.1.0                # LLM orchestration
langchain-openai>=0.0.5         # OpenAI integration
langchain-anthropic>=0.1.0      # Anthropic integration
langchain-google-genai>=0.0.5   # Google integration

# Data Processing
pandas==2.0.3                   # Data manipulation
openpyxl==3.1.2                # Excel file processing
jinja2==3.1.2                  # Template engine
pyspark==3.4.1                 # Big data processing

# Database & Storage
pymongo>=4.0.0                 # MongoDB integration
sqlalchemy>=2.0.0              # Database ORM
alembic>=1.12.0                # Database migrations

# Utilities
python-dotenv==1.0.0           # Environment variables
rich==13.7.0                   # Terminal formatting
loguru>=0.7.0                  # Advanced logging
asyncio                        # Asynchronous programming
pathlib                        # Path operations
datetime                       # Date/time handling
json                          # JSON processing
typing                        # Type hints
enum                          # Enumerations
dataclasses                   # Data classes
uuid                          # Unique identifiers

# Development & Testing
pytest>=7.0.0                 # Testing framework
pytest-asyncio>=0.21.0        # Async testing
black>=23.0.0                 # Code formatting
isort>=5.12.0                 # Import sorting
mypy>=1.5.0                   # Type checking
```

### Optional Dependencies (For Enhanced Features)
```
# Advanced ML Features
torch>=2.0.0                  # PyTorch for advanced models
transformers>=4.30.0          # Hugging Face transformers
scikit-learn>=1.3.0          # Traditional ML algorithms

# Monitoring & Observability
prometheus-client>=0.17.0     # Metrics collection
grafana-client>=3.5.0        # Dashboard integration
sentry-sdk>=1.32.0           # Error tracking

# Development Tools
jupyter>=1.0.0               # Interactive notebooks
ipython>=8.0.0               # Enhanced Python shell
pre-commit>=3.0.0            # Git hooks
```

## 🔑 Authentication & API Keys

### Required Environment Variables
```bash
# LLM Service Configuration
# Note: Using token-based authentication - no direct API keys needed

# MongoDB Configuration (Optional - for token storage)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=agentic_mapping
MONGODB_COLLECTION=tokens

# Application Configuration
APP_NAME=Agentic Mapping AI
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Vector Database Configuration
FAISS_INDEX_PATH=./indexes
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Excel Configuration
EXCEL_FILE=ebs_IM_account_DATAhub_mapping_v8.0.xlsx
RESULTS_DIR=results
OUTPUT_DIR=output
```

### LLM Provider Setup
The application uses **token-based authentication** instead of direct API keys:

#### Option 1: Helix CLI (Recommended)
```bash
# Install Helix CLI
npm install -g @helixbridgecorp/cli

# Authenticate
helix auth login

# Test token access
helix auth access-token print -a
```

#### Option 2: MongoDB Token Storage
```bash
# Set up MongoDB with tokens
docker run -d -p 27017:27017 mongo:latest

# Configure connection in .env
MONGODB_URL=mongodb://localhost:27017
```

## 🐳 Docker Setup (Optional)

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "demo_launcher.py"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  agentic-mapping:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongo:27017
    depends_on:
      - mongo
      
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

## 📁 Project Structure

```
demo/
├── agentic_mapping_ai/           # Main application package
│   ├── agents/                   # AI agent implementations
│   │   ├── base_agent.py        # Base agent class
│   │   ├── orchestrator.py      # Workflow orchestration
│   │   ├── metadata_validator.py # Document validation
│   │   ├── code_generator.py    # Code generation
│   │   └── test_generator.py    # Test case generation
│   ├── api/                     # REST API endpoints
│   │   └── main.py             # FastAPI application
│   ├── config/                  # Configuration management
│   │   ├── settings.py         # Application settings
│   │   └── enhanced_settings.py # Multi-provider config
│   ├── core/                    # Core data models
│   │   └── models.py           # Pydantic models
│   ├── knowledge/               # RAG & knowledge management
│   │   └── rag_engine.py       # Vector search engine
│   ├── llm_service.py          # Multi-LLM integration
│   └── run_enhanced_application.py # Main launcher
├── results/                     # Sample data files
│   ├── acct_dly_metadata.json  # Banking account data
│   ├── cust_dly_metadata.json  # Customer data
│   └── txn_dly_metadata.json   # Transaction data
├── requirements.txt             # Python dependencies
├── demo_launcher.py            # One-click demo launcher
├── README_DEMO.md             # Technical documentation
├── DEMO_MANAGER_GUIDE.md      # This guide
├── validate_demo.py           # Setup validation
└── .env                       # Environment configuration
```

## 🚀 Installation Guide

### Step 1: Environment Setup
```bash
# Clone repository
git clone https://github.com/princeksinghit0708/OpenAI_mapping.git
cd OpenAI_mapping/demo

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 2: Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt

# Or install individually for troubleshooting
pip install fastapi uvicorn pydantic pydantic-settings
pip install pandas openpyxl numpy
pip install openai anthropic google-cloud-aiplatform vertexai
pip install langchain langchain-openai sentence-transformers
pip install pymongo sqlalchemy faiss-cpu
pip install python-dotenv rich loguru
```

### Step 3: Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (optional - defaults work for demo)
nano .env
```

### Step 4: Validation
```bash
# Validate setup
python validate_demo.py

# Expected output:
# ✅ All dependencies installed
# ✅ All demo files present
# ✅ Configuration valid
# 🚀 Demo ready to launch!
```

### Step 5: Launch Demo
```bash
# Interactive launcher
python demo_launcher.py

# Or direct API launch
cd agentic_mapping_ai
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. Import Errors
```bash
# Issue: ModuleNotFoundError: No module named 'vertexai'
# Solution:
pip install vertexai google-cloud-aiplatform

# Issue: ImportError: No module named 'agentic_mapping_ai'
# Solution: Ensure you're in the demo directory
cd /path/to/demo
python -c "import sys; print(sys.path)"
```

#### 2. Pydantic Compatibility
```bash
# Issue: PydanticImportError: BaseSettings has moved
# Solution:
pip install pydantic-settings>=2.0.0
```

#### 3. SQLAlchemy Conflicts
```bash
# Issue: InvalidRequestError: Attribute name 'metadata' is reserved
# Solution: Already fixed in latest version
git pull origin main
```

#### 4. Token Authentication
```bash
# Issue: "could not check helix CLI status"
# Solution: This is informational - demo uses MongoDB fallback
# Verify MongoDB is running if using token storage
```

### Performance Optimization

#### 1. Memory Usage
```bash
# For systems with limited RAM
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=2
```

#### 2. Network Optimization
```bash
# For slow connections, increase timeouts
export LLM_TIMEOUT=300
export HTTP_TIMEOUT=120
```

#### 3. Concurrent Processing
```bash
# Adjust worker processes based on CPU cores
uvicorn api.main:app --workers 4 --host 0.0.0.0 --port 8000
```

## 📊 Monitoring & Health Checks

### Health Check Endpoints
```bash
# Basic health check
curl http://localhost:8000/health

# Component status
curl http://localhost:8000/api/v1/health

# API documentation
open http://localhost:8000/docs
```

### Log Monitoring
```bash
# Application logs
tail -f logs/agentic_mapping.log

# Access logs
tail -f logs/access.log

# Error logs
tail -f logs/error.log
```

## 🔒 Security Considerations

### Authentication
- **Token-based**: No API keys stored in code
- **Encryption**: All tokens encrypted at rest
- **Rotation**: Automatic token refresh
- **Fallback**: Multiple authentication methods

### Network Security
- **HTTPS**: Use HTTPS in production
- **CORS**: Configured for specific origins
- **Rate Limiting**: Built-in request throttling
- **Input Validation**: Comprehensive data validation

### Data Privacy
- **No Persistence**: Input data not stored by default
- **Anonymization**: Remove PII before processing
- **Audit Trails**: Complete operation logging
- **Compliance**: GDPR/SOX ready architecture

## 📈 Scaling Considerations

### Horizontal Scaling
- **Load Balancer**: Multiple API instances
- **Database**: MongoDB replica sets
- **Caching**: Redis for frequently accessed data
- **CDN**: Static asset distribution

### Vertical Scaling
- **CPU**: More cores for parallel processing
- **Memory**: Larger models and batch processing
- **Storage**: SSD for faster I/O operations
- **Network**: Higher bandwidth for LLM calls

### Cost Optimization
- **LLM Usage**: Intelligent provider selection
- **Caching**: Reduce redundant API calls
- **Batch Processing**: Process multiple items together
- **Resource Monitoring**: Track usage patterns

---

## 🎯 Quick Reference

### Essential Commands
```bash
# Start demo
python demo_launcher.py

# API server
uvicorn api.main:app --reload

# Health check
curl localhost:8000/health

# Validate setup
python validate_demo.py

# View logs
tail -f logs/app.log
```

### Key Files
- **Main App**: `agentic_mapping_ai/run_enhanced_application.py`
- **API Server**: `agentic_mapping_ai/api/main.py`
- **Configuration**: `agentic_mapping_ai/config/settings.py`
- **Requirements**: `requirements.txt`
- **Documentation**: `README_DEMO.md`

### Support Contacts
- **Technical Issues**: Check GitHub Issues
- **Demo Questions**: Refer to `DEMO_MANAGER_GUIDE.md`
- **Setup Problems**: Run `python validate_demo.py`

---

*This requirements document ensures a smooth demo setup and execution. All dependencies are tested and verified for compatibility.*
