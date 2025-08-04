"""
JSON Field Extractor - Extract database field definitions from complex JSON files
Searches for fields with specific structure: providedKey, displayName, physicalName, etc.
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import argparse
from datetime import datetime

class JSONFieldExtractor:
    """
    Extracts database field definitions from complex JSON structures
    
    The extractor searches for objects that contain the following structure:
    {
        "providedKey": "database.table.field",
        "displayName": "field_name",
        "physicalName": "field_name",
        "dataType": "Character/Integer/etc",
        "isNullable": true/false,
        "format": "varchar/int/etc",
        "description": "Field description"
    }
    """
    
    def __init__(self):
        """Initialize the extractor with required field structure"""
        self.required_keys = {
            'providedKey', 'displayName', 'physicalName', 
            'dataType', 'isNullable', 'format', 'description'
        }
        self.extracted_fields = {}
        self.extraction_stats = {
            'total_fields_found': 0,
            'databases_found': set(),
            'tables_found': set(),
            'extraction_timestamp': datetime.now().isoformat()
        }
    
    def load_json_file(self, file_path: str) -> Dict:
        """
        Load JSON file with comprehensive error handling
        
        Args:
            file_path (str): Path to the JSON file
            
        Returns:
            Dict: Loaded JSON data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If JSON is invalid
            Exception: For other errors
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                print(f"✓ Successfully loaded JSON file: {file_path}")
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise Exception(f"Error loading JSON file: {e}")
    
    def is_field_definition(self, obj: Any) -> bool:
        """
        Check if an object matches the expected field definition structure
        
        Args:
            obj: Object to check
            
        Returns:
            bool: True if object matches field definition structure
        """
        if not isinstance(obj, dict):
            return False
        
        # Check if all required keys are present
        obj_keys = set(obj.keys())
        return self.required_keys.issubset(obj_keys)
    
    def extract_database_from_provided_key(self, provided_key: str) -> Optional[str]:
        """
        Extract database name from providedKey
        
        Assumes format like: "database.table.field" or "table.field"
        
        Args:
            provided_key (str): The providedKey value
            
        Returns:
            Optional[str]: Database name or None
        """
        if not provided_key:
            return None
        
        parts = provided_key.split('.')
        if len(parts) >= 3:
            return parts[0]  # First part is likely database
        elif len(parts) == 2:
            return "default"  # No explicit database, use default
        else:
            return "unknown"
    
    def extract_table_from_provided_key(self, provided_key: str) -> Optional[str]:
        """
        Extract table name from providedKey
        
        Args:
            provided_key (str): The providedKey value
            
        Returns:
            Optional[str]: Table name or None
        """
        if not provided_key:
            return None
        
        parts = provided_key.split('.')
        if len(parts) >= 2:
            return parts[-2]  # Second to last part is likely table
        else:
            return "unknown"
    
    def recursive_extract_fields(self, data: Any, path: str = "root") -> None:
        """
        Recursively search through JSON structure to find field definitions
        
        Args:
            data: JSON data structure to search
            path (str): Current path in the JSON structure (for debugging)
        """
        if isinstance(data, dict):
            # Check if current dict is a field definition
            if self.is_field_definition(data):
                field_name = data.get('displayName', data.get('physicalName', 'unknown'))
                provided_key = data.get('providedKey', '')
                
                # Extract database and table info
                database = self.extract_database_from_provided_key(provided_key)
                table = self.extract_table_from_provided_key(provided_key)
                
                # Update stats
                self.extraction_stats['total_fields_found'] += 1
                if database:
                    self.extraction_stats['databases_found'].add(database)
                if table:
                    self.extraction_stats['tables_found'].add(table)
                
                # Initialize nested dictionaries if they don't exist
                if database not in self.extracted_fields:
                    self.extracted_fields[database] = {}
                if table not in self.extracted_fields[database]:
                    self.extracted_fields[database][table] = {}
                
                # Store the field definition
                self.extracted_fields[database][table][field_name] = {
                    'providedKey': data.get('providedKey'),
                    'displayName': data.get('displayName'),
                    'physicalName': data.get('physicalName'),
                    'dataType': data.get('dataType'),
                    'isNullable': data.get('isNullable'),
                    'format': data.get('format'),
                    'description': data.get('description'),
                    'extraction_path': path  # For debugging purposes
                }
                
                print(f"✓ Found field: {database}.{table}.{field_name}")
            
            # Continue searching in nested dictionaries
            for key, value in data.items():
                self.recursive_extract_fields(value, f"{path}.{key}")
        
        elif isinstance(data, list):
            # Search in list items
            for i, item in enumerate(data):
                self.recursive_extract_fields(item, f"{path}[{i}]")
    
    def filter_by_database(self, database_name: str) -> Dict:
        """
        Filter extracted fields by specific database
        
        Args:
            database_name (str): Name of the database to filter by
            
        Returns:
            Dict: Filtered field definitions for the specified database
        """
        if database_name in self.extracted_fields:
            return {database_name: self.extracted_fields[database_name]}
        else:
            print(f"⚠ Database '{database_name}' not found in extracted data")
            available_dbs = list(self.extracted_fields.keys())
            print(f"Available databases: {available_dbs}")
            return {}
    
    def get_all_databases(self) -> List[str]:
        """
        Get list of all databases found during extraction
        
        Returns:
            List[str]: List of database names
        """
        return list(self.extracted_fields.keys())
    
    def get_tables_for_database(self, database_name: str) -> List[str]:
        """
        Get list of tables for a specific database
        
        Args:
            database_name (str): Name of the database
            
        Returns:
            List[str]: List of table names in the database
        """
        if database_name in self.extracted_fields:
            return list(self.extracted_fields[database_name].keys())
        return []
    
    def get_field_count_by_database(self) -> Dict[str, int]:
        """
        Get field count for each database
        
        Returns:
            Dict[str, int]: Database name to field count mapping
        """
        counts = {}
        for db_name, db_data in self.extracted_fields.items():
            total_fields = sum(len(table_fields) for table_fields in db_data.values())
            counts[db_name] = total_fields
        return counts
    
    def save_results(self, output_path: str, database_filter: Optional[str] = None, 
                    format_type: str = 'json') -> None:
        """
        Save extraction results to file
        
        Args:
            output_path (str): Directory path for output files
            database_filter (Optional[str]): Filter by specific database
            format_type (str): Output format ('json' or 'csv')
        """
        # Prepare data to save
        if database_filter:
            data_to_save = self.filter_by_database(database_filter)
            filename_suffix = f"_{database_filter}"
        else:
            data_to_save = self.extracted_fields
            filename_suffix = "_all"
        
        # Convert sets to lists for JSON serialization
        stats_copy = self.extraction_stats.copy()
        stats_copy['databases_found'] = list(stats_copy['databases_found'])
        stats_copy['tables_found'] = list(stats_copy['tables_found'])
        
        result = {
            'extraction_metadata': stats_copy,
            'field_counts_by_database': self.get_field_count_by_database(),
            'extracted_fields': data_to_save
        }
        
        # Ensure output directory exists
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        if format_type == 'json':
            output_file = Path(output_path) / f"extracted_fields{filename_suffix}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'csv':
            try:
                import pandas as pd
                
                # Flatten data for CSV format
                flattened_data = []
                
                for db_name, db_data in data_to_save.items():
                    for table_name, table_data in db_data.items():
                        for field_name, field_data in table_data.items():
                            row = {
                                'database': db_name,
                                'table': table_name,
                                'field_name': field_name,
                                'providedKey': field_data.get('providedKey'),
                                'displayName': field_data.get('displayName'),
                                'physicalName': field_data.get('physicalName'),
                                'dataType': field_data.get('dataType'),
                                'isNullable': field_data.get('isNullable'),
                                'format': field_data.get('format'),
                                'description': field_data.get('description'),
                                'extraction_path': field_data.get('extraction_path')
                            }
                            flattened_data.append(row)
                
                df = pd.DataFrame(flattened_data)
                output_file = Path(output_path) / f"extracted_fields{filename_suffix}.csv"
                df.to_csv(output_file, index=False)
                
            except ImportError:
                print("⚠ pandas not available. Install pandas to save CSV format: pip install pandas")
                return
        
        print(f"✓ Results saved to: {output_file}")
    
    def print_summary(self):
        """
        Print comprehensive extraction summary
        """
        print("\n" + "="*70)
        print("JSON FIELD EXTRACTION SUMMARY")
        print("="*70)
        print(f"Total fields found: {self.extraction_stats['total_fields_found']}")
        print(f"Databases found: {len(self.extraction_stats['databases_found'])}")
        print(f"Tables found: {len(self.extraction_stats['tables_found'])}")
        print(f"Extraction timestamp: {self.extraction_stats['extraction_timestamp']}")
        
        print(f"\n{'Database':<20} {'Tables':<10} {'Fields':<10}")
        print("-" * 40)
        
        field_counts = self.get_field_count_by_database()
        for db in sorted(self.extraction_stats['databases_found']):
            table_count = len(self.get_tables_for_database(db))
            field_count = field_counts.get(db, 0)
            print(f"{db:<20} {table_count:<10} {field_count:<10}")
        
        print("-" * 40)
        print(f"{'TOTAL':<20} {len(self.extraction_stats['tables_found']):<10} {self.extraction_stats['total_fields_found']:<10}")
    
    def print_detailed_results(self, max_description_length: int = 100):
        """
        Print detailed extraction results
        
        Args:
            max_description_length (int): Maximum length for description display
        """
        print("\n" + "="*70)
        print("DETAILED EXTRACTION RESULTS")
        print("="*70)
        
        for db_name, db_data in self.extracted_fields.items():
            print(f"\n📊 DATABASE: {db_name}")
            print("-" * 50)
            
            for table_name, table_data in db_data.items():
                print(f"\n  📋 TABLE: {table_name}")
                print("  " + "-" * 40)
                
                for field_name, field_data in table_data.items():
                    description = field_data.get('description', 'No description')
                    if len(description) > max_description_length:
                        description = description[:max_description_length] + "..."
                    
                    print(f"    🔹 {field_name}")
                    print(f"      Type: {field_data.get('dataType')} ({field_data.get('format')})")
                    print(f"      Nullable: {field_data.get('isNullable')}")
                    print(f"      Key: {field_data.get('providedKey')}")
                    print(f"      Description: {description}")
                    print()
    
    def extract_from_file(self, json_file_path: str, database_filter: Optional[str] = None) -> Dict:
        """
        Main extraction method
        
        Args:
            json_file_path (str): Path to the JSON file to process
            database_filter (Optional[str]): Filter results by database name
            
        Returns:
            Dict: Extracted field definitions
        """
        print(f"🚀 Starting extraction from: {json_file_path}")
        
        # Load JSON data
        json_data = self.load_json_file(json_file_path)
        
        # Extract fields
        print("🔍 Searching for field definitions...")
        self.recursive_extract_fields(json_data)
        
        # Print summary
        self.print_summary()
        
        # Return filtered results if database specified
        if database_filter:
            return self.filter_by_database(database_filter)
        else:
            return self.extracted_fields

    def extract_all(self, json_file_path: str, output_dir: str = "./output", 
                   database_filter: Optional[str] = None, save_formats: List[str] = ['json'],
                   show_detailed: bool = False, auto_save: bool = True) -> Dict:
        """
        One-step extraction with automatic processing and saving
        
        Args:
            json_file_path (str): Path to the JSON file to process
            output_dir (str): Directory to save results (default: ./output)
            database_filter (Optional[str]): Filter by specific database
            save_formats (List[str]): Formats to save ['json', 'csv'] (default: ['json'])
            show_detailed (bool): Print detailed results (default: False)
            auto_save (bool): Automatically save results (default: True)
            
        Returns:
            Dict: Extracted field definitions
        """
        print("🎯 JSON Field Extractor - One-Step Processing")
        print("=" * 60)
        
        # Extract fields
        results = self.extract_from_file(json_file_path, database_filter)
        
        # Show detailed results if requested
        if show_detailed:
            self.print_detailed_results()
        
        # Auto-save results
        if auto_save:
            for format_type in save_formats:
                self.save_results(output_dir, database_filter, format_type)
        
        # Print completion message
        print(f"\n✅ Processing completed!")
        if auto_save:
            print(f"📁 Results saved to: {output_dir}")
        
        return results


def extract_fields_from_json(json_file_path: str, database_name: Optional[str] = None, 
                           output_dir: str = "./output", formats: List[str] = ['json'], 
                           detailed: bool = False) -> Dict:
    """
    Convenience function to extract fields from JSON file with minimal setup
    
    Args:
        json_file_path (str): Path to your JSON file
        database_name (Optional[str]): Extract only this database (optional)
        output_dir (str): Where to save results (default: ./output)
        formats (List[str]): Save formats ['json', 'csv'] (default: ['json'])
        detailed (bool): Show detailed output (default: False)
    
    Returns:
        Dict: Extracted field definitions
        
    Example:
        # Simple extraction - just provide file path
        fields = extract_fields_from_json("my_data.json")
        
        # Extract specific database and save as CSV
        fields = extract_fields_from_json("my_data.json", 
                                        database_name="finance_db",
                                        formats=['json', 'csv'])
    """
    extractor = JSONFieldExtractor()
    return extractor.extract_all(
        json_file_path=json_file_path,
        output_dir=output_dir,
        database_filter=database_name,
        save_formats=formats,
        show_detailed=detailed
    )


def quick_extract(json_file_path: str) -> Dict:
    """
    Ultra-simple extraction - just provide the JSON file path
    
    Args:
        json_file_path (str): Path to your JSON file
        
    Returns:
        Dict: Extracted field definitions
        
    Example:
        # Extract everything with default settings
        results = quick_extract("my_schema.json")
    """
    return extract_fields_from_json(json_file_path)


def main():
    """
    Command line interface for the JSON Field Extractor
    """
    parser = argparse.ArgumentParser(
        description="Extract database field definitions from JSON files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python json_field_extractor.py data.json
  python json_field_extractor.py data.json --database finance_db
  python json_field_extractor.py data.json --format csv --output ./results
        """
    )
    
    parser.add_argument(
        "json_file", 
        help="Path to the JSON file to process"
    )
    parser.add_argument(
        "--database", "-d",
        help="Filter results by specific database name"
    )
    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Output directory for results (default: ./output)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=['json', 'csv'],
        default='json',
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--detailed", 
        action='store_true',
        help="Print detailed results to console"
    )
    parser.add_argument(
        "--quiet", "-q",
        action='store_true',
        help="Suppress verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"✗ Error: JSON file not found: {args.json_file}")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    try:
        os.makedirs(args.output, exist_ok=True)
    except Exception as e:
        print(f"✗ Error creating output directory: {e}")
        sys.exit(1)
    
    # Initialize extractor
    extractor = JSONFieldExtractor()
    
    try:
        # Perform extraction
        results = extractor.extract_from_file(args.json_file, args.database)
        
        # Print detailed results if requested
        if args.detailed and not args.quiet:
            extractor.print_detailed_results()
        
        # Save results
        extractor.save_results(args.output, args.database, args.format)
        
        if not args.quiet:
            print(f"\n✅ Extraction completed successfully!")
            print(f"📁 Results saved to: {args.output}")
        
    except Exception as e:
        print(f"✗ Error during extraction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 