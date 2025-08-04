"""
Example Usage of JSON Field Extractor
Demonstrates various ways to use the extractor for database field definitions
"""

import json
import os
from pathlib import Path
from json_field_extractor import JSONFieldExtractor, extract_fields_from_json, quick_extract

def create_sample_data():
    """
    Create sample JSON data for demonstration
    """
    sample_data = {
        "metadata": {
            "version": "2.0",
            "created": "2024-01-01",
            "description": "Sample database schema definitions"
        },
        "system_config": {
            "max_connections": 100,
            "timeout": 30
        },
        "schemas": {
            "finance_db": {
                "version": "1.2.3",
                "tables": {
                    "credit_arrangements": {
                        "metadata": {
                            "row_count": 1000000,
                            "last_updated": "2024-01-15"
                        },
                        "columns": {
                            "bkg_dt": {
                                "providedKey": "finance_db.credit_arrangements.bkg_dt",
                                "displayName": "bkg_dt",
                                "physicalName": "bkg_dt",
                                "dataType": "Character",
                                "isNullable": True,
                                "format": "varchar(10)",
                                "description": "Booking Date is defined as account opening date. This may be the same as the Effective Date of the Account/Arrangement or could be either earlier or later than the Effective Date. If deposits are automatically renewed that Booking date will be the original Booking date. For Mortgages this will be the Loan Closing Date. For Cards the booking date and effective date would be the same and is known as account open date."
                            },
                            "account_id": {
                                "providedKey": "finance_db.credit_arrangements.account_id",
                                "displayName": "account_id",
                                "physicalName": "account_id",
                                "dataType": "Integer",
                                "isNullable": False,
                                "format": "bigint",
                                "description": "Unique identifier for the account arrangement. Primary key for the table."
                            },
                            "customer_name": {
                                "providedKey": "finance_db.credit_arrangements.customer_name",
                                "displayName": "customer_name",
                                "physicalName": "customer_name",
                                "dataType": "Character",
                                "isNullable": True,
                                "format": "varchar(255)",
                                "description": "Full name of the customer associated with the account arrangement."
                            }
                        }
                    },
                    "transaction_log": {
                        "columns": {
                            "transaction_id": {
                                "providedKey": "finance_db.transaction_log.transaction_id",
                                "displayName": "transaction_id",
                                "physicalName": "transaction_id",
                                "dataType": "Character",
                                "isNullable": False,
                                "format": "varchar(50)",
                                "description": "Unique identifier for each transaction record."
                            },
                            "amount": {
                                "providedKey": "finance_db.transaction_log.amount",
                                "displayName": "amount",
                                "physicalName": "amount",
                                "dataType": "Decimal",
                                "isNullable": False,
                                "format": "decimal(15,2)",
                                "description": "Transaction amount in the base currency."
                            }
                        }
                    }
                }
            },
            "hr_db": {
                "tables": {
                    "employees": {
                        "columns": {
                            "emp_id": {
                                "providedKey": "hr_db.employees.emp_id",
                                "displayName": "emp_id",
                                "physicalName": "emp_id",
                                "dataType": "Integer",
                                "isNullable": False,
                                "format": "bigint",
                                "description": "Employee unique identifier, primary key."
                            },
                            "hire_date": {
                                "providedKey": "hr_db.employees.hire_date",
                                "displayName": "hire_date",
                                "physicalName": "hire_date",
                                "dataType": "Date",
                                "isNullable": True,
                                "format": "date",
                                "description": "Date when the employee was hired by the organization."
                            }
                        }
                    }
                }
            }
        },
        "lookup_tables": [
            {
                "reference_data": {
                    "country_code": {
                        "providedKey": "ref.country_code",
                        "displayName": "country_code",
                        "physicalName": "country_code",
                        "dataType": "Character",
                        "isNullable": False,
                        "format": "char(2)",
                        "description": "ISO 2-letter country code for standardized country identification."
                    }
                }
            }
        ]
    }
    return sample_data

def example_1_basic_extraction():
    """
    Example 1: Basic extraction of all fields from a JSON file
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Field Extraction")
    print("="*60)
    
    # Create sample data file
    sample_data = create_sample_data()
    sample_file = "sample_schema.json"
    
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"📝 Created sample file: {sample_file}")
    
    # Initialize extractor
    extractor = JSONFieldExtractor()
    
    # Extract all fields
    print("\n🔍 Extracting all fields...")
    results = extractor.extract_from_file(sample_file)
    
    # Show available databases
    databases = extractor.get_all_databases()
    print(f"\n📊 Available databases: {databases}")
    
    # Save results
    extractor.save_results("./output_example1", format_type='json')
    
    # Clean up
    os.remove(sample_file)
    
    return extractor, results

def example_2_database_filtering():
    """
    Example 2: Filter extraction by specific database
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Database-Specific Extraction")
    print("="*60)
    
    # Create sample data file
    sample_data = create_sample_data()
    sample_file = "sample_schema_db_filter.json"
    
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    # Initialize extractor
    extractor = JSONFieldExtractor()
    
    # Extract fields for specific database
    target_database = "finance_db"
    print(f"\n🎯 Extracting fields for database: {target_database}")
    
    db_results = extractor.extract_from_file(sample_file, database_filter=target_database)
    
    # Show tables in the database
    tables = extractor.get_tables_for_database(target_database)
    print(f"\n📋 Tables in {target_database}: {tables}")
    
    # Save filtered results
    extractor.save_results("./output_example2", database_filter=target_database, format_type='json')
    
    # Also save as CSV
    extractor.save_results("./output_example2", database_filter=target_database, format_type='csv')
    
    # Clean up
    os.remove(sample_file)
    
    return extractor, db_results

def example_3_detailed_analysis():
    """
    Example 3: Detailed analysis and reporting
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Detailed Analysis and Reporting")
    print("="*60)
    
    # Create sample data file
    sample_data = create_sample_data()
    sample_file = "sample_schema_detailed.json"
    
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    # Initialize extractor
    extractor = JSONFieldExtractor()
    
    # Extract all fields
    results = extractor.extract_from_file(sample_file)
    
    # Show detailed results
    print("\n📋 Detailed field information:")
    extractor.print_detailed_results(max_description_length=80)
    
    # Show field counts by database
    field_counts = extractor.get_field_count_by_database()
    print(f"\n📊 Field counts by database:")
    for db, count in field_counts.items():
        print(f"  - {db}: {count} fields")
    
    # Analyze data types
    print(f"\n🔍 Data type analysis:")
    data_types = {}
    for db_name, db_data in results.items():
        for table_name, table_data in db_data.items():
            for field_name, field_data in table_data.items():
                dtype = field_data.get('dataType', 'Unknown')
                data_types[dtype] = data_types.get(dtype, 0) + 1
    
    for dtype, count in sorted(data_types.items()):
        print(f"  - {dtype}: {count} fields")
    
    # Clean up
    os.remove(sample_file)
    
    return extractor, results

def example_4_programmatic_usage():
    """
    Example 4: Advanced programmatic usage
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Advanced Programmatic Usage")
    print("="*60)
    
    # Create sample data file
    sample_data = create_sample_data()
    sample_file = "sample_schema_advanced.json"
    
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    # Initialize extractor
    extractor = JSONFieldExtractor()
    
    # Extract fields
    results = extractor.extract_from_file(sample_file)
    
    # Custom analysis: Find nullable fields
    print("\n🔍 Finding nullable fields:")
    nullable_fields = []
    for db_name, db_data in results.items():
        for table_name, table_data in db_data.items():
            for field_name, field_data in table_data.items():
                if field_data.get('isNullable'):
                    nullable_fields.append({
                        'database': db_name,
                        'table': table_name,
                        'field': field_name,
                        'type': field_data.get('dataType'),
                        'providedKey': field_data.get('providedKey')
                    })
    
    print(f"Found {len(nullable_fields)} nullable fields:")
    for field in nullable_fields:
        print(f"  - {field['providedKey']} ({field['type']})")
    
    # Custom analysis: Find long descriptions
    print(f"\n📝 Finding fields with long descriptions (>100 chars):")
    long_desc_fields = []
    for db_name, db_data in results.items():
        for table_name, table_data in db_data.items():
            for field_name, field_data in table_data.items():
                desc = field_data.get('description', '')
                if len(desc) > 100:
                    long_desc_fields.append({
                        'providedKey': field_data.get('providedKey'),
                        'description_length': len(desc),
                        'description_preview': desc[:100] + "..."
                    })
    
    print(f"Found {len(long_desc_fields)} fields with long descriptions:")
    for field in long_desc_fields[:3]:  # Show first 3
        print(f"  - {field['providedKey']} ({field['description_length']} chars)")
        print(f"    Preview: {field['description_preview']}")
    
    # Generate a custom report
    report = {
        'extraction_timestamp': extractor.extraction_stats['extraction_timestamp'],
        'total_fields': extractor.extraction_stats['total_fields_found'],
        'databases': list(extractor.extraction_stats['databases_found']),
        'nullable_fields_count': len(nullable_fields),
        'long_description_fields_count': len(long_desc_fields),
        'field_counts_by_database': extractor.get_field_count_by_database()
    }
    
    # Save custom report
    os.makedirs("./output_example4", exist_ok=True)
    with open("./output_example4/custom_analysis_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📊 Custom analysis report saved to: ./output_example4/custom_analysis_report.json")
    
    # Clean up
    os.remove(sample_file)
    
    return extractor, results, report

def example_5_error_handling():
    """
    Example 5: Error handling and edge cases
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Error Handling and Edge Cases")
    print("="*60)
    
    extractor = JSONFieldExtractor()
    
    # Test 1: Non-existent file
    print("\n🧪 Test 1: Non-existent file")
    try:
        extractor.extract_from_file("non_existent_file.json")
    except FileNotFoundError as e:
        print(f"✓ Caught expected error: {e}")
    
    # Test 2: Invalid JSON
    print("\n🧪 Test 2: Invalid JSON file")
    invalid_json_file = "invalid.json"
    with open(invalid_json_file, 'w') as f:
        f.write("{ invalid json content ")
    
    try:
        extractor.extract_from_file(invalid_json_file)
    except ValueError as e:
        print(f"✓ Caught expected JSON error: {e}")
    finally:
        os.remove(invalid_json_file)
    
    # Test 3: Empty JSON
    print("\n🧪 Test 3: Empty JSON file")
    empty_json_file = "empty.json"
    with open(empty_json_file, 'w') as f:
        json.dump({}, f)
    
    results = extractor.extract_from_file(empty_json_file)
    print(f"✓ Empty JSON handled gracefully. Found {extractor.extraction_stats['total_fields_found']} fields.")
    os.remove(empty_json_file)
    
    # Test 4: JSON with no matching fields
    print("\n🧪 Test 4: JSON with no field definitions")
    no_fields_data = {
        "config": {"version": "1.0"},
        "settings": {"debug": True},
        "data": [1, 2, 3, 4, 5]
    }
    no_fields_file = "no_fields.json"
    with open(no_fields_file, 'w') as f:
        json.dump(no_fields_data, f)
    
    # Reset extractor for clean test
    extractor = JSONFieldExtractor()
    results = extractor.extract_from_file(no_fields_file)
    print(f"✓ No field definitions found. Total: {extractor.extraction_stats['total_fields_found']} fields.")
    os.remove(no_fields_file)
    
    print("\n✅ All error handling tests completed successfully!")

def example_6_ultra_simple_usage():
    """
    Example 6: Ultra-simple usage - just provide JSON file path
    """
    print("\n" + "="*60)
    print("EXAMPLE 6: Ultra-Simple Usage")
    print("="*60)
    
    # Create sample data file
    sample_data = create_sample_data()
    sample_file = "sample_schema_simple.json"
    
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"📝 Created sample file: {sample_file}")
    
    # Method 1: Ultra-simple - just one line!
    print("\n🚀 Method 1: Ultra-simple extraction")
    results1 = quick_extract(sample_file)
    print(f"✓ Found {sum(len(table) for db in results1.values() for table in db.values())} fields")
    
    # Method 2: Simple with options
    print("\n🚀 Method 2: Simple with options")
    results2 = extract_fields_from_json(
        json_file_path=sample_file,
        database_name="finance_db",  # Extract only finance_db
        formats=['json', 'csv'],     # Save in both formats
        detailed=True                # Show detailed output
    )
    
    # Method 3: One-step processing with class
    print("\n🚀 Method 3: One-step class method")
    extractor = JSONFieldExtractor()
    results3 = extractor.extract_all(
        json_file_path=sample_file,
        output_dir="./output_simple",
        save_formats=['json'],
        show_detailed=False
    )
    
    # Show comparison
    print(f"\n📊 Results Comparison:")
    print(f"Method 1 (quick_extract): {len(results1)} databases")
    print(f"Method 2 (with filter): {len(results2)} databases") 
    print(f"Method 3 (class method): {len(results3)} databases")
    
    # Clean up
    os.remove(sample_file)
    
    return results1, results2, results3

def main():
    """
    Run all examples
    """
    print("🚀 JSON Field Extractor - Usage Examples")
    print("=" * 70)
    
    try:
        # Create output directories
        output_dirs = ["./output_example1", "./output_example2", "./output_example3", 
                      "./output_example4", "./output_simple"]
        for output_dir in output_dirs:
            os.makedirs(output_dir, exist_ok=True)
        
        # Run examples
        example_1_basic_extraction()
        example_2_database_filtering()
        example_3_detailed_analysis()
        example_4_programmatic_usage()
        example_5_error_handling()
        example_6_ultra_simple_usage()  # New example
        
        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("📁 Check the output directories for generated files:")
        for output_dir in output_dirs:
            if os.path.exists(output_dir):
                files = list(Path(output_dir).glob("*"))
                print(f"  - {output_dir}: {len(files)} files")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        raise

if __name__ == "__main__":
    main() 