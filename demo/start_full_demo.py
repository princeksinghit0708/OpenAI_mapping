#!/usr/bin/env python3
"""
🚀 Full Demo Starter
Starts both the FastAPI backend and React UI simultaneously
"""

import os
import sys
import subprocess
import threading
import time
import signal
from pathlib import Path

class DemoLauncher:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🔧 Starting FastAPI Backend...")
        
        try:
            # Change to demo directory
            os.chdir(Path.cwd())
            
            # Start FastAPI server
            backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "agentic_mapping_ai.api.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            self.processes.append(("Backend", backend_process))
            
            # Monitor backend output
            for line in iter(backend_process.stdout.readline, ''):
                if not self.running:
                    break
                print(f"[BACKEND] {line.strip()}")
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
    
    def start_frontend(self):
        """Start the React frontend"""
        print("🎨 Starting React Frontend...")
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        try:
            react_dir = Path.cwd() / "react-ui"
            
            if not react_dir.exists():
                print("❌ React directory not found!")
                return
            
            # Change to React directory
            os.chdir(react_dir)
            
            # Check if dependencies are installed
            if not (react_dir / "node_modules").exists():
                print("📦 Installing React dependencies...")
                subprocess.run(["npm", "install", "--silent"], check=True)
            
            # Set environment variables
            env = os.environ.copy()
            env["REACT_APP_API_URL"] = "http://localhost:8000"
            env["BROWSER"] = "none"
            env["CI"] = "true"  # Suppress some warnings
            
            # Start React development server
            frontend_process = subprocess.Popen([
                "npm", "start"
            ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
               text=True, env=env)
            
            self.processes.append(("Frontend", frontend_process))
            
            # Monitor frontend output
            for line in iter(frontend_process.stdout.readline, ''):
                if not self.running:
                    break
                if line.strip():  # Only print non-empty lines
                    print(f"[FRONTEND] {line.strip()}")
                    
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
    
    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping all services...")
        self.running = False
        
        for name, process in self.processes:
            try:
                print(f"   Stopping {name}...")
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"   Force killing {name}...")
                process.kill()
            except Exception as e:
                print(f"   Error stopping {name}: {e}")
        
        print("✅ All services stopped")
    
    def run(self):
        """Run the full demo"""
        print("🚀 Agentic Mapping AI - Full Demo Launcher")
        print("=" * 60)
        print("📡 Backend API: http://localhost:8000")
        print("🎨 Frontend UI: http://localhost:3000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("=" * 60)
        print("\n⚠️  Press Ctrl+C to stop all services\n")
        
        try:
            # Start backend in a separate thread
            backend_thread = threading.Thread(target=self.start_backend, daemon=True)
            backend_thread.start()
            
            # Start frontend in main thread (to capture output)
            self.start_frontend()
            
        except KeyboardInterrupt:
            print("\n🔄 Shutting down...")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.stop_all()

def check_dependencies():
    """Check if required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    python_version = sys.version.split()[0]
    print(f"✅ Python: {python_version}")
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found! Please install from https://nodejs.org/")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found! Please install from https://nodejs.org/")
        return False
    
    # Check uvicorn
    try:
        import uvicorn
        print("✅ uvicorn available")
    except ImportError:
        print("❌ uvicorn not found! Please install: pip install uvicorn")
        return False
    
    return True

def main():
    if not check_dependencies():
        print("\n❌ Missing dependencies. Please install them and try again.")
        sys.exit(1)
    
    # Set up signal handling
    launcher = DemoLauncher()
    
    def signal_handler(sig, frame):
        launcher.stop_all()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the demo
    launcher.run()

if __name__ == "__main__":
    main()
