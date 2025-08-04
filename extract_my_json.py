#!/usr/bin/env python3
"""
Extract My JSON - Simple Field Extractor

Just change the file path below and run the script!
"""

from json_field_extractor import quick_extract, extract_fields_from_json

# 🎯 PUT YOUR JSON FILE PATH HERE:
JSON_FILE_PATH = "your_file.json"  # ← Change this to your actual file path

def find_dictionary_name_simple(field_info, original_json_data, db_name):
    """
    Extract DB name from the dictionary.providedKey field
    Expected format: "PBWM.GCB_AAC_NAM.gcgservnapsd_genesis_bcd_t_db"
    Returns the last part: "gcgservnapsd_genesis_bcd_t_db"
    
    CONSTRAINT: Only extracts names ending with '_db'
    """
    
    # Method 1: Look for "dictionary" object with "providedKey"
    if original_json_data and isinstance(original_json_data, dict):
        if 'dictionary' in original_json_data:
            dictionary_obj = original_json_data['dictionary']
            if isinstance(dictionary_obj, dict) and 'providedKey' in dictionary_obj:
                provided_key = dictionary_obj['providedKey']
                print(f"🔍 Found providedKey in dictionary: {provided_key}")
                
                # Extract the last part after splitting by dots
                if provided_key and isinstance(provided_key, str):
                    parts = provided_key.split('.')
                    if len(parts) >= 1:
                        db_name_extracted = parts[-1]  # Get the last part
                        print(f"🔍 Extracted potential DB name: {db_name_extracted}")
                        
                        # Only use if it ends with '_db'
                        if db_name_extracted.endswith('_db'):
                            print(f"✅ DB name ends with '_db': {db_name_extracted}")
                            return db_name_extracted
                        else:
                            print(f"❌ DB name doesn't end with '_db', skipping: {db_name_extracted}")
    
    # Method 2: Search recursively for any "providedKey" field
    def search_for_provided_key(obj, path="root"):
        if isinstance(obj, dict):
            # Check if current dictionary has 'providedKey' key
            if 'providedKey' in obj:
                provided_key = obj['providedKey']
                print(f"🔍 Found providedKey at {path}: {provided_key}")
                
                # Extract the last part after splitting by dots
                if provided_key and isinstance(provided_key, str):
                    parts = provided_key.split('.')
                    if len(parts) >= 1:
                        db_name_extracted = parts[-1]  # Get the last part
                        print(f"🔍 Extracted potential DB name from {path}: {db_name_extracted}")
                        
                        # Only use if it ends with '_db'
                        if db_name_extracted.endswith('_db'):
                            print(f"✅ DB name ends with '_db': {db_name_extracted}")
                            return db_name_extracted
                        else:
                            print(f"❌ DB name doesn't end with '_db', skipping: {db_name_extracted}")
            
            # Search in all values of current dictionary
            for key, value in obj.items():
                result = search_for_provided_key(value, f"{path}.{key}")
                if result:
                    return result
                    
        elif isinstance(obj, list):
            # Search in all items of the list
            for i, item in enumerate(obj):
                result = search_for_provided_key(item, f"{path}[{i}]")
                if result:
                    return result
        
        return None
    
    # Search in the entire original JSON data
    if original_json_data:
        found_name = search_for_provided_key(original_json_data)
        if found_name:
            return found_name
    
    # Fallback: use database name from extraction
    return db_name

def print_tabular_results(results, original_json_data=None):
    """
    Display results in tabular format: DB_name | table_name | column_name | data_type | description
    """
    print(f"\n📋 EXTRACTED FIELDS - TABULAR VIEW")
    print("=" * 120)
    
    # Create table data
    table_data = []
    for db_name, tables in results.items():
        for table_name, fields in tables.items():
            for field_name, field_info in fields.items():
                # Search for dictionary_name at different levels
                dict_name = find_dictionary_name_simple(field_info, original_json_data, db_name)
                
                row = {
                    'DB_name': dict_name,  # Use found dictionary_name or fallback
                    'table_name': table_name, 
                    'column_name': field_info.get('physicalName', field_name),  # Use physicalName from DB
                    'data_type': field_info.get('dataType', 'Unknown'),
                    'description': field_info.get('description', 'No description')[:80] + ('...' if len(field_info.get('description', '')) > 80 else '')
                }
                table_data.append(row)
    
    if not table_data:
        print("No field definitions found!")
        return
    
    # Calculate column widths
    col_widths = {
        'DB_name': max(len('DB_name'), max(len(row['DB_name']) for row in table_data)),
        'table_name': max(len('table_name'), max(len(row['table_name']) for row in table_data)),
        'column_name': max(len('column_name'), max(len(row['column_name']) for row in table_data)),
        'data_type': max(len('data_type'), max(len(row['data_type']) for row in table_data)),
        'description': min(80, max(len('description'), max(len(row['description']) for row in table_data)))
    }
    
    # Print header
    header = f"{'DB_name':<{col_widths['DB_name']}} | {'table_name':<{col_widths['table_name']}} | {'column_name':<{col_widths['column_name']}} | {'data_type':<{col_widths['data_type']}} | {'description':<{col_widths['description']}}"
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in table_data:
        row_str = f"{row['DB_name']:<{col_widths['DB_name']}} | {row['table_name']:<{col_widths['table_name']}} | {row['column_name']:<{col_widths['column_name']}} | {row['data_type']:<{col_widths['data_type']}} | {row['description']:<{col_widths['description']}}"
        print(row_str)
    
    print("-" * len(header))
    print(f"Total: {len(table_data)} fields")

def main():
    print("🎯 Extracting Fields from Your JSON")
    print("=" * 50)
    
    try:
        print(f"📂 Processing: {JSON_FILE_PATH}")
        
        # Load original JSON data to search for dictionary_name
        import json
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            original_json_data = json.load(f)
        
        # Extract all fields
        results = quick_extract(JSON_FILE_PATH)
        
        # Count total fields
        total_fields = 0
        for db_name, db_data in results.items():
            for table_name, table_data in db_data.items():
                total_fields += len(table_data)
        
        print(f"\n✅ SUCCESS!")
        print(f"📊 Found {total_fields} fields in {len(results)} databases")
        
        # Display results in tabular format
        print_tabular_results(results, original_json_data)
        
        # Auto-save the results
        print(f"\n💾 Saving results...")
        extract_fields_from_json(
            json_file_path=JSON_FILE_PATH,
            output_dir="./my_extracted_fields",
            formats=['json', 'csv']
        )
        
        print(f"\n🎉 DONE! Check './my_extracted_fields' folder for saved results.")
        
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file: {JSON_FILE_PATH}")
        print(f"💡 Make sure to update JSON_FILE_PATH on line 11 with your actual file path")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main() 