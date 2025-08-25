#!/usr/bin/env python3
"""
Test Demo Components - Windows Compatible
Verifies that all demo components can be imported and initialized
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test core imports
        from agents.metadata_validator import MetadataValidatorAgent
        print("OK - MetadataValidatorAgent imported successfully")
        
        from agents.code_generator import CodeGeneratorAgent
        print("OK - CodeGeneratorAgent imported successfully")
        
        from agents.orchestrator import OrchestratorAgent
        print("OK - OrchestratorAgent imported successfully")
        
        from agents.base_agent import AgentConfig
        print("OK - AgentConfig imported successfully")
        
        from core.models import (
            FieldDefinition, SchemaDefinition, MappingRule, 
            ValidationResult, CodeGenerationRequest, GeneratedCode
        )
        print("OK - Core models imported successfully")
        
        from parsers.excel_mapping_parser import ExcelMappingParser
        print("OK - ExcelMappingParser imported successfully")
        
        print("OK - All imports successful!")
        return True
        
    except ImportError as e:
        print(f"ERROR - Import failed: {e}")
        return False
    except Exception as e:
        print(f"ERROR - Unexpected error during import: {e}")
        return False

def test_agent_config():
    """Test agent configuration creation"""
    print("\nTesting agent configuration...")
    
    try:
        from agents.base_agent import AgentConfig
        
        config = AgentConfig(
            name="Test Agent",
            description="Test agent for validation",
            model="gpt-4",
            temperature=0.1
        )
        
        print(f"OK - AgentConfig created: {config.name}")
        print(f"   Description: {config.description}")
        print(f"   Model: {config.model}")
        print(f"   Temperature: {config.temperature}")
        
        return True
        
    except Exception as e:
        print(f"ERROR - AgentConfig creation failed: {e}")
        return False

def test_excel_parser():
    """Test Excel parser initialization"""
    print("\nTesting Excel parser...")
    
    try:
        from parsers.excel_mapping_parser import ExcelMappingParser
        
        parser = ExcelMappingParser()
        print("OK - ExcelMappingParser initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"ERROR - ExcelParser initialization failed: {e}")
        return False

def test_core_models():
    """Test core model creation"""
    print("\nTesting core models...")
    
    try:
        from core.models import FieldDefinition, SchemaDefinition, MappingRule
        
        # Test FieldDefinition
        field = FieldDefinition(
            name="test_field",
            data_type="VARCHAR(50)",
            description="Test field for validation"
        )
        print("OK - FieldDefinition created successfully")
        
        # Test SchemaDefinition
        schema = SchemaDefinition(
            name="test_schema",
            description="Test schema for validation",
            fields=[field]
        )
        print("OK - SchemaDefinition created successfully")
        
        # Test MappingRule
        rule = MappingRule(
            source_field="source_field",
            target_field="target_field",
            transformation="direct"
        )
        print("OK - MappingRule created successfully")
        
        return True
        
    except Exception as e:
        print(f"ERROR - Core model creation failed: {e}")
        return False

def test_directory_structure():
    """Test that necessary directories exist"""
    print("\nTesting directory structure...")
    
    base_dir = Path(__file__).parent
    required_dirs = [
        "agents",
        "core", 
        "parsers",
        "config",
        "knowledge",
        "ui",
        "api",
        "templates",
        "tests",
        "examples",
        "utils"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"OK - Directory exists: {dir_name}")
        else:
            print(f"WARNING - Directory missing: {dir_name}")
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\nWARNING - Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("OK - All required directories exist")
    return True

def test_file_permissions():
    """Test file permissions and accessibility"""
    print("\nTesting file permissions...")
    
    try:
        # Test if we can read the current file
        with open(__file__, 'r') as f:
            content = f.read()
        
        print("OK - Can read test file")
        
        # Test if we can create output directory
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        # Test if we can write a file
        test_file = output_dir / "test.txt"
        with open(test_file, 'w') as f:
            f.write("Test content")
        
        print("OK - Can write to output directory")
        
        # Cleanup
        test_file.unlink()
        output_dir.rmdir()
        
        return True
        
    except Exception as e:
        print(f"ERROR - File permission test failed: {e}")
        return False

def main():
    """Main test function"""
    print("AGENTIC MAPPING AI - DEMO COMPONENT TEST")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Agent Config Test", test_agent_config),
        ("Excel Parser Test", test_excel_parser),
        ("Core Models Test", test_core_models),
        ("Directory Structure Test", test_directory_structure),
        ("File Permissions Test", test_file_permissions)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"ERROR - Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS - All tests passed! Demo components are ready.")
        return True
    else:
        print("WARNING - Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
