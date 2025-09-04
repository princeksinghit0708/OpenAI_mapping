#!/usr/bin/env python3
"""
Offline Agentic Chat Demo Launcher
Runs the agentic chat-based demo with specialized agents
Uses only built-in Python libraries + minimal dependencies
"""

import sys
import os
from pathlib import Path

def check_offline_agentic_requirements():
    """Check if offline agentic requirements are installed"""
    print("🔍 Checking offline agentic requirements...")
    print("   📦 Specialized agents with built-in Python libraries")
    
    # Only check for essential libraries
    required_modules = [
        'pandas', 'openpyxl', 'numpy', 'faiss', 'sklearn'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"   ❌ {module} - Missing")
    
    # Check built-in modules
    builtin_modules = [
        'json', 'os', 'sys', 'pathlib', 'datetime', 'typing', 
        're', 'math', 'collections', 'random', 'asyncio', 'logging'
    ]
    
    print("   📦 Built-in Python modules:")
    for module in builtin_modules:
        try:
            __import__(module)
            print(f"   ✅ {module} (built-in)")
        except ImportError:
            print(f"   ❌ {module} - Unexpected missing built-in module")
    
    if missing_modules:
        print(f"\n❌ Missing essential modules: {', '.join(missing_modules)}")
        print("Please install minimal requirements:")
        print("pip install pandas openpyxl numpy faiss-cpu scikit-learn")
        return False
    
    print("✅ All offline agentic requirements are available!")
    print("🤖 Specialized agents ready for deployment")
    print("🔒 Complete privacy - no internet required")
    return True

def main():
    """Main launcher function"""
    print("🚀 Offline Agentic Chat-Based AI Demo")
    print("=" * 60)
    print("🤖 Specialized Agents for Different Tasks")
    print("🔒 Complete Privacy - No Internet Required")
    print("📦 Built-in Python Libraries + Minimal Dependencies")
    print("=" * 60)
    
    # Check requirements
    if not check_offline_agentic_requirements():
        sys.exit(1)
    
    # Check if offline_agentic_main.py exists
    offline_agentic_main_path = Path("offline_agentic_main.py")
    if not offline_agentic_main_path.exists():
        print("❌ offline_agentic_main.py not found!")
        print("Please ensure you're in the chatbased_demo_app directory")
        sys.exit(1)
    
    print("\n🎯 Starting offline agentic demo...")
    print("🤖 Agents: Data Processor, Schema Mapper, Validator, Code Generator")
    print("🔒 Privacy: No data will be sent to external services")
    print("=" * 60)
    
    # Import and run the offline agentic demo
    try:
        from offline_agentic_main import main as run_offline_agentic_demo
        run_offline_agentic_demo()
    except Exception as e:
        print(f"❌ Error starting offline agentic demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
