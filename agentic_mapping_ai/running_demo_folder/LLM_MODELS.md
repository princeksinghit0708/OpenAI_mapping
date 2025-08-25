# 🚀 LLM Models Configuration

## 📋 **Default LLM Service Models**

The Agentic Mapping AI platform uses the following default models from your LLM service:

### 🤖 **Primary Default Models**

| Provider | Model | Description |
|----------|-------|-------------|
| **Claude** | `claude-3-7-sonnet@20250219` | **Default Model** - Claude 3.7 Sonnet |
| **Gemini** | `gemini-2.5-pro` | Google Gemini 2.5 Pro |
| **Stellar** | `Meta-Llama-3.2-90B-Vision-Instruct` | Meta Llama 3.2 90B Vision |

### ⚙️ **Configuration**

The default model is configured in:
- **File**: `config/settings.py`
- **Setting**: `LLMSettings.default_model`
- **Current Value**: `claude-3-7-sonnet@20250219`

### 🔧 **How to Change Default Model**

#### **Option 1: Environment Variable**
```bash
export LLM_DEFAULT_MODEL="gemini-2.5-pro"
```

#### **Option 2: Update Settings File**
```python
# In config/settings.py
class LLMSettings(BaseSettings):
    default_model: str = Field(default="gemini-2.5-pro")
    default_provider: str = Field(default="gemini")
```

#### **Option 3: Runtime Configuration**
```python
from config.settings import LLMSettings

llm_settings = LLMSettings()
llm_settings.default_model = "Meta-Llama-3.2-90B-Vision-Instruct"
```

### 🎯 **Model Selection by Use Case**

| Use Case | Recommended Model | Reason |
|----------|-------------------|---------|
| **General AI Tasks** | `claude-3-7-sonnet@20250219` | Balanced performance and cost |
| **Code Generation** | `gemini-2.5-pro` | Excellent code understanding |
| **Vision Tasks** | `Meta-Llama-3.2-90B-Vision-Instruct` | Advanced vision capabilities |
| **High Performance** | `claude-3-7-sonnet@20250219` | Claude's reasoning capabilities |

### 📊 **Model Capabilities**

#### **Claude 3.7 Sonnet**
- ✅ **Reasoning**: Excellent for complex logic
- ✅ **Code**: Strong programming capabilities
- ✅ **Safety**: Built-in safety measures
- ✅ **Cost**: Balanced pricing

#### **Gemini 2.5 Pro**
- ✅ **Code**: Superior code generation
- ✅ **Multimodal**: Text, code, images
- ✅ **Performance**: High-speed processing
- ✅ **Integration**: Google ecosystem

#### **Meta Llama 3.2 90B Vision**
- ✅ **Vision**: Advanced image understanding
- ✅ **Open Source**: Community-driven
- ✅ **Customization**: Highly configurable
- ✅ **Multilingual**: Multiple languages

### 🚀 **Quick Start**

The demo automatically uses the default model from your LLM service. No additional configuration needed!

**Current Default**: `claude-3-7-sonnet@20250219`

### 📝 **Notes**

- All models are accessed through your centralized LLM service
- Token-based authentication is used (no API keys needed)
- Models can be switched dynamically during runtime
- Fallback mechanisms ensure service availability
