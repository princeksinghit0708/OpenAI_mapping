# 📁 File Interaction Map - Agentic Mapping AI

## 🎯 Complete File Dependencies and Call Flow

### **📊 File Interaction Matrix**

| **From File** | **Calls** | **Method/Function** | **Data Passed** | **Returns** |
|---------------|-----------|-------------------|-----------------|-------------|
| `demo_launcher.py` | `orchestrator.py` | `OrchestratorAgent()` | AgentConfig | Agent Instance |
| `orchestrator.py` | `metadata_validator.py` | `validate_document_metadata()` | Document Dict | ValidationResult |
| `orchestrator.py` | `code_generator.py` | `generate_transformation_code()` | CodeGenerationRequest | GeneratedCode |
| `orchestrator.py` | `test_generator.py` | `generate_comprehensive_tests()` | GeneratedCode | TestSuite |
| `metadata_validator.py` | `llm_service.py` | `query_llm()` | Prompt + Context | LLM Response |
| `code_generator.py` | `llm_service.py` | `query_llm()` | Code Prompt | Generated Code |
| `test_generator.py` | `llm_service.py` | `query_llm()` | Test Prompt | Test Cases |
| `base_agent.py` | `llm_service.py` | `initialize()` | Config | Service Instance |
| `api/main.py` | `orchestrator.py` | `_execute_core_logic()` | Workflow Data | Results Dict |
| `enhanced_main.py` | `rag_engine.py` | `retrieve()` | Query String | Knowledge Results |
| `rag_engine.py` | `llm_service.py` | `encode_text()` | Text String | Embedding Vector |

---

## 🔄 **Detailed Call Sequences**

### **Sequence 1: Demo Launcher → Agent Framework**

```python
# File: demo_launcher.py (Line 45)
def run_agent_framework_demo():
    # Step 1: Load demo data
    metadata_files = load_demo_metadata()  # → results/*.json
    
    # Step 2: Initialize orchestrator
    config = AgentConfig(name="Demo Orchestrator")
    orchestrator = OrchestratorAgent(config)  # → orchestrator.py
    
    # Step 3: Execute workflow
    results = orchestrator.execute_full_pipeline(metadata_files)
    
    return results

# File: orchestrator.py (Line 150)
def execute_full_pipeline(self, data):
    # Step 1: Metadata validation
    validation_result = self.metadata_validator.validate_document_metadata(data)
    # → metadata_validator.py:validate_document_metadata()
    
    # Step 2: Code generation  
    code_result = self.code_generator.generate_transformation_code(validation_result)
    # → code_generator.py:generate_transformation_code()
    
    # Step 3: Test generation
    test_result = self.test_generator.generate_comprehensive_tests(code_result)
    # → test_generator.py:generate_comprehensive_tests()
    
    return {
        'validation': validation_result,
        'code': code_result,
        'tests': test_result
    }
```

### **Sequence 2: API Request → Agent Processing**

```python
# File: api/main.py (Line 165)
@app.post("/api/v1/validate")
async def validate_document(request: DocumentValidationRequest):
    # Step 1: Extract request data
    document = request.document  # Pydantic validation
    
    # Step 2: Call orchestrator
    workflow_result = await orchestrator_agent._execute_core_logic({
        "workflow_type": WorkflowType.VALIDATION_ONLY.value,
        "workflow_data": request.dict()
    })
    # → orchestrator.py:_execute_core_logic()
    
    # Step 3: Format response
    return ValidationResponse(
        success=workflow_result.get("success"),
        data=workflow_result.get("validation_result")
    )

# File: orchestrator.py (Line 300)
async def _execute_core_logic(self, workflow_data):
    workflow_type = workflow_data["workflow_type"]
    
    if workflow_type == WorkflowType.VALIDATION_ONLY.value:
        # Route to validation workflow
        return await self._execute_validation_workflow(workflow_data)
        # → orchestrator.py:_execute_validation_workflow()
    
    elif workflow_type == WorkflowType.CODE_GENERATION.value:
        # Route to code generation workflow  
        return await self._execute_code_generation_workflow(workflow_data)
        # → orchestrator.py:_execute_code_generation_workflow()
```

### **Sequence 3: Enhanced Main → Excel Processing**

```python
# File: enhanced_main.py (Line 585)
def run_enhanced(self):
    # Step 1: Load Excel data
    if not self.load_excel_data():  # → enhanced_main.py:load_excel_data()
        return
    
    # Step 2: Load table metadata
    self._load_table_metadata_enhanced()  # → enhanced_main.py:_load_table_metadata_enhanced()
    
    # Step 3: Build vector database
    self._build_enhanced_vector_database()  # → enhanced_main.py:_build_enhanced_vector_database()
    
    # Step 4: Process mappings
    self.process_all_mappings_enhanced()  # → enhanced_main.py:process_all_mappings_enhanced()

# File: enhanced_main.py (Line 142)
def load_excel_data(self) -> bool:
    # Step 1: Read Excel sheets
    mapping_df = pd.read_excel(self.excel_file, sheet_name=self.mapping_sheet_name)
    goldref_df = pd.read_excel(self.excel_file, sheet_name=self.goldref_sheet_name)
    
    # Step 2: Detect structure
    column_mapping = self.detect_excel_structure(mapping_df)
    # → enhanced_main.py:detect_excel_structure()
    
    # Step 3: Standardize data
    self.processed_mapping_data = self._standardize_mapping_data(mapping_df, column_mapping)
    # → enhanced_main.py:_standardize_mapping_data()
    
    return True
```

---

## 🤖 **LLM Service Integration Points**

### **All Agent → LLM Service Calls**

```python
# File: metadata_validator.py (Line 85)
def validate_document_metadata(self, document):
    prompt = self._build_validation_prompt(document)
    
    # Call LLM service
    response = self.llm_service.query_llm(
        prompt=prompt,
        context={"task": "metadata_validation"},
        provider="azure"  # or fallback to claude/gemini
    )
    # → llm_service.py:query_llm()
    
    return self._parse_validation_response(response)

# File: code_generator.py (Line 120)
def generate_transformation_code(self, request):
    prompt = self._build_code_generation_prompt(request)
    
    # Call LLM service with code-specific settings
    response = self.llm_service.query_llm(
        prompt=prompt,
        context={"task": "code_generation", "language": "pyspark"},
        temperature=0.1,  # Lower temperature for code
        max_tokens=2000
    )
    # → llm_service.py:query_llm()
    
    return self._parse_generated_code(response)

# File: test_generator.py (Line 100)
def generate_comprehensive_tests(self, code):
    prompt = self._build_test_generation_prompt(code)
    
    # Call LLM service for test generation
    response = self.llm_service.query_llm(
        prompt=prompt,
        context={"task": "test_generation"},
        provider="claude"  # Claude often better for tests
    )
    # → llm_service.py:query_llm()
    
    return self._parse_test_cases(response)
```

### **LLM Service → Provider Routing**

```python
# File: llm_service.py (Line 150)
def query_llm(self, prompt, context=None, provider=None, **kwargs):
    # Step 1: Select provider
    selected_provider = provider or self.default_provider
    
    # Step 2: Route to appropriate provider
    if selected_provider == "azure":
        return self._call_azure_openai(prompt, **kwargs)
        # → llm_service.py:_call_azure_openai()
    
    elif selected_provider == "claude":
        return self._call_anthropic(prompt, **kwargs)
        # → llm_service.py:_call_anthropic()
    
    elif selected_provider == "gemini":
        return self._call_google_gemini(prompt, **kwargs)
        # → llm_service.py:_call_google_gemini()
    
    # Step 3: Fallback on failure
    except Exception as e:
        return self._try_fallback_providers(prompt, **kwargs)
        # → llm_service.py:_try_fallback_providers()
```

---

## 📚 **RAG Engine Knowledge Flow**

### **Agent → RAG Engine Queries**

```python
# File: metadata_validator.py (Line 95)
def _enhance_validation_with_knowledge(self, field_definitions):
    # Query RAG for similar validation patterns
    query = f"validation patterns for {field_definitions['type']}"
    
    knowledge_results = self.rag_engine.retrieve(
        query=query,
        max_results=3,
        category_filter="validation"
    )
    # → rag_engine.py:retrieve()
    
    return self._apply_knowledge_to_validation(knowledge_results)

# File: code_generator.py (Line 140)
def _enhance_code_with_patterns(self, base_code):
    # Query RAG for similar code patterns
    query = f"pyspark transformation patterns for {base_code['operation']}"
    
    pattern_results = self.rag_engine.retrieve(
        query=query,
        max_results=5,
        category_filter="code_patterns"
    )
    # → rag_engine.py:retrieve()
    
    return self._apply_patterns_to_code(pattern_results, base_code)
```

### **RAG Engine → Vector Processing**

```python
# File: rag_engine.py (Line 440)
async def retrieve(self, query, max_results=5, category_filter=None):
    # Step 1: Generate query embedding
    query_embedding = self._encode_text(query)
    # → rag_engine.py:_encode_text()
    
    # Step 2: Search FAISS index
    scores, indices = self.faiss_index.search(
        query_embedding.reshape(1, -1), 
        max_results
    )
    
    # Step 3: Filter and format results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if self._passes_category_filter(idx, category_filter):
            results.append(self._format_result(idx, score))
    
    return results

# File: rag_engine.py (Line 169)
def _encode_text(self, text):
    if self.embedding_model is not None:
        # Online mode: Use SentenceTransformer
        return self.embedding_model.encode([text])[0]
    else:
        # Offline mode: Use hash-based embedding
        return self._create_simple_embedding(text, 384)
        # → rag_engine.py:_create_simple_embedding()
```

---

## 🗂️ **Configuration and Settings Flow**

### **Settings Initialization Chain**

```python
# File: config/settings.py (Line 135)
settings = AppSettings()  # Global instance

# File: base_agent.py (Line 45)
def __init__(self, config: AgentConfig):
    # Import settings
    from agentic_mapping_ai.config.settings import settings
    self.settings = settings
    
    # Initialize LLM service
    self.llm_service = llm_service  # Global instance
    # → llm_service.py (imported globally)

# File: llm_service.py (Line 50)
def __init__(self):
    # Load configuration
    from agentic_mapping_ai.config.settings import settings
    self.config = settings.llm
    
    # Initialize providers based on config
    self._initialize_providers()
    # → llm_service.py:_initialize_providers()
```

### **Environment Variable Flow**

```
.env file → os.getenv() → Pydantic Settings → Application Config
```

```python
# File: config/settings.py (Line 15)
class DatabaseSettings(BaseSettings):
    url: str = Field(default="sqlite:///./app.db")
    echo: bool = Field(default=False)
    
    class Config:
        env_file = ".env"  # Reads from .env file
        env_prefix = "DATABASE_"  # Looks for DATABASE_URL, DATABASE_ECHO

# Environment variables:
# DATABASE_URL=postgresql://user:pass@localhost/db
# DATABASE_ECHO=true
```

---

## 📊 **Data Model Flow**

### **Pydantic Model Validation**

```python
# File: core/models.py (Line 85)
class ValidationResult(BaseModel):
    is_valid: bool
    field_definitions: List[FieldDefinition]
    errors: List[str] = []
    confidence_score: float = 0.0

# Usage in agent:
# File: metadata_validator.py (Line 110)
def validate_document_metadata(self, document):
    # Process document...
    
    # Create validated result
    result = ValidationResult(
        is_valid=len(errors) == 0,
        field_definitions=extracted_fields,
        errors=errors,
        confidence_score=calculate_confidence(extracted_fields)
    )
    # Pydantic automatically validates types and constraints
    
    return result
```

### **SQLAlchemy Database Models**

```python
# File: core/models.py (Line 179)
class Document(Base):
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    doc_metadata = Column(JSON)  # Fixed: was 'metadata'

# Usage in RAG engine:
# File: rag_engine.py (Line 200)
def store_document(self, content, metadata):
    # Create database record
    doc = Document(
        name=metadata.get('name'),
        doc_metadata=metadata  # Uses renamed column
    )
    
    session.add(doc)
    session.commit()
```

---

## 🔍 **Error Handling and Logging Flow**

### **Error Propagation Chain**

```python
# File: llm_service.py (Line 200)
def _call_azure_openai(self, prompt, **kwargs):
    try:
        response = self.azure_client.chat.completions.create(...)
        return response
    except Exception as e:
        logger.error(f"Azure OpenAI call failed: {e}")
        raise LLMServiceError(f"Azure OpenAI: {e}")
        # → Propagates to calling agent

# File: metadata_validator.py (Line 90)
def validate_document_metadata(self, document):
    try:
        response = self.llm_service.query_llm(prompt)
        return self._parse_response(response)
    except LLMServiceError as e:
        logger.error(f"LLM service error in validation: {e}")
        # Return partial result with error info
        return ValidationResult(
            is_valid=False,
            errors=[f"LLM service unavailable: {e}"]
        )
        # → Graceful degradation

# File: orchestrator.py (Line 180)
def execute_full_pipeline(self, data):
    try:
        validation_result = self.metadata_validator.validate_document_metadata(data)
        if not validation_result.is_valid:
            logger.warning("Validation failed, continuing with available data")
            # Continue processing with warnings
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return {"success": False, "error": str(e)}
        # → Return error to user
```

### **Logging Flow**

```
Agent Operation → Logger → Log File → Monitoring System
```

```python
# File: base_agent.py (Line 30)
import logging
logger = logging.getLogger(__name__)

# File: orchestrator.py (Line 160)
def execute_workflow(self, data):
    logger.info(f"Starting workflow execution with {len(data)} items")
    
    for item in data:
        logger.debug(f"Processing item: {item['id']}")
        result = self.process_item(item)
        logger.info(f"Item {item['id']} processed successfully")
    
    logger.info("Workflow execution completed")
```

---

## 🎯 **Performance Monitoring Points**

### **Key Metrics Collection Points**

```python
# File: base_agent.py (Line 100)
def track_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        logger.info(f"{func.__name__} completed in {duration:.2f}s")
        # → Metrics collection
        
        return result
    return wrapper

# Usage:
# File: metadata_validator.py (Line 85)
@track_performance
def validate_document_metadata(self, document):
    # Validation logic...
    pass
```

This comprehensive file interaction map shows exactly how every file connects to every other file, what data flows between them, and how the system orchestrates complex multi-agent workflows. Use this for debugging, optimization, and understanding the complete system architecture.
