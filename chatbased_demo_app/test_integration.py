#!/usr/bin/env python3
"""
Integration Test Script
Tests if all components are properly integrated and working with consolidated agents
"""

import asyncio
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test FAISS engine
        from agents.faiss_similarity_engine import get_faiss_engine
        print("✅ FAISS engine import: SUCCESS")
        
        # Test chat suggestion manager
        from agents.chat_suggestion_manager import chat_suggestion_manager
        print("✅ Chat suggestion manager import: SUCCESS")
        
        # Test agent manager
        from agents.agent_manager import agent_manager
        print("✅ Agent manager import: SUCCESS")
        
        # Test main application
        from main import ChatBasedAgenticDemo
        print("✅ Main application import: SUCCESS")
        
        # Test demo script
        from demo_faiss_features import FAISSFeaturesDemo
        print("✅ Demo script import: SUCCESS")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        return False

def test_consolidated_agents():
    """Test if consolidated agents can be imported"""
    print("\nTesting consolidated agents...")
    
    try:
        # Test importing from consolidated agents
        from agents import (
            EnhancedOrchestrator,
            create_enhanced_metadata_validator,
            create_enhanced_code_generator,
            EnhancedAgentConfig
        )
        print("✅ Consolidated agents import: SUCCESS")
        
        # Test agent manager functionality
        from agents.agent_manager import agent_manager
        
        # Get agent status
        agent_status = agent_manager.get_agent_status()
        print(f"✅ Agent manager status: {agent_status['agents_source']}")
        print(f"✅ Total agents available: {agent_status['total_agents']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Consolidated agents test failed: {str(e)}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    print("\nTesting dependencies...")
    
    try:
        import faiss
        print("✅ FAISS: SUCCESS")
    except ImportError:
        print("❌ FAISS: NOT INSTALLED")
        return False
    
    try:
        import sentence_transformers
        print("✅ Sentence Transformers: SUCCESS")
    except ImportError:
        print("❌ Sentence Transformers: NOT INSTALLED")
        return False
    
    try:
        import numpy
        print("✅ NumPy: SUCCESS")
    except ImportError:
        print("❌ NumPy: NOT INSTALLED")
        return False
    
    try:
        import pandas
        print("✅ Pandas: SUCCESS")
    except ImportError:
        print("❌ Pandas: NOT INSTALLED")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "agents/__init__.py",
        "agents/faiss_similarity_engine.py",
        "agents/chat_suggestion_manager.py",
        "agents/agent_manager.py",
        "main.py",
        "demo_faiss_features.py",
        "requirements_enhanced.txt",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}: EXISTS")
        else:
            print(f"❌ {file_path}: MISSING")
            all_exist = False
    
    return all_exist

def test_consolidated_structure():
    """Test if the consolidated agents structure exists"""
    print("\nTesting consolidated agents structure...")
    
    try:
        # Check if consolidated agents directory exists
        parent_dir = Path(__file__).parent.parent
        consolidated_dir = parent_dir / "agentic_mapping_ai" / "agents"
        
        if not consolidated_dir.exists():
            print(f"❌ Consolidated agents directory not found: {consolidated_dir}")
            return False
        
        print(f"✅ Consolidated agents directory: {consolidated_dir}")
        
        # Check subdirectories
        expected_categories = ['core', 'enhanced_v2', 'enhanced', 'basic', 'specialized', 'chat']
        
        for category in expected_categories:
            category_dir = consolidated_dir / category
            if category_dir.exists():
                py_files = list(category_dir.glob("*.py"))
                agent_files = [f for f in py_files if f.name != "__init__.py"]
                print(f"   ✅ {category}/: {len(agent_files)} agent files")
            else:
                print(f"   ❌ {category}/: Missing")
                return False
        
        # Check main __init__.py
        main_init = consolidated_dir / "__init__.py"
        if main_init.exists():
            print(f"✅ Main __init__.py: EXISTS")
        else:
            print(f"❌ Main __init__.py: MISSING")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Consolidated structure test failed: {str(e)}")
        return False

async def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        # Test FAISS engine creation
        from agents.faiss_similarity_engine import get_faiss_engine
        faiss_engine = get_faiss_engine()
        print("✅ FAISS engine creation: SUCCESS")
        
        # Test chat suggestion manager
        from agents.chat_suggestion_manager import chat_suggestion_manager
        print("✅ Chat suggestion manager creation: SUCCESS")
        
        # Test main app creation
        from main import ChatBasedAgenticDemo
        app = ChatBasedAgenticDemo()
        print("✅ Main application creation: SUCCESS")
        
        # Test demo creation
        from demo_faiss_features import FAISSFeaturesDemo
        demo = FAISSFeaturesDemo()
        print("✅ Demo creation: SUCCESS")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting Integration Tests")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test consolidated agents
    consolidated_agents_ok = test_consolidated_agents()
    
    # Test consolidated structure
    consolidated_structure_ok = test_consolidated_structure()
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test file structure
    files_ok = test_file_structure()
    
    # Test basic functionality
    print("\nTesting basic functionality (async)...")
    try:
        func_ok = asyncio.run(test_basic_functionality())
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        func_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 50)
    
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"Consolidated Agents: {'✅ PASS' if consolidated_agents_ok else '❌ FAIL'}")
    print(f"Consolidated Structure: {'✅ PASS' if consolidated_structure_ok else '❌ FAIL'}")
    print(f"Dependencies: {'✅ PASS' if deps_ok else '❌ PASS'}")
    print(f"File Structure: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"Basic Functionality: {'✅ PASS' if func_ok else '❌ FAIL'}")
    
    if all([imports_ok, consolidated_agents_ok, consolidated_structure_ok, deps_ok, files_ok, func_ok]):
        print("\n🎉 ALL TESTS PASSED! System is properly integrated.")
        print("\nYou can now run:")
        print("  • python main.py - Chat-based application")
        print("  • python demo_faiss_features.py - FAISS features demo")
        return True
    else:
        print("\n❌ SOME TESTS FAILED. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
