#!/usr/bin/env python3
"""
Simple test script to verify agent imports work in chatbased demo
"""

import sys
import os
from pathlib import Path

def test_agent_imports():
    """Test if agents can be imported in the chatbased demo context"""
    print("🧪 Testing Agent Imports in Chatbased Demo")
    print("=" * 50)
    
    # Add parent directory to path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))
    
    print(f"Added to path: {parent_dir}")
    
    # Test 1: Try to import from main agents directory
    try:
        print("\n🔍 Test 1: Importing from main agents directory...")
        from agentic_mapping_ai.agents import EnhancedOrchestrator
        print("   ✅ EnhancedOrchestrator imported successfully!")
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 2: Try to import from demo agents directory
    try:
        print("\n🔍 Test 2: Importing from demo agents directory...")
        from demo.agentic_mapping_ai.agents import EnhancedOrchestrator
        print("   ✅ EnhancedOrchestrator imported from demo successfully!")
        return True
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test 3: Check what's actually available
    try:
        print("\n🔍 Test 3: Checking available modules...")
        import agentic_mapping_ai
        print(f"   ✅ agentic_mapping_ai module found")
        
        if hasattr(agentic_mapping_ai, 'agents'):
            print(f"   ✅ agents submodule found")
            agent_files = list(Path(agentic_mapping_ai.__file__).parent.glob("agents/**/*.py"))
            print(f"   📁 Found {len(agent_files)} agent files")
        else:
            print(f"   ❌ agents submodule not found")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    return False

def test_directory_structure():
    """Test the directory structure"""
    print("\n📁 Testing Directory Structure")
    print("=" * 30)
    
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    # Check main agents directory
    main_agents_dir = parent_dir / "agentic_mapping_ai" / "agents"
    if main_agents_dir.exists():
        print(f"✅ Main agents directory: {main_agents_dir}")
        
        # Check subdirectories
        subdirs = [d for d in main_agents_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
        print(f"   📂 Subdirectories: {[d.name for d in subdirs]}")
        
        # Check main __init__.py
        main_init = main_agents_dir / "__init__.py"
        if main_init.exists():
            print(f"   📄 Main __init__.py: Found")
        else:
            print(f"   ❌ Main __init__.py: Missing")
    else:
        print(f"❌ Main agents directory not found: {main_agents_dir}")
    
    # Check demo agents directory
    demo_agents_dir = parent_dir / "demo" / "agentic_mapping_ai" / "agents"
    if demo_agents_dir.exists():
        print(f"✅ Demo agents directory: {demo_agents_dir}")
        
        # Check demo __init__.py
        demo_init = demo_agents_dir / "__init__.py"
        if demo_init.exists():
            print(f"   📄 Demo __init__.py: Found")
        else:
            print(f"   ❌ Demo __init__.py: Missing")
    else:
        print(f"❌ Demo agents directory not found: {demo_agents_dir}")

if __name__ == "__main__":
    print("🚀 Starting Agent Import Tests...")
    
    # Test directory structure first
    test_directory_structure()
    
    # Test agent imports
    success = test_agent_imports()
    
    if success:
        print("\n🎉 Agent import test PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Agent import test FAILED!")
        print("\n💡 Recommendations:")
        print("1. Check if all required dependencies are installed")
        print("2. Verify the agent file paths are correct")
        print("3. Check for import path issues in agent files")
        sys.exit(1)
