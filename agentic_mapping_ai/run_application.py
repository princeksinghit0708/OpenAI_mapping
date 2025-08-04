#!/usr/bin/env python3
"""
Agentic Mapping AI Application Runner
Starts the API server and optionally the UI
"""

import asyncio
import os
import sys
import subprocess
import time
import signal
from pathlib import Path
import argparse
from typing import List, Optional

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

from config.settings import settings
from loguru import logger


class ApplicationRunner:
    """Application runner for coordinating API server and UI"""
    
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.running = False
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        required_packages = [
            "fastapi", "uvicorn", "streamlit", "langchain", 
            "chromadb", "sentence-transformers", "pyspark"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing required packages: {missing_packages}")
            logger.info("Install missing packages with: pip install -r requirements.txt")
            return False
        
        return True
    
    def setup_environment(self):
        """Setup environment variables and directories"""
        # Ensure required directories exist
        directories = [
            settings.codegen.code_output_dir,
            settings.codegen.test_output_dir,
            settings.vector_db.chroma_persist_directory,
            "./data/input",
            "./data/processed",
            "./output/reports",
            "./logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def start_api_server(self, background: bool = True) -> Optional[subprocess.Popen]:
        """Start the FastAPI server"""
        try:
            cmd = [
                sys.executable, "-m", "uvicorn",
                "api.main:app",
                "--host", settings.api.host,
                "--port", str(settings.api.port),
                "--reload" if settings.api.reload else "--no-reload",
                "--log-level", settings.monitoring.log_level.lower()
            ]
            
            logger.info(f"Starting API server: {' '.join(cmd)}")
            
            if background:
                process = subprocess.Popen(
                    cmd,
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.processes.append(process)
                
                # Wait a moment and check if process started successfully
                time.sleep(2)
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    logger.error(f"API server failed to start:")
                    logger.error(f"STDOUT: {stdout.decode()}")
                    logger.error(f"STDERR: {stderr.decode()}")
                    return None
                
                logger.info(f"API server started with PID: {process.pid}")
                return process
            else:
                # Run in foreground
                subprocess.run(cmd, cwd=PROJECT_ROOT)
                return None
                
        except Exception as e:
            logger.error(f"Failed to start API server: {str(e)}")
            return None
    
    def start_ui(self, background: bool = True) -> Optional[subprocess.Popen]:
        """Start the Streamlit UI"""
        try:
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "ui/streamlit_app.py",
                "--server.port", str(settings.ui.streamlit_port),
                "--server.address", settings.ui.streamlit_host,
                "--server.headless", "true" if background else "false"
            ]
            
            logger.info(f"Starting UI server: {' '.join(cmd)}")
            
            if background:
                process = subprocess.Popen(
                    cmd,
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                self.processes.append(process)
                
                # Wait a moment for startup
                time.sleep(3)
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    logger.error(f"UI server failed to start:")
                    logger.error(f"STDOUT: {stdout.decode()}")
                    logger.error(f"STDERR: {stderr.decode()}")
                    return None
                
                logger.info(f"UI server started with PID: {process.pid}")
                return process
            else:
                # Run in foreground
                subprocess.run(cmd, cwd=PROJECT_ROOT)
                return None
                
        except Exception as e:
            logger.error(f"Failed to start UI server: {str(e)}")
            return None
    
    def check_server_health(self, url: str, timeout: int = 30) -> bool:
        """Check if server is healthy"""
        import requests
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    logger.info(f"Server at {url} is healthy")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            time.sleep(1)
        
        logger.error(f"Server at {url} failed health check")
        return False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.shutdown()
        sys.exit(0)
    
    def shutdown(self):
        """Shutdown all processes"""
        logger.info("Shutting down application...")
        self.running = False
        
        for process in self.processes:
            if process and process.poll() is None:
                logger.info(f"Terminating process {process.pid}")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing process {process.pid}")
                    process.kill()
        
        logger.info("Application shutdown completed")
    
    def run_full_stack(self, ui: bool = True, wait: bool = True):
        """Run the full application stack"""
        logger.info("Starting Agentic Mapping AI Platform")
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start API server
        api_process = self.start_api_server(background=True)
        if not api_process:
            logger.error("Failed to start API server")
            return False
        
        # Check API health
        api_url = f"http://{settings.api.host}:{settings.api.port}"
        if not self.check_server_health(api_url):
            logger.error("API server health check failed")
            self.shutdown()
            return False
        
        # Start UI if requested
        ui_process = None
        if ui:
            ui_process = self.start_ui(background=True)
            if ui_process:
                ui_url = f"http://{settings.ui.streamlit_host}:{settings.ui.streamlit_port}"
                if self.check_server_health(ui_url):
                    logger.info(f"UI available at: {ui_url}")
                else:
                    logger.warning("UI server health check failed, but continuing...")
        
        # Print access information
        self.print_access_info()
        
        # Keep running if requested
        if wait:
            self.running = True
            try:
                while self.running:
                    time.sleep(1)
                    
                    # Check if processes are still running
                    for process in self.processes[:]:  # Copy list to avoid modification during iteration
                        if process.poll() is not None:
                            logger.warning(f"Process {process.pid} has terminated")
                            self.processes.remove(process)
                    
                    if not self.processes:
                        logger.error("All processes have terminated")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
            finally:
                self.shutdown()
        
        return True
    
    def print_access_info(self):
        """Print application access information"""
        print("\n" + "="*60)
        print("🚀 AGENTIC MAPPING AI PLATFORM STARTED")
        print("="*60)
        print(f"📡 API Server: http://{settings.api.host}:{settings.api.port}")
        print(f"📖 API Documentation: http://{settings.api.host}:{settings.api.port}/docs")
        print(f"🌐 UI Dashboard: http://{settings.ui.streamlit_host}:{settings.ui.streamlit_port}")
        print(f"📊 Health Check: http://{settings.api.host}:{settings.api.port}/health")
        print("\n🔧 Available Endpoints:")
        print("  - POST /api/v1/validate - Validate documents")
        print("  - POST /api/v1/generate/code - Generate code")
        print("  - POST /api/v1/pipeline/full - Run full pipeline")
        print("  - GET  /api/v1/workflows - List workflows")
        print("  - POST /api/v1/knowledge/query - Query knowledge base")
        print("\n📝 To stop the application, press Ctrl+C")
        print("="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Agentic Mapping AI Application Runner")
    parser.add_argument("--api-only", action="store_true", help="Run API server only")
    parser.add_argument("--ui-only", action="store_true", help="Run UI only")
    parser.add_argument("--no-wait", action="store_true", help="Don't wait after starting")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies only")
    
    args = parser.parse_args()
    
    runner = ApplicationRunner()
    
    # Check dependencies
    if args.check_deps:
        if runner.check_dependencies():
            print("✅ All dependencies are installed")
            return 0
        else:
            print("❌ Missing dependencies")
            return 1
    
    # Check dependencies before starting
    if not runner.check_dependencies():
        return 1
    
    # Setup environment
    runner.setup_environment()
    
    try:
        if args.api_only:
            # Run API server only
            logger.info("Starting API server only")
            runner.start_api_server(background=False)
            
        elif args.ui_only:
            # Run UI only
            logger.info("Starting UI only")
            runner.start_ui(background=False)
            
        else:
            # Run full stack
            success = runner.run_full_stack(
                ui=True,
                wait=not args.no_wait
            )
            
            if not success:
                return 1
    
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())