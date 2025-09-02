#!/usr/bin/env python3
"""
AA Member Test Data Excel Converter - Windows Compatible
Converts JSON test data to organized Excel workbook with multiple sheets
"""

import json
import pandas as pd
from datetime import datetime
import os
import sys

class AATestDataExcelConverterWindows:
    def __init__(self, json_file='aa_comprehensive_test_data_windows.json'):
        self.json_file = json_file
        self.excel_file = 'AA_Member_Test_Data_Windows.xlsx'
        
        # Load the test data
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {json_file} not found!")
            print("Please run 'python aa_comprehensive_generator_windows.py' first.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading {json_file}: {e}")
            sys.exit(1)
        
        print(f"📊 Loaded {len(self.test_data)} test records from {json_file}")
    
    def convert_to_excel(self):
        """Convert test data to Excel with multiple organized sheets"""
        print("🔄 Converting test data to Excel format (Windows Compatible)...")
        
        # Create Excel writer object
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            
            # 1. Summary Sheet
            self.create_summary_sheet(writer)
            
            # 2. All Test Data Sheet
            self.create_all_data_sheet(writer)
            
            # 3. Scenario-specific sheets
            self.create_scenario_sheets(writer)
            
            # 4. Data Quality Tests Sheet
            self.create_data_quality_sheet(writer)
            
            # 5. Edge Cases Sheet
            self.create_edge_cases_sheet(writer)
            
            # 6. Validation Results Sheet
            self.create_validation_sheet(writer)
        
        print(f"✅ Excel file created: {self.excel_file}")
        return self.excel_file
    
    def create_summary_sheet(self, writer):
        """Create summary sheet with statistics"""
        print("📋 Creating summary sheet...")
        
        # Calculate statistics
        scenario_counts = {}
        for record in self.test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        # Create summary data
        summary_data = []
        for scenario, count in sorted(scenario_counts.items()):
            summary_data.append({
                'Scenario': scenario,
                'Count': count,
                'Percentage': round((count / len(self.test_data)) * 100, 2),
                'Description': self.get_scenario_description(scenario)
            })
        
        # Add totals
        summary_data.append({
            'Scenario': 'TOTAL',
            'Count': len(self.test_data),
            'Percentage': 100.0,
            'Description': 'Total test records'
        })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add metadata
        metadata = pd.DataFrame([
            {'Field': 'Generated Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Field': 'Total Records', 'Value': len(self.test_data)},
            {'Field': 'Scenarios Covered', 'Value': len(scenario_counts)},
            {'Field': 'Data Quality Tests', 'Value': len([r for r in self.test_data if r['scenario'].startswith('DataQuality')])},
            {'Field': 'Edge Cases', 'Value': len([r for r in self.test_data if r['scenario'].startswith('EdgeCase')])},
            {'Field': 'Platform', 'Value': 'Windows Compatible'}
        ])
        metadata.to_excel(writer, sheet_name='Summary', startrow=len(summary_data) + 3, index=False)
    
    def create_all_data_sheet(self, writer):
        """Create sheet with all test data flattened"""
        print("📊 Creating all data sheet...")
        
        all_data = []
        for i, record in enumerate(self.test_data):
            row = {
                'Record_ID': i + 1,
                'Scenario': record['scenario'],
                'Description': record['description'],
                'Expected_Result': record.get('expected_result', 'N/A')
            }
            
            # Add AA record fields
            aa_record = record.get('aa_record', {})
            for key, value in aa_record.items():
                row[f'AA_{key}'] = value
            
            # Add application record fields if present
            app_record = record.get('application_record', {})
            for key, value in app_record.items():
                row[f'APP_{key}'] = value
            
            all_data.append(row)
        
        df_all = pd.DataFrame(all_data)
        df_all.to_excel(writer, sheet_name='All_Test_Data', index=False)
    
    def create_scenario_sheets(self, writer):
        """Create separate sheets for each matching scenario"""
        print("📋 Creating scenario-specific sheets...")
        
        # Group data by scenario
        scenario_groups = {}
        for record in self.test_data:
            scenario = record['scenario']
            if scenario not in scenario_groups:
                scenario_groups[scenario] = []
            scenario_groups[scenario].append(record)
        
        # Create sheets for main matching scenarios
        main_scenarios = ['Match1', 'Match2', 'Match3', 'Match4', 'Match5', 
                         'Match6', 'Match7', 'Match8', 'Match9', 'Match10', 'Invalid']
        
        for scenario in main_scenarios:
            if scenario in scenario_groups:
                print(f"  📄 Creating {scenario} sheet...")
                self.create_scenario_sheet(writer, scenario, scenario_groups[scenario])
    
    def create_scenario_sheet(self, writer, scenario, records):
        """Create a sheet for a specific scenario"""
        sheet_data = []
        
        for i, record in enumerate(records):
            row = {
                'Record_ID': i + 1,
                'Description': record['description'],
                'Expected_Result': record.get('expected_result', scenario)
            }
            
            # Add AA record fields
            aa_record = record.get('aa_record', {})
            for key, value in aa_record.items():
                row[f'AA_{key}'] = value
            
            # Add application record fields if present
            app_record = record.get('application_record', {})
            for key, value in app_record.items():
                row[f'APP_{key}'] = value
            
            sheet_data.append(row)
        
        df_scenario = pd.DataFrame(sheet_data)
        df_scenario.to_excel(writer, sheet_name=scenario, index=False)
    
    def create_data_quality_sheet(self, writer):
        """Create sheet for data quality test scenarios"""
        print("🔍 Creating data quality tests sheet...")
        
        quality_records = [r for r in self.test_data if r['scenario'].startswith('DataQuality')]
        
        quality_data = []
        for i, record in enumerate(quality_records):
            row = {
                'Test_ID': i + 1,
                'Test_Name': record['scenario'],
                'Description': record['description'],
                'Expected_Result': record.get('expected_result', 'Data Quality Error')
            }
            
            # Add AA record fields
            aa_record = record.get('aa_record', {})
            for key, value in aa_record.items():
                row[f'AA_{key}'] = value
            
            quality_data.append(row)
        
        df_quality = pd.DataFrame(quality_data)
        df_quality.to_excel(writer, sheet_name='Data_Quality_Tests', index=False)
    
    def create_edge_cases_sheet(self, writer):
        """Create sheet for edge case scenarios"""
        print("🔬 Creating edge cases sheet...")
        
        edge_records = [r for r in self.test_data if r['scenario'].startswith('EdgeCase')]
        
        edge_data = []
        for i, record in enumerate(edge_records):
            row = {
                'Case_ID': i + 1,
                'Case_Type': record['scenario'],
                'Description': record['description'],
                'Expected_Result': record.get('expected_result', 'Edge Case')
            }
            
            # Add AA record fields
            aa_record = record.get('aa_record', {})
            for key, value in aa_record.items():
                row[f'AA_{key}'] = value
            
            edge_data.append(row)
        
        df_edge = pd.DataFrame(edge_data)
        df_edge.to_excel(writer, sheet_name='Edge_Cases', index=False)
    
    def create_validation_sheet(self, writer):
        """Create sheet with validation results and test cases"""
        print("✅ Creating validation results sheet...")
        
        # Create test case matrix
        test_cases = []
        
        # Matching criteria test cases
        matching_criteria = [
            'First Name Match', 'Last Name Match', 'AAdvantage Number Match',
            'DOB Match', 'Email Match', 'Phone Match', 'Address Match',
            'City Match', 'Postal Code Match'
        ]
        
        scenarios = ['Match1', 'Match2', 'Match3', 'Match4', 'Match5', 
                    'Match6', 'Match7', 'Match8', 'Match9', 'Match10']
        
        for scenario in scenarios:
            for criteria in matching_criteria:
                test_cases.append({
                    'Scenario': scenario,
                    'Test_Criteria': criteria,
                    'Expected_Result': 'PASS' if self.should_criteria_pass(scenario, criteria) else 'FAIL',
                    'Test_Type': 'Functional',
                    'Priority': 'High' if scenario in ['Match1', 'Match2', 'Match3'] else 'Medium'
                })
        
        # Data quality test cases
        quality_tests = [
            'Null First Name', 'Null Last Name', 'Null DOB', 'Empty AA Number',
            'Invalid DOB Format', 'Invalid Phone Format', 'Invalid Email Format',
            'Invalid Postal Code', 'Long Names', 'Long Addresses', 'Special Characters'
        ]
        
        for test in quality_tests:
            test_cases.append({
                'Scenario': 'DataQuality',
                'Test_Criteria': test,
                'Expected_Result': 'ERROR',
                'Test_Type': 'Data Quality',
                'Priority': 'High'
            })
        
        df_validation = pd.DataFrame(test_cases)
        df_validation.to_excel(writer, sheet_name='Validation_Matrix', index=False)
    
    def should_criteria_pass(self, scenario, criteria):
        """Determine if a criteria should pass for a given scenario"""
        criteria_map = {
            'Match1': ['First Name Match', 'Last Name Match', 'AAdvantage Number Match', 'DOB Match'],
            'Match2': ['First Name Match', 'AAdvantage Number Match', 'Email Match', 'DOB Match'],
            'Match3': ['First Name Match', 'AAdvantage Number Match', 'Phone Match', 'DOB Match'],
            'Match4': ['First Name Match', 'AAdvantage Number Match', 'Address Match', 'City Match', 'DOB Match'],
            'Match5': ['First Name Match', 'Last Name Match', 'Email Match', 'DOB Match'],
            'Match6': ['First Name Match', 'Last Name Match', 'Email Match', 'DOB Match'],
            'Match7': ['First Name Match', 'Last Name Match', 'Phone Match', 'DOB Match'],
            'Match8': ['First Name Match', 'Last Name Match', 'Phone Match', 'DOB Match'],
            'Match9': ['First Name Match', 'Last Name Match', 'Address Match', 'City Match', 'Postal Code Match', 'DOB Match'],
            'Match10': ['First Name Match', 'Last Name Match', 'Address Match', 'City Match', 'Postal Code Match', 'DOB Match']
        }
        
        return criteria in criteria_map.get(scenario, [])
    
    def get_scenario_description(self, scenario):
        """Get description for a scenario"""
        descriptions = {
            'Match1': 'Perfect match - all key fields align',
            'Match2': 'Last name mismatch but other key fields match',
            'Match3': 'Last name and email mismatch but phone matches',
            'Match4': 'Only address matches with valid AA number',
            'Match5': 'Email match with invalid AA number (single record)',
            'Match6': 'Email match with invalid AA number (multiple records)',
            'Match7': 'Phone match with invalid AA number (single record)',
            'Match8': 'Phone match with invalid AA number (multiple records)',
            'Match9': 'Address match with invalid AA number (single record)',
            'Match10': 'Address match with invalid AA number (multiple records)',
            'Invalid': 'No matching criteria met'
        }
        
        if scenario.startswith('DataQuality'):
            return 'Data quality validation test'
        elif scenario.startswith('EdgeCase'):
            return 'Edge case and boundary condition test'
        else:
            return descriptions.get(scenario, 'Unknown scenario')
    
    def get_file_size(self, filename):
        """Get file size in MB"""
        size_bytes = os.path.getsize(filename)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)

if __name__ == "__main__":
    print("🚀 AA Member Test Data Excel Converter (Windows Compatible)")
    print("=" * 60)
    
    converter = AATestDataExcelConverterWindows()
    excel_file = converter.convert_to_excel()
    
    file_size = converter.get_file_size(excel_file)
    
    print(f"\n📊 CONVERSION SUMMARY:")
    print(f"✅ Excel file created: {excel_file}")
    print(f"📁 File size: {file_size} MB")
    print(f"📋 Sheets created: 7 (Summary, All_Test_Data, Match1-10, Data_Quality_Tests, Edge_Cases, Validation_Matrix)")
    print(f"📊 Total records: {len(converter.test_data)}")
    
    print(f"\n🎉 Conversion completed successfully!")
    print(f"📂 You can now open {excel_file} in Excel or any spreadsheet application.")
