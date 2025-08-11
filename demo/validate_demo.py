#!/usr/bin/env python3
"""
🔍 Demo Validation Script
Checks if all required files and dependencies are available for the demo
"""

import sys
import os
from pathlib import Path
import importlib.util

def check_file(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        # Add current directory to path for local imports
        sys.path.insert(0, '.')
        sys.path.insert(0, './agentic_mapping_ai')
        
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print(f"✅ {description}: {module_name}")
            return True
        else:
            print(f"❌ {description}: {module_name} - NOT FOUND")
            return False
    except Exception as e:
        print(f"❌ {description}: {module_name} - ERROR: {e}")
        return False

def main():
    print("🔍 Demo Validation Report")
    print("=" * 50)
    
    all_good = True
    
    # Check core files
    print("\n📁 Core Files:")
    files_to_check = [
        ("README_DEMO.md", "Demo documentation"),
        (".env", "Environment configuration"),
        ("demo_launcher.py", "Demo launcher"),
        ("test_agent_demo.py", "Test Generator demo"),
        ("metadata_validator_demo.py", "Metadata Validator demo"),
        ("enhanced_main.py", "Enhanced main application"),
        ("gpt4_prompt_engine.py", "Prompt engine"),
        ("faiss_integration.py", "FAISS integration"),
        ("requirements.txt", "Requirements file"),
    ]
    
    for file_path, desc in files_to_check:
        if not check_file(file_path, desc):
            all_good = False
    
    # Check agent framework files
    print("\n🤖 Agent Framework:")
    agent_files = [
        ("agentic_mapping_ai/llm_service.py", "LLM Service"),
        ("agentic_mapping_ai/run_enhanced_application.py", "Main launcher"),
        ("agentic_mapping_ai/agents/base_agent.py", "Base agent"),
        ("agentic_mapping_ai/agents/enhanced_base_agent.py", "Enhanced base agent"),
        ("agentic_mapping_ai/agents/orchestrator.py", "Orchestrator agent"),
        ("agentic_mapping_ai/agents/metadata_validator.py", "Metadata validator"),
        ("agentic_mapping_ai/agents/code_generator.py", "Code generator"),
        ("agentic_mapping_ai/agents/test_generator.py", "Test generator (NEW!)"),
        ("agentic_mapping_ai/core/models.py", "Core models"),
        ("agentic_mapping_ai/knowledge/rag_engine.py", "RAG engine"),
        ("agentic_mapping_ai/config/settings.py", "Settings"),
        ("agentic_mapping_ai/api/main.py", "API endpoints"),
    ]
    
    for file_path, desc in agent_files:
        if not check_file(file_path, desc):
            all_good = False
    
    # Check Excel file
    print("\n📊 Data Files:")
    excel_files = list(Path(".").glob("*.xlsx"))
    if excel_files:
        for excel_file in excel_files:
            print(f"✅ Excel file found: {excel_file}")
    else:
        print("⚠️  No Excel file found - add ebs_IM_account_DATAhub_mapping_v8.0.xlsx manually")
        # Not marking as failed since it can be added later
    
    # Check metadata files
    print("\n📋 Metadata Files:")
    metadata_files = list(Path("results").glob("*_metadata.json")) if Path("results").exists() else []
    if metadata_files:
        for metadata_file in metadata_files:
            print(f"✅ Metadata file: {metadata_file}")
    else:
        print("⚠️  No metadata files found in results/ directory")
        if not Path("results").exists():
            print("💡 Creating results/ directory structure...")
    
    # Check Python imports (basic validation)
    print("\n🐍 Python Modules:")
    modules_to_check = [
        ("llm_service", "LLM Service module"),
        ("gpt4_prompt_engine", "Prompt engine module"),
        ("faiss_integration", "FAISS integration module"),
    ]
    
    for module, desc in modules_to_check:
        if not check_import(module, desc):
            all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 Demo validation PASSED!")
        print("✅ All essential files are present")
        print("🚀 Ready for demo!")
        print("\nTo start demo:")
        print("  python demo_launcher.py")
        print("  OR")
        print("  python agentic_mapping_ai/run_enhanced_application.py")
    else:
        print("⚠️  Demo validation FAILED!")
        print("❌ Some files are missing")
        print("📋 Check the errors above and copy missing files")
    
    print("\n💡 Demo Tips:")
    print("- Add your Excel file: ebs_IM_account_DATAhub_mapping_v8.0.xlsx")
    print("- Ensure helix CLI is available for token authentication")
    print("- Select option 2 in the menu for best demo experience")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
