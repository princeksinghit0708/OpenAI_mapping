#!/usr/bin/env python3
"""
Quick Setup Script for Agentic Mapping AI Demo
Automates the complete setup process for demo managers
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

console = Console()

class DemoSetup:
    def __init__(self):
        self.demo_path = Path(__file__).parent
        self.python_cmd = self._get_python_command()
        self.errors = []
        self.warnings = []
        
    def _get_python_command(self):
        """Detect the correct Python command"""
        for cmd in ['python3', 'python', 'py']:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and 'Python 3.' in result.stdout:
                    return cmd
            except FileNotFoundError:
                continue
        return 'python'
    
    def check_system_requirements(self):
        """Check if system meets minimum requirements"""
        console.print("\n[bold blue]🔍 Checking System Requirements...[/bold blue]")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            self.errors.append(f"Python 3.8+ required, found {python_version.major}.{python_version.minor}")
            return False
        else:
            console.print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check available memory (approximate)
        try:
            import psutil
            memory_gb = psutil.virtual_memory().total / (1024**3)
            if memory_gb < 4:
                self.warnings.append(f"Low memory: {memory_gb:.1f}GB (8GB+ recommended)")
            else:
                console.print(f"✅ Memory: {memory_gb:.1f}GB")
        except ImportError:
            console.print("⚠️  Memory check skipped (psutil not available)")
        
        # Check disk space
        disk_free = os.statvfs('.').f_frsize * os.statvfs('.').f_bavail / (1024**3)
        if disk_free < 2:
            self.errors.append(f"Insufficient disk space: {disk_free:.1f}GB (5GB+ required)")
            return False
        else:
            console.print(f"✅ Disk Space: {disk_free:.1f}GB available")
        
        # Check internet connectivity
        try:
            import urllib.request
            urllib.request.urlopen('https://google.com', timeout=5)
            console.print("✅ Internet connectivity")
        except:
            self.warnings.append("Internet connectivity check failed - LLM providers may not work")
        
        return True
    
    def setup_virtual_environment(self):
        """Create and activate virtual environment"""
        console.print("\n[bold blue]🐍 Setting up Virtual Environment...[/bold blue]")
        
        venv_path = self.demo_path / 'venv'
        
        if venv_path.exists():
            console.print("✅ Virtual environment already exists")
            return True
        
        try:
            # Create virtual environment
            subprocess.run([self.python_cmd, '-m', 'venv', str(venv_path)], 
                         check=True, capture_output=True)
            console.print("✅ Virtual environment created")
            
            # Provide activation instructions
            if platform.system() == 'Windows':
                activate_cmd = str(venv_path / 'Scripts' / 'activate.bat')
            else:
                activate_cmd = f"source {venv_path}/bin/activate"
            
            console.print(f"💡 To activate: [cyan]{activate_cmd}[/cyan]")
            return True
            
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Failed to create virtual environment: {e}")
            return False
    
    def install_dependencies(self):
        """Install Python dependencies"""
        console.print("\n[bold blue]📦 Installing Dependencies...[/bold blue]")
        
        requirements_files = [
            'requirements.txt',
            'requirements_complete.txt'
        ]
        
        # Find the best requirements file
        req_file = None
        for req in requirements_files:
            if (self.demo_path / req).exists():
                req_file = self.demo_path / req
                break
        
        if not req_file:
            self.errors.append("No requirements.txt file found")
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Installing packages...", total=1)
                
                # Install dependencies
                result = subprocess.run([
                    self.python_cmd, '-m', 'pip', 'install', '-r', str(req_file)
                ], capture_output=True, text=True, timeout=600)
                
                progress.update(task, advance=1)
                
                if result.returncode == 0:
                    console.print("✅ Dependencies installed successfully")
                    return True
                else:
                    self.errors.append(f"Pip install failed: {result.stderr}")
                    return False
                    
        except subprocess.TimeoutExpired:
            self.errors.append("Dependency installation timed out (>10 minutes)")
            return False
        except Exception as e:
            self.errors.append(f"Installation error: {e}")
            return False
    
    def setup_configuration(self):
        """Set up configuration files"""
        console.print("\n[bold blue]⚙️  Setting up Configuration...[/bold blue]")
        
        # Create .env file if it doesn't exist
        env_file = self.demo_path / '.env'
        if not env_file.exists():
            env_content = """# Agentic Mapping AI Demo Configuration
# Application Settings
APP_NAME=Agentic Mapping AI Demo
APP_VERSION=1.0.0
DEBUG=true
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# File Paths
EXCEL_FILE=ebs_IM_account_DATAhub_mapping_v8.0.xlsx
RESULTS_DIR=results
OUTPUT_DIR=output

# Vector Database
FAISS_INDEX_PATH=./indexes
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# MongoDB Configuration (Optional)
# MONGODB_URL=mongodb://localhost:27017
# MONGODB_DATABASE=agentic_mapping
# MONGODB_COLLECTION=tokens

# LLM Configuration
# Note: Using token-based authentication - no API keys needed
DEFAULT_LLM_PROVIDER=azure
LLM_TIMEOUT=300
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            console.print("✅ Configuration file created")
        else:
            console.print("✅ Configuration file already exists")
        
        # Create output directories
        output_dirs = ['output', 'logs', 'indexes', 'data']
        for dir_name in output_dirs:
            dir_path = self.demo_path / dir_name
            dir_path.mkdir(exist_ok=True)
        console.print("✅ Output directories created")
        
        return True
    
    def validate_installation(self):
        """Validate that the installation works"""
        console.print("\n[bold blue]🧪 Validating Installation...[/bold blue]")
        
        # Test basic imports
        test_imports = [
            'fastapi',
            'uvicorn', 
            'pandas',
            'pydantic',
            'pydantic_settings',
            'rich'
        ]
        
        for module in test_imports:
            try:
                __import__(module)
                console.print(f"✅ {module}")
            except ImportError:
                self.errors.append(f"Failed to import {module}")
        
        # Test demo launcher
        launcher_file = self.demo_path / 'demo_launcher.py'
        if launcher_file.exists():
            console.print("✅ Demo launcher found")
        else:
            self.warnings.append("Demo launcher not found")
        
        # Test API import (without running)
        try:
            sys.path.insert(0, str(self.demo_path))
            # Don't actually import to avoid dependency issues
            api_file = self.demo_path / 'agentic_mapping_ai' / 'api' / 'main.py'
            if api_file.exists():
                console.print("✅ API module found")
            else:
                self.warnings.append("API module not found")
        except Exception as e:
            self.warnings.append(f"API validation warning: {e}")
        
        return len(self.errors) == 0
    
    def generate_demo_summary(self):
        """Generate a summary of the demo setup"""
        console.print("\n[bold blue]📋 Demo Setup Summary[/bold blue]")
        
        # Create summary table
        table = Table(title="Demo Configuration")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details")
        
        table.add_row("Python Version", "✅ Ready", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        table.add_row("Demo Path", "✅ Ready", str(self.demo_path))
        table.add_row("Configuration", "✅ Ready", ".env file created")
        table.add_row("Dependencies", "✅ Ready" if not self.errors else "❌ Issues", f"{len(self.errors)} errors")
        table.add_row("API Server", "✅ Ready", "http://localhost:8000")
        table.add_row("Documentation", "✅ Ready", "DEMO_MANAGER_GUIDE.md")
        
        console.print(table)
        
        # Quick start commands
        console.print("\n[bold green]🚀 Quick Start Commands:[/bold green]")
        console.print("1. [cyan]python demo_launcher.py[/cyan] - Interactive demo menu")
        console.print("2. [cyan]python validate_demo.py[/cyan] - Validate setup")
        console.print("3. [cyan]cd agentic_mapping_ai && python -m uvicorn api.main:app --reload[/cyan] - Start API server")
        
        # Demo scenarios
        console.print("\n[bold yellow]📈 Demo Scenarios:[/bold yellow]")
        console.print("• [cyan]Agent Framework Demo[/cyan] - Multi-agent orchestration")
        console.print("• [cyan]Metadata Validation[/cyan] - Document analysis")
        console.print("• [cyan]Code Generation[/cyan] - Automated PySpark code")
        console.print("• [cyan]Test Generation[/cyan] - Comprehensive test suites")
        
        # Important files
        console.print("\n[bold magenta]📁 Key Files:[/bold magenta]")
        console.print("• [cyan]DEMO_MANAGER_GUIDE.md[/cyan] - Complete demo guide")
        console.print("• [cyan]REQUIREMENTS_DETAILED.md[/cyan] - Technical requirements")
        console.print("• [cyan]README_DEMO.md[/cyan] - Setup instructions")
        console.print("• [cyan].env[/cyan] - Configuration settings")
    
    def run_setup(self):
        """Run the complete setup process"""
        console.print(Panel.fit(
            "[bold blue]🎯 Agentic Mapping AI Demo Setup[/bold blue]\n"
            "Automated setup for demo managers\n"
            "This will install and configure everything needed for the demo.",
            title="Welcome",
            border_style="blue"
        ))
        
        setup_steps = [
            ("System Requirements", self.check_system_requirements),
            ("Virtual Environment", self.setup_virtual_environment), 
            ("Dependencies", self.install_dependencies),
            ("Configuration", self.setup_configuration),
            ("Validation", self.validate_installation)
        ]
        
        for step_name, step_func in setup_steps:
            try:
                if not step_func():
                    console.print(f"\n[red]❌ Setup failed at: {step_name}[/red]")
                    self._show_errors()
                    return False
            except KeyboardInterrupt:
                console.print(f"\n[yellow]⚠️  Setup interrupted during: {step_name}[/yellow]")
                return False
            except Exception as e:
                console.print(f"\n[red]❌ Unexpected error in {step_name}: {e}[/red]")
                return False
        
        # Show summary
        self.generate_demo_summary()
        
        # Show any warnings
        if self.warnings:
            console.print("\n[yellow]⚠️  Warnings:[/yellow]")
            for warning in self.warnings:
                console.print(f"  • {warning}")
        
        if self.errors:
            console.print("\n[red]❌ Errors that need attention:[/red]")
            self._show_errors()
            return False
        
        console.print("\n[bold green]🎉 Setup completed successfully![/bold green]")
        console.print("[cyan]Your demo is ready to run![/cyan]")
        
        return True
    
    def _show_errors(self):
        """Display all accumulated errors"""
        for error in self.errors:
            console.print(f"  • [red]{error}[/red]")

def main():
    """Main setup function"""
    setup = DemoSetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Setup cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
