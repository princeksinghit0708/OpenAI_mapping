#!/usr/bin/env python3
"""
Debug Dictionary Search - Simple debugging tool

Just put your JSON file path here and see if providedKey is found.
Extracts the last part of providedKey as the database name.
Example: "PBWM.GCB_AAC_NAM.gcgservnapsd_genesis_bcd_t_db" → "gcgservnapsd_genesis_bcd_t_db"
"""

import json

# 🎯 PUT YOUR JSON FILE PATH HERE:
JSON_FILE_PATH = "your_file.json"  # ← Change this to your actual file path

def search_for_provided_key_debug(obj, path="root", indent=0):
    """
    Debug version that shows the search process for providedKey
    """
    prefix = "  " * indent
    
    if isinstance(obj, dict):
        print(f"{prefix}📁 Checking dict at {path} (keys: {list(obj.keys())})")
        
        # Check if current dictionary has 'providedKey' key
        if 'providedKey' in obj:
            provided_key = obj['providedKey']
            print(f"{prefix}🎯 FOUND providedKey at {path}: '{provided_key}'")
            
            # Extract the last part after splitting by dots
            if provided_key and isinstance(provided_key, str):
                parts = provided_key.split('.')
                if len(parts) >= 1:
                    db_name = parts[-1]  # Get the last part
                    print(f"{prefix}🔍 Extracted potential DB name: '{db_name}'")
                    
                    # Only use if it ends with '_db'
                    if db_name.endswith('_db'):
                        print(f"{prefix}✅ DB name ends with '_db': '{db_name}'")
                        return db_name
                    else:
                        print(f"{prefix}❌ DB name doesn't end with '_db', skipping: '{db_name}'")
                        return None
            return None
        
        # Search in all values of current dictionary
        for key, value in obj.items():
            print(f"{prefix}🔍 Searching in {path}.{key}...")
            result = search_for_provided_key_debug(value, f"{path}.{key}", indent + 1)
            if result:
                return result
                
    elif isinstance(obj, list):
        print(f"{prefix}📋 Checking list at {path} (length: {len(obj)})")
        # Search in all items of the list
        for i, item in enumerate(obj):
            print(f"{prefix}🔍 Searching in {path}[{i}]...")
            result = search_for_provided_key_debug(item, f"{path}[{i}]", indent + 1)
            if result:
                return result
    else:
        print(f"{prefix}📄 Found value at {path}: {type(obj).__name__}")
    
    return None

def main():
    print("🔍 ProvidedKey Database Name Extractor")
    print("=" * 50)
    
    try:
        print(f"📂 Loading JSON file: {JSON_FILE_PATH}")
        
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print(f"✅ JSON loaded successfully!")
        print(f"📊 Top-level keys: {list(json_data.keys()) if isinstance(json_data, dict) else 'Not a dict'}")
        
        print(f"\n🔍 Starting search for 'providedKey' and extracting DB name...")
        print("-" * 30)
        
        found_name = search_for_provided_key_debug(json_data)
        
        print("-" * 30)
        if found_name:
            print(f"🎉 SUCCESS! Extracted DB name: '{found_name}'")
        else:
            print(f"❌ No 'providedKey' found in the JSON file")
            print(f"💡 Make sure your JSON contains a 'dictionary' object with 'providedKey' field")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {JSON_FILE_PATH}")
        print(f"💡 Update the JSON_FILE_PATH variable with your actual file path")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: Invalid JSON format: {e}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main() 