#!/usr/bin/env python3
"""
Windows-specific fix for SQLAlchemy metadata conflicts
Addresses the exact error: Attribute name 'metadata' is reserved when using the Declarative API
"""

import os
import sys
import re
from pathlib import Path

def clear_python_cache():
    """Clear Python cache files"""
    print("🧹 Clearing Python cache files...")
    
    cache_dirs = []
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs[:]:
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                cache_dirs.append(cache_path)
                try:
                    import shutil
                    shutil.rmtree(cache_path)
                    print(f"   Removed: {cache_path}")
                    dirs.remove(dir_name)
                except Exception as e:
                    print(f"   Warning: Could not remove {cache_path}: {e}")
    
    # Remove .pyc files
    pyc_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                pyc_files.append(pyc_path)
                try:
                    os.remove(pyc_path)
                    print(f"   Removed: {pyc_path}")
                except Exception as e:
                    print(f"   Warning: Could not remove {pyc_path}: {e}")
    
    print(f"   ✅ Cleared {len(cache_dirs)} cache directories and {len(pyc_files)} .pyc files")

def fix_models_file(file_path):
    """Fix a specific models.py file"""
    print(f"🔧 Fixing: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"   ❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Fix SQLAlchemy column names
    fixes = [
        # SQLAlchemy columns
        (r'doc_metadata\s*=\s*Column\(JSON\)', 'document_metadata = Column(JSON)'),
        (r'artifact_metadata\s*=\s*Column\(JSON\)', 'artifact_info = Column(JSON)'),
        (r'metadata\s*=\s*Column\(JSON\)', 'metadata_info = Column(JSON)'),
        
        # Pydantic fields (rename to avoid confusion)
        (r'metadata:\s*Optional\[Dict\[str,\s*Any\]\]\s*=\s*None', 'model_metadata: Optional[Dict[str, Any]] = None'),
        (r'metadata:\s*Dict\[str,\s*Any\]\s*=\s*\{\}', 'model_metadata: Dict[str, Any] = {}'),
    ]
    
    for pattern, replacement in fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes.append(f"Fixed: {pattern} → {replacement}")
    
    if content != original_content:
        # Create backup
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"   📁 Backup created: {backup_path}")
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Made {len(changes)} changes:")
        for change in changes:
            print(f"      • {change}")
        return True
    else:
        print(f"   ✅ No changes needed")
        return False

def test_import():
    """Test if the models can be imported"""
    print("🧪 Testing SQLAlchemy import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Test import
        from agentic_mapping_ai.core.models import Document, MappingProject
        print("   ✅ Successfully imported SQLAlchemy models!")
        print(f"   📊 Document table: {Document.__tablename__}")
        print(f"   📊 Document columns: {[col.name for col in Document.__table__.columns]}")
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 Windows SQLAlchemy Metadata Conflict Fix")
    print("=" * 60)
    
    # Step 1: Clear cache
    clear_python_cache()
    print()
    
    # Step 2: Fix model files
    model_files = [
        'agentic_mapping_ai/core/models.py',
        'demo/agentic_mapping_ai/core/models.py',
        'agentic_mapping_ai/running_demo_folder/core/models.py',
    ]
    
    fixed_files = []
    for file_path in model_files:
        if fix_models_file(file_path):
            fixed_files.append(file_path)
        print()
    
    # Step 3: Test import
    success = test_import()
    print()
    
    if success:
        print("🎉 Fix completed successfully!")
        print("You can now run your application without SQLAlchemy metadata conflicts.")
    else:
        print("❌ Fix incomplete. Please check the errors above.")
        print("\nAdditional troubleshooting steps:")
        print("1. Restart your Python environment")
        print("2. Check if you're in the correct directory")
        print("3. Verify all files were updated correctly")
        print("4. Try running: python -c \"import agentic_mapping_ai.core.models\"")

if __name__ == "__main__":
    main()
