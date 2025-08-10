# Migration to Token-Based Authentication

## Overview

The entire Agentic Mapping AI project has been migrated from API key-based authentication to token-based authentication using the `LLMService` class. This change improves security and centralizes authentication management.

## What Changed

### 1. Authentication Method
- **Before**: Used individual API keys for OpenAI, Anthropic, Google, etc.
- **After**: Uses token-based authentication via `helix auth access-token print -a` command
- **Fallback**: MongoDB token storage for backup token retrieval

### 2. Files Updated

#### Core Agent Files
- `agentic_mapping_ai/agents/base_agent.py`
  - Removed `ChatOpenAI` direct initialization
  - Added `LLMService` integration
  - Updated `chat()` and `health_check()` methods

#### Main Application Files
- `main.py`
  - Removed OpenAI API key requirements
  - Updated to use `LLMService`
  - Modified `setup_openai()` → `setup_llm_service()`

- `enhanced_main.py`
  - Similar updates to main.py
  - Removed API key dependencies

#### Configuration Files
- `agentic_mapping_ai/config/settings.py`
  - Removed API key fields from `LLMSettings`
  - Added `default_provider` configuration

- `agentic_mapping_ai/config/enhanced_settings.py`
  - Updated provider configurations to use token auth
  - Removed API key references

- `agentic_mapping_ai/env_template.txt`
  - Updated template to reflect token-based auth
  - Added MongoDB configuration for token storage

#### Utility Files
- `faiss_integration.py`
  - Removed OpenAI API key dependency
  - Implemented hash-based embedding simulation
  - Updated constructor to not require API key

- `run_application.py`
  - Removed API key prompts
  - Updated environment file creation

### 3. LLM Service Integration

The `LLMService` class (`agentic_mapping_ai/llm_service.py.py`) provides:

- **Token Management**: Automatic token retrieval and refresh
- **Multi-Provider Support**: Azure, Stellar, Gemini, Claude
- **Fallback Mechanisms**: MongoDB token storage if primary method fails
- **Unified Interface**: Single API for all LLM interactions

## Usage

### Prerequisites

1. **Helix CLI**: Ensure `helix` command is available and configured
   ```bash
   helix auth access-token print -a
   ```

2. **MongoDB Access** (Optional): For token storage fallback
   - Set `DEV_MONGO_USER` and `DEV_MONGO_KEY` environment variables

### Running the Application

No API keys required! Simply run:

```bash
# Main application
python main.py

# Enhanced application
python enhanced_main.py

# Quick setup
python run_application.py
```

### Environment Configuration

Create a `.env` file with:

```bash
# Token-based authentication - no API keys required
EXCEL_FILE=Testing1 copy.xlsx
RESULTS_DIR=results
OUTPUT_DIR=output

# Optional: MongoDB for token storage
DEV_MONGO_USER=your_mongo_user
DEV_MONGO_KEY=your_mongo_key

# LLM Configuration
LLM_DEFAULT_MODEL=gpt-4
LLM_DEFAULT_PROVIDER=azure
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
```

## API Reference

### LLM Service Usage

```python
from agentic_mapping_ai.llm_service import llm_service

# Query any supported model
response = llm_service.query_llm(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.1,
    max_tokens=2000,
    llm_provider="azure"  # azure, stellar, gemini, claude
)

# Use default model
response = llm_service.call_default_llm(
    messages=messages,
    temperature=0.2
)
```

### Supported Providers

1. **Azure**: Default GPT-4 models
2. **Stellar**: Meta-Llama models
3. **Gemini**: Google's Gemini models
4. **Claude**: Anthropic's Claude models

## Benefits

1. **Security**: No API keys stored in code or environment
2. **Centralized Auth**: Single authentication point
3. **Auto-Refresh**: Tokens automatically refreshed
4. **Fallback**: Multiple token sources for reliability
5. **Simplified Setup**: No complex API key management

## Troubleshooting

### Token Issues
```bash
# Test token generation
helix auth access-token print -a

# Check MongoDB connection (if using)
python -c "from agentic_mapping_ai.llm_service import get_token_from_mongo; print(get_token_from_mongo())"
```

### Common Errors
- **"Failed to retrieve token"**: Ensure helix CLI is installed and authenticated
- **"MongoDB connection failed"**: Check DEV_MONGO_USER and DEV_MONGO_KEY
- **"Model not found"**: Verify the model name and provider combination

## Migration Checklist

- [x] Updated base agent classes
- [x] Modified main application files
- [x] Updated configuration files
- [x] Removed API key dependencies
- [x] Updated FAISS integration
- [x] Created migration documentation
- [x] Updated environment templates

## Next Steps

1. Test the integration with actual data
2. Verify all model providers work correctly
3. Update any remaining files that might have API key references
4. Consider implementing proper embedding service for FAISS
