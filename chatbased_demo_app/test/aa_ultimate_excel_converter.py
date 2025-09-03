#!/usr/bin/env python3
"""
Ultimate AA Member Test Data Excel Converter
Converts the comprehensive test data into organized Excel sheets
"""

import json
import pandas as pd
from datetime import datetime
import os

class AAUltimateExcelConverter:
    def __init__(self, json_file='aa_ultimate_test_data.json'):
        self.json_file = json_file
        self.test_data = []
        self.load_data()
    
    def load_data(self):
        """Load test data from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
            print(f"📊 Loaded {len(self.test_data)} test records from {self.json_file}")
        except FileNotFoundError:
            print(f"❌ File {self.json_file} not found!")
            return
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return
    
    def convert_to_excel(self, output_file='AA_Ultimate_Test_Data.xlsx'):
        """Convert test data to comprehensive Excel file"""
        if not self.test_data:
            print("❌ No test data to convert!")
            return
        
        print(f"🔄 Converting {len(self.test_data)} records to Excel...")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 1. All Test Data Summary
            self.create_summary_sheet(writer)
            
            # 2. AA Member Matching Criteria Sheets
            self.create_matching_criteria_sheets(writer)
            
            # 3. Data Quality Test Sheets
            self.create_data_quality_sheets(writer)
            
            # 4. Date Format Test Sheets
            self.create_date_format_sheets(writer)
            
            # 5. Special Character Test Sheets
            self.create_special_character_sheets(writer)
            
            # 6. Email Format Test Sheets
            self.create_email_format_sheets(writer)
            
            # 7. Phone Number Test Sheets
            self.create_phone_test_sheets(writer)
            
            # 8. Postal Code Test Sheets
            self.create_postal_test_sheets(writer)
            
            # 9. Edge Case Test Sheets
            self.create_edge_case_sheets(writer)
            
            # 10. Validation Results Sheet
            self.create_validation_results_sheet(writer)
        
        print(f"✅ Excel file created: {output_file}")
        self.print_excel_structure(output_file)
    
    def create_summary_sheet(self, writer):
        """Create summary sheet with overview statistics"""
        summary_data = []
        
        # Scenario distribution
        scenario_counts = {}
        for record in self.test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        for scenario, count in sorted(scenario_counts.items()):
            summary_data.append({
                'Scenario': scenario,
                'Count': count,
                'Percentage': round((count / len(self.test_data)) * 100, 2)
            })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add metadata
        metadata = pd.DataFrame([
            {'Metric': 'Total Records', 'Value': len(self.test_data)},
            {'Metric': 'Generation Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Metric': 'Unique Scenarios', 'Value': len(scenario_counts)},
            {'Metric': 'Data Quality Tests', 'Value': len([r for r in self.test_data if 'DataQuality' in r['scenario']])},
            {'Metric': 'Edge Cases', 'Value': len([r for r in self.test_data if 'UltimateEdgeCase' in r['scenario']])},
            {'Metric': 'Invalid Scenarios', 'Value': len([r for r in self.test_data if r['scenario'] == 'Invalid'])}
        ])
        metadata.to_excel(writer, sheet_name='Metadata', index=False)
    
    def create_matching_criteria_sheets(self, writer):
        """Create sheets for each matching criteria scenario"""
        matching_scenarios = ['Match1', 'Match2', 'Match3', 'Match4', 'Match5', 
                             'Match6', 'Match7', 'Match8', 'Match9', 'Match10', 'Invalid']
        
        for scenario in matching_scenarios:
            scenario_records = [r for r in self.test_data if r['scenario'] == scenario]
            if scenario_records:
                self.create_scenario_sheet(writer, scenario, scenario_records)
    
    def create_scenario_sheet(self, writer, scenario_name, records):
        """Create a sheet for a specific scenario"""
        sheet_data = []
        
        for i, record in enumerate(records):
            row = {
                'Record_ID': i + 1,
                'Scenario': record['scenario'],
                'Description': record['description'],
                'Expected_Result': record['expected_result']
            }
            
            # Add AA record fields
            if 'aa_record' in record:
                aa_record = record['aa_record']
                for key, value in aa_record.items():
                    row[f'AA_{key}'] = value
            
            # Add application record fields
            if 'application_record' in record:
                app_record = record['application_record']
                for key, value in app_record.items():
                    row[f'APP_{key}'] = value
            
            # Add test-specific fields
            for key in ['date_format', 'name_type', 'address_type', 'email_format', 
                       'phone_type', 'postal_type', 'special_char_category', 'test_value', 
                       'field_type', 'test_date', 'test_email', 'test_phone', 'test_postal']:
                if key in record:
                    row[key] = record[key]
            
            sheet_data.append(row)
        
        df = pd.DataFrame(sheet_data)
        df.to_excel(writer, sheet_name=scenario_name, index=False)
    
    def create_data_quality_sheets(self, writer):
        """Create sheets for data quality tests"""
        data_quality_records = [r for r in self.test_data if 'DataQuality' in r['scenario']]
        
        if data_quality_records:
            # Group by test type
            date_tests = [r for r in data_quality_records if 'Date' in r['scenario']]
            special_char_tests = [r for r in data_quality_records if 'SpecialChar' in r['scenario']]
            email_tests = [r for r in data_quality_records if 'Email' in r['scenario']]
            
            if date_tests:
                self.create_scenario_sheet(writer, 'DataQuality_Date', date_tests)
            if special_char_tests:
                self.create_scenario_sheet(writer, 'DataQuality_SpecialChar', special_char_tests)
            if email_tests:
                self.create_scenario_sheet(writer, 'DataQuality_Email', email_tests)
    
    def create_date_format_sheets(self, writer):
        """Create sheets for date format tests"""
        date_test_records = [r for r in self.test_data if 'DateTest' in r['scenario']]
        
        if date_test_records:
            # Group by date format
            date_formats = {}
            for record in date_test_records:
                date_format = record.get('date_format', 'unknown')
                if date_format not in date_formats:
                    date_formats[date_format] = []
                date_formats[date_format].append(record)
            
            for date_format, records in date_formats.items():
                sheet_name = f'DateTest_{date_format}'[:31]  # Excel sheet name limit
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_special_character_sheets(self, writer):
        """Create sheets for special character tests"""
        special_char_records = [r for r in self.test_data if 'SpecialCharTest' in r['scenario']]
        
        if special_char_records:
            # Group by category
            categories = {}
            for record in special_char_records:
                category = record.get('special_char_category', 'unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(record)
            
            for category, records in categories.items():
                sheet_name = f'SpecialChar_{category}'[:31]
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_email_format_sheets(self, writer):
        """Create sheets for email format tests"""
        email_test_records = [r for r in self.test_data if 'EmailTest' in r['scenario']]
        
        if email_test_records:
            # Group by email format
            email_formats = {}
            for record in email_test_records:
                email_format = record.get('email_format', 'unknown')
                if email_format not in email_formats:
                    email_formats[email_format] = []
                email_formats[email_format].append(record)
            
            for email_format, records in email_formats.items():
                sheet_name = f'EmailTest_{email_format}'[:31]
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_phone_test_sheets(self, writer):
        """Create sheets for phone number tests"""
        phone_test_records = [r for r in self.test_data if 'PhoneTest' in r['scenario']]
        
        if phone_test_records:
            # Group by phone type
            phone_types = {}
            for record in phone_test_records:
                phone_type = record.get('phone_type', 'unknown')
                if phone_type not in phone_types:
                    phone_types[phone_type] = []
                phone_types[phone_type].append(record)
            
            for phone_type, records in phone_types.items():
                sheet_name = f'PhoneTest_{phone_type}'[:31]
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_postal_test_sheets(self, writer):
        """Create sheets for postal code tests"""
        postal_test_records = [r for r in self.test_data if 'PostalTest' in r['scenario']]
        
        if postal_test_records:
            # Group by postal type
            postal_types = {}
            for record in postal_test_records:
                postal_type = record.get('postal_type', 'unknown')
                if postal_type not in postal_types:
                    postal_types[postal_type] = []
                postal_types[postal_type].append(record)
            
            for postal_type, records in postal_types.items():
                sheet_name = f'PostalTest_{postal_type}'[:31]
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_edge_case_sheets(self, writer):
        """Create sheets for edge case tests"""
        edge_case_records = [r for r in self.test_data if 'UltimateEdgeCase' in r['scenario']]
        
        if edge_case_records:
            # Group by edge case type
            edge_case_types = {}
            for record in edge_case_records:
                edge_case_type = record['scenario'].replace('UltimateEdgeCase_', '')
                if edge_case_type not in edge_case_types:
                    edge_case_types[edge_case_type] = []
                edge_case_types[edge_case_type].append(record)
            
            for edge_case_type, records in edge_case_types.items():
                sheet_name = f'EdgeCase_{edge_case_type}'[:31]
                self.create_scenario_sheet(writer, sheet_name, records)
    
    def create_validation_results_sheet(self, writer):
        """Create validation results summary sheet"""
        validation_data = []
        
        # Count validation results by scenario type
        scenario_validation = {}
        for record in self.test_data:
            scenario = record['scenario']
            expected_result = record.get('expected_result', 'Unknown')
            
            if scenario not in scenario_validation:
                scenario_validation[scenario] = {}
            if expected_result not in scenario_validation[scenario]:
                scenario_validation[scenario][expected_result] = 0
            scenario_validation[scenario][expected_result] += 1
        
        for scenario, results in scenario_validation.items():
            for expected_result, count in results.items():
                validation_data.append({
                    'Scenario': scenario,
                    'Expected_Result': expected_result,
                    'Count': count,
                    'Validation_Status': 'PASS' if expected_result in ['Valid', 'Match1', 'Match2', 'Match3', 'Match4', 'Match5', 'Match6', 'Match7', 'Match8', 'Match9', 'Match10'] else 'FAIL'
                })
        
        df_validation = pd.DataFrame(validation_data)
        df_validation.to_excel(writer, sheet_name='Validation_Results', index=False)
    
    def print_excel_structure(self, excel_file):
        """Print the structure of the created Excel file"""
        try:
            xl_file = pd.ExcelFile(excel_file)
            print(f"\n📋 Excel File Structure: {excel_file}")
            print("=" * 50)
            print("Sheets created:")
            for i, sheet_name in enumerate(xl_file.sheet_names, 1):
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                print(f"  {i:2d}. {sheet_name:<30} ({len(df):>4} rows, {len(df.columns):>2} columns)")
            print("=" * 50)
        except Exception as e:
            print(f"❌ Error reading Excel structure: {e}")

if __name__ == "__main__":
    converter = AAUltimateExcelConverter()
    converter.convert_to_excel()
