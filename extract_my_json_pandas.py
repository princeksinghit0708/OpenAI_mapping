#!/usr/bin/env python3
"""
Extract My JSON - Enhanced Tabular Output with Pandas

Just change the file path below and run the script!
Beautiful tabular output with: DB_name | table_name | column_name | data_type | description
"""

from json_field_extractor import quick_extract, extract_fields_from_json

# 🎯 PUT YOUR JSON FILE PATH HERE:
JSON_FILE_PATH = "your_file.json"  # ← Change this to your actual file path

def find_dictionary_name(field_info, table_data, db_data, original_json_data):
    """
    Extract DB name from the dictionary.providedKey field
    Expected format: "PBWM.GCB_AAC_NAM.gcgservnapsd_genesis_bcd_t_db"
    Returns the last part: "gcgservnapsd_genesis_bcd_t_db"
    
    Improved logic: First check field_info for providedKey, then search globally
    """
    
    # Method 1: Check if the current field_info already has a providedKey
    if field_info and isinstance(field_info, dict) and 'providedKey' in field_info:
        provided_key = field_info['providedKey']
        print(f"🔍 Found providedKey in field_info: {provided_key}")
        
        if provided_key and isinstance(provided_key, str):
            parts = provided_key.split('.')
            if len(parts) >= 1:
                db_name = parts[-1]  # Get the last part
                print(f"🔍 Extracted DB name from field: {db_name}")
                
                if db_name.strip():  # Just ensure it's not empty
                    print(f"✅ Using DB name from field: {db_name}")
                    return db_name
    
    # Method 2: Look for "dictionary" object with "providedKey" in root
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
                        db_name = parts[-1]  # Get the last part
                        print(f"🔍 Extracted DB name from dictionary: {db_name}")
                        
                        # Return the extracted name (removed the '_db' constraint)
                        if db_name.strip():  # Just ensure it's not empty
                            print(f"✅ Using DB name from dictionary: {db_name}")
                            return db_name
    
    # Method 3: Search recursively for any "providedKey" field
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
                        db_name = parts[-1]  # Get the last part
                        print(f"🔍 Extracted DB name from {path}: {db_name}")
                        
                        # Return the extracted name (removed the '_db' constraint)
                        if db_name.strip():  # Just ensure it's not empty
                            print(f"✅ Using DB name from {path}: {db_name}")
                            return db_name
            
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
    
    # Fallback: return None so we use db_name
    print("🔍 No providedKey found anywhere, using fallback db_name")
    return None

def create_results_dataframe(results, original_json_data=None):
    """
    Convert extraction results to pandas DataFrame with requested columns
    """
    try:
        import pandas as pd
    except ImportError:
        print("⚠️  pandas not installed. Install with: pip install pandas")
        return None
    
    # Create table data
    table_data = []
    for db_name, tables in results.items():
        for table_name, fields in tables.items():
            for field_name, field_info in fields.items():
                # Search for dictionary_name at different levels
                print(f"\n🔧 DEBUG: Processing field {field_name} in {db_name}.{table_name}")
                print(f"🔧 DEBUG: Original db_name from extractor: {db_name}")
                print(f"🔧 DEBUG: field_info keys: {list(field_info.keys()) if isinstance(field_info, dict) else 'Not a dict'}")
                
                dict_name = find_dictionary_name(
                    field_info, 
                    tables.get(table_name, {}), 
                    results.get(db_name, {}),
                    original_json_data
                )
                
                print(f"🔧 DEBUG: dict_name returned: {dict_name}")
                final_db_name = dict_name if dict_name else db_name
                print(f"🔧 DEBUG: Final DB_name will be: {final_db_name}")
                
                row = {
                    'DB_name': final_db_name,  # Use found dictionary_name or fallback
                    'table_name': table_name,
                    'column_name': field_info.get('physicalName', field_name),  # Use physicalName from DB
                    'data_type': field_info.get('dataType', 'Unknown'),
                    'description': field_info.get('description', 'No description')
                }
                table_data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(table_data)
    return df

def print_tabular_results_pandas(results, original_json_data=None):
    """
    Display results using pandas for beautiful tabular format
    """
    df = create_results_dataframe(results, original_json_data)
    
    if df is None:
        # Fallback to simple tabular format
        print_simple_tabular_results(results)
        return df
    
    if df.empty:
        print("No field definitions found!")
        return df
    
    print(f"\n📋 EXTRACTED FIELDS - TABULAR VIEW")
    print("=" * 120)
    
    # Configure pandas display options
    import pandas as pd
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 60)
    
    # Display the table
    print(df.to_string(index=False))
    
    print("-" * 120)
    print(f"Total: {len(df)} fields from {df['DB_name'].nunique()} databases")
    
    # Show summary by database
    print(f"\n📊 SUMMARY BY DATABASE:")
    summary = df.groupby('DB_name').agg({
        'table_name': 'nunique',
        'column_name': 'count'
    }).rename(columns={'table_name': 'tables', 'column_name': 'fields'})
    print(summary.to_string())
    
    return df

def print_simple_tabular_results(results):
    """
    Simple tabular format without pandas
    """
    print(f"\n📋 EXTRACTED FIELDS - TABULAR VIEW")
    print("=" * 140)
    
    # Create table data
    table_data = []
    for db_name, tables in results.items():
        for table_name, fields in tables.items():
            for field_name, field_info in fields.items():
                row = {
                    'DB_name': field_info.get('dictionary_name', db_name),  # Use dictionary_name from JSON
                    'table_name': table_name, 
                    'column_name': field_info.get('physicalName', field_name),  # Use physicalName from DB
                    'data_type': field_info.get('dataType', 'Unknown'),
                    'description': field_info.get('description', 'No description')[:70] + ('...' if len(field_info.get('description', '')) > 70 else '')
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
        'description': min(70, max(len('description'), max(len(row['description']) for row in table_data)))
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

def save_tabular_results(results, original_json_data=None, output_dir="./my_extracted_fields"):
    """
    Save results in the requested tabular format
    """
    df = create_results_dataframe(results, original_json_data)
    
    if df is not None and not df.empty:
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as CSV with exact columns requested
        csv_file = f"{output_dir}/extracted_fields_tabular.csv"
        df.to_csv(csv_file, index=False)
        print(f"📄 Saved tabular CSV: {csv_file}")
        
        # Save as Excel for better formatting
        try:
            excel_file = f"{output_dir}/extracted_fields_tabular.xlsx"
            df.to_excel(excel_file, index=False, sheet_name='Field_Definitions')
            print(f"📊 Saved Excel file: {excel_file}")
        except ImportError:
            print("⚠️  openpyxl not installed. Install with: pip install openpyxl (for Excel export)")

def main():
    print("🎯 Extracting Fields from Your JSON - Enhanced Tabular View")
    print("=" * 70)
    
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
        
        # Display results in beautiful tabular format
        df = print_tabular_results_pandas(results, original_json_data)
        
        # Save results in tabular format
        print(f"\n💾 Saving results...")
        save_tabular_results(results, original_json_data)
        
        # Also save using the original extractor (for JSON format)
        extract_fields_from_json(
            json_file_path=JSON_FILE_PATH,
            output_dir="./my_extracted_fields",
            formats=['json']  # We're handling CSV ourselves with better format
        )
        
        print(f"\n🎉 DONE! Check './my_extracted_fields' folder for saved results.")
        print(f"📋 Files saved:")
        print(f"  - extracted_fields_tabular.csv (Your requested format)")
        print(f"  - extracted_fields_tabular.xlsx (Excel version)")
        print(f"  - extracted_fields_all.json (Original JSON format)")
        
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file: {JSON_FILE_PATH}")
        print(f"💡 Make sure to update JSON_FILE_PATH on line 12 with your actual file path")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main() 