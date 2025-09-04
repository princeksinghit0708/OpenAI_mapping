#!/usr/bin/env python3
"""
Pure Offline Chat Demo Launcher
Runs the chat-based demo using ONLY built-in Python libraries
No external dependencies required
"""

import sys
import os
from pathlib import Path

def check_pure_offline_requirements():
    """Check if pure offline requirements are installed"""
    print("🔍 Checking pure offline requirements...")
    print("   📦 Only built-in Python libraries + minimal dependencies")
    
    # Only check for essential libraries that are lightweight
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
    
    print("✅ All pure offline requirements are available!")
    print("🔒 No external model downloads required")
    print("📦 Using only built-in Python libraries + minimal dependencies")
    return True

def main():
    """Main launcher function"""
    print("🚀 Pure Offline Chat-Based Agentic AI Demo")
    print("=" * 60)
    print("🔒 Complete Privacy - No Internet Required")
    print("📦 Built-in Python Libraries Only")
    print("=" * 60)
    
    # Check requirements
    if not check_pure_offline_requirements():
        sys.exit(1)
    
    # Check if pure_offline_main.py exists
    pure_offline_main_path = Path("pure_offline_main.py")
    if not pure_offline_main_path.exists():
        print("❌ pure_offline_main.py not found!")
        print("Please ensure you're in the chatbased_demo_app directory")
        sys.exit(1)
    
    print("\n🎯 Starting pure offline demo...")
    print("🔒 Privacy: No data will be sent to external services")
    print("📦 Processing: Using only built-in Python libraries")
    print("=" * 60)
    
    # Import and run the pure offline demo
    try:
        from pure_offline_main import main as run_pure_offline_demo
        run_pure_offline_demo()
    except Exception as e:
        print(f"❌ Error starting pure offline demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
