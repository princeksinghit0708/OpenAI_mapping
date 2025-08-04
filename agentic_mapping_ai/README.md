# Agentic AI Mapping & Code Generation Platform

## 🎯 Overview
An intelligent, agentic AI system that validates document metadata, generates PySpark code, creates unit tests, and manages data mapping workflows using RAG (Retrieval Augmented Generation) and vector databases.

## 🏗️ Architecture

### Core Components
- **Agent Layer**: Specialized AI agents for different tasks
- **Knowledge Layer**: Vector DB + RAG for intelligent retrieval
- **Generation Layer**: Code and test generation
- **Orchestration Layer**: Multi-agent coordination

### Tech Stack
- **Framework**: LangChain + CrewAI
- **Vector DB**: Chroma (local) / Pinecone (cloud)
- **LLM**: OpenAI GPT-4 / Claude
- **Database**: PostgreSQL
- **API**: FastAPI
- **UI**: Streamlit
- **Code Gen**: PySpark, SQL, Python
- **Testing**: pytest, unittest

## 📁 Project Structure

```
agentic_mapping_ai/
├── agents/                 # AI Agents
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── metadata_validator.py
│   ├── schema_mapper.py
│   ├── code_generator.py
│   ├── test_generator.py
│   └── orchestrator.py
├── core/                  # Core functionality
│   ├── __init__.py
│   ├── models.py         # Data models
│   ├── database.py       # DB connections
│   └── exceptions.py     # Custom exceptions
├── knowledge/            # Knowledge management
│   ├── __init__.py
│   ├── vector_store.py   # Vector DB operations
│   ├── rag_engine.py     # RAG implementation
│   └── embeddings.py     # Text embeddings
├── api/                  # REST API
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── routes/          # API routes
│   └── middleware.py    # API middleware
├── ui/                   # User interface
│   ├── streamlit_app.py # Main UI
│   └── components/      # UI components
├── templates/            # Prompt templates
│   ├── code_generation/
│   ├── validation/
│   └── testing/
├── config/              # Configuration
│   ├── settings.py
│   └── prompts.yaml
├── data/               # Data storage
│   ├── input/
│   ├── processed/
│   └── embeddings/
├── output/             # Generated output
│   ├── code/
│   ├── tests/
│   └── reports/
├── tests/              # Unit tests
├── utils/              # Utilities
└── requirements.txt    # Dependencies
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the Application**
   ```bash
   # API Server
   uvicorn api.main:app --reload
   
   # UI Dashboard
   streamlit run ui/streamlit_app.py
   ```

## 🤖 Agents Overview

### 1. Metadata Validation Agent
- Validates JSON/XML document structure
- Checks field mappings and constraints
- Reports validation errors and suggestions

### 2. Schema Mapping Agent
- Maps source schemas to target schemas
- Handles complex nested structures
- Maintains mapping history and versions

### 3. Code Generation Agent
- Generates PySpark transformation code
- Creates SQL scripts and data pipelines
- Optimizes code for performance

### 4. Test Generation Agent
- Creates comprehensive unit tests
- Generates integration test scenarios
- Validates data quality checks

### 5. Orchestrator Agent
- Coordinates multi-agent workflows
- Manages task dependencies
- Handles error recovery and retries

## 🧠 RAG & Knowledge Management

- **Vector Store**: Stores embeddings of code patterns, schemas, and documentation
- **Retrieval**: Context-aware retrieval for better code generation
- **Learning**: Continuous learning from user feedback and execution results

## 📊 Features

✅ Document metadata validation  
✅ Intelligent schema mapping  
✅ PySpark code generation  
✅ Unit test automation  
✅ RAG-powered context retrieval  
✅ Multi-agent orchestration  
✅ Real-time monitoring  
✅ Feedback learning loop  

## 🔧 Configuration

See `config/settings.py` for detailed configuration options.

## 📝 Usage Examples

See the `examples/` directory for detailed usage examples and tutorials.