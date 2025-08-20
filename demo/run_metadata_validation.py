#!/usr/bin/env python3
"""
🚀 Metadata Validation Demo Launcher
Easy way to run the Hive metadata validation demo
"""

import sys
import os
from pathlib import Path

def main():
    """Main launcher for metadata validation demo"""
    print("🚀 Metadata Validation Demo Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    # Check for agentic_mapping_ai
    if not Path("agentic_mapping_ai/agents/metadata_validator.py").exists():
        print("❌ agentic_mapping_ai not found!")
        print("💡 Make sure you're running from the demo directory")
        return 1
    
    # Check for results directory
    if not Path("results").exists():
        print("❌ results/ directory not found!")
        print("💡 Make sure you have the metadata JSON files")
        return 1
    
    # Check for metadata files
    metadata_files = list(Path("results").glob("*_metadata.json"))
    if not metadata_files:
        print("❌ No metadata files found in results/")
        print("💡 Expected: acct_dly_metadata.json, cust_dly_metadata.json, txn_dly_metadata.json")
        return 1
    
    print(f"✅ Found {len(metadata_files)} metadata files")
    for file in metadata_files:
        print(f"   📄 {file.name}")
    
    print("\n🎯 Ready to run metadata validation demo!")
    print("=" * 50)
    
    # Ask user what they want to do
    print("\nWhat would you like to do?")
    print("1. 🧪 Test the agent first (recommended)")
    print("2. 🚀 Run the full demo directly")
    print("3. 📊 View metadata files")
    print("4. ❌ Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🧪 Running agent test...")
        os.system("python test_metadata_agent.py")
        
        # Ask if they want to continue to demo
        continue_choice = input("\nContinue to full demo? (y/n): ").strip().lower()
        if continue_choice == 'y':
            choice = "2"
    
    if choice == "2":
        print("\n🚀 Running full metadata validation demo...")
        os.system("python hive_metadata_validation_demo.py")
        
    elif choice == "3":
        print("\n📊 Metadata files content:")
        for file in metadata_files:
            print(f"\n📄 {file.name}:")
            try:
                with open(file, 'r') as f:
                    import json
                    data = json.load(f)
                    print(f"   Table: {data.get('table_name', 'Unknown')}")
                    print(f"   Database: {data.get('database_name', 'Unknown')}")
                    print(f"   Columns: {len(data.get('columns', []))}")
                    print(f"   Rows: {data.get('row_count', 'Unknown'):,}")
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        
        # Ask if they want to run demo
        demo_choice = input("\nRun the validation demo now? (y/n): ").strip().lower()
        if demo_choice == 'y':
            print("\n🚀 Running metadata validation demo...")
            os.system("python hive_metadata_validation_demo.py")
    
    elif choice == "4":
        print("👋 Goodbye!")
        return 0
    
    else:
        print("❌ Invalid choice. Please run the script again.")
        return 1
    
    print("\n🎉 Demo completed!")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
