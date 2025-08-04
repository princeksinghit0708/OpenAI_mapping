#!/usr/bin/env python3
"""
Simple JSON Field Extractor - With Hardcoded File Path

This version allows you to directly specify the JSON file path in the code
instead of using command line arguments.
"""

from json_field_extractor import quick_extract, extract_fields_from_json

def main():
    """
    Extract fields with hardcoded file path
    """
    
    # 🎯 CHANGE THIS LINE TO YOUR JSON FILE PATH:
    json_file = "your_data_file.json"  # <-- Put your file path here
    
    # Uncomment one of these examples:
    # json_file = "my_schema.json"
    # json_file = "/full/path/to/your/data.json"  
    # json_file = "../data/schema.json"
    # json_file = "C:\\Users\\YourName\\Documents\\data.json"  # Windows
    
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
        
        # Show the structure
        for db_name, tables in results.items():
            print(f"  📊 {db_name}: {len(tables)} tables")
            for table_name, fields in tables.items():
                print(f"    📋 {table_name}: {len(fields)} fields")
        
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
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file}")
        print("💡 Make sure to update the 'json_file' variable with your actual file path")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure your JSON file contains field definitions with this structure:")
        print_expected_structure()

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