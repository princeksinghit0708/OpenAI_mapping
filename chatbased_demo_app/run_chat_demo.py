#!/usr/bin/env python3
"""
🚀 Chat-Based Agentic AI Demo Launcher
Simple launcher script for the chat-based interface
"""

import os
import sys
from pathlib import Path

def main():
    """Main launcher function"""
    print("🚀 Chat-Based Agentic AI Demo Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Check if main.py exists
    if not Path("main.py").exists():
        print("❌ main.py not found!")
        print("💡 Make sure you're running from the chatbased_demo_app directory")
        return 1
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    # Check if parent directories exist
    parent_dir = current_dir.parent
    if not (parent_dir / "agentic_mapping_ai").exists():
        print("❌ agentic_mapping_ai directory not found!")
        print("💡 Make sure the AI framework is properly installed")
        return 1
    
    if not (parent_dir / "demo").exists():
        print("❌ demo directory not found!")
        print("💡 Make sure the demo system is properly installed")
        return 1
    
    print("✅ Prerequisites check passed")
    
    # Check for Excel files in parent demo directory
    demo_dir = parent_dir / "demo"
    excel_files = list(demo_dir.glob("*.xlsx")) + list(demo_dir.glob("*.xls"))
    
    if excel_files:
        print(f"\n📊 Found {len(excel_files)} Excel file(s) in demo directory:")
        for excel_file in excel_files:
            print(f"   📄 {excel_file.name}")
        
        print("\n💡 You can use these files with the chat interface:")
        print(f"   upload {excel_file}")
    
    # Confirm before running
    print(f"\n🎯 Ready to launch chat-based demo!")
    print("\nThis will start the interactive chat interface with:")
    print("• 🤖 AI Agent integration")
    print("• 💬 Natural language commands")
    print("• 📊 Excel file processing")
    print("• 🔍 Intelligent validation")
    print("• 💻 Code generation")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("👋 Demo launch cancelled")
        return 0
    
    # Launch the chat demo
    print(f"\n🚀 Launching chat-based demo...")
    print("=" * 60)
    
    try:
        # Import and run the main application
        from main import main as run_main
        import asyncio
        
        # Run the async main function
        asyncio.run(run_main())
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed")
        return 1
    except Exception as e:
        print(f"❌ Demo execution failed: {e}")
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
