#!/usr/bin/env python3
"""
Test _db Constraint - Verify only names ending with _db are used

This tests that the extraction only uses database names ending with '_db'
"""

import json
import tempfile
import os
from extract_my_json_pandas import find_dictionary_name
from json_field_extractor import quick_extract

def create_test_cases():
    """
    Create test cases with different providedKey formats
    """
    test_cases = [
        {
            "name": "Valid - ends with _db",
            "providedKey": "PBWM.GCB_AAC_NAM.gcgservnapsd_genesis_bcd_t_db",
            "expected": "gcgservnapsd_genesis_bcd_t_db",
            "should_extract": True
        },
        {
            "name": "Invalid - doesn't end with _db",
            "providedKey": "PBWM.GCB_AAC_NAM.some_other_system",
            "expected": None,
            "should_extract": False
        },
        {
            "name": "Valid - another _db case",
            "providedKey": "CORP.FINANCE.customer_data_db",
            "expected": "customer_data_db", 
            "should_extract": True
        },
        {
            "name": "Invalid - ends with _database",
            "providedKey": "CORP.FINANCE.customer_database",
            "expected": None,
            "should_extract": False
        }
    ]
    return test_cases

def test_db_constraint():
    """
    Test the _db constraint with various cases
    """
    print("🧪 Testing '_db' Constraint")
    print("=" * 50)
    
    test_cases = create_test_cases()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}: {test_case['name']}")
        print(f"🔍 ProvidedKey: {test_case['providedKey']}")
        
        # Create test JSON
        test_data = {
            "dictionary": {
                "providedKey": test_case['providedKey'],
                "version": 1
            },
            "field_definitions": {
                "test_table": {
                    "test_field": {
                        "providedKey": f"{test_case['providedKey']}.test_field",
                        "displayName": "test_field",
                        "physicalName": "test_field_physical",
                        "dataType": "Character",
                        "isNullable": True,
                        "format": "varchar(50)",
                        "description": "Test field"
                    }
                }
            }
        }
        
        # Create temporary file
        test_file = f"test_case_{i}.json"
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        try:
            # Load original JSON
            with open(test_file, 'r', encoding='utf-8') as f:
                original_json_data = json.load(f)
            
            # Extract fields
            results = quick_extract(test_file)
            
            if results:
                # Get first field for testing
                first_db = list(results.keys())[0]
                first_table = list(results[first_db].keys())[0]
                first_field = list(results[first_db][first_table].keys())[0]
                field_info = results[first_db][first_table][first_field]
                
                # Test extraction
                extracted_name = find_dictionary_name(
                    field_info,
                    results[first_db][first_table],
                    results[first_db],
                    original_json_data
                )
                
                print(f"🎯 Result: {extracted_name}")
                
                # Verify result
                if test_case['should_extract']:
                    if extracted_name == test_case['expected']:
                        print(f"✅ PASS: Correctly extracted '{extracted_name}'")
                    else:
                        print(f"❌ FAIL: Expected '{test_case['expected']}', got '{extracted_name}'")
                else:
                    if extracted_name is None:
                        print(f"✅ PASS: Correctly rejected (doesn't end with '_db')")
                    else:
                        print(f"❌ FAIL: Should have been rejected, but got '{extracted_name}'")
            else:
                print("❌ No field definitions found")
        
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)

def main():
    print("🎯 Database Name '_db' Constraint Test")
    print("=" * 60)
    print("Testing that only database names ending with '_db' are extracted")
    
    test_db_constraint()
    
    print("\n" + "=" * 60)
    print("📋 CONSTRAINT SUMMARY:")
    print("✅ Names ending with '_db' → Extract database name")
    print("❌ Names NOT ending with '_db' → Use fallback (original db key)")

if __name__ == "__main__":
    main() 