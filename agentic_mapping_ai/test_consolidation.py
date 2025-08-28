#!/usr/bin/env python3
"""
Test script to verify the consolidated agents structure
"""

import sys
import os
from pathlib import Path

def test_agent_structure():
    """Test that the agent structure is properly organized"""
    print("🧪 Testing Consolidated Agents Structure")
    print("=" * 50)
    
    # Check directory structure
    agents_dir = Path(__file__).parent / "agents"
    
    expected_dirs = ['core', 'enhanced_v2', 'enhanced', 'basic', 'specialized', 'chat']
    
    print("📁 Checking directory structure:")
    for dir_name in expected_dirs:
        dir_path = agents_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {dir_name}/ - Found")
            # Check if __init__.py exists
            init_file = dir_path / "__init__.py"
            if init_file.exists():
                print(f"      ✅ __init__.py - Found")
            else:
                print(f"      ❌ __init__.py - Missing")
        else:
            print(f"   ❌ {dir_name}/ - Missing")
    
    # Check main __init__.py
    main_init = agents_dir / "__init__.py"
    if main_init.exists():
        print(f"\n📄 Main __init__.py - Found")
    else:
        print(f"\n❌ Main __init__.py - Missing")
    
    print("\n" + "=" * 50)
    
    # Check file counts in each directory
    print("📊 File counts by category:")
    for dir_name in expected_dirs:
        dir_path = agents_dir / dir_name
        if dir_path.exists():
            py_files = list(dir_path.glob("*.py"))
            init_files = [f for f in py_files if f.name == "__init__.py"]
            agent_files = [f for f in py_files if f.name != "__init__.py"]
            print(f"   {dir_name}/: {len(agent_files)} agent files, {len(init_files)} init files")
    
    print("\n" + "=" * 50)
    
    # Test basic import (without complex dependencies)
    try:
        print("🔍 Testing basic imports...")
        
        # Test core imports
        sys.path.insert(0, str(agents_dir))
        from core import BaseAgent, AgentConfig, AgentFactory
        print("   ✅ Core agents imported successfully")
        
        # Test enhanced_v2 imports
        from enhanced_v2 import EnhancedOrchestrator
        print("   ✅ Enhanced V2 agents imported successfully")
        
        # Test basic imports
        from basic import CodeGeneratorAgent, MetadataValidatorAgent, OrchestratorAgent
        print("   ✅ Basic agents imported successfully")
        
        # Test specialized imports
        from specialized import GoldRefValidator, PySparkCodeGenerator, TransformationAgent
        print("   ✅ Specialized agents imported successfully")
        
        # Test chat imports
        from chat import TestGeneratorAgent, ChatAgent
        print("   ✅ Chat agents imported successfully")
        
        print("\n🎉 All agent categories imported successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    success = test_agent_structure()
    if success:
        print("\n✅ Consolidation test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Consolidation test FAILED!")
        sys.exit(1)
