#!/usr/bin/env python3
"""
Windows-specific fix for SQLAlchemy metadata conflict
This script will:
1. Clear Python cache files
2. Check for metadata conflicts
3. Apply fixes if needed
4. Verify the fix
"""

import os
import sys
import shutil
import glob
from pathlib import Path

def clear_python_cache():
    """Clear Python cache files that might be causing import issues"""
    print("🧹 Clearing Python cache files...")
    
    # Find and remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs[:]:  # Create a copy to safely modify during iteration
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                print(f"   Removing: {cache_path}")
                try:
                    shutil.rmtree(cache_path)
                    dirs.remove(dir_name)  # Remove from dirs list to avoid walking into it
                except Exception as e:
                    print(f"   Warning: Could not remove {cache_path}: {e}")
    
    # Remove .pyc files
    pyc_files = glob.glob('**/*.pyc', recursive=True)
    for pyc_file in pyc_files:
        try:
            os.remove(pyc_file)
            print(f"   Removed: {pyc_file}")
        except Exception as e:
            print(f"   Warning: Could not remove {pyc_file}: {e}")
    
    print("   ✅ Python cache cleared")

def check_metadata_conflicts():
    """Check for metadata attribute conflicts in model files"""
    print("🔍 Checking for metadata conflicts...")
    
    model_files = [
        'agentic_mapping_ai/core/models.py',
        'demo/agentic_mapping_ai/core/models.py',
        'agentic_mapping_ai/running_demo_folder/core/models.py'
    ]
    
    conflicts_found = []
    
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"   Checking: {model_file}")
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Check for problematic metadata patterns in Pydantic models
                    if ('metadata: Optional[Dict' in line or 
                        'metadata: Dict' in line or
                        'metadata = Column' in line):
                        conflicts_found.append({
                            'file': model_file,
                            'line': i,
                            'content': line.strip()
                        })
        else:
            print(f"   File not found: {model_file}")
    
    if conflicts_found:
        print("   ❌ Metadata conflicts found:")
        for conflict in conflicts_found:
            print(f"      {conflict['file']}:{conflict['line']} - {conflict['content']}")
        return conflicts_found
    else:
        print("   ✅ No metadata conflicts found")
        return []

def fix_metadata_conflicts(conflicts):
    """Fix metadata conflicts by renaming attributes"""
    print("🔧 Fixing metadata conflicts...")
    
    fixes = {
        'metadata: Optional[Dict[str, Any]] = None  # SchemaDefinition': 'schema_metadata: Optional[Dict[str, Any]] = None',
        'metadata: Optional[Dict[str, Any]] = None  # ValidationResult': 'validation_metadata: Optional[Dict[str, Any]] = None',
        'metadata: Dict[str, Any] = {}  # ExcelMappingProject': 'project_metadata: Dict[str, Any] = {}',
        'metadata: Optional[Dict[str, Any]] = None  # ChatMessage': 'message_metadata: Optional[Dict[str, Any]] = None'
    }
    
    files_to_fix = set(conflict['file'] for conflict in conflicts)
    
    for file_path in files_to_fix:
        print(f"   Fixing: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply specific fixes based on context
        replacements = [
            # SchemaDefinition
            ('metadata: Optional[Dict[str, Any]] = None\n    version: str = "1.0"', 
             'schema_metadata: Optional[Dict[str, Any]] = None\n    version: str = "1.0"'),
            
            # ValidationResult  
            ('suggestions: List[str] = []\n    metadata: Optional[Dict[str, Any]] = None',
             'suggestions: List[str] = []\n    validation_metadata: Optional[Dict[str, Any]] = None'),
            
            # ExcelMappingProject
            ('validation_results: Optional[ValidationResult] = None\n    metadata: Dict[str, Any] = {}',
             'validation_results: Optional[ValidationResult] = None\n    project_metadata: Dict[str, Any] = {}'),
            
            # ChatMessage
            ('timestamp: datetime = PydanticField(default_factory=datetime.utcnow)\n    metadata: Optional[Dict[str, Any]] = None',
             'timestamp: datetime = PydanticField(default_factory=datetime.utcnow)\n    message_metadata: Optional[Dict[str, Any]] = None'),
        ]
        
        original_content = content
        for old_pattern, new_pattern in replacements:
            content = content.replace(old_pattern, new_pattern)
        
        if content != original_content:
            # Backup original file
            backup_path = f"{file_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"      Created backup: {backup_path}")
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"      ✅ Fixed: {file_path}")
        else:
            print(f"      No changes needed: {file_path}")

def verify_fix():
    """Verify that the fix worked by testing imports"""
    print("✅ Verifying fix...")
    
    try:
        # Test SQLAlchemy imports
        from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
        from sqlalchemy.ext.declarative import declarative_base
        print("   ✅ SQLAlchemy imports successful")
        
        # Test creating declarative base
        Base = declarative_base()
        print("   ✅ Declarative base created")
        
        # Test importing models
        sys.path.insert(0, '.')
        from agentic_mapping_ai.core.models import Document, MappingProject
        print("   ✅ Core models imported successfully")
        
        # Test model creation
        print(f"   Document columns: {[col.name for col in Document.__table__.columns]}")
        print("   ✅ Models working correctly")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main fix function"""
    print("🔧 Windows SQLAlchemy Metadata Conflict Fix")
    print("=" * 50)
    
    # Step 1: Clear cache
    clear_python_cache()
    print()
    
    # Step 2: Check for conflicts
    conflicts = check_metadata_conflicts()
    print()
    
    # Step 3: Fix conflicts if found
    if conflicts:
        fix_metadata_conflicts(conflicts)
        print()
    
    # Step 4: Verify fix
    success = verify_fix()
    print()
    
    if success:
        print("🎉 Fix completed successfully!")
        print("You can now run the chatbased demo app:")
        print("   cd chatbased_demo_app")
        print("   python main.py")
    else:
        print("❌ Fix failed. Please check the errors above.")
        print("You may need to:")
        print("   1. Restart your Python environment")
        print("   2. Check for any remaining import conflicts")
        print("   3. Ensure all dependencies are properly installed")

if __name__ == "__main__":
    main()
