#!/usr/bin/env python3
"""
🔧 Demo Setup Script
Prepares the environment for the End-to-End Agentic Mapping AI Demo
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'pandas',
        'openpyxl', 
        'loguru',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("\n📥 Installing dependencies...")
    
    try:
        # Install from demo requirements
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'demo_requirements.txt'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    base_dir = Path(__file__).parent
    directories = [
        "demo_output",
        "demo_output/excel_parsed",
        "demo_output/validation_reports", 
        "demo_output/test_cases",
        "demo_output/generated_code",
        "demo_output/workflow_logs",
        "demo_output/final_reports",
        "demo_logs"
    ]
    
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}")

def check_agent_files():
    """Check if agent files exist"""
    print("\n🤖 Checking agent files...")
    
    base_dir = Path(__file__).parent
    required_files = [
        "agents/metadata_validator.py",
        "agents/code_generator.py", 
        "agents/orchestrator.py",
        "agents/base_agent.py",
        "core/models.py",
        "parsers/excel_mapping_parser.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required agent files exist")
    return True

def run_component_test():
    """Run the component test to verify everything works"""
    print("\n🧪 Running component test...")
    
    try:
        result = subprocess.run([
            sys.executable, 'test_demo_components.py'
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Component test passed")
            return True
        else:
            print(f"❌ Component test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running component test: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 AGENTIC MAPPING AI - DEMO SETUP")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version incompatible")
        return False
    
    # Check dependencies
    if not check_dependencies():
        print("\n📥 Installing missing dependencies...")
        if not install_dependencies():
            print("\n❌ Setup failed: Could not install dependencies")
            return False
    
    # Create directories
    create_directories()
    
    # Check agent files
    if not check_agent_files():
        print("\n❌ Setup failed: Missing required agent files")
        return False
    
    # Run component test
    if not run_component_test():
        print("\n❌ Setup failed: Component test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("\n🚀 You can now run the demo:")
    print("   python run_demo.py")
    print("\n📚 For more information, see DEMO_GUIDE.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
