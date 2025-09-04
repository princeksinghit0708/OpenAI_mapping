#!/usr/bin/env python3
"""
Comprehensive fix for all SQLAlchemy metadata conflicts
This script will fix all metadata conflicts across all model files
"""

import os
import re
from pathlib import Path

def fix_metadata_conflicts_in_file(file_path):
    """Fix metadata conflicts in a specific file"""
    print(f"🔧 Checking: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"   ❌ File not found: {file_path}")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    # Fix SQLAlchemy column names that contain 'metadata'
    sqlalchemy_fixes = [
        (r'doc_metadata\s*=\s*Column', 'document_metadata = Column'),
        (r'artifact_metadata\s*=\s*Column', 'artifact_info = Column'),
        (r'metadata\s*=\s*Column', 'metadata_info = Column'),
    ]
    
    for pattern, replacement in sqlalchemy_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made.append(f"Fixed SQLAlchemy column: {pattern} → {replacement}")
    
    # Fix Pydantic model fields that use 'metadata' (should be renamed to avoid confusion)
    pydantic_fixes = [
        (r'metadata:\s*Optional\[Dict\[str,\s*Any\]\]\s*=\s*None', 'model_metadata: Optional[Dict[str, Any]] = None'),
        (r'metadata:\s*Dict\[str,\s*Any\]\s*=\s*\{\}', 'model_metadata: Dict[str, Any] = {}'),
    ]
    
    for pattern, replacement in pydantic_fixes:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes_made.append(f"Fixed Pydantic field: {pattern} → {replacement}")
    
    if content != original_content:
        # Create backup
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"   📁 Created backup: {backup_path}")
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Fixed {len(changes_made)} issues:")
        for change in changes_made:
            print(f"      • {change}")
        return True
    else:
        print(f"   ✅ No metadata conflicts found")
        return False

def main():
    """Main function to fix all metadata conflicts"""
    print("🔧 Comprehensive SQLAlchemy Metadata Conflict Fix")
    print("=" * 60)
    
    # Files to check and fix
    files_to_fix = [
        'agentic_mapping_ai/core/models.py',
        'demo/agentic_mapping_ai/core/models.py',
        'agentic_mapping_ai/running_demo_folder/core/models.py',
    ]
    
    fixed_files = []
    
    for file_path in files_to_fix:
        if fix_metadata_conflicts_in_file(file_path):
            fixed_files.append(file_path)
        print()
    
    if fixed_files:
        print(f"🎉 Fixed {len(fixed_files)} files:")
        for file_path in fixed_files:
            print(f"   • {file_path}")
        
        print("\n📋 Next steps:")
        print("1. Test the imports:")
        print("   python -c \"from agentic_mapping_ai.core.models import Document; print('Success!')\"")
        print("2. Run your application")
        print("3. If issues persist, restart your Python environment")
    else:
        print("✅ No metadata conflicts found in any files!")
        print("The issue might be:")
        print("• Python cache files (try deleting __pycache__ folders)")
        print("• Different file versions")
        print("• Import path issues")

if __name__ == "__main__":
    main()
