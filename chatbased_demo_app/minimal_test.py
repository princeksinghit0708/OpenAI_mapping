#!/usr/bin/env python3
"""
Minimal test to isolate import issues
"""

import sys
from pathlib import Path

def test_consolidated_agents_detailed():
    """Test consolidated agents import with detailed info"""
    print("🧪 Testing Consolidated Agents Import (Detailed)")
    print("=" * 30)
    
    try:
        # Add parent directory to path
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        sys.path.insert(0, str(parent_dir))
        
        print(f"Added to path: {parent_dir}")
        
        # Try to import consolidated agents directly
        import agentic_mapping_ai.agents
        print("✅ agentic_mapping_ai.agents: SUCCESS")
        
        # Check what's available
        if hasattr(agentic_mapping_ai.agents, '__all__'):
            print(f"✅ Available exports: {len(agentic_mapping_ai.agents.__all__)} items")
            for item in agentic_mapping_ai.agents.__all__:
                print(f"   - {item}")
        
        return True
        
    except Exception as e:
        print(f"❌ Consolidated agents import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_consolidated_agents():
    """Test consolidated agents import"""
    print("\n🔍 Testing Consolidated Agents Import")
    print("=" * 30)
    
    try:
        # Try to import consolidated agents
        import agentic_mapping_ai.agents
        print("✅ agentic_mapping_ai.agents: SUCCESS")
        
        # Check what's available
        if hasattr(agentic_mapping_ai.agents, '__all__'):
            print(f"✅ Available exports: {len(agentic_mapping_ai.agents.__all__)} items")
            for item in agentic_mapping_ai.agents.__all__[:5]:  # Show first 5
                print(f"   - {item}")
        
        return True
        
    except Exception as e:
        print(f"❌ Consolidated agents import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Minimal Import Tests")
    print("=" * 50)
    
    consolidated_detailed_success = test_consolidated_agents_detailed()
    consolidated_success = test_consolidated_agents()
    
    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)
    print(f"Consolidated Agents (Detailed): {'✅ PASS' if consolidated_detailed_success else '❌ FAIL'}")
    print(f"Consolidated Agents (Basic): {'✅ PASS' if consolidated_success else '❌ FAIL'}")
    
    if consolidated_detailed_success and consolidated_success:
        print("\n🎉 ALL CONSOLIDATED IMPORTS WORKING!")
    else:
        print("\n⚠️ Some imports failed. Check the errors above.")
