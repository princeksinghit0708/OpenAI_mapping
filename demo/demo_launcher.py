#!/usr/bin/env python3
"""
🎯 Quick Demo Launcher
One-click demo starter for the agent framework
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🎯 Agent Framework Demo Launcher")
    print("=" * 50)
    
    # Check if we're in the demo directory
    if not Path("agentic_mapping_ai/run_enhanced_application.py").exists():
        print("❌ Please run this from the demo directory")
        print("Usage: cd demo && python demo_launcher.py")
        sys.exit(1)
    
    # Check for Excel file
    excel_files = list(Path(".").glob("*.xlsx"))
    if not excel_files:
        print("⚠️  Excel file not found!")
        print("Please add: ebs_IM_account_DATAhub_mapping_v8.0.xlsx")
        print("Or any Excel mapping file to the demo folder")
        print()
    
    # Check helix CLI
    try:
        result = subprocess.run(["which", "helix"], capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠️  helix CLI not found. Token authentication may not work.")
            print("The demo will attempt MongoDB fallback if configured.")
        else:
            print("✅ helix CLI found - token authentication ready")
    except:
        print("⚠️  Could not check helix CLI status")
    
    print()
    print("🚀 Demo Options:")
    print("1. 🤖 Agent Framework Demo (Interactive)")
    print("2. ⚡ Enhanced Main Application (Direct)")
    print("3. 🧪 Test Generator Agent Demo")
    print("4. 🔍 Metadata Validator Demo")
    print("5. 📊 Setup Excel File (Required for demos)")
    print("6. 🎨 Start React UI Only")
    print("7. 🚀 Start Full Demo (API + UI)")
    print("8. 📖 View Demo Documentation")
    print("0. 🚪 Exit")
    
    choice = input("\nSelect option (0-8): ").strip()
    
    if choice == "1":
        print("\n🤖 Starting Agent Framework Demo...")
        print("💡 In the menu, select option 2: 'Run Enhanced Features Demo'")
        
        agent_app = Path("agentic_mapping_ai/run_enhanced_application.py")
        if agent_app.exists():
            subprocess.run([sys.executable, str(agent_app)])
        else:
            print("❌ Agent framework app not found")
            print(f"Expected: {agent_app.absolute()}")
    
    elif choice == "2":
        print("\n⚡ Starting Enhanced Main Application...")
        
        main_app = Path("enhanced_main.py")
        if main_app.exists():
            subprocess.run([sys.executable, str(main_app)])
        else:
            print("❌ Enhanced main application not found")
            print(f"Expected: {main_app.absolute()}")
    
    elif choice == "3":
        print("\n🧪 Starting Test Generator Agent Demo...")
        print("💡 This demonstrates standalone test generation capabilities")
        
        test_demo = Path("test_agent_demo.py")
        if test_demo.exists():
            subprocess.run([sys.executable, str(test_demo)])
        else:
            print("❌ Test generator demo not found")
            print(f"Expected: {test_demo.absolute()}")
    
    elif choice == "4":
        print("\n🔍 Starting Metadata Validator Demo...")
        print("💡 This validates real banking table metadata from results/ folder")
        
        # Check if the demo file exists
        demo_file = Path("metadata_validator_demo.py")
        if not demo_file.exists():
            print("❌ metadata_validator_demo.py not found in current directory")
            print(f"Current directory: {os.getcwd()}")
            print("Available Python files:")
            for py_file in Path(".").glob("*.py"):
                print(f"  - {py_file}")
            return
        
        try:
            subprocess.run([sys.executable, str(demo_file)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running demo: {e}")
        except FileNotFoundError as e:
            print(f"❌ File not found: {e}")
            print(f"Trying absolute path...")
            abs_path = demo_file.absolute()
            subprocess.run([sys.executable, str(abs_path)])
    
    elif choice == "5":
        print("\n📊 Setting up Excel File...")
        
        setup_script = Path("setup_excel.py")
        if setup_script.exists():
            subprocess.run([sys.executable, str(setup_script)])
        else:
            print("❌ Excel setup script not found")
    
    elif choice == "6":
        print("\n🎨 Starting React UI Only...")
        print("💡 Make sure the API server is running separately!")
        
        ui_script = Path("start_react_ui.py")
        if ui_script.exists():
            subprocess.run([sys.executable, str(ui_script)])
        else:
            print("❌ React UI script not found")
    
    elif choice == "7":
        print("\n🚀 Starting Full Demo (API + UI)...")
        print("💡 This will start both backend and frontend together")
        
        full_demo_script = Path("start_full_demo.py")
        if full_demo_script.exists():
            subprocess.run([sys.executable, str(full_demo_script)])
        else:
            print("❌ Full demo script not found")
    
    elif choice == "8":
        print("\n📖 Demo Documentation:")
        print("See README_DEMO.md for detailed instructions")
        if Path("README_DEMO.md").exists():
            with open("README_DEMO.md", "r") as f:
                content = f.read()
                print(content[:1000] + "..." if len(content) > 1000 else content)
    
    elif choice == "0":
        print("👋 Demo ended. Good luck with your presentation!")
    
    else:
        print("❌ Invalid option. Please select 0-8.")

if __name__ == "__main__":
    main()
