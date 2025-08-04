"""
Test Suite for JSON Field Extractor
Comprehensive testing of the JSONFieldExtractor functionality
"""

import json
import tempfile
import os
import sys
import unittest
from pathlib import Path
from json_field_extractor import JSONFieldExtractor

class TestJSONFieldExtractor(unittest.TestCase):
    """
    Test suite for JSONFieldExtractor class
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.extractor = JSONFieldExtractor()
        self.temp_files = []
    
    def tearDown(self):
        """Clean up after each test method."""
        # Clean up temporary files
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def create_temp_json_file(self, data, suffix='.json'):
        """Helper method to create temporary JSON files"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as temp_file:
            json.dump(data, temp_file, indent=2)
            temp_file_path = temp_file.name
            self.temp_files.append(temp_file_path)
            return temp_file_path
    
    def create_sample_field_data(self):
        """Create sample field data for testing"""
        return {
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01"
            },
            "databases": {
                "test_db": {
                    "tables": {
                        "test_table": {
                            "fields": {
                                "test_field": {
                                    "providedKey": "test_db.test_table.test_field",
                                    "displayName": "test_field",
                                    "physicalName": "test_field",
                                    "dataType": "Character",
                                    "isNullable": True,
                                    "format": "varchar(50)",
                                    "description": "Test field for unit testing"
                                },
                                "numeric_field": {
                                    "providedKey": "test_db.test_table.numeric_field",
                                    "displayName": "numeric_field",
                                    "physicalName": "numeric_field",
                                    "dataType": "Integer",
                                    "isNullable": False,
                                    "format": "int",
                                    "description": "Numeric test field"
                                }
                            }
                        }
                    }
                }
            }
        }
    
    def test_initialization(self):
        """Test extractor initialization"""
        extractor = JSONFieldExtractor()
        
        # Check required keys are set correctly
        expected_keys = {'providedKey', 'displayName', 'physicalName', 
                        'dataType', 'isNullable', 'format', 'description'}
        self.assertEqual(extractor.required_keys, expected_keys)
        
        # Check initial state
        self.assertEqual(extractor.extracted_fields, {})
        self.assertEqual(extractor.extraction_stats['total_fields_found'], 0)
        self.assertEqual(len(extractor.extraction_stats['databases_found']), 0)
    
    def test_is_field_definition_valid(self):
        """Test field definition validation with valid data"""
        valid_field = {
            "providedKey": "db.table.field",
            "displayName": "field",
            "physicalName": "field",
            "dataType": "Character",
            "isNullable": True,
            "format": "varchar",
            "description": "Test field"
        }
        
        self.assertTrue(self.extractor.is_field_definition(valid_field))
    
    def test_is_field_definition_invalid(self):
        """Test field definition validation with invalid data"""
        # Missing required key
        invalid_field = {
            "providedKey": "db.table.field",
            "displayName": "field",
            "physicalName": "field",
            "dataType": "Character",
            "isNullable": True,
            "format": "varchar"
            # Missing 'description'
        }
        
        self.assertFalse(self.extractor.is_field_definition(invalid_field))
        
        # Non-dictionary
        self.assertFalse(self.extractor.is_field_definition("not a dict"))
        self.assertFalse(self.extractor.is_field_definition(None))
        self.assertFalse(self.extractor.is_field_definition([]))
    
    def test_extract_database_from_provided_key(self):
        """Test database name extraction from providedKey"""
        # Three-part key
        self.assertEqual(
            self.extractor.extract_database_from_provided_key("finance_db.users.id"),
            "finance_db"
        )
        
        # Two-part key
        self.assertEqual(
            self.extractor.extract_database_from_provided_key("users.id"),
            "default"
        )
        
        # Single part key
        self.assertEqual(
            self.extractor.extract_database_from_provided_key("id"),
            "unknown"
        )
        
        # Empty/None key
        self.assertIsNone(self.extractor.extract_database_from_provided_key(""))
        self.assertIsNone(self.extractor.extract_database_from_provided_key(None))
    
    def test_extract_table_from_provided_key(self):
        """Test table name extraction from providedKey"""
        # Three-part key
        self.assertEqual(
            self.extractor.extract_table_from_provided_key("finance_db.users.id"),
            "users"
        )
        
        # Two-part key
        self.assertEqual(
            self.extractor.extract_table_from_provided_key("users.id"),
            "users"
        )
        
        # Single part key
        self.assertEqual(
            self.extractor.extract_table_from_provided_key("id"),
            "unknown"
        )
        
        # Empty/None key
        self.assertIsNone(self.extractor.extract_table_from_provided_key(""))
        self.assertIsNone(self.extractor.extract_table_from_provided_key(None))
    
    def test_load_json_file_valid(self):
        """Test loading valid JSON file"""
        test_data = {"test": "data"}
        temp_file = self.create_temp_json_file(test_data)
        
        loaded_data = self.extractor.load_json_file(temp_file)
        self.assertEqual(loaded_data, test_data)
    
    def test_load_json_file_not_found(self):
        """Test loading non-existent JSON file"""
        with self.assertRaises(FileNotFoundError):
            self.extractor.load_json_file("non_existent_file.json")
    
    def test_load_json_file_invalid_json(self):
        """Test loading invalid JSON file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_file.write("{ invalid json content")
            temp_file_path = temp_file.name
            self.temp_files.append(temp_file_path)
        
        with self.assertRaises(ValueError):
            self.extractor.load_json_file(temp_file_path)
    
    def test_extract_from_file_simple(self):
        """Test basic field extraction from file"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        results = self.extractor.extract_from_file(temp_file)
        
        # Check extraction stats
        self.assertEqual(self.extractor.extraction_stats['total_fields_found'], 2)
        self.assertIn('test_db', self.extractor.extraction_stats['databases_found'])
        
        # Check extracted data structure
        self.assertIn('test_db', results)
        self.assertIn('test_table', results['test_db'])
        self.assertIn('test_field', results['test_db']['test_table'])
        self.assertIn('numeric_field', results['test_db']['test_table'])
        
        # Check field data
        test_field = results['test_db']['test_table']['test_field']
        self.assertEqual(test_field['dataType'], 'Character')
        self.assertEqual(test_field['isNullable'], True)
        self.assertEqual(test_field['format'], 'varchar(50)')
    
    def test_extract_from_file_with_database_filter(self):
        """Test extraction with database filtering"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        results = self.extractor.extract_from_file(temp_file, database_filter='test_db')
        
        # Should only contain the filtered database
        self.assertEqual(len(results), 1)
        self.assertIn('test_db', results)
    
    def test_filter_by_database(self):
        """Test database filtering functionality"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        # First extract all
        all_results = self.extractor.extract_from_file(temp_file)
        
        # Then filter
        filtered_results = self.extractor.filter_by_database('test_db')
        self.assertEqual(len(filtered_results), 1)
        self.assertIn('test_db', filtered_results)
        
        # Test non-existent database
        empty_results = self.extractor.filter_by_database('non_existent_db')
        self.assertEqual(empty_results, {})
    
    def test_get_all_databases(self):
        """Test getting list of all databases"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        self.extractor.extract_from_file(temp_file)
        databases = self.extractor.get_all_databases()
        
        self.assertEqual(databases, ['test_db'])
    
    def test_get_tables_for_database(self):
        """Test getting tables for a specific database"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        self.extractor.extract_from_file(temp_file)
        tables = self.extractor.get_tables_for_database('test_db')
        
        self.assertEqual(tables, ['test_table'])
        
        # Test non-existent database
        empty_tables = self.extractor.get_tables_for_database('non_existent_db')
        self.assertEqual(empty_tables, [])
    
    def test_get_field_count_by_database(self):
        """Test field count calculation by database"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        self.extractor.extract_from_file(temp_file)
        field_counts = self.extractor.get_field_count_by_database()
        
        self.assertEqual(field_counts['test_db'], 2)
    
    def test_complex_nested_structure(self):
        """Test extraction from complex nested JSON structure"""
        complex_data = {
            "level1": {
                "level2": {
                    "level3": [
                        {
                            "some_field": {
                                "providedKey": "complex.nested.field",
                                "displayName": "nested_field",
                                "physicalName": "nested_field",
                                "dataType": "Text",
                                "isNullable": False,
                                "format": "text",
                                "description": "Deeply nested field"
                            }
                        }
                    ]
                }
            }
        }
        
        temp_file = self.create_temp_json_file(complex_data)
        results = self.extractor.extract_from_file(temp_file)
        
        self.assertEqual(self.extractor.extraction_stats['total_fields_found'], 1)
        self.assertIn('complex', results)
    
    def test_empty_json(self):
        """Test extraction from empty JSON"""
        empty_data = {}
        temp_file = self.create_temp_json_file(empty_data)
        
        results = self.extractor.extract_from_file(temp_file)
        
        self.assertEqual(results, {})
        self.assertEqual(self.extractor.extraction_stats['total_fields_found'], 0)
    
    def test_json_with_no_field_definitions(self):
        """Test extraction from JSON with no matching field definitions"""
        no_fields_data = {
            "config": {"version": "1.0"},
            "settings": {"debug": True},
            "data": [1, 2, 3, 4, 5],
            "incomplete_field": {
                "providedKey": "test.field",
                "displayName": "test"
                # Missing required keys
            }
        }
        
        temp_file = self.create_temp_json_file(no_fields_data)
        results = self.extractor.extract_from_file(temp_file)
        
        self.assertEqual(results, {})
        self.assertEqual(self.extractor.extraction_stats['total_fields_found'], 0)
    
    def test_save_results_json(self):
        """Test saving results in JSON format"""
        sample_data = self.create_sample_field_data()
        temp_file = self.create_temp_json_file(sample_data)
        
        self.extractor.extract_from_file(temp_file)
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractor.save_results(temp_dir, format_type='json')
            
            # Check if output file was created
            output_file = Path(temp_dir) / "extracted_fields_all.json"
            self.assertTrue(output_file.exists())
            
            # Verify content
            with open(output_file, 'r') as f:
                saved_data = json.load(f)
            
            self.assertIn('extraction_metadata', saved_data)
            self.assertIn('extracted_fields', saved_data)
            self.assertIn('field_counts_by_database', saved_data)
    
    def test_multiple_databases(self):
        """Test extraction with multiple databases"""
        multi_db_data = {
            "schemas": {
                "db1": {
                    "table1": {
                        "field1": {
                            "providedKey": "db1.table1.field1",
                            "displayName": "field1",
                            "physicalName": "field1",
                            "dataType": "Character",
                            "isNullable": True,
                            "format": "varchar",
                            "description": "Field in database 1"
                        }
                    }
                },
                "db2": {
                    "table2": {
                        "field2": {
                            "providedKey": "db2.table2.field2",
                            "displayName": "field2",
                            "physicalName": "field2",
                            "dataType": "Integer",
                            "isNullable": False,
                            "format": "int",
                            "description": "Field in database 2"
                        }
                    }
                }
            }
        }
        
        temp_file = self.create_temp_json_file(multi_db_data)
        results = self.extractor.extract_from_file(temp_file)
        
        self.assertEqual(self.extractor.extraction_stats['total_fields_found'], 2)
        self.assertEqual(len(self.extractor.get_all_databases()), 2)
        self.assertIn('db1', results)
        self.assertIn('db2', results)


def run_comprehensive_tests():
    """
    Run comprehensive tests with detailed output
    """
    print("🧪 Running Comprehensive JSON Field Extractor Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestJSONFieldExtractor)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    if result.wasSuccessful():
        print(f"\n✅ All tests passed successfully!")
        return True
    else:
        print(f"\n❌ Some tests failed. Please check the output above.")
        return False


def run_integration_test():
    """
    Run an integration test with a realistic scenario
    """
    print("\n🔧 Running Integration Test")
    print("-" * 40)
    
    # Create realistic test data
    realistic_data = {
        "data_dictionary": {
            "version": "3.1.4",
            "last_updated": "2024-01-15",
            "databases": {
                "customer_db": {
                    "description": "Customer management database",
                    "tables": {
                        "customers": {
                            "row_count": 50000,
                            "columns": {
                                "customer_id": {
                                    "providedKey": "customer_db.customers.customer_id",
                                    "displayName": "customer_id",
                                    "physicalName": "customer_id",
                                    "dataType": "Integer",
                                    "isNullable": False,
                                    "format": "bigint",
                                    "description": "Unique identifier for customer records. Auto-generated primary key."
                                },
                                "email_address": {
                                    "providedKey": "customer_db.customers.email_address",
                                    "displayName": "email_address",
                                    "physicalName": "email_address",
                                    "dataType": "Character",
                                    "isNullable": True,
                                    "format": "varchar(320)",
                                    "description": "Customer's primary email address used for communication and account verification."
                                },
                                "registration_date": {
                                    "providedKey": "customer_db.customers.registration_date",
                                    "displayName": "registration_date",
                                    "physicalName": "registration_date",
                                    "dataType": "DateTime",
                                    "isNullable": False,
                                    "format": "timestamp",
                                    "description": "Timestamp when the customer account was first created in the system."
                                }
                            }
                        }
                    }
                },
                "orders_db": {
                    "description": "Order processing database",
                    "tables": {
                        "orders": {
                            "columns": {
                                "order_total": {
                                    "providedKey": "orders_db.orders.order_total",
                                    "displayName": "order_total",
                                    "physicalName": "order_total",
                                    "dataType": "Decimal",
                                    "isNullable": False,
                                    "format": "decimal(12,2)",
                                    "description": "Total monetary value of the order including taxes and fees."
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(realistic_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        
        # Test the extractor
        extractor = JSONFieldExtractor()
        results = extractor.extract_from_file(temp_file_path)
        
        # Validate results
        expected_fields = 4
        actual_fields = extractor.extraction_stats['total_fields_found']
        
        print(f"Expected fields: {expected_fields}")
        print(f"Actual fields found: {actual_fields}")
        print(f"Databases found: {list(extractor.extraction_stats['databases_found'])}")
        
        # Test database filtering
        customer_db_results = extractor.filter_by_database('customer_db')
        customer_fields = sum(len(table_data) for table_data in customer_db_results.get('customer_db', {}).values())
        
        print(f"Customer DB fields: {customer_fields}")
        
        # Test saving
        with tempfile.TemporaryDirectory() as temp_dir:
            extractor.save_results(temp_dir)
            output_file = Path(temp_dir) / "extracted_fields_all.json"
            success = output_file.exists()
            print(f"File save test: {'✅ PASSED' if success else '❌ FAILED'}")
        
        # Overall validation
        integration_success = (
            actual_fields == expected_fields and
            len(extractor.extraction_stats['databases_found']) == 2 and
            customer_fields == 3 and
            success
        )
        
        print(f"\n🔧 Integration Test: {'✅ PASSED' if integration_success else '❌ FAILED'}")
        return integration_success
        
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        return False
    
    finally:
        # Clean up
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def main():
    """
    Main test runner
    """
    print("🚀 JSON Field Extractor - Test Suite")
    print("=" * 70)
    
    try:
        # Run unit tests
        unit_test_success = run_comprehensive_tests()
        
        # Run integration test
        integration_test_success = run_integration_test()
        
        # Final summary
        print("\n" + "=" * 70)
        print("FINAL TEST SUMMARY")
        print("=" * 70)
        print(f"Unit Tests: {'✅ PASSED' if unit_test_success else '❌ FAILED'}")
        print(f"Integration Test: {'✅ PASSED' if integration_test_success else '❌ FAILED'}")
        
        overall_success = unit_test_success and integration_test_success
        print(f"Overall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
        
        return 0 if overall_success else 1
        
    except Exception as e:
        print(f"\n💥 Test runner failed with error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 