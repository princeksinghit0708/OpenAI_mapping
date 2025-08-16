#!/usr/bin/env python3
"""
📊 Excel File Setup Helper
Helps you configure your Excel file for the demo
"""

import os
import sys
from pathlib import Path
import pandas as pd

def main():
    print("📊 Excel File Setup Helper")
    print("=" * 50)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Look for Excel files
    excel_files = list(current_dir.glob("*.xlsx"))
    
    if not excel_files:
        print("\n❌ No Excel files found in the current directory!")
        print("\n🔧 To fix this:")
        print("1. Copy your Excel file to this directory:")
        print(f"   {current_dir}")
        print("2. Make sure the filename is: ebs_IM_account_DATAhub_mapping_v8.0.xlsx")
        print("   (or update the configuration to match your filename)")
        
        # Ask user for their Excel file location
        print("\n💡 Do you have an Excel file somewhere else?")
        user_path = input("Enter full path to your Excel file (or press Enter to skip): ").strip()
        
        if user_path and Path(user_path).exists():
            try:
                # Copy the file
                source = Path(user_path)
                target = current_dir / "ebs_IM_account_DATAhub_mapping_v8.0.xlsx"
                
                print(f"📋 Copying {source.name} to {target.name}...")
                import shutil
                shutil.copy2(source, target)
                print(f"✅ File copied successfully!")
                
                # Verify sheets
                verify_excel_sheets(target)
                
            except Exception as e:
                print(f"❌ Error copying file: {e}")
        else:
            print("\n📝 Please manually copy your Excel file to:")
            print(f"   {current_dir / 'ebs_IM_account_DATAhub_mapping_v8.0.xlsx'}")
            
    else:
        print(f"\n✅ Found {len(excel_files)} Excel file(s):")
        for excel_file in excel_files:
            print(f"   📄 {excel_file.name}")
            
        # Check if we have the expected filename
        expected_name = "ebs_IM_account_DATAhub_mapping_v8.0.xlsx"
        if not any(f.name == expected_name for f in excel_files):
            print(f"\n⚠️  Expected filename: {expected_name}")
            print("📝 Options:")
            print("1. Rename your file to match the expected name")
            print("2. Update the configuration in enhanced_main.py")
            
            # Offer to rename
            if len(excel_files) == 1:
                current_file = excel_files[0]
                rename = input(f"\nRename '{current_file.name}' to '{expected_name}'? (y/n): ").strip().lower()
                if rename == 'y':
                    try:
                        new_path = current_dir / expected_name
                        current_file.rename(new_path)
                        print(f"✅ Renamed to {expected_name}")
                        verify_excel_sheets(new_path)
                    except Exception as e:
                        print(f"❌ Error renaming: {e}")
        else:
            # File exists with correct name, verify sheets
            correct_file = next(f for f in excel_files if f.name == expected_name)
            verify_excel_sheets(correct_file)

def verify_excel_sheets(excel_path):
    """Verify that the Excel file has the required sheets"""
    try:
        print(f"\n🔍 Checking sheets in {excel_path.name}...")
        
        # Read Excel file info
        excel_file = pd.ExcelFile(excel_path)
        sheets = excel_file.sheet_names
        
        print(f"📋 Found {len(sheets)} sheets:")
        for i, sheet in enumerate(sheets, 1):
            print(f"   {i}. {sheet}")
        
        # Check for required sheets
        required_sheets = ["datahub standard mapping", "goldref"]
        found_sheets = {}
        
        for required in required_sheets:
            # Try exact match first
            if required in sheets:
                found_sheets[required] = required
                print(f"✅ Found required sheet: '{required}'")
            else:
                # Try fuzzy matching
                matches = [s for s in sheets if required.lower() in s.lower() or 
                          any(word in s.lower() for word in required.split())]
                if matches:
                    found_sheets[required] = matches[0]
                    print(f"🔍 Found similar sheet for '{required}': '{matches[0]}'")
                else:
                    print(f"❌ Missing required sheet: '{required}'")
        
        if len(found_sheets) == len(required_sheets):
            print(f"\n✅ Excel file is properly configured!")
            
            # Show sample data
            for required, actual in found_sheets.items():
                try:
                    df = pd.read_excel(excel_path, sheet_name=actual, nrows=3)
                    print(f"\n📊 Sample from '{actual}' sheet:")
                    print(f"   Columns: {list(df.columns)[:5]}...")  # Show first 5 columns
                    print(f"   Rows: {len(df)} (showing first 3)")
                except Exception as e:
                    print(f"⚠️  Could not read sheet '{actual}': {e}")
        else:
            print(f"\n⚠️  Excel file needs the following sheets:")
            for required in required_sheets:
                print(f"   - '{required}'")
            
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")

if __name__ == "__main__":
    main()
