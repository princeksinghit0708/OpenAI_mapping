#!/usr/bin/env python3
"""
🎨 React UI Starter Script
Starts the React development server for the Agentic Mapping AI UI
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def main():
    print("🎨 Starting React UI for Agentic Mapping AI")
    print("=" * 50)
    
    # Check if we're in the demo directory
    current_dir = Path.cwd()
    react_dir = current_dir / "react-ui"
    
    if not react_dir.exists():
        print("❌ React UI directory not found!")
        print(f"Expected: {react_dir}")
        print("Please run this from the demo directory")
        sys.exit(1)
    
    # Check for Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            print(f"✅ Node.js found: {node_version}")
        else:
            print("❌ Node.js not found!")
            print("Please install Node.js from https://nodejs.org/")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ Node.js not found!")
        print("Please install Node.js from https://nodejs.org/")
        sys.exit(1)
    
    # Check for npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            print(f"✅ npm found: {npm_version}")
        else:
            print("❌ npm not found!")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ npm not found!")
        print("Please install npm (comes with Node.js)")
        sys.exit(1)
    
    # Change to react directory
    os.chdir(react_dir)
    
    # Check if dependencies are installed
    node_modules = react_dir / "node_modules"
    if not node_modules.exists():
        print("📦 Installing React dependencies...")
        print("This may take a few minutes...")
        
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("\nTrying with --legacy-peer-deps flag...")
            try:
                subprocess.run(["npm", "install", "--legacy-peer-deps"], check=True)
                print("✅ Dependencies installed successfully!")
            except subprocess.CalledProcessError as e2:
                print(f"❌ Failed to install dependencies: {e2}")
                sys.exit(1)
    else:
        print("✅ Dependencies already installed")
    
    # Start the development server
    print("\n🚀 Starting React development server...")
    print("📱 UI will be available at: http://localhost:3000")
    print("🔗 API should be running at: http://localhost:8000")
    print("\n💡 Make sure the FastAPI backend is running!")
    print("   Run: python agentic_mapping_ai/api/main.py")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Set environment variables
        env = os.environ.copy()
        env["REACT_APP_API_URL"] = "http://localhost:8000"
        env["BROWSER"] = "none"  # Don't auto-open browser on some systems
        
        # Start the React development server
        if platform.system() == "Windows":
            subprocess.run(["npm.cmd", "start"], env=env)
        else:
            subprocess.run(["npm", "start"], env=env)
            
    except KeyboardInterrupt:
        print("\n\n👋 React UI stopped")
    except Exception as e:
        print(f"\n❌ Error starting React UI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
