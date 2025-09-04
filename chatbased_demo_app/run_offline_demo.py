#!/usr/bin/env python3
"""
Offline Chat Demo Launcher
Runs the chat-based demo without any internet dependencies
"""

import sys
import os
from pathlib import Path

def check_offline_requirements():
    """Check if offline requirements are installed"""
    print("🔍 Checking offline requirements...")
    
    required_modules = [
        'pandas', 'openpyxl', 'numpy', 'faiss', 'sklearn', 
        'nltk', 'loguru', 'rich', 'faker', 'sqlalchemy'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"   ❌ {module} - Missing")
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("Please install offline requirements:")
        print("pip install -r offline_requirements.txt")
        return False
    
    print("✅ All offline requirements are installed!")
    return True

def main():
    """Main launcher function"""
    print("🚀 Offline Chat-Based Agentic AI Demo")
    print("=" * 50)
    
    # Check requirements
    if not check_offline_requirements():
        sys.exit(1)
    
    # Check if offline_main.py exists
    offline_main_path = Path("offline_main.py")
    if not offline_main_path.exists():
        print("❌ offline_main.py not found!")
        print("Please ensure you're in the chatbased_demo_app directory")
        sys.exit(1)
    
    print("\n🎯 Starting offline demo...")
    print("Privacy: No data will be sent to external services")
    print("=" * 50)
    
    # Import and run the offline demo
    try:
        from offline_main import main as run_offline_demo
        run_offline_demo()
    except Exception as e:
        print(f"❌ Error starting offline demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
