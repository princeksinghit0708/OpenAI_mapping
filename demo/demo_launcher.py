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
    print("4. 🔍 Metadata Validator Demo (NEW!)")
    print("5. 📖 View Demo Documentation")
    print("0. 🚪 Exit")
    
    choice = input("\nSelect option (0-5): ").strip()
    
    if choice == "1":
        print("\n🤖 Starting Agent Framework Demo...")
        print("💡 In the menu, select option 2: 'Run Enhanced Features Demo'")
        subprocess.run([sys.executable, "agentic_mapping_ai/run_enhanced_application.py"])
    
    elif choice == "2":
        print("\n⚡ Starting Enhanced Main Application...")
        subprocess.run([sys.executable, "enhanced_main.py"])
    
    elif choice == "3":
        print("\n🧪 Starting Test Generator Agent Demo...")
        print("💡 This demonstrates standalone test generation capabilities")
        subprocess.run([sys.executable, "test_agent_demo.py"])
    
    elif choice == "4":
        print("\n🔍 Starting Metadata Validator Demo...")
        print("💡 This validates real banking table metadata from results/ folder")
        subprocess.run([sys.executable, "metadata_validator_demo.py"])
    
    elif choice == "5":
        print("\n📖 Demo Documentation:")
        print("See README_DEMO.md for detailed instructions")
        if Path("README_DEMO.md").exists():
            with open("README_DEMO.md", "r") as f:
                content = f.read()
                print(content[:1000] + "..." if len(content) > 1000 else content)
    
    elif choice == "0":
        print("👋 Demo ended. Good luck with your presentation!")
    
    else:
        print("❌ Invalid option. Please select 0-5.")

if __name__ == "__main__":
    main()
