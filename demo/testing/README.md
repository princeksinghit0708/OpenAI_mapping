# 🧪 Testing Suite for Agentic Mapping AI

This folder contains comprehensive testing scripts to verify that your LLM service and AI agents are working correctly.

## 📁 Test Files

### 1. **`test_llm_service.py`** - Complete LLM Testing Suite
- **Purpose**: Comprehensive testing of all LLM functionality
- **Tests**: Import, basic responses, multiple providers, chat agent, API endpoints
- **Usage**: Run when you want to verify everything is working

### 2. **`quick_llm_test.py`** - Quick LLM Test
- **Purpose**: Fast verification that AI models can respond
- **Tests**: Basic import and response generation
- **Usage**: Quick check before running full tests

### 3. **`test_chat_agent.py`** - Chat Agent Testing
- **Purpose**: Focused testing of conversational AI functionality
- **Tests**: Agent creation, response generation, intent detection, async methods
- **Usage**: When you specifically want to test chat capabilities

### 4. **`test_langchain_huggingface.py`** - LangChain + Hugging Face Testing
- **Purpose**: Test local models using LangChain and Hugging Face libraries
- **Tests**: Local model loading, LangChain integration, embeddings, vector stores
- **Usage**: When you want to test without API keys using local models

### 5. **`test_llm_service_direct.py`** - Direct LLM Service Testing
- **Purpose**: Test LLM service directly with local model fallbacks
- **Tests**: Service capabilities, local integration, RAG functionality
- **Usage**: When you want to test the service without external dependencies

## 🚀 How to Run Tests

### **Prerequisites**
Make sure you're in the demo directory:
```bash
cd C:\CitiDev\POC\171306.github-repo.genai-poc\demo
```

### **Option 1: Quick Test (Recommended First)**
```bash
cd testing
python quick_llm_test.py
```
**Expected Output**: ✅ Import successful + AI response

### **Option 2: Chat Agent Test**
```bash
cd testing
python test_chat_agent.py
```
**Expected Output**: ✅ All chat agent tests passing

### **Option 3: Full Test Suite**
```bash
cd testing
python test_llm_service.py
```
**Expected Output**: ✅ All tests passing with detailed results

### **Option 4: LangChain + Hugging Face Testing**
```bash
cd testing
python test_langchain_huggingface.py
```
**Expected Output**: ✅ Local models working without API keys

### **Option 5: Direct LLM Service Testing**
```bash
cd testing
python test_llm_service_direct.py
```
**Expected Output**: ✅ Service working with local model fallbacks

## 🎯 What Each Test Verifies

### **LLM Service Tests**
- ✅ **Import**: Can import the LLM service module
- ✅ **Basic Response**: AI models can generate responses
- ✅ **Multiple Providers**: Claude, Azure, Stellar are accessible
- ✅ **Error Handling**: Graceful handling of failures

### **Chat Agent Tests**
- ✅ **Creation**: Can instantiate ConversationalAgent
- ✅ **Response Generation**: Can process messages and respond
- ✅ **Intent Detection**: Can identify user intentions
- ✅ **Async Methods**: Async functionality works correctly

### **API Tests**
- ✅ **Health Endpoint**: Server is running and healthy
- ✅ **Chat Endpoint**: Chat API is functional
- ✅ **Response Format**: API returns proper JSON responses

### **Local Model Tests**
- ✅ **LangChain Integration**: Local models working through LangChain
- ✅ **Hugging Face Models**: Local model loading and inference
- ✅ **Embeddings**: Local embedding generation
- ✅ **Vector Stores**: Local RAG functionality
- ✅ **No API Keys**: Development without external dependencies

## 🔍 Troubleshooting

### **Common Issues & Solutions**

#### **1. Import Errors**
```bash
# Make sure you're in the demo directory
cd C:\CitiDev\POC\171306.github-repo.genai-poc\demo

# Check if modules exist
dir agentic_mapping_ai\agents\chat_agent.py
dir agentic_mapping_ai\llm_service.py
```

#### **2. LLM Service Not Responding**
```bash
# Check environment variables
echo %BASE_URL%
echo %DEV_MONGO_USER%
echo %DEV_MONGO_KEY%

# Test with simple import
python -c "from agentic_mapping_ai.llm_service import llm_service; print('OK')"
```

#### **3. Chat Agent Creation Fails**
```bash
# Check if all abstract methods are implemented
python -c "from agentic_mapping_ai.agents.chat_agent import ConversationalAgent; print('OK')"
```

#### **4. API Server Not Running**
```bash
# Start the API server first
cd agentic_mapping_ai
python run_enhanced_application.py
# Select option 1 to start server
```

## 📊 Expected Test Results

### **✅ Successful Test Run Should Show:**
```
🚀 LLM Service & AI Agent Testing Suite
============================================================
🧪 Test 1: LLM Service Import
✅ LLM Service imported successfully
Service type: <class 'agentic_mapping_ai.llm_service.LLMService'>

🧪 Test 2: Basic LLM Response
✅ LLM Response received:
Response: Hello! I'm a helpful data mapping assistant...
Response length: 45 characters

🧪 Test 3: LLM Provider Testing
✅ CLAUDE: Hello!...
✅ AZURE: Hello!...
✅ STELLAR: Hello!...

🧪 Test 4: Chat Agent Testing
✅ Chat agent created successfully
✅ Agent response: Hello! I can help you with...
✅ Intent detected: greeting
✅ Confidence: 0.95

🧪 Test 5: API Endpoint Testing
✅ Health endpoint working
✅ Chat endpoint working
```

### **❌ Failed Test Run Might Show:**
```
❌ Import failed: No module named 'agentic_mapping_ai.llm_service'
❌ Basic response failed: Token authentication failed
❌ Chat agent test failed: Can't instantiate abstract class
❌ API server not running
```

## 🎯 Test Scenarios

### **Scenario 1: First-Time Setup**
1. Run `quick_llm_test.py` - Should pass
2. Run `test_chat_agent.py` - Should pass
3. Run `test_llm_service.py` - Should pass all tests

### **Scenario 2: After Code Changes**
1. Run `quick_llm_test.py` to verify basic functionality
2. Run specific test files for areas you modified

### **Scenario 3: Production Verification**
1. Run full test suite before deployment
2. Check all providers are accessible
3. Verify API endpoints are responding

## 🚀 Next Steps After Successful Tests

Once all tests pass:

1. **Start the API server**: `python run_enhanced_application.py`
2. **Access the web interface**: `http://localhost:8000`
3. **Test with real data**: Upload Excel files and process them
4. **Use the chat interface**: Interact with the conversational AI

## 📞 Support

If tests continue to fail:
1. Check the error messages carefully
2. Verify all dependencies are installed
3. Ensure environment variables are set correctly
4. Check that the API server is running

**Happy Testing! 🧪✨**
