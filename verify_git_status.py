#!/usr/bin/env python3
"""
🔍 VERIFY GIT STATUS - Check running_demo_folder in git
"""

import subprocess
import os

def run_command(cmd):
    """Run a command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    """Main verification function"""
    print("🔍 VERIFYING GIT STATUS OF running_demo_folder")
    print("=" * 60)
    
    # Check current directory
    current_dir = run_command("pwd")
    print(f"📍 Current Directory: {current_dir}")
    
    # Check git status
    git_status = run_command("git status --porcelain")
    print(f"\n📊 Git Status (porcelain):")
    if git_status:
        print(git_status)
    else:
        print("✅ Working directory clean")
    
    # Check if running_demo_folder exists
    folder_exists = os.path.exists("running_demo_folder")
    print(f"\n📁 running_demo_folder exists: {'✅ YES' if folder_exists else '❌ NO'}")
    
    # Count files in running_demo_folder
    if folder_exists:
        file_count = run_command("find running_demo_folder/ -type f | wc -l")
        print(f"📊 Total files in running_demo_folder: {file_count}")
    
    # Check git tracked files
    tracked_files = run_command("git ls-files | grep running_demo_folder | wc -l")
    print(f"📊 Git tracked files in running_demo_folder: {tracked_files}")
    
    # Show some tracked files
    print(f"\n📋 Sample tracked files:")
    sample_files = run_command("git ls-files | grep running_demo_folder | head -5")
    if sample_files:
        for file in sample_files.split('\n'):
            print(f"   • {file}")
    
    # Check last commit
    last_commit = run_command("git log --oneline -1")
    print(f"\n📝 Last Commit: {last_commit}")
    
    # Check remote status
    remote_status = run_command("git status -uno")
    print(f"\n🌐 Remote Status:")
    print(remote_status)
    
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION COMPLETE!")

if __name__ == "__main__":
    main()
