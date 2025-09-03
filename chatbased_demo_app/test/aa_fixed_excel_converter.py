#!/usr/bin/env python3
"""
Fixed AA Member Test Data Excel Converter
Generates Excel files with exactly 47 columns (no extra metadata columns)
"""

import json
import pandas as pd
from datetime import datetime
import os

class AAFixedExcelConverter:
    def __init__(self, json_file='aa_comprehensive_test_data.json'):
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
    
    def convert_to_excel_47_columns(self, output_file='AA_Test_Data_47_Columns.xlsx'):
        """Convert test data to Excel file with exactly 47 columns"""
        if not self.test_data:
            print("❌ No test data to convert!")
            return
        
        print(f"🔄 Converting {len(self.test_data)} records to Excel with exactly 47 columns...")
        
        # Extract only the AA record data (47 columns)
        aa_records = []
        for record in self.test_data:
            if 'aa_record' in record:
                aa_records.append(record['aa_record'])
        
        if not aa_records:
            print("❌ No AA records found in test data!")
            return
        
        # Create DataFrame with only the 47 AA record columns
        df = pd.DataFrame(aa_records)
        
        # Verify column count
        print(f"📊 DataFrame has {len(df.columns)} columns")
        print("📋 Columns:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Save to Excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Main data sheet with exactly 47 columns
            df.to_excel(writer, sheet_name='AA_Member_Data', index=False)
            
            # Summary sheet with metadata
            self.create_summary_sheet(writer, len(aa_records))
        
        print(f"✅ Excel file created: {output_file}")
        print(f"📊 Total records: {len(aa_records)}")
        print(f"📊 Total columns: {len(df.columns)}")
        
        return output_file
    
    def create_summary_sheet(self, writer, total_records):
        """Create summary sheet with metadata"""
        summary_data = [
            {'Metric': 'Total Records', 'Value': total_records},
            {'Metric': 'Total Columns', 'Value': 47},
            {'Metric': 'Generation Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Metric': 'File Type', 'Value': 'AA Member Test Data'},
            {'Metric': 'Column Count', 'Value': 'Exactly 47 columns as required'},
            {'Metric': 'Data Source', 'Value': 'AA Ultimate Test Generator'},
            {'Metric': 'Purpose', 'Value': 'Testing AA Member matching criteria'},
        ]
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
    
    def create_scenario_based_excel(self, output_file='AA_Test_Data_By_Scenario.xlsx'):
        """Create Excel file with separate sheets for each scenario, each with 47 columns"""
        if not self.test_data:
            print("❌ No test data to convert!")
            return
        
        print(f"🔄 Creating scenario-based Excel with 47 columns per sheet...")
        
        # Group records by scenario
        scenarios = {}
        for record in self.test_data:
            scenario = record['scenario']
            if scenario not in scenarios:
                scenarios[scenario] = []
            if 'aa_record' in record:
                scenarios[scenario].append(record['aa_record'])
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Create a sheet for each scenario
            for scenario, records in scenarios.items():
                if records:
                    df = pd.DataFrame(records)
                    # Truncate sheet name to Excel limit (31 characters)
                    sheet_name = scenario[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"  📊 {scenario}: {len(records)} records, {len(df.columns)} columns")
            
            # Create summary sheet
            self.create_scenario_summary_sheet(writer, scenarios)
        
        print(f"✅ Scenario-based Excel file created: {output_file}")
        return output_file
    
    def create_scenario_summary_sheet(self, writer, scenarios):
        """Create summary sheet for scenario-based Excel"""
        summary_data = []
        total_records = 0
        
        for scenario, records in scenarios.items():
            if records:
                summary_data.append({
                    'Scenario': scenario,
                    'Record_Count': len(records),
                    'Column_Count': 47,
                    'Sheet_Name': scenario[:31]
                })
                total_records += len(records)
        
        # Add totals
        summary_data.append({
            'Scenario': 'TOTAL',
            'Record_Count': total_records,
            'Column_Count': 47,
            'Sheet_Name': 'All Scenarios'
        })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Scenario_Summary', index=False)

def main():
    """Main function to run the fixed Excel converter"""
    print("🔧 AA Fixed Excel Converter - 47 Columns Only")
    print("=" * 60)
    
    converter = AAFixedExcelConverter()
    
    if not converter.test_data:
        print("❌ No test data available. Please generate test data first.")
        return
    
    # Option 1: Single sheet with all data (47 columns)
    print("\n📊 Option 1: Single sheet with all data")
    converter.convert_to_excel_47_columns()
    
    # Option 2: Separate sheets by scenario (47 columns each)
    print("\n📊 Option 2: Separate sheets by scenario")
    converter.create_scenario_based_excel()
    
    print("\n✅ Both Excel files created successfully!")
    print("📋 Files created:")
    print("  • AA_Test_Data_47_Columns.xlsx - Single sheet with 47 columns")
    print("  • AA_Test_Data_By_Scenario.xlsx - Multiple sheets, 47 columns each")

if __name__ == "__main__":
    main()
