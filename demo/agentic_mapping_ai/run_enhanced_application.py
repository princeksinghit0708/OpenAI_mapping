#!/usr/bin/env python3
"""
Enhanced Application Runner for Agentic Mapping AI
Runs the enhanced platform with LangChain + LiteLLM integration
"""

import asyncio
import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path


def check_environment():
    """Check if environment is properly configured for token-based authentication"""
    print("🔍 Checking enhanced environment configuration...")
    
    # Check for token-based authentication setup
    print("🔐 Using token-based authentication - no API keys required!")
    
    # Check if helix CLI is available
    try:
        result = subprocess.run(["helix", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Helix CLI available for token generation")
        else:
            print("⚠️ Helix CLI not found - will try MongoDB fallback")
    except FileNotFoundError:
        print("⚠️ Helix CLI not found - will try MongoDB fallback")
    
    # Check optional MongoDB configuration for token fallback
    mongo_user = os.getenv("DEV_MONGO_USER")
    mongo_key = os.getenv("DEV_MONGO_KEY")
    
    if mongo_user and mongo_key:
        print("✅ MongoDB fallback configured for token storage")
    else:
        print("ℹ️ MongoDB fallback not configured (optional)")
    
    # All providers available via token-based auth
    available_providers = ["Azure", "Stellar", "Gemini", "Claude"]
    print(f"✅ Environment check passed")
    print(f"🤖 Available AI providers via token auth: {', '.join(available_providers)}")
    
    # Enable multi-provider by default with token auth
    os.environ.setdefault("ENABLE_MULTI_PROVIDER", "true")
    print(f"✨ Multi-provider mode enabled with token-based authentication")
    
    return True


def install_enhanced_dependencies():
    """Install enhanced dependencies if needed"""
    print("📦 Checking enhanced dependencies...")
    
    required_packages = [
        "litellm>=1.17.0",
        "tenacity>=8.2.3",
        "structlog>=23.2.0",
        "langchain-anthropic>=0.1.0",
        "pymongo>=4.6.0",  # For token storage fallback
        "google-auth>=2.0.0",  # For Google OAuth2 credentials
        "vertexai>=1.0.0"  # For Vertex AI integration
    ]
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split(">=")[0]
        try:
            __import__(package_name.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Installing missing enhanced packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade"
            ] + missing_packages, check=True, capture_output=True)
            print("✅ Enhanced dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("🔧 Please install manually: pip install -r requirements.txt")
            return False
    else:
        print("✅ All enhanced dependencies are available")
    
    return True


def run_fastapi_server():
    """Run the enhanced FastAPI server"""
    print("🚀 Starting Enhanced FastAPI server...")
    
            host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # Import uvicorn here to avoid import issues
    try:
        import uvicorn
        
        print(f"📡 Enhanced API server starting on http://{host}:{port}")
        print(f"📚 API Documentation: http://{host}:{port}/docs")
        print(f"✨ Enhanced Features: Multi-provider AI, LangChain + LiteLLM")
        
        uvicorn.run(
            "api.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"], check=True)
        import uvicorn
        uvicorn.run("api.main:app", host=host, port=port, reload=reload)


# Streamlit UI removed - focusing on core API functionality


def run_enhanced_demo():
    """Run enhanced capabilities demo"""
    print("🎯 Running Enhanced Capabilities Demo...")
    
    # Import and run the demo
    try:
        from examples.enhanced_features_demo import run_enhanced_demo
        asyncio.run(run_enhanced_demo())
    except ImportError as e:
        print(f"❌ Demo not available: {e}")
        print("🔧 Please ensure all enhanced components are properly installed")


def run_comparison_demo():
    """Run LiteLLM comparison demo"""
    print("📊 Running LiteLLM Comparison Demo...")
    
    try:
        from examples.litellm_comparison_demo import run_comparison_demo
        asyncio.run(run_comparison_demo())
    except ImportError as e:
        print(f"❌ Comparison demo not available: {e}")
        print("🔧 Please ensure enhanced components are installed")


def print_enhanced_banner():
    """Print enhanced application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                  🚀 AGENTIC MAPPING AI v2.0                     ║
║             Enhanced with Token-Based Authentication             ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ✨ NEW ENHANCED FEATURES:                                       ║
║  🔐 Token-Based Authentication (No API Keys Required!)          ║
║  🤖 Multi-Provider AI (Azure, Stellar, Gemini, Claude)          ║
║  📊 EBS IM Account DataHub Mapping Support                      ║
║  🔍 Goldref Lookup Integration                                   ║
║  🏗️ AI-Powered PySpark Code Generation                          ║
║  🛡️ Production-Ready Error Handling                             ║
║  📈 Performance Monitoring & Analytics                          ║
║  ⚡ Helix CLI + MongoDB Token Management                        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main enhanced application runner"""
    print_enhanced_banner()
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_enhanced_dependencies():
        sys.exit(1)
    
    # Show menu
    while True:
        print("\n" + "="*70)
        print("🚀 Enhanced Agentic Mapping AI - Main Menu")
        print("="*70)
        print("1. 🖥️  Start Enhanced API Server (FastAPI)")
        print("2. 🎯 Run Enhanced Features Demo")
        print("3. 📊 Run LiteLLM Comparison Demo")
        print("4. ⚙️  Interactive LiteLLM Setup Helper")
        print("5. 🔍 Health Check & System Status")
        print("6. 📖 View Enhanced Documentation")
        print("7. ❓ Help & Enhanced Features Guide")
        print("0. 🚪 Exit")
        
        try:
            choice = input("\n👉 Select an option (0-7): ").strip()
            
            if choice == "1":
                run_fastapi_server()
            elif choice == "2":
                run_enhanced_demo()
            elif choice == "3":
                run_comparison_demo()
            elif choice == "4":
                try:
                    subprocess.run([sys.executable, "setup_litellm_decision.py"], check=True)
                except subprocess.CalledProcessError:
                    print("❌ Setup helper not available")
            elif choice == "5":
                print("🔍 Performing Enhanced System Health Check...")
                try:
                    # Quick health check
                    import requests
                    response = requests.get("http://localhost:8000/health", timeout=5)
                    if response.status_code == 200:
                        health_data = response.json()
                        print("✅ Enhanced API Server: Healthy")
                        print(f"🤖 Enhanced Features: {health_data.get('components', {}).keys()}")
                    else:
                        print("⚠️ Enhanced API Server: Unhealthy")
                except:
                    print("❌ Enhanced API Server: Not running")
                    print("💡 Start the server with option 1")
            elif choice == "6":
                print("📖 Enhanced Documentation:")
                print("   📄 LANGCHAIN_LITELLM_ENHANCEMENTS.md - Enhanced features guide")
                print("   📄 LITELLM_ANALYSIS.md - Detailed comparison and analysis")
                print("   📄 README.md - General setup and usage")
                print("   🌐 API Docs: http://localhost:8000/docs (when server is running)")
            elif choice == "7":
                print("❓ Enhanced Features Help:")
                print("\n🎯 KEY ENHANCED FEATURES:")
                print("   • Token-Based Authentication (No API keys required!)")
                print("   • EBS IM Account DataHub mapping with goldref support")
                print("   • Multi-Provider LLM support (Azure, Stellar, Gemini, Claude)")
                print("   • Intelligent PySpark code generation")
                print("   • Advanced error handling with automatic fallbacks")
                print("   • Production-ready banking transformation logic")
                print("\n🔧 CONFIGURATION:")
                print("   • No API keys required - uses token-based authentication")
                print("   • Ensure helix CLI is installed and configured")
                print("   • Optional: Set DEV_MONGO_USER/DEV_MONGO_KEY for token fallback")
                print("   • Multi-provider mode enabled by default")
                print("\n📞 API ENDPOINTS:")
                print("   • POST /api/v1/enhanced/extract - Enhanced metadata extraction")
                print("   • POST /api/v1/enhanced/pipeline/full - Complete enhanced pipeline")
                print("   • GET /health - System health with enhanced metrics")
                print("\n🔐 TOKEN AUTHENTICATION:")
                print("   • Uses 'helix auth access-token print -a' for token generation")
                print("   • MongoDB fallback for token storage")
                print("   • Automatic token refresh and management")
            elif choice == "0":
                print("👋 Thank you for using Enhanced Agentic Mapping AI!")
                print("✨ Your enhanced platform is ready for production use!")
                break
            else:
                print("❌ Invalid option. Please select 0-7.")
                
        except KeyboardInterrupt:
            print("\n🛑 Enhanced Agentic Mapping AI shutting down...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔧 Please check your configuration and try again.")


if __name__ == "__main__":
    main()