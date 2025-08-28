#!/usr/bin/env python3
"""
Simple test to verify the consolidated agents structure
"""

import sys
import os
from pathlib import Path

def test_structure():
    """Test the consolidated agents structure"""
    print("🧪 Testing Consolidated Agents Structure")
    print("=" * 50)
    
    # Check directory structure
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    
    main_agents_dir = parent_dir / "agentic_mapping_ai" / "agents"
    demo_agents_dir = parent_dir / "demo" / "agentic_mapping_ai" / "agents"
    
    print(f"📁 Main agents directory: {main_agents_dir}")
    print(f"📁 Demo agents directory: {demo_agents_dir}")
    
    # Check main agents structure
    if main_agents_dir.exists():
        print("\n✅ Main agents directory structure:")
        subdirs = [d for d in main_agents_dir.iterdir() if d.is_dir() and not d.name.startswith('_')]
        for subdir in sorted(subdirs):
            py_files = list(subdir.glob("*.py"))
            init_files = [f for f in py_files if f.name == "__init__.py"]
            agent_files = [f for f in py_files if f.name != "__init__.py"]
            print(f"   📂 {subdir.name}/: {len(agent_files)} agent files, {len(init_files)} init files")
            
            # Check if __init__.py exists
            init_file = subdir / "__init__.py"
            if init_file.exists():
                print(f"      ✅ __init__.py - Found")
            else:
                print(f"      ❌ __init__.py - Missing")
        
        # Check main __init__.py
        main_init = main_agents_dir / "__init__.py"
        if main_init.exists():
            print(f"\n📄 Main __init__.py - Found")
        else:
            print(f"\n❌ Main __init__.py - Missing")
    else:
        print("❌ Main agents directory not found")
    
    # Check demo agents structure
    if demo_agents_dir.exists():
        print(f"\n✅ Demo agents directory structure:")
        py_files = list(demo_agents_dir.glob("*.py"))
        init_files = [f for f in py_files if f.name == "__init__.py"]
        agent_files = [f for f in py_files if f.name != "__init__.py"]
        print(f"   📁 Total: {len(agent_files)} agent files, {len(init_files)} init files")
        
        # Check demo __init__.py
        demo_init = demo_agents_dir / "__init__.py"
        if demo_init.exists():
            print(f"   📄 Demo __init__.py - Found")
        else:
            print(f"   ❌ Demo __init__.py - Missing")
    else:
        print("❌ Demo agents directory not found")
    
    print("\n" + "=" * 50)
    
    # Test basic file reading
    print("🔍 Testing basic file reading...")
    try:
        # Read main __init__.py
        main_init_content = (main_agents_dir / "__init__.py").read_text()
        print("   ✅ Main __init__.py - Readable")
        
        # Check if it contains expected exports
        expected_exports = [
            "EnhancedOrchestrator",
            "create_enhanced_metadata_validator", 
            "create_enhanced_code_generator",
            "EnhancedAgentConfig"
        ]
        
        for export in expected_exports:
            if export in main_init_content:
                print(f"      ✅ Exports: {export}")
            else:
                print(f"      ❌ Missing: {export}")
                
    except Exception as e:
        print(f"   ❌ Failed to read main __init__.py: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Structure Test Complete!")
    return True

if __name__ == "__main__":
    test_structure()
