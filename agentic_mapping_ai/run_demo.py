#!/usr/bin/env python3
"""
🚀 Simple Launcher for End-to-End Agentic Mapping AI Demo
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from end_to_end_demo import main

if __name__ == "__main__":
    print("🎯 Launching End-to-End Agentic Mapping AI Demo...")
    print("="*60)
    
    try:
        # Run the demo
        success = asyncio.run(main())
        
        if success:
            print("\n🎉 Demo completed successfully!")
            print("📁 Check the 'demo_output' directory for all generated files")
        else:
            print("\n❌ Demo encountered errors")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Demo failed with error: {str(e)}")
        sys.exit(1)
