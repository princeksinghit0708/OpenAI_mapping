#!/usr/bin/env python3
"""
Simple JSON Field Extractor - Just provide the file path!

This script demonstrates the simplest possible way to extract database field 
definitions from a JSON file - just provide the file path and everything else 
is handled automatically.
"""

import sys
from json_field_extractor import quick_extract, extract_fields_from_json

def main():
    """
    Ultra-simple extraction examples
    """
    
    # Check if file path provided
    if len(sys.argv) < 2:
        print("📋 Simple JSON Field Extractor")
        print("=" * 40)
        print("Usage: python simple_extract.py <json_file_path>")
        print("\nExamples:")
        print("  python simple_extract.py my_schema.json")
        print("  python simple_extract.py /path/to/data.json")
        print("\n🚀 Or use these simple functions in your code:")
        print_code_examples()
        return
    
    json_file = sys.argv[1]
    
    print("🎯 Simple JSON Field Extractor")
    print("=" * 50)
    print(f"📂 Processing: {json_file}")
    
    try:
        # Method 1: Ultra-simple - just extract everything
        print("\n🚀 Method 1: Quick Extract (no files saved)")
        print("-" * 30)
        results = quick_extract(json_file)
        
        # Show basic stats
        total_fields = 0
        for db_name, db_data in results.items():
            for table_name, table_data in db_data.items():
                total_fields += len(table_data)
        
        print(f"✅ Success! Found {total_fields} fields")
        print(f"📊 Databases: {list(results.keys())}")
        
        # Method 2: Extract with auto-save
        print("\n🚀 Method 2: Extract with Auto-Save")
        print("-" * 30)
        extract_fields_from_json(
            json_file_path=json_file,
            output_dir="./extracted_results",
            formats=['json', 'csv']
        )
        
        print("\n✨ That's it! Your field definitions have been extracted.")
        print("📁 Check the './extracted_results' folder for the output files.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your JSON file contains field definitions with this structure:")
        print_expected_structure()

def print_code_examples():
    """Print code usage examples"""
    print("""
# In your Python code:

# 1. Ultra-simple - one line extraction
from json_field_extractor import quick_extract
results = quick_extract("my_schema.json")

# 2. Simple with options
from json_field_extractor import extract_fields_from_json
fields = extract_fields_from_json(
    json_file_path="my_schema.json",
    database_name="finance_db",    # Optional: filter by database
    formats=['json', 'csv'],       # Save in multiple formats
    detailed=True                  # Show detailed output
)

# 3. Access the extracted data
for database, tables in results.items():
    print(f"Database: {database}")
    for table, fields in tables.items():
        print(f"  Table: {table} ({len(fields)} fields)")
        for field_name, field_info in fields.items():
            print(f"    - {field_name}: {field_info['dataType']}")
""")

def print_expected_structure():
    """Print expected JSON field structure"""
    print("""
{
  "field_name": {
    "providedKey": "database.table.field",
    "displayName": "field_name",
    "physicalName": "field_name",
    "dataType": "Character|Integer|Decimal|Date",
    "isNullable": true|false,
    "format": "varchar(50)|int|decimal(15,2)",
    "description": "Field description text"
  }
}
""")

if __name__ == "__main__":
    main() 