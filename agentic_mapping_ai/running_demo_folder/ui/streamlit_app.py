"""
Streamlit UI for Agentic Mapping AI Platform
"""

import asyncio
import json
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional

# Page configuration
st.set_page_config(
    page_title="Agentic Mapping AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration
API_BASE_URL = "http://localhost:8000"


def check_api_health():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def call_api(endpoint: str, method: str = "GET", data: Dict = None):
    """Make API call"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, timeout=30)
        else:
            st.error(f"Unsupported HTTP method: {method}")
            return None
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        st.error("API request timed out")
        return None
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API server")
        return None
    except Exception as e:
        st.error(f"API call failed: {str(e)}")
        return None


def main():
    """Main application"""
    
    # Header
    st.title("🤖 Agentic Mapping AI Platform")
    st.markdown("Intelligent document metadata validation and code generation")
    
    # Check API health
    if not check_api_health():
        st.error("⚠️ API server is not available. Please start the API server first.")
        st.markdown("Run: `uvicorn api.main:app --reload`")
        return
    
    st.success("✅ API server is running")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        [
            "🏠 Dashboard",
            "📄 Document Validation", 
            "🔧 Code Generation",
            "🔄 Full Pipeline",
            "📊 Workflows",
            "🧠 Knowledge Base",
            "⚙️ Settings"
        ]
    )
    
    # Route to different pages
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📄 Document Validation":
        show_document_validation()
    elif page == "🔧 Code Generation":
        show_code_generation()
    elif page == "🔄 Full Pipeline":
        show_full_pipeline()
    elif page == "📊 Workflows":
        show_workflows()
    elif page == "🧠 Knowledge Base":
        show_knowledge_base()
    elif page == "⚙️ Settings":
        show_settings()


def show_dashboard():
    """Dashboard page"""
    st.header("📊 Dashboard")
    
    # Get system health
    health_data = call_api("/health")
    if health_data:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("System Status", "Healthy" if health_data.get("status") == "healthy" else "Unhealthy")
        
        with col2:
            st.metric("Version", health_data.get("version", "Unknown"))
        
        with col3:
            components = health_data.get("components", {})
            healthy_components = sum(1 for comp in components.values() if comp.get("status") == "healthy")
            st.metric("Components", f"{healthy_components}/{len(components)}")
        
        with col4:
            st.metric("Last Check", datetime.now().strftime("%H:%M:%S"))
    
    # Get knowledge base stats
    st.subheader("Knowledge Base Statistics")
    kb_stats = call_api("/api/v1/knowledge/stats")
    if kb_stats and kb_stats.get("success"):
        stats_data = kb_stats.get("data", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Documents", stats_data.get("total_documents", 0))
        with col2:
            st.metric("Categories", len(stats_data.get("categories", [])))
        
        if stats_data.get("categories"):
            st.write("**Categories:**", ", ".join(stats_data["categories"]))
    
    # Recent workflows
    st.subheader("Recent Workflows")
    workflows_data = call_api("/api/v1/workflows")
    if workflows_data and workflows_data.get("success"):
        workflows = workflows_data.get("data", {}).get("workflows", [])
        
        if workflows:
            df = pd.DataFrame(workflows)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No active workflows")


def show_document_validation():
    """Document validation page"""
    st.header("📄 Document Validation")
    
    tab1, tab2 = st.tabs(["JSON Input", "File Upload"])
    
    with tab1:
        st.subheader("Validate JSON Document")
        
        # JSON input
        json_input = st.text_area(
            "Paste your JSON document here:",
            height=400,
            placeholder='{\n  "dictionary": {\n    "providedKey": "PBWM.GCB_AAC_NAM.database_name"\n  },\n  "fields": [...]\n}'
        )
        
        # Validation rules
        validation_rules = st.multiselect(
            "Validation Rules (optional)",
            [
                "check_required_fields",
                "validate_data_types", 
                "check_naming_conventions",
                "validate_descriptions"
            ]
        )
        
        if st.button("Validate Document", type="primary"):
            if json_input.strip():
                try:
                    # Parse JSON
                    document = json.loads(json_input)
                    
                    # Call validation API
                    with st.spinner("Validating document..."):
                        result = call_api(
                            "/api/v1/validate",
                            method="POST",
                            data={
                                "document": document,
                                "validation_rules": validation_rules
                            }
                        )
                    
                    if result and result.get("success"):
                        validation_data = result.get("data", {})
                        
                        # Show validation status
                        if validation_data.get("is_valid"):
                            st.success("✅ Document is valid!")
                        else:
                            st.error("❌ Document validation failed")
                        
                        # Show errors
                        if validation_data.get("errors"):
                            st.subheader("Errors")
                            for error in validation_data["errors"]:
                                st.error(error)
                        
                        # Show warnings
                        if validation_data.get("warnings"):
                            st.subheader("Warnings")
                            for warning in validation_data["warnings"]:
                                st.warning(warning)
                        
                        # Show suggestions
                        if validation_data.get("suggestions"):
                            st.subheader("Suggestions")
                            for suggestion in validation_data["suggestions"]:
                                st.info(suggestion)
                    
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {str(e)}")
            else:
                st.warning("Please enter a JSON document")
    
    with tab2:
        st.subheader("Upload Document File")
        
        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=['json'],
            help="Upload a JSON document for validation"
        )
        
        if uploaded_file is not None:
            if st.button("Process Uploaded File", type="primary"):
                try:
                    # Read and parse file
                    content = uploaded_file.read()
                    document = json.loads(content)
                    
                    # Call upload API
                    with st.spinner("Processing uploaded file..."):
                        # Note: This would need to be implemented differently for file upload
                        # For now, we'll use the validation API
                        result = call_api(
                            "/api/v1/extract",
                            method="POST",
                            data={"document": document}
                        )
                    
                    if result and result.get("success"):
                        st.success("File processed successfully!")
                        
                        # Show results
                        data = result.get("data", {})
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Fields Found", data.get("field_count", 0))
                        with col2:
                            st.metric("Database Name", data.get("database_name", "Not found"))
                        
                        # Show extracted fields
                        if data.get("extracted_fields"):
                            st.subheader("Extracted Fields")
                            fields_df = pd.DataFrame(data["extracted_fields"])
                            st.dataframe(fields_df, use_container_width=True)
                
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON file: {str(e)}")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")


def show_code_generation():
    """Code generation page"""
    st.header("🔧 Code Generation")
    
    st.markdown("Generate PySpark, SQL, or Python code from schema mappings")
    
    # Code generation form
    with st.form("code_generation_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Source Schema")
            source_schema_name = st.text_input("Schema Name", value="source_schema")
            source_fields_json = st.text_area(
                "Fields (JSON format)",
                height=200,
                placeholder='[{"name": "field1", "data_type": "string", "is_nullable": true}]'
            )
        
        with col2:
            st.subheader("Target Schema")
            target_schema_name = st.text_input("Schema Name", value="target_schema")
            target_fields_json = st.text_area(
                "Fields (JSON format)",
                height=200,
                placeholder='[{"name": "field1", "data_type": "string", "is_nullable": true}]'
            )
        
        st.subheader("Generation Options")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            code_type = st.selectbox("Code Type", ["pyspark", "sql", "python"])
        
        with col4:
            optimization_level = st.selectbox("Optimization", ["basic", "standard", "advanced"])
        
        with col5:
            include_tests = st.checkbox("Include Tests", value=True)
        
        # Mapping rules
        st.subheader("Mapping Rules")
        mapping_rules_json = st.text_area(
            "Mapping Rules (JSON format)",
            height=150,
            placeholder='[{"source_field": "field1", "target_field": "field1", "transformation": null}]'
        )
        
        submitted = st.form_submit_button("Generate Code", type="primary")
        
        if submitted:
            try:
                # Parse inputs
                source_fields = json.loads(source_fields_json) if source_fields_json.strip() else []
                target_fields = json.loads(target_fields_json) if target_fields_json.strip() else []
                mapping_rules = json.loads(mapping_rules_json) if mapping_rules_json.strip() else []
                
                # Prepare request
                request_data = {
                    "source_schema": {
                        "name": source_schema_name,
                        "fields": source_fields
                    },
                    "target_schema": {
                        "name": target_schema_name,
                        "fields": target_fields
                    },
                    "mapping_rules": mapping_rules,
                    "code_type": code_type,
                    "optimization_level": optimization_level,
                    "include_tests": include_tests
                }
                
                # Generate code
                with st.spinner("Generating code..."):
                    result = call_api(
                        "/api/v1/generate/code",
                        method="POST",
                        data=request_data
                    )
                
                if result and result.get("success"):
                    generated_code = result.get("data", {})
                    
                    st.success("Code generated successfully!")
                    
                    # Show generated code
                    st.subheader(f"Generated {code_type.upper()} Code")
                    st.code(generated_code.get("code", ""), language=code_type)
                    
                    # Show test code if included
                    if include_tests and generated_code.get("test_code"):
                        st.subheader("Test Code")
                        st.code(generated_code["test_code"], language="python")
                    
                    # Show documentation
                    if generated_code.get("documentation"):
                        st.subheader("Documentation")
                        st.markdown(generated_code["documentation"])
                    
                    # Show dependencies
                    if generated_code.get("dependencies"):
                        st.subheader("Dependencies")
                        st.write(", ".join(generated_code["dependencies"]))
                
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON in inputs: {str(e)}")
            except Exception as e:
                st.error(f"Code generation failed: {str(e)}")


def show_full_pipeline():
    """Full pipeline page"""
    st.header("🔄 Full Pipeline")
    
    st.markdown("Run the complete pipeline from document validation to code generation")
    
    # Pipeline configuration
    with st.form("pipeline_form"):
        st.subheader("Input Document")
        document_json = st.text_area(
            "JSON Document",
            height=300,
            placeholder='{\n  "dictionary": {\n    "providedKey": "PBWM.GCB_AAC_NAM.database_name"\n  },\n  "fields": [...]\n}'
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            code_type = st.selectbox("Code Type", ["pyspark", "sql", "python"])
            optimization_level = st.selectbox("Optimization", ["basic", "standard", "advanced"])
        
        with col2:
            include_validation = st.checkbox("Include Validation", value=True)
            include_tests = st.checkbox("Include Tests", value=True)
        
        submitted = st.form_submit_button("Run Full Pipeline", type="primary")
        
        if submitted:
            if document_json.strip():
                try:
                    document = json.loads(document_json)
                    
                    # Run full pipeline
                    with st.spinner("Running full pipeline..."):
                        result = call_api(
                            "/api/v1/pipeline/full",
                            method="POST",
                            data={
                                "document": document,
                                "code_type": code_type,
                                "optimization_level": optimization_level
                            }
                        )
                    
                    if result and result.get("success"):
                        data = result.get("data", {})
                        
                        st.success("Pipeline completed successfully!")
                        
                        # Show document processing results
                        doc_processing = data.get("document_processing", {})
                        if doc_processing:
                            st.subheader("Document Processing Results")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Fields Extracted", doc_processing.get("field_count", 0))
                            with col2:
                                st.metric("Database Name", doc_processing.get("database_name", "Not found"))
                        
                        # Show code generation results
                        code_gen = data.get("code_generation", {})
                        if code_gen and code_gen.get("generated_code"):
                            st.subheader("Generated Code")
                            generated_code = code_gen["generated_code"]
                            st.code(generated_code.get("code", ""), language=code_type)
                            
                            if generated_code.get("test_code"):
                                with st.expander("Test Code"):
                                    st.code(generated_code["test_code"], language="python")
                
                except json.JSONDecodeError as e:
                    st.error(f"Invalid JSON: {str(e)}")
                except Exception as e:
                    st.error(f"Pipeline execution failed: {str(e)}")
            else:
                st.warning("Please enter a JSON document")


def show_workflows():
    """Workflows page"""
    st.header("📊 Workflows")
    
    # List active workflows
    workflows_data = call_api("/api/v1/workflows")
    
    if workflows_data and workflows_data.get("success"):
        workflows = workflows_data.get("data", {}).get("workflows", [])
        
        if workflows:
            st.subheader("Active Workflows")
            
            for workflow in workflows:
                with st.expander(f"Workflow: {workflow.get('name', 'Unknown')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**ID:** {workflow.get('workflow_id')}")
                        st.write(f"**Description:** {workflow.get('description', 'No description')}")
                        st.write(f"**Tasks:** {workflow.get('task_count', 0)}")
                    
                    with col2:
                        st.write(f"**Created:** {workflow.get('created_at', 'Unknown')}")
                        
                        if st.button(f"Cancel", key=f"cancel_{workflow.get('workflow_id')}"):
                            result = call_api(
                                f"/api/v1/workflows/{workflow.get('workflow_id')}",
                                method="DELETE"
                            )
                            
                            if result and result.get("success"):
                                st.success("Workflow cancelled")
                                st.experimental_rerun()
                    
                    # Show task statuses
                    task_statuses = workflow.get("task_statuses", [])
                    if task_statuses:
                        st.write("**Task Statuses:**")
                        for task in task_statuses:
                            status_color = {
                                "completed": "🟢",
                                "in_progress": "🟡", 
                                "failed": "🔴",
                                "pending": "⚪",
                                "cancelled": "⚫"
                            }.get(task.get("status", "unknown"), "❓")
                            
                            st.write(f"{status_color} {task.get('agent_type')} - {task.get('status')}")
        else:
            st.info("No active workflows")
    else:
        st.error("Failed to load workflows")


def show_knowledge_base():
    """Knowledge base page"""
    st.header("🧠 Knowledge Base")
    
    tab1, tab2 = st.tabs(["Query Knowledge", "Add Knowledge"])
    
    with tab1:
        st.subheader("Query Knowledge Base")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input("Enter your query:", placeholder="How to optimize PySpark code?")
        
        with col2:
            max_results = st.selectbox("Max Results", [5, 10, 15, 20], index=0)
        
        category_filter = st.selectbox(
            "Category Filter (optional)",
            ["All", "pyspark_patterns", "validation_patterns", "performance_optimization", "error_handling"],
        )
        
        if st.button("Search", type="primary"):
            if query.strip():
                # Query knowledge base
                with st.spinner("Searching knowledge base..."):
                    result = call_api(
                        "/api/v1/knowledge/query",
                        method="POST",
                        data={
                            "query": query,
                            "max_results": max_results,
                            "category_filter": None if category_filter == "All" else category_filter
                        }
                    )
                
                if result and result.get("success"):
                    results = result.get("data", {}).get("results", [])
                    
                    if results:
                        st.subheader(f"Found {len(results)} results")
                        
                        for i, res in enumerate(results):
                            with st.expander(f"Result {i+1} (Score: {res.get('score', 0):.3f})"):
                                st.write(f"**Category:** {res.get('metadata', {}).get('category', 'Unknown')}")
                                st.write(f"**Title:** {res.get('metadata', {}).get('title', 'Untitled')}")
                                st.write("**Content:**")
                                st.write(res.get("content", ""))
                    else:
                        st.info("No results found")
            else:
                st.warning("Please enter a query")
    
    with tab2:
        st.subheader("Add Knowledge")
        
        with st.form("add_knowledge_form"):
            content = st.text_area("Content", height=200)
            
            col1, col2 = st.columns(2)
            with col1:
                category = st.text_input("Category", placeholder="e.g., pyspark_patterns")
                title = st.text_input("Title", placeholder="Brief description")
            
            with col2:
                tags = st.text_input("Tags (comma-separated)", placeholder="tag1, tag2, tag3")
                doc_id = st.text_input("Document ID (optional)", placeholder="Auto-generated if empty")
            
            submitted = st.form_submit_button("Add Knowledge")
            
            if submitted:
                if content.strip():
                    metadata = {
                        "category": category,
                        "title": title,
                        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": "manual_entry"
                    }
                    
                    result = call_api(
                        "/api/v1/knowledge/add",
                        method="POST",
                        data={
                            "content": content,
                            "metadata": metadata,
                            "doc_id": doc_id if doc_id.strip() else None
                        }
                    )
                    
                    if result and result.get("success"):
                        st.success(f"Knowledge added successfully! ID: {result.get('data', {}).get('doc_id')}")
                else:
                    st.warning("Please enter content")


def show_settings():
    """Settings page"""
    st.header("⚙️ Settings")
    
    st.markdown("### API Configuration")
    st.code(f"API Base URL: {API_BASE_URL}")
    
    # Check API health
    health_data = call_api("/health")
    if health_data:
        st.markdown("### System Health")
        st.json(health_data)
    
    st.markdown("### Knowledge Base Statistics")
    kb_stats = call_api("/api/v1/knowledge/stats")
    if kb_stats and kb_stats.get("success"):
        st.json(kb_stats.get("data", {}))


if __name__ == "__main__":
    main()