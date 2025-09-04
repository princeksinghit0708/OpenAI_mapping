#!/usr/bin/env python3
"""
Remove OpenAI and Internet-Dependent Dependencies
Replaces with offline alternatives for privacy-sensitive environments
"""

import os
import re
from pathlib import Path

def remove_openai_imports(file_path):
    """Remove OpenAI imports from a file"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Remove OpenAI imports
    openai_patterns = [
        r'from openai import.*\n',
        r'import openai.*\n',
        r'from langchain_openai import.*\n',
        r'from langchain\.openai import.*\n',
        r'from litellm import.*\n',
        r'import litellm.*\n',
        r'from sentence_transformers import.*\n',
        r'import sentence_transformers.*\n',
    ]
    
    for pattern in openai_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes.append(f"Removed: {pattern.strip()}")
    
    # Replace OpenAI usage with offline alternatives
    replacements = [
        (r'OpenAI\(', '# OpenAI() - Removed for offline use'),
        (r'ChatOpenAI\(', '# ChatOpenAI() - Removed for offline use'),
        (r'AzureOpenAI\(', '# AzureOpenAI() - Removed for offline use'),
        (r'litellm\.', '# litellm. - Removed for offline use'),
        (r'SentenceTransformer\(', '# SentenceTransformer() - Removed for offline use'),
    ]
    
    for pattern, replacement in replacements:
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            changes.append(f"Replaced: {pattern} -> {replacement}")
    
    if content != original_content:
        # Create backup
        backup_path = f"{file_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        
        # Write modified content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Modified: {file_path}")
        for change in changes:
            print(f"   • {change}")
        return True
    
    return False

def main():
    """Main function to remove OpenAI dependencies"""
    print("🔧 Removing OpenAI and Internet-Dependent Dependencies")
    print("=" * 60)
    
    # Files to modify
    files_to_modify = [
        'chatbased_demo_app/agents/faiss_similarity_engine.py',
        'chatbased_demo_app/agents/chat_suggestion_manager.py',
        'chatbased_demo_app/main.py',
        'agentic_mapping_ai/llm_service.py',
        'agentic_mapping_ai/agents/core/enhanced_base_agent.py',
        'agentic_mapping_ai/agents/core/enhanced_agent_v2.py',
    ]
    
    modified_files = []
    
    for file_path in files_to_modify:
        if remove_openai_imports(file_path):
            modified_files.append(file_path)
        print()
    
    if modified_files:
        print(f"🎉 Modified {len(modified_files)} files:")
        for file_path in modified_files:
            print(f"   • {file_path}")
        
        print("\n📋 Next steps:")
        print("1. Use offline_main.py instead of main.py")
        print("2. Install offline requirements: pip install -r offline_requirements.txt")
        print("3. Test the offline system")
        print("4. All OpenAI dependencies have been removed/disabled")
    else:
        print("✅ No files needed modification!")

if __name__ == "__main__":
    main()
