#!/usr/bin/env python3
"""
Quick Demo - Simplest possible JSON field extraction

Shows how you can extract database field definitions with just one line of code!
"""

import json
import tempfile
import os
from json_field_extractor import quick_extract, extract_fields_from_json

def create_demo_data():
    """Create some demo JSON data to extract from"""
    demo_data = {
        "company_metadata": {
            "name": "Demo Corp",
            "version": "1.0"
        },
        "database_schemas": {
            "customer_db": {
                "tables": {
                    "customers": {
                        "customer_id": {
                            "providedKey": "customer_db.customers.customer_id",
                            "displayName": "customer_id",
                            "physicalName": "customer_id",
                            "dataType": "Integer",
                            "isNullable": False,
                            "format": "bigint",
                            "description": "Unique customer identifier"
                        },
                        "email": {
                            "providedKey": "customer_db.customers.email",
                            "displayName": "email",
                            "physicalName": "email",
                            "dataType": "Character",
                            "isNullable": True,
                            "format": "varchar(255)",
                            "description": "Customer email address"
                        }
                    }
                }
            },
            "orders_db": {
                "orders_table": {
                    "order_total": {
                        "providedKey": "orders_db.orders_table.order_total",
                        "displayName": "order_total",
                        "physicalName": "order_total",
                        "dataType": "Decimal",
                        "isNullable": False,
                        "format": "decimal(10,2)",
                        "description": "Total order amount"
                    }
                }
            }
        }
    }
    return demo_data

def main():
    print("🎯 Quick Demo - JSON Field Extractor")
    print("=" * 50)
    
    # Create demo JSON file
    demo_data = create_demo_data()
    demo_file = "demo_schema.json"
    
    with open(demo_file, 'w') as f:
        json.dump(demo_data, f, indent=2)
    
    print(f"📝 Created demo file: {demo_file}")
    
    try:
        print("\n🚀 Method 1: Ultra-simple - One line!")
        print("-" * 30)
        
        # THIS IS ALL YOU NEED! Just provide the file path:
        results = quick_extract(demo_file)
        
        # Show what we extracted
        total_fields = sum(len(table) for db in results.values() for table in db.values())
        print(f"✅ Extracted {total_fields} fields from {len(results)} databases")
        
        # Show the structure
        for db_name, tables in results.items():
            print(f"  📊 {db_name}: {len(tables)} tables")
            for table_name, fields in tables.items():
                print(f"    📋 {table_name}: {len(fields)} fields")
                for field_name, field_info in fields.items():
                    print(f"      🔹 {field_name} ({field_info['dataType']})")
        
        print(f"\n🚀 Method 2: Simple with auto-save")
        print("-" * 30)
        
        # Extract and automatically save results
        extract_fields_from_json(
            json_file_path=demo_file,
            output_dir="./demo_output",
            formats=['json', 'csv']
        )
        
        print("✨ Done! Check './demo_output' folder for the extracted results.")
        
        print(f"\n💡 That's it! Just provide your JSON file path and everything is handled automatically.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Clean up
        if os.path.exists(demo_file):
            os.remove(demo_file)

if __name__ == "__main__":
    main() 