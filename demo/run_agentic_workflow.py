#!/usr/bin/env python3
"""
🚀 Agentic Excel Workflow Launcher
Simple launcher for the complete agentic workflow application
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher"""
    print("🚀 Agentic Excel Workflow Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    if not Path("agentic_excel_workflow_app.py").exists():
        print("❌ agentic_excel_workflow_app.py not found!")
        print("💡 Make sure you're running from the demo directory")
        return 1
    
    if not Path("agentic_mapping_ai/agents/metadata_validator.py").exists():
        print("❌ agentic_mapping_ai not found!")
        print("💡 Make sure the AI framework is properly installed")
        return 1
    
    print("✅ Prerequisites check passed")
    
    # Check for Excel files
    excel_files = list(current_dir.glob("*.xlsx"))
    if excel_files:
        print(f"\n📊 Found {len(excel_files)} Excel file(s):")
        for excel_file in excel_files:
            print(f"   📄 {excel_file.name}")
        
        # Ask user which file to use
        print("\nWhich Excel file would you like to process?")
        for i, excel_file in enumerate(excel_files, 1):
            print(f"{i}. {excel_file.name}")
        print(f"{len(excel_files) + 1}. Create sample Excel file")
        print(f"{len(excel_files) + 2}. Enter custom path")
        
        try:
            choice = int(input(f"\nEnter your choice (1-{len(excel_files) + 2}): ").strip())
            
            if 1 <= choice <= len(excel_files):
                selected_file = excel_files[choice - 1]
                print(f"✅ Selected: {selected_file.name}")
                
            elif choice == len(excel_files) + 1:
                # Create sample file
                print("📊 Creating sample Excel file...")
                try:
                    from create_sample_excel import create_sample_excel
                    selected_file = Path(create_sample_excel())
                    print(f"✅ Sample file created: {selected_file.name}")
                except Exception as e:
                    print(f"❌ Failed to create sample file: {e}")
                    return 1
                    
            elif choice == len(excel_files) + 2:
                # Custom path
                custom_path = input("Enter full path to Excel file: ").strip()
                selected_file = Path(custom_path)
                if not selected_file.exists():
                    print(f"❌ File not found: {custom_path}")
                    return 1
                print(f"✅ Using custom file: {selected_file.name}")
                
            else:
                print("❌ Invalid choice")
                return 1
                
        except ValueError:
            print("❌ Please enter a valid number")
            return 1
        except KeyboardInterrupt:
            print("\n👋 Cancelled by user")
            return 0
    else:
        print("\n📊 No Excel files found in current directory")
        print("💡 Creating sample Excel file...")
        
        try:
            from create_sample_excel import create_sample_excel
            selected_file = Path(create_sample_excel())
            print(f"✅ Sample file created: {selected_file.name}")
        except Exception as e:
            print(f"❌ Failed to create sample file: {e}")
            return 1
    
    # Confirm before running
    print(f"\n🎯 Ready to run agentic workflow with: {selected_file.name}")
    print("\nThis will execute the complete workflow:")
    print("1. 📊 Excel Reading & Parsing")
    print("2. 🔍 Metadata Validation")
    print("3. 🧪 Testing & Quality Assurance")
    print("4. 💻 Code Generation")
    print("5. 🎯 Workflow Orchestration")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("👋 Workflow cancelled")
        return 0
    
    # Run the workflow
    print(f"\n🚀 Starting agentic workflow...")
    print("=" * 60)
    
    try:
        # Import and run the workflow
        from agentic_excel_workflow_app import AgenticExcelWorkflowApp
        import asyncio
        
        app = AgenticExcelWorkflowApp()
        success = asyncio.run(app.run_complete_workflow(str(selected_file)))
        
        if success:
            print("\n🎉 Workflow completed successfully!")
            print("💡 Check the output/ directory for results")
            return 0
        else:
            print("\n❌ Workflow completed with errors")
            print("💡 Check the output/final_reports/ for error details")
            return 1
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        return 1
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
