#!/usr/bin/env python3
"""
Run Excel Converter with Different JSON Files
"""

import sys
import os
from aa_ultimate_excel_converter import AAUltimateExcelConverter

def main():
    """Run the Excel converter with specified JSON file"""
    
    # Available JSON files
    json_files = {
        '1': 'aa_comprehensive_test_data.json',
        '2': 'aa_comprehensive_test_data_with_georef.json', 
        '3': 'aa_comprehensive_test_data_with_georef_enhanced.json'
    }
    
    print("🚀 AA Ultimate Excel Converter")
    print("=" * 40)
    print("Available JSON files:")
    for key, filename in json_files.items():
        if os.path.exists(filename):
            print(f"  {key}. {filename} ✅")
        else:
            print(f"  {key}. {filename} ❌ (not found)")
    
    # Get user choice
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice not in json_files:
        print("❌ Invalid choice!")
        return
    
    json_file = json_files[choice]
    
    if not os.path.exists(json_file):
        print(f"❌ File {json_file} not found!")
        return
    
    print(f"\n🔄 Converting {json_file} to Excel...")
    
    # Create converter and run
    converter = AAUltimateExcelConverter(json_file)
    converter.convert_to_excel()
    
    print(f"\n✅ Conversion completed!")
    print(f"📁 Output file: AA_Ultimate_Test_Data.xlsx")

if __name__ == "__main__":
    main()
