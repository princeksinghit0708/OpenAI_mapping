#!/usr/bin/env python3
"""
Test Dictionary Name Search - Debug the search functionality

This script tests the dictionary_name search to make sure it's working correctly.
"""

import json
import tempfile
import os
from extract_my_json_pandas import find_dictionary_name, create_results_dataframe
from json_field_extractor import quick_extract

def create_test_json_with_dictionary_name():
    """
    Create test JSON with dictionary_name in different locations
    """
    test_data = {
        "metadata": {
            "version": "1.0",
            "dictionary_name": "PRODUCTION_DATABASE"  # This should be found!
        },
        "system_info": {
            "environment": "prod"
        },
        "database_schemas": {
            "finance_db": {
                "tables": {
                    "customers": {
                        "customer_id": {
                            "providedKey": "finance_db.customers.customer_id",
                            "displayName": "customer_id",
                            "physicalName": "cust_id",
                            "dataType": "Integer",
                            "isNullable": False,
                            "format": "bigint",
                            "description": "Unique customer identifier"
                        },
                        "email": {
                            "providedKey": "finance_db.customers.email",
                            "displayName": "email",
                            "physicalName": "email_address",
                            "dataType": "Character", 
                            "isNullable": True,
                            "format": "varchar(255)",
                            "description": "Customer email address"
                        }
                    }
                }
            }
        }
    }
    return test_data

def test_search_functionality():
    """
    Test the dictionary_name search functionality
    """
    print("🧪 Testing Dictionary Name Search")
    print("=" * 50)
    
    # Create test JSON file
    test_data = create_test_json_with_dictionary_name()
    test_file = "test_dict_search.json"
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"📝 Created test file: {test_file}")
    
    try:
        print(f"\n🔍 Contents of JSON file:")
        print(json.dumps(test_data, indent=2))
        
        # Load the original JSON data
        with open(test_file, 'r', encoding='utf-8') as f:
            original_json_data = json.load(f)
        
        # Extract fields using the main extractor
        results = quick_extract(test_file)
        
        print(f"\n📊 Extracted results structure:")
        for db_name, tables in results.items():
            print(f"  Database: {db_name}")
            for table_name, fields in tables.items():
                print(f"    Table: {table_name}")
                for field_name, field_info in fields.items():
                    print(f"      Field: {field_name}")
        
        # Test the search function directly
        print(f"\n🔍 Testing dictionary_name search:")
        
        # Get the first field for testing
        first_db = list(results.keys())[0]
        first_table = list(results[first_db].keys())[0] 
        first_field = list(results[first_db][first_table].keys())[0]
        field_info = results[first_db][first_table][first_field]
        
        print(f"Testing with field: {first_field}")
        
        # Test the find function
        found_dict_name = find_dictionary_name(
            field_info, 
            results[first_db][first_table],
            results[first_db],
            original_json_data
        )
        
        print(f"🎯 Result: {found_dict_name}")
        
        if found_dict_name == "PRODUCTION_DATABASE":
            print("✅ SUCCESS: Found dictionary_name correctly!")
        else:
            print(f"❌ FAILED: Expected 'PRODUCTION_DATABASE', got '{found_dict_name}'")
        
        # Test the full DataFrame creation
        print(f"\n📋 Testing full DataFrame creation:")
        df = create_results_dataframe(results, original_json_data)
        
        if df is not None:
            print("DataFrame created successfully:")
            print(df.to_string(index=False))
            
            # Check if DB_name column has the correct value
            unique_db_names = df['DB_name'].unique()
            print(f"\nUnique DB_name values: {unique_db_names}")
            
            if "PRODUCTION_DATABASE" in unique_db_names:
                print("✅ SUCCESS: DataFrame contains correct dictionary_name!")
            else:
                print(f"❌ FAILED: DataFrame DB_name values are incorrect")
        else:
            print("❌ FAILED: DataFrame creation failed")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_search_functionality() 