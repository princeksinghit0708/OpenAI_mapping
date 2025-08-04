# JSON Field Extractor

A comprehensive Python tool for extracting database field definitions from complex JSON files. This tool searches for objects with specific field structures and organizes them by database and table for easy analysis and processing.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Field Structure](#field-structure)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Output Formats](#output-formats)

## ✨ Features

- **Flexible JSON Parsing**: Recursively searches through complex nested JSON structures
- **Database Filtering**: Extract fields for specific databases
- **Multiple Output Formats**: Supports JSON and CSV output
- **Comprehensive Statistics**: Provides extraction summary and analytics
- **Robust Error Handling**: Handles various JSON structures and edge cases
- **Path Tracking**: Tracks where each field was found in the JSON structure
- **Command Line Interface**: Easy-to-use CLI with various options
- **Programmatic API**: Full Python API for integration into other tools

## 🚀 Installation

1. **Clone or download the files:**
   ```bash
   # Download the three main files:
   # - json_field_extractor.py
   # - example_usage.py  
   # - test_extractor.py
   ```

2. **Install dependencies:**
   ```bash
   # Core dependencies (built-in Python modules)
   # No additional installation required for basic functionality
   
   # Optional: For CSV export functionality
   pip install pandas
   ```

## ⚡ Quick Start

### 🎯 Ultra-Simple Usage (NEW!)

**Just provide the JSON file path - that's it!**

```python
# Method 1: One line extraction
from json_field_extractor import quick_extract
results = quick_extract("your_data_file.json")

# Method 2: Simple with auto-save
from json_field_extractor import extract_fields_from_json
fields = extract_fields_from_json("your_data_file.json")  # Auto-saves to ./output
```

**Or use the standalone script:**
```bash
python simple_extract.py your_data_file.json
```

### Command Line Usage

```bash
# Extract all fields from your JSON file
python json_field_extractor.py your_data_file.json

# Extract fields for a specific database
python json_field_extractor.py your_data_file.json --database "finance_db"

# Save as CSV format
python json_field_extractor.py your_data_file.json --format csv

# Specify output directory with detailed results
python json_field_extractor.py your_data_file.json --output ./results --detailed
```

### Advanced Programmatic Usage

```python
from json_field_extractor import JSONFieldExtractor

# Initialize the extractor
extractor = JSONFieldExtractor()

# Extract all fields
results = extractor.extract_from_file("your_data_file.json")

# Filter by specific database
finance_fields = extractor.filter_by_database("finance_db")

# Save results
extractor.save_results("./output", format_type='json')
```

## 🔍 Field Structure

The extractor searches for objects that contain this specific structure:

```json
{
  "providedKey": "database.table.field_name",
  "displayName": "field_name",
  "physicalName": "field_name", 
  "dataType": "Character|Integer|Decimal|Date|etc",
  "isNullable": true|false,
  "format": "varchar(50)|int|decimal(15,2)|etc",
  "description": "Detailed field description"
}
```

### Example Field Definition

```json
{
  "bkg_dt": {
    "providedKey": "crd_arrg_dim.bkg_dt",
    "displayName": "bkg_dt",
    "physicalName": "bkg_dt",
    "dataType": "Character",
    "isNullable": true,
    "format": "varchar(10)",
    "description": "Booking Date is defined as account opening date..."
  }
}
```

## 📖 Usage

### Command Line Interface

```bash
python json_field_extractor.py [JSON_FILE] [OPTIONS]

Arguments:
  JSON_FILE                 Path to the JSON file to process

Options:
  --database, -d DATABASE   Filter results by specific database name
  --output, -o OUTPUT       Output directory (default: ./output)
  --format, -f FORMAT       Output format: json or csv (default: json)
  --detailed                Print detailed results to console
  --quiet, -q               Suppress verbose output
  --help                    Show help message
```

### Python API

#### Basic Extraction

```python
from json_field_extractor import JSONFieldExtractor

# Initialize
extractor = JSONFieldExtractor()

# Extract from file
results = extractor.extract_from_file("schema.json")

# Get statistics
print(f"Total fields found: {extractor.extraction_stats['total_fields_found']}")
print(f"Databases: {extractor.get_all_databases()}")
```

#### Advanced Usage

```python
# Extract with database filtering
results = extractor.extract_from_file("schema.json", database_filter="finance_db")

# Get tables for a specific database
tables = extractor.get_tables_for_database("finance_db")

# Get field counts by database
field_counts = extractor.get_field_count_by_database()

# Save results in different formats
extractor.save_results("./output", format_type='json')
extractor.save_results("./output", format_type='csv')
```

## 💡 Examples

### Example 1: Ultra-Simple - Just Provide File Path

```python
# Just one line - extracts everything!
from json_field_extractor import quick_extract
results = quick_extract("my_schema.json")

# Print what we found
print(f"Found {len(results)} databases")
for db_name, tables in results.items():
    print(f"  {db_name}: {len(tables)} tables")
```

### Example 2: Simple with Options

```python
# Extract with options and auto-save
from json_field_extractor import extract_fields_from_json

fields = extract_fields_from_json(
    json_file_path="my_schema.json",
    database_name="finance_db",      # Filter by database
    formats=['json', 'csv'],         # Save in both formats  
    output_dir="./my_results",       # Custom output directory
    detailed=True                    # Show detailed output
)
```

### Example 3: Comprehensive Examples

```python
# Run the comprehensive example suite
python example_usage.py
```

This will demonstrate:
- Basic field extraction
- Database filtering  
- Detailed analysis
- Custom reporting
- Error handling

### Example 4: Custom Analysis

```python
from json_field_extractor import JSONFieldExtractor

extractor = JSONFieldExtractor()
results = extractor.extract_from_file("data.json")

# Find all nullable fields
nullable_fields = []
for db_name, db_data in results.items():
    for table_name, table_data in db_data.items():
        for field_name, field_data in table_data.items():
            if field_data.get('isNullable'):
                nullable_fields.append({
                    'database': db_name,
                    'table': table_name,
                    'field': field_name,
                    'type': field_data.get('dataType')
                })

print(f"Found {len(nullable_fields)} nullable fields")
```

## 📚 API Reference

### Simple Functions (Recommended)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `quick_extract(json_file_path)` | Ultra-simple one-line extraction | `json_file_path`: Path to JSON file | Dict of extracted fields |
| `extract_fields_from_json(json_file_path, database_name=None, output_dir="./output", formats=['json'], detailed=False)` | Simple extraction with options | `json_file_path`: JSON file path<br>`database_name`: Optional filter<br>`output_dir`: Output directory<br>`formats`: Save formats<br>`detailed`: Show details | Dict of extracted fields |

### JSONFieldExtractor Class

#### Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `__init__()` | Initialize the extractor | None | None |
| `extract_from_file(file_path, database_filter=None)` | Main extraction method | `file_path`: JSON file path<br>`database_filter`: Optional database name | Dict of extracted fields |
| `extract_all(json_file_path, output_dir="./output", database_filter=None, save_formats=['json'], show_detailed=False, auto_save=True)` | One-step extraction with auto-save | `json_file_path`: JSON file path<br>`output_dir`: Output directory<br>`database_filter`: Optional filter<br>`save_formats`: List of formats<br>`show_detailed`: Show details<br>`auto_save`: Auto-save results | Dict of extracted fields |
| `filter_by_database(database_name)` | Filter results by database | `database_name`: Database to filter | Filtered results dict |
| `get_all_databases()` | Get list of all databases | None | List of database names |
| `get_tables_for_database(database_name)` | Get tables for database | `database_name`: Database name | List of table names |
| `save_results(output_path, database_filter=None, format_type='json')` | Save results to file | `output_path`: Output directory<br>`database_filter`: Optional filter<br>`format_type`: 'json' or 'csv' | None |
| `print_summary()` | Print extraction summary | None | None |
| `print_detailed_results(max_description_length=100)` | Print detailed results | `max_description_length`: Max chars for description | None |

#### Properties

| Property | Description | Type |
|----------|-------------|------|
| `extracted_fields` | Extracted field data organized by database/table | Dict |
| `extraction_stats` | Statistics about the extraction | Dict |
| `required_keys` | Required keys for field definitions | Set |

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_extractor.py

# The test suite includes:
# - Unit tests for all methods
# - Integration tests with realistic data
# - Error handling tests
# - Edge case validation
```

### Test Coverage

- ✅ Field definition validation
- ✅ Database/table name extraction
- ✅ JSON file loading and error handling
- ✅ Recursive field extraction
- ✅ Database filtering
- ✅ Result saving (JSON/CSV)
- ✅ Complex nested structures
- ✅ Edge cases and error conditions

## 📄 Output Formats

### JSON Output

```json
{
  "extraction_metadata": {
    "total_fields_found": 25,
    "databases_found": ["finance_db", "hr_db"],
    "tables_found": ["customers", "accounts", "employees"],
    "extraction_timestamp": "2024-01-15T10:30:00"
  },
  "field_counts_by_database": {
    "finance_db": 20,
    "hr_db": 5
  },
  "extracted_fields": {
    "finance_db": {
      "customers": {
        "customer_id": {
          "providedKey": "finance_db.customers.customer_id",
          "displayName": "customer_id",
          "physicalName": "customer_id",
          "dataType": "Integer",
          "isNullable": false,
          "format": "bigint",
          "description": "Unique customer identifier"
        }
      }
    }
  }
}
```

### CSV Output

| database | table | field_name | providedKey | displayName | physicalName | dataType | isNullable | format | description |
|----------|-------|------------|-------------|-------------|--------------|----------|------------|---------|-------------|
| finance_db | customers | customer_id | finance_db.customers.customer_id | customer_id | customer_id | Integer | false | bigint | Unique customer identifier |

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Set default output directory
export JSON_EXTRACTOR_OUTPUT_DIR="./default_output"

# Optional: Set default format
export JSON_EXTRACTOR_FORMAT="csv"
```

### Custom Field Structure

To modify the required field structure, update the `required_keys` set in the `__init__` method:

```python
def __init__(self):
    self.required_keys = {
        'providedKey', 'displayName', 'physicalName', 
        'dataType', 'isNullable', 'format', 'description'
        # Add or remove keys as needed
    }
```

## 🚨 Error Handling

The extractor handles various error conditions gracefully:

- **File not found**: Clear error message with file path
- **Invalid JSON**: JSON parsing error details
- **Empty files**: Handles gracefully with zero results
- **Missing required fields**: Ignores incomplete field definitions
- **Complex structures**: Recursively searches all levels

## 🎯 Use Cases

1. **Data Dictionary Analysis**: Extract and analyze database schemas
2. **Documentation Generation**: Create field documentation from JSON metadata
3. **Schema Migration**: Understand field structures for migrations
4. **Data Lineage**: Track field definitions across systems
5. **Compliance Reporting**: Generate field reports for audits

## 🤝 Contributing

To extend or modify the extractor:

1. **Add new field types**: Update the `is_field_definition()` method
2. **Add output formats**: Extend the `save_results()` method
3. **Add analysis features**: Create new methods for specific analyses
4. **Improve performance**: Optimize the recursive search algorithm

## 📝 License

This project is provided as-is for educational and commercial use.

## 📞 Support

For issues or questions:
1. Check the test suite for examples
2. Review the example usage file
3. Examine error messages for specific issues
4. Validate your JSON structure matches the expected format

---

**Happy extracting! 🎉** 