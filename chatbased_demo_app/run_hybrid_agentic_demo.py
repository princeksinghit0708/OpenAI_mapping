#!/usr/bin/env python3
"""
Hybrid Agentic Chat Demo Launcher
Runs the hybrid agentic chat-based demo with LLM integration
Uses llm_service.py but removes Hugging Face dependencies
"""

import sys
import os
from pathlib import Path

def check_hybrid_agentic_requirements():
    """Check if hybrid agentic requirements are installed"""
    print("🔍 Checking hybrid agentic requirements...")
    print("   🔗 Using llm_service.py for LLM integration")
    print("   🚫 Removed Hugging Face dependencies")
    
    # Check for essential libraries
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
    
    # Check for LLM service dependencies
    llm_dependencies = [
        'openai', 'anthropic', 'google', 'vertexai'
    ]
    
    print("   🔗 LLM Service Dependencies:")
    llm_available = True
    for module in llm_dependencies:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ⚠️ {module} - Optional (some LLM providers may not work)")
            llm_available = False
    
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
        print("Please install requirements:")
        print("pip install pandas openpyxl numpy faiss-cpu scikit-learn")
        return False
    
    if not llm_available:
        print("\n⚠️ Some LLM dependencies are missing. The system will work in offline mode.")
        print("To enable full LLM functionality, install:")
        print("pip install openai anthropic google-cloud-aiplatform")
    
    print("✅ Hybrid agentic requirements are available!")
    print("🤖 Specialized agents with LLM integration ready")
    print("🔗 Using your llm_service.py for intelligent responses")
    return True

def main():
    """Main launcher function"""
    print("🚀 Hybrid Agentic Chat-Based AI Demo")
    print("=" * 60)
    print("🤖 Specialized Agents with LLM Integration")
    print("🔗 Using llm_service.py for Online Responses")
    print("🚫 Hugging Face Dependencies Removed")
    print("📦 Built-in Python Libraries + Minimal Dependencies")
    print("=" * 60)
    
    # Check requirements
    if not check_hybrid_agentic_requirements():
        sys.exit(1)
    
    # Check if hybrid_agentic_main.py exists
    hybrid_agentic_main_path = Path("hybrid_agentic_main.py")
    if not hybrid_agentic_main_path.exists():
        print("❌ hybrid_agentic_main.py not found!")
        print("Please ensure you're in the chatbased_demo_app directory")
        sys.exit(1)
    
    print("\n🎯 Starting hybrid agentic demo...")
    print("🤖 Agents: Data Processor, Schema Mapper, Validator, Code Generator")
    print("🔗 LLM Integration: Using your llm_service.py")
    print("🚫 Hugging Face: Dependencies removed")
    print("=" * 60)
    
    # Import and run the hybrid agentic demo
    try:
        from hybrid_agentic_main import main as run_hybrid_agentic_demo
        run_hybrid_agentic_demo()
    except Exception as e:
        print(f"❌ Error starting hybrid agentic demo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
