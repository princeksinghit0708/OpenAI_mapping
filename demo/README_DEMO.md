# 🎯 Agent Framework Demo

This demo folder contains **only the essential files** needed to demonstrate the advanced agentic AI mapping system with multi-agent orchestration.

## 🚀 Quick Demo Start

### **Option 1: Agent Framework Demo (Recommended)**
```bash
cd demo
python agentic_mapping_ai/run_enhanced_application.py
```

**Demo Menu Options:**
- **Option 1**: Start Enhanced API Server (FastAPI)
- **Option 2**: Run Enhanced Features Demo ⭐ **Best for Demo**
- **Option 5**: Health Check & System Status

### **Option 2: Direct Enhanced Application**
```bash
cd demo
python enhanced_main.py
```

## 📁 Demo File Structure

```
demo/
├── README_DEMO.md                              # This file
├── .env                                        # Demo configuration
├── enhanced_main.py                            # Backup direct application
├── gpt4_prompt_engine.py                       # Prompt generation
├── faiss_integration.py                        # Vector search
├── ebs_IM_account_DATAhub_mapping_v8.0.xlsx   # Demo data (add manually)
├── requirements.txt                            # Python dependencies
└── agentic_mapping_ai/
    ├── llm_service.py                          # 🔐 Token-based auth
    ├── run_enhanced_application.py             # 🎯 Main demo launcher
    ├── agents/
    │   ├── base_agent.py                       # Base agent class
    │   ├── enhanced_base_agent.py              # Advanced agent class
    │   ├── orchestrator.py                     # Agent orchestration
    │   ├── enhanced_orchestrator_v2.py         # Advanced orchestration
    │   ├── metadata_validator.py               # Schema validation
    │   └── code_generator.py                   # PySpark code generation
    ├── core/
    │   └── models.py                           # Data models
    ├── knowledge/
    │   └── rag_engine.py                       # RAG integration
    ├── config/
    │   ├── settings.py                         # Basic settings
    │   └── enhanced_settings.py                # Advanced settings
    └── api/
        └── main.py                             # FastAPI endpoints
```

## 🎪 Demo Features

### **🤖 Multi-Agent System**
- **OrchestratorAgent**: Coordinates complex workflows
- **MetadataValidator**: Validates Excel schemas and field definitions
- **CodeGeneratorAgent**: Generates production-ready PySpark code
- **EnhancedOrchestrator**: AI-powered workflow planning

### **🔐 Token-Based Authentication**
- No API keys required
- Secure token management via helix CLI
- MongoDB fallback for enterprise environments
- Multi-provider support: Azure, Claude, Gemini, Stellar

### **📊 Advanced Features**
- **Excel Intelligence**: Auto-detects columns and sheets
- **Goldref Logic**: Handles complex lookup transformations
- **Vector Search**: FAISS-powered similarity matching
- **Production Code**: Banking-grade PySpark generation

## 🎯 Demo Script (2-Hour Presentation)

### **Phase 1: Setup (2 minutes)**
```bash
cd demo
# Add your Excel file: ebs_IM_account_DATAhub_mapping_v8.0.xlsx
python agentic_mapping_ai/run_enhanced_application.py
```

### **Phase 2: Agent Demo (20 minutes)**
1. **Select Option 2**: "Run Enhanced Features Demo"
2. **Show**: Multi-agent coordination
3. **Highlight**: Token-based authentication
4. **Demonstrate**: Excel processing with goldref logic

### **Phase 3: API Demo (15 minutes)**
1. **Select Option 1**: "Start Enhanced API Server"
2. **Access**: http://localhost:8000/docs
3. **Show**: FastAPI endpoints and real-time processing

### **Phase 4: Health Check (5 minutes)**
1. **Select Option 5**: "Health Check & System Status"
2. **Show**: System monitoring and metrics

## 🔧 Prerequisites

### **Required:**
- Python 3.8+
- Access to helix CLI (for token authentication)
- Your Excel file: `ebs_IM_account_DATAhub_mapping_v8.0.xlsx`

### **Optional:**
- MongoDB access (for token storage fallback)
- Docker (for containerized demo)

## 🎬 Demo Talking Points

### **🔐 Authentication Innovation**
"Traditional LLM applications require managing multiple API keys. Our system uses enterprise-grade token authentication with automatic refresh and fallback mechanisms."

### **🤖 Intelligent Agents**
"Instead of simple scripts, we have specialized AI agents that can reason, plan, and coordinate complex data transformation workflows."

### **📊 Production Ready**
"This isn't just a proof-of-concept. Every generated PySpark transformation includes error handling, logging, and performance optimizations suitable for banking production environments."

### **🎯 EBS IM Focus**
"Specifically designed for EBS IM Account DataHub mappings with intelligent goldref lookup capabilities and complex derivation logic."

## 🚨 Troubleshooting

### **If Agent Demo Fails:**
```bash
# Fallback to direct application
python enhanced_main.py
```

### **If Token Auth Fails:**
```bash
# Check helix CLI
which helix
helix auth access-token print -a
```

### **If Excel File Missing:**
- Add `ebs_IM_account_DATAhub_mapping_v8.0.xlsx` to the demo folder
- Or use any Excel mapping file and update `.env`

---

**Ready for your demo! 🎉 Focus on the agent orchestration and token authentication as key differentiators.**
