#!/usr/bin/env python3
"""
Validate the integration of georef data with comprehensive test data
"""

import json
from collections import Counter

def validate_georef_integration(file_path):
    """Validate the georef integration in the comprehensive test data"""
    print("🔍 Validating georef data integration...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} records for validation")
        
        # Validation metrics
        cities = []
        zip_codes = []
        states = []
        counties = []
        
        # Check for real georef data presence
        georef_fields_present = 0
        total_records = 0
        
        for record in data:
            if 'aa_record' in record:
                total_records += 1
                
                # Check if georef fields are present
                if all(field in record['aa_record'] for field in ['CITY_NM', 'POSTAL_CD', 'STATE_CD', 'STATE_NM', 'COUNTY_NM']):
                    georef_fields_present += 1
                    
                    cities.append(record['aa_record']['CITY_NM'])
                    zip_codes.append(record['aa_record']['POSTAL_CD'])
                    states.append(record['aa_record']['STATE_CD'])
                    counties.append(record['aa_record']['COUNTY_NM'])
        
        # Generate validation report
        print("\n📊 VALIDATION REPORT")
        print("=" * 50)
        print(f"Total AA Records: {total_records}")
        print(f"Records with Georef Data: {georef_fields_present}")
        print(f"Georef Integration Rate: {(georef_fields_present/total_records)*100:.1f}%")
        
        print(f"\nUnique Cities: {len(set(cities))}")
        print(f"Unique Zip Codes: {len(set(zip_codes))}")
        print(f"Unique States: {len(set(states))}")
        print(f"Unique Counties: {len(set(counties))}")
        
        # Show edge case breakdown
        edge_case_scenarios = ['EdgeCase_', 'DataQuality_', 'Invalid']
        edge_case_records = sum(1 for record in data if any(scenario in record.get('scenario', '') for scenario in edge_case_scenarios))
        non_edge_case_records = total_records - edge_case_records
        
        print(f"\nEdge Case Records: {edge_case_records}")
        print(f"Regular Records: {non_edge_case_records}")
        
        # Show sample data
        print("\n📋 SAMPLE DATA:")
        print("-" * 30)
        for i, record in enumerate(data[:5]):
            if 'aa_record' in record:
                aa_record = record['aa_record']
                print(f"Record {i+1}:")
                print(f"  City: {aa_record.get('CITY_NM', 'N/A')}")
                print(f"  Zip: {aa_record.get('POSTAL_CD', 'N/A')}")
                print(f"  State: {aa_record.get('STATE_CD', 'N/A')} - {aa_record.get('STATE_NM', 'N/A')}")
                print(f"  County: {aa_record.get('COUNTY_NM', 'N/A')}")
                print(f"  Population: {aa_record.get('POPULATION', 'N/A')}")
                print(f"  Timezone: {aa_record.get('TIMEZONE', 'N/A')}")
                print()
        
        # Check for data quality issues
        print("🔍 DATA QUALITY CHECKS:")
        print("-" * 30)
        
        # Check for empty or invalid data
        empty_cities = sum(1 for city in cities if not city or city == 'Unknown City')
        empty_zips = sum(1 for zip_code in zip_codes if not zip_code or zip_code == '00000')
        empty_states = sum(1 for state in states if not state or state == 'XX')
        
        print(f"Empty/Invalid Cities: {empty_cities}")
        print(f"Empty/Invalid Zip Codes: {empty_zips}")
        print(f"Empty/Invalid States: {empty_states}")
        
        # Check zip code format (should be 5 digits)
        invalid_zips = sum(1 for zip_code in zip_codes if not zip_code.isdigit() or len(zip_code) != 5)
        print(f"Invalid Zip Code Format: {invalid_zips}")
        
        # Show most common cities and states
        print("\n🏙️ MOST COMMON CITIES:")
        city_counts = Counter(cities)
        for city, count in city_counts.most_common(10):
            print(f"  {city}: {count} records")
        
        print("\n🗺️ MOST COMMON STATES:")
        state_counts = Counter(states)
        for state, count in state_counts.most_common(10):
            print(f"  {state}: {count} records")
        
        # Overall validation result - be more lenient for edge cases and data quality scenarios
        # These scenarios may intentionally have missing or invalid data
        edge_case_scenarios = ['EdgeCase_', 'DataQuality_', 'Invalid']
        edge_case_records = sum(1 for record in data if any(scenario in record.get('scenario', '') for scenario in edge_case_scenarios))
        
        # For non-edge case records, all should have georef data
        non_edge_case_records = total_records - edge_case_records
        non_edge_case_with_georef = georef_fields_present - edge_case_records
        
        validation_passed = (
            non_edge_case_with_georef >= non_edge_case_records * 0.95 and  # 95% of non-edge cases should have georef data
            empty_cities == 0 and
            empty_zips == 0 and
            empty_states == 0 and
            invalid_zips == 0
        )
        
        print(f"\n✅ VALIDATION RESULT: {'PASSED' if validation_passed else 'FAILED'}")
        
        return validation_passed
        
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False

def main():
    """Main validation function"""
    print("🚀 Starting Georef Integration Validation")
    print("=" * 50)
    
    # File paths to validate
    files_to_validate = [
        "/Applications/Mapping/chatbased_demo_app/test/aa_comprehensive_test_data_with_georef.json",
        "/Applications/Mapping/chatbased_demo_app/test/aa_comprehensive_test_data_with_georef_enhanced.json"
    ]
    
    all_passed = True
    
    for file_path in files_to_validate:
        print(f"\n📁 Validating: {file_path}")
        print("-" * 50)
        
        try:
            passed = validate_georef_integration(file_path)
            all_passed = all_passed and passed
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            all_passed = False
    
    print(f"\n🎯 OVERALL VALIDATION RESULT: {'PASSED' if all_passed else 'FAILED'}")
    
    if all_passed:
        print("🎉 All georef integrations are working correctly!")
    else:
        print("⚠️ Some validation issues were found. Please review the output above.")

if __name__ == "__main__":
    main()
