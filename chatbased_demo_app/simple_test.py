#!/usr/bin/env python3
"""
Simple test script to isolate issues and test basic functionality
"""

import sys
import os
from pathlib import Path

def test_basic_imports():
    """Test basic imports without complex dependencies"""
    print("🧪 Testing Basic Imports")
    print("=" * 30)
    
    try:
        # Test basic Python imports
        import json
        import asyncio
        print("✅ Basic Python imports: SUCCESS")
        
        # Test pathlib
        from pathlib import Path
        print("✅ Pathlib import: SUCCESS")
        
        # Test typing
        from typing import Dict, List, Any
        print("✅ Typing imports: SUCCESS")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic imports failed: {e}")
        return False

def test_agent_structure():
    """Test if the agent structure is accessible"""
    print("\n📁 Testing Agent Structure")
    print("=" * 30)
    
    try:
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        
        # Check if consolidated agents directory exists
        consolidated_dir = parent_dir / "agentic_mapping_ai" / "agents"
        if consolidated_dir.exists():
            print(f"✅ Consolidated agents directory: {consolidated_dir}")
            
            # Check subdirectories
            categories = ['core', 'enhanced_v2', 'enhanced', 'basic', 'specialized', 'chat']
            for category in categories:
                category_dir = consolidated_dir / category
                if category_dir.exists():
                    py_files = list(category_dir.glob("*.py"))
                    agent_files = [f for f in py_files if f.name != "__init__.py"]
                    print(f"   ✅ {category}/: {len(agent_files)} agent files")
                else:
                    print(f"   ❌ {category}/: Missing")
                    return False
        else:
            print(f"❌ Consolidated agents directory not found: {consolidated_dir}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Agent structure test failed: {e}")
        return False

def test_simple_agent_import():
    """Test simple agent import without complex dependencies"""
    print("\n🔍 Testing Simple Agent Import")
    print("=" * 30)
    
    try:
        # Add parent directory to path
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        sys.path.insert(0, str(parent_dir))
        
        print(f"Added to path: {parent_dir}")
        
        # Try to import just the structure
        import agentic_mapping_ai.agents
        print("✅ agentic_mapping_ai.agents module: SUCCESS")
        
        # Check what's available
        if hasattr(agentic_mapping_ai.agents, '__all__'):
            print(f"✅ Available exports: {len(agentic_mapping_ai.agents.__all__)} items")
            for item in agentic_mapping_ai.agents.__all__[:5]:  # Show first 5
                print(f"   - {item}")
        else:
            print("⚠️ No __all__ attribute found")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple agent import failed: {e}")
        return False

def test_file_operations():
    """Test basic file operations"""
    print("\n📄 Testing File Operations")
    print("=" * 30)
    
    try:
        # Test creating output directory
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        print("✅ Output directory creation: SUCCESS")
        
        # Test writing a simple file
        test_file = output_dir / "test.txt"
        test_file.write_text("Test content")
        print("✅ File writing: SUCCESS")
        
        # Test reading the file
        content = test_file.read_text()
        if content == "Test content":
            print("✅ File reading: SUCCESS")
        else:
            print("❌ File reading: FAILED")
            return False
        
        # Clean up
        test_file.unlink()
        output_dir.rmdir()
        print("✅ File cleanup: SUCCESS")
        
        return True
        
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Simple Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Agent Structure", test_agent_structure),
        ("Simple Agent Import", test_simple_agent_import),
        ("File Operations", test_file_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Basic functionality is working.")
        print("The issue might be with specific dependencies or complex imports.")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
