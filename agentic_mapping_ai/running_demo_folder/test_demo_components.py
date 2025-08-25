#!/usr/bin/env python3
"""
🧪 Test Demo Components
Verifies that all demo components can be imported and initialized
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Test core imports
        from agents.metadata_validator import MetadataValidatorAgent
        print("✅ MetadataValidatorAgent imported successfully")
        
        from agents.code_generator import CodeGeneratorAgent
        print("✅ CodeGeneratorAgent imported successfully")
        
        from agents.orchestrator import OrchestratorAgent
        print("✅ OrchestratorAgent imported successfully")
        
        from agents.base_agent import AgentConfig
        print("✅ AgentConfig imported successfully")
        
        from core.models import (
            FieldDefinition, SchemaDefinition, MappingRule, 
            ValidationResult, CodeGenerationRequest, GeneratedCode
        )
        print("✅ Core models imported successfully")
        
        from parsers.excel_mapping_parser import ExcelMappingParser
        print("✅ ExcelMappingParser imported successfully")
        
        print("✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_agent_config():
    """Test agent configuration creation"""
    print("\n🔧 Testing agent configuration...")
    
    try:
        from agents.base_agent import AgentConfig
        
        config = AgentConfig(
            name="Test Agent",
            description="Test agent for validation",
            model="gpt-4",
            temperature=0.1
        )
        
        print(f"✅ AgentConfig created: {config.name}")
        print(f"   Description: {config.description}")
        print(f"   Model: {config.model}")
        print(f"   Temperature: {config.temperature}")
        
        return True
        
    except Exception as e:
        print(f"❌ AgentConfig creation failed: {e}")
        return False

def test_excel_parser():
    """Test Excel parser initialization"""
    print("\n📊 Testing Excel parser...")
    
    try:
        from parsers.excel_mapping_parser import ExcelMappingParser
        
        parser = ExcelMappingParser()
        print("✅ ExcelMappingParser initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ ExcelMappingParser initialization failed: {e}")
        return False

def test_core_models():
    """Test core model creation"""
    print("\n🏗️  Testing core models...")
    
    try:
        from core.models import FieldDefinition, SchemaDefinition, MappingRule
        
        # Test FieldDefinition
        field = FieldDefinition(
            name="test_field",
            data_type="string",
            is_nullable=True,
            description="Test field"
        )
        print("✅ FieldDefinition created successfully")
        
        # Test SchemaDefinition
        schema = SchemaDefinition(
            name="test_schema",
            fields=[field],
            version="1.0"
        )
        print("✅ SchemaDefinition created successfully")
        
        # Test MappingRule
        mapping = MappingRule(
            source_field="source_field",
            target_field="target_field",
            transformation="direct",
            mapping_type="Direct"
        )
        print("✅ MappingRule created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Core model creation failed: {e}")
        return False

def test_directory_structure():
    """Test that required directories exist"""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        "agents",
        "core", 
        "parsers",
        "config",
        "examples"
    ]
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = Path(__file__).parent / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 AGENTIC MAPPING AI - DEMO COMPONENT TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Config Test", test_agent_config),
        ("Excel Parser Test", test_excel_parser),
        ("Core Models Test", test_core_models),
        ("Directory Structure Test", test_directory_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Demo components are ready.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
