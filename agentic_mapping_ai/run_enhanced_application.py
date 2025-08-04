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
    """Check if environment is properly configured for enhanced features"""
    print("🔍 Checking enhanced environment configuration...")
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("📝 Please check your .env file or set these variables")
        return False
    
    # Check optional multi-provider keys
    optional_providers = {
        "ANTHROPIC_API_KEY": "Claude",
        "GOOGLE_API_KEY": "Gemini",
        "AZURE_OPENAI_API_KEY": "Azure OpenAI"
    }
    
    available_providers = ["OpenAI"]  # OpenAI is required
    for var, provider in optional_providers.items():
        if os.getenv(var):
            available_providers.append(provider)
    
    print(f"✅ Environment check passed")
    print(f"🤖 Available AI providers: {', '.join(available_providers)}")
    
    # Set enhanced features based on available providers
    if len(available_providers) > 1:
        os.environ.setdefault("ENABLE_MULTI_PROVIDER", "true")
        print(f"✨ Multi-provider mode enabled with {len(available_providers)} providers")
    else:
        os.environ.setdefault("ENABLE_MULTI_PROVIDER", "false")
        print(f"🔧 Single-provider mode (OpenAI only)")
    
    return True


def install_enhanced_dependencies():
    """Install enhanced dependencies if needed"""
    print("📦 Checking enhanced dependencies...")
    
    required_packages = [
        "litellm>=1.17.0",
        "tenacity>=8.2.3",
        "structlog>=23.2.0",
        "langchain-anthropic>=0.1.0"
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
    
    host = os.getenv("API_HOST", "0.0.0.0")
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


def run_streamlit_ui():
    """Run the enhanced Streamlit UI"""
    print("🎨 Starting Enhanced Streamlit UI...")
    
    host = os.getenv("STREAMLIT_HOST", "localhost")
    port = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    try:
        import streamlit.web.cli as stcli
        sys.argv = [
            "streamlit", "run", "ui/streamlit_app.py",
            "--server.address", host,
            "--server.port", str(port),
            "--theme.base", "dark"
        ]
        stcli.main()
    except ImportError:
        print("❌ streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], check=True)
        run_streamlit_ui()


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
║                Enhanced with LangChain + LiteLLM                 ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ✨ NEW ENHANCED FEATURES:                                       ║
║  🤖 Multi-Provider AI (OpenAI, Claude, Gemini)                  ║
║  🔗 LangChain Integration for Advanced Workflows                ║
║  ⚡ LiteLLM for Intelligent Provider Routing                    ║
║  🎯 Enhanced Metadata Validation (Fixes DB Name Issue)          ║
║  🏗️ AI-Powered Code Generation                                   ║
║  📊 Advanced Cost Tracking & Optimization                       ║
║  🛡️ Production-Ready Error Handling                             ║
║  📈 Performance Monitoring & Analytics                          ║
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
        print("2. 🎨 Start Enhanced UI (Streamlit)")
        print("3. 🔄 Start Both API & UI (Recommended)")
        print("4. 🎯 Run Enhanced Features Demo")
        print("5. 📊 Run LiteLLM Comparison Demo")
        print("6. ⚙️  Interactive LiteLLM Setup Helper")
        print("7. 🔍 Health Check & System Status")
        print("8. 📖 View Enhanced Documentation")
        print("9. ❓ Help & Enhanced Features Guide")
        print("0. 🚪 Exit")
        
        try:
            choice = input("\n👉 Select an option (0-9): ").strip()
            
            if choice == "1":
                run_fastapi_server()
            elif choice == "2":
                run_streamlit_ui()
            elif choice == "3":
                print("🚀 Starting both Enhanced API server and UI...")
                print("📡 API will be available at: http://localhost:8000")
                print("🎨 UI will be available at: http://localhost:8501")
                
                # Start API in background process
                api_process = multiprocessing.Process(target=run_fastapi_server)
                api_process.start()
                
                # Wait a moment for API to start
                time.sleep(3)
                
                # Start UI in main process
                try:
                    run_streamlit_ui()
                except KeyboardInterrupt:
                    print("🛑 Shutting down Enhanced Agentic Mapping AI...")
                    api_process.terminate()
                    api_process.join()
                    break
                    
            elif choice == "4":
                run_enhanced_demo()
            elif choice == "5":
                run_comparison_demo()
            elif choice == "6":
                try:
                    subprocess.run([sys.executable, "setup_litellm_decision.py"], check=True)
                except subprocess.CalledProcessError:
                    print("❌ Setup helper not available")
            elif choice == "7":
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
                    print("💡 Start the server with option 1 or 3")
            elif choice == "8":
                print("📖 Enhanced Documentation:")
                print("   📄 LANGCHAIN_LITELLM_ENHANCEMENTS.md - Enhanced features guide")
                print("   📄 LITELLM_ANALYSIS.md - Detailed comparison and analysis")
                print("   📄 README.md - General setup and usage")
                print("   🌐 API Docs: http://localhost:8000/docs (when server is running)")
            elif choice == "9":
                print("❓ Enhanced Features Help:")
                print("\n🎯 KEY ENHANCED FEATURES:")
                print("   • Multi-Strategy Database Name Extraction (fixes your original issue)")
                print("   • AI-Powered Field Validation with confidence scoring")
                print("   • Multi-Provider LLM support (OpenAI, Claude, Gemini)")
                print("   • Intelligent cost optimization and provider routing")
                print("   • Advanced error handling with automatic fallbacks")
                print("   • Comprehensive testing and documentation generation")
                print("\n🔧 CONFIGURATION:")
                print("   • Set API keys in .env file")
                print("   • Enable ENABLE_MULTI_PROVIDER=true for advanced features")
                print("   • Use /api/v1/enhanced/ endpoints for new capabilities")
                print("\n📞 API ENDPOINTS:")
                print("   • POST /api/v1/enhanced/extract - Enhanced metadata extraction")
                print("   • POST /api/v1/enhanced/pipeline/full - Complete enhanced pipeline")
                print("   • GET /health - System health with enhanced metrics")
            elif choice == "0":
                print("👋 Thank you for using Enhanced Agentic Mapping AI!")
                print("✨ Your enhanced platform is ready for production use!")
                break
            else:
                print("❌ Invalid option. Please select 0-9.")
                
        except KeyboardInterrupt:
            print("\n🛑 Enhanced Agentic Mapping AI shutting down...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔧 Please check your configuration and try again.")


if __name__ == "__main__":
    main()