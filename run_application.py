#!/usr/bin/env python3
"""
Production-Ready Data Mapping Application Runner
Simplifies running the application with proper setup
"""
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

def check_requirements():
    """Check if all requirements are met"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append("Python 3.8+ is required")
    
    # Check for .env file
    if not Path(".env").exists() and not os.getenv("OPENAI_API_KEY"):
        issues.append("OpenAI API key not configured")
    
    # Check for Excel file
    excel_files = list(Path(".").glob("*.xlsx"))
    if not excel_files:
        issues.append("No Excel files found in directory")
    
    return issues

def setup_environment():
    """Interactive setup for first-time users"""
    console.print(Panel.fit("🔧 First-Time Setup", style="bold blue"))
    
    # Check for .env file
    if not Path(".env").exists():
        console.print("[yellow]No .env file found. Let's create one![/yellow]")
        
        # No API key required - using token-based authentication
        console.print("[green]Using token-based authentication - no API key required[/green]")
        
        # Create .env file with basic configuration
        with open(".env", "w") as f:
            f.write("# Token-based authentication - no API key required\n")
            f.write("EXCEL_FILE=ebs_IM_account_DATAhub_mapping_v8.0.xlsx\n")
            f.write("RESULTS_DIR=results\n")
            f.write("OUTPUT_DIR=output\n")
            f.write("GPT_MODEL=gpt-4\n")
            f.write("MAX_TOKENS=8000\n")
            f.write("TEMPERATURE=0.1\n")
        
        console.print("[green]✓ Created .env file[/green]")
    
    # Create necessary directories
    dirs_to_create = ["results", "output", "indexes", "logs"]
    for dir_name in dirs_to_create:
        Path(dir_name).mkdir(exist_ok=True)
    
    console.print("[green]✓ Created necessary directories[/green]")

def display_info():
    """Display application information"""
    info_text = """
    🚀 Data Mapping Application
    
    This application uses GPT-4 with advanced prompt engineering to:
    • Analyze Excel mapping specifications
    • Generate production-ready PySpark code
    • Create comprehensive test cases
    • Build validation rules
    • Provide intelligent recommendations
    
    Features:
    • FAISS vector database for similarity search
    • Table metadata integration
    • Comprehensive error handling
    • Beautiful progress tracking
    """
    
    console.print(Panel(info_text, style="cyan"))

def main():
    """Main runner function"""
    console.print(Panel.fit("🎯 Data Mapping Application Runner", style="bold magenta"))
    
    # Check requirements
    issues = check_requirements()
    
    if issues:
        console.print("[red]⚠️  Setup Issues Found:[/red]")
        for issue in issues:
            console.print(f"  • {issue}")
        
        if Confirm.ask("\nWould you like to run the setup wizard?"):
            setup_environment()
        else:
            console.print("[yellow]Please resolve the issues and try again.[/yellow]")
            return
    
    # Display info
    display_info()
    
    # Check Excel file
    excel_files = list(Path(".").glob("*.xlsx"))
    if excel_files:
        console.print("\n[cyan]Found Excel files:[/cyan]")
        for i, file in enumerate(excel_files, 1):
            console.print(f"  {i}. {file.name}")
        
        if len(excel_files) > 1:
            choice = Prompt.ask(
                "Which file would you like to process?",
                choices=[str(i) for i in range(1, len(excel_files) + 1)],
                default="1"
            )
            selected_file = excel_files[int(choice) - 1]
            
            # Update .env with selected file
            if Path(".env").exists():
                with open(".env", "r") as f:
                    lines = f.readlines()
                
                with open(".env", "w") as f:
                    for line in lines:
                        if line.startswith("EXCEL_FILE="):
                            f.write(f"EXCEL_FILE={selected_file.name}\n")
                        else:
                            f.write(line)
    
    # Confirm execution
    if Confirm.ask("\n[bold]Ready to process mappings?[/bold]"):
        console.print("\n[green]Starting application...[/green]\n")
        
        # Import and run the main application
        try:
            from main import main as run_app
            run_app()
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print("[yellow]Please check the logs for details.[/yellow]")
    else:
        console.print("[yellow]Cancelled by user.[/yellow]")

if __name__ == "__main__":
    main() 