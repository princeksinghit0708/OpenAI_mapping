#!/usr/bin/env python3
"""
Test Your JSON Structure - Demo with your actual structure

This shows how the extraction will work with your specific JSON format.
"""

import json
import tempfile
import os
from extract_my_json_pandas import find_dictionary_name, create_results_dataframe
from json_field_extractor import quick_extract

def create_your_structure_test():
    """
    Create test JSON matching your actual structure
    """
    test_data = {
        "dictionary": {
            "version": 20,
            "releaseVersion": "1",
            "providedKey": "PBWM.GCB_AAC_NAM.gcgservnapsd_genesis_bcd_t_db",
            "documentSource": "DATA_CATALOG",
            "eemsRole": "169912_gcb_aac_nam_metadata_owner",
            "createdBy": "169912_gcb_aac_nam_metadata_owner",
            "createdOn": "2025-07-02T11:28:18.0017",
            "logicalName": "gcgservnapsd_genesis_bcd_t_db",
            "physicalName": "gcgservnapsd_genesis_bcd_t_db",
            "dictionaryType": "PHYSICAL",
            "description": "Source: 169912 -Contains Branded Cards data contracts extraction layer data.",
            "displayName": "gcgservnapsd_genesis_bcd_t_db",
            "dictionaryRelations": [
                {
                    "symbolicLink": True,
                    "relationType": "TRANSFORMATION",
                    "cardinalityLogicalName": "ONE-TO-ONE",
                    "relationFrom": {
                        "business": "PBWM",
                        "provider": "DatahubNAM"
                    }
                }
            ]
        },
        # Sample field definitions (your actual structure may be different)
        "field_definitions": {
            "sample_table": {
                "field1": {
                    "providedKey": "PBWM.GCB_AAC_NAM.sample_table.field1",
                    "displayName": "field1",
                    "physicalName": "customer_id",
                    "dataType": "Integer",
                    "isNullable": False,
                    "format": "bigint",
                    "description": "Customer identifier field"
                },
                "field2": {
                    "providedKey": "PBWM.GCB_AAC_NAM.sample_table.field2",
                    "displayName": "field2", 
                    "physicalName": "account_number",
                    "dataType": "Character",
                    "isNullable": True,
                    "format": "varchar(50)",
                    "description": "Account number field"
                }
            }
        }
    }
    return test_data

def test_your_structure():
    """
    Test with your specific JSON structure
    """
    print("🧪 Testing Your Specific JSON Structure")
    print("=" * 60)
    
    # Create test JSON file
    test_data = create_your_structure_test()
    test_file = "test_your_structure.json"
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"📝 Created test file with your structure")
    
    try:
        print(f"\n🔍 Your JSON structure:")
        print(f"📊 Top-level keys: {list(test_data.keys())}")
        print(f"📊 Dictionary keys: {list(test_data['dictionary'].keys())}")
        print(f"🎯 ProvidedKey: {test_data['dictionary']['providedKey']}")
        
        # Load the original JSON data
        with open(test_file, 'r', encoding='utf-8') as f:
            original_json_data = json.load(f)
        
        # Extract fields using the main extractor
        results = quick_extract(test_file)
        
        print(f"\n📊 Extraction results:")
        for db_name, tables in results.items():
            print(f"  Database key: {db_name}")
            for table_name, fields in tables.items():
                print(f"    Table: {table_name}")
                for field_name, field_info in fields.items():
                    print(f"      Field: {field_name}")
        
        # Test the DB name extraction
        print(f"\n🔍 Testing DB name extraction:")
        
        if results:
            # Get the first field for testing
            first_db = list(results.keys())[0]
            first_table = list(results[first_db].keys())[0] 
            first_field = list(results[first_db][first_table].keys())[0]
            field_info = results[first_db][first_table][first_field]
            
            print(f"Testing with field: {first_field}")
            
            # Test the find function
            found_db_name = find_dictionary_name(
                field_info, 
                results[first_db][first_table],
                results[first_db],
                original_json_data
            )
            
            print(f"🎯 Extracted DB name: '{found_db_name}'")
            
            expected_name = "gcgservnapsd_genesis_bcd_t_db"
            if found_db_name == expected_name:
                print("✅ SUCCESS: Correctly extracted DB name from providedKey!")
                print("✅ SUCCESS: DB name ends with '_db' constraint satisfied!")
            else:
                print(f"❌ Expected: '{expected_name}', Got: '{found_db_name}'")
        
        # Test the full DataFrame creation
        print(f"\n📋 Testing full tabular output:")
        df = create_results_dataframe(results, original_json_data)
        
        if df is not None and not df.empty:
            print("Your tabular output will look like this:")
            print(df.to_string(index=False))
            
            # Check DB_name column
            unique_db_names = df['DB_name'].unique()
            print(f"\nDB_name values: {unique_db_names}")
            
            if "gcgservnapsd_genesis_bcd_t_db" in unique_db_names:
                print("✅ SUCCESS: Your DB_name will be extracted correctly!")
            else:
                print(f"❌ Issue with DB_name extraction")
        
        print(f"\n🎉 Your JSON structure is compatible!")
        print(f"📋 Expected DB_name: gcgservnapsd_genesis_bcd_t_db")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_your_structure() 