#!/usr/bin/env python3
"""
Extract City Names and Zip Codes from Georef JSON and Integrate with Comprehensive Data
"""

import json
import random
from typing import List, Dict, Any

def extract_georef_data(georef_file_path: str) -> List[Dict[str, str]]:
    """
    Extract city names and zip codes from the georef JSON file
    """
    print("🔍 Extracting city names and zip codes from georef data...")
    
    try:
        with open(georef_file_path, 'r', encoding='utf-8') as f:
            georef_data = json.load(f)
        
        extracted_data = []
        for record in georef_data:
            if 'usps_city' in record and 'zip_code' in record:
                extracted_data.append({
                    'city_name': record['usps_city'],
                    'zip_code': record['zip_code'],
                    'state_code': record.get('stusps_code', ''),
                    'state_name': record.get('ste_name', ''),
                    'county_name': record.get('primary_coty_name', ''),
                    'population': record.get('population', 0),
                    'density': record.get('density', 0),
                    'timezone': record.get('timezone', ''),
                    'coordinates': record.get('geo_point_2d', {})
                })
        
        print(f"✅ Extracted {len(extracted_data)} city/zip combinations")
        return extracted_data
        
    except Exception as e:
        print(f"❌ Error extracting georef data: {e}")
        return []

def load_comprehensive_data(comprehensive_file_path: str) -> List[Dict[str, Any]]:
    """
    Load the existing comprehensive test data
    """
    print("📂 Loading comprehensive test data...")
    
    try:
        with open(comprehensive_file_path, 'r', encoding='utf-8') as f:
            comprehensive_data = json.load(f)
        
        print(f"✅ Loaded {len(comprehensive_data)} comprehensive test records")
        return comprehensive_data
        
    except Exception as e:
        print(f"❌ Error loading comprehensive data: {e}")
        return []

def integrate_georef_data(comprehensive_data: List[Dict[str, Any]], georef_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Integrate georef data into comprehensive test data
    """
    print("🔗 Integrating georef data with comprehensive test data...")
    
    # Create a mapping of zip codes to city data for quick lookup
    zip_to_city = {}
    for georef_record in georef_data:
        zip_code = georef_record['zip_code']
        if zip_code not in zip_to_city:
            zip_to_city[zip_code] = []
        zip_to_city[zip_code].append(georef_record)
    
    updated_records = []
    
    for record in comprehensive_data:
        # Update AA record with real city/zip data
        if 'aa_record' in record:
            # Randomly select a city/zip combination
            random_georef = random.choice(georef_data)
            
            # Update city and postal code in AA record
            record['aa_record']['CITY_NM'] = random_georef['city_name']
            record['aa_record']['POSTAL_CD'] = random_georef['zip_code']
            
            # Add additional georef data as metadata
            record['aa_record']['STATE_CD'] = random_georef['state_code']
            record['aa_record']['STATE_NM'] = random_georef['state_name']
            record['aa_record']['COUNTY_NM'] = random_georef['county_name']
            record['aa_record']['POPULATION'] = random_georef['population']
            record['aa_record']['DENSITY'] = random_georef['density']
            record['aa_record']['TIMEZONE'] = random_georef['timezone']
            record['aa_record']['COORDINATES'] = random_georef['coordinates']
        
        # Update application record with real city/zip data
        if 'application_record' in record:
            # Use the same city/zip as AA record for consistency in match scenarios
            if 'aa_record' in record:
                record['application_record']['CITY_NM'] = record['aa_record']['CITY_NM']
                record['application_record']['POSTAL_CD'] = record['aa_record']['POSTAL_CD']
                record['application_record']['STATE_CD'] = record['aa_record']['STATE_CD']
                record['application_record']['STATE_NM'] = record['aa_record']['STATE_NM']
            else:
                # If no AA record, use random georef data
                random_georef = random.choice(georef_data)
                record['application_record']['CITY_NM'] = random_georef['city_name']
                record['application_record']['POSTAL_CD'] = random_georef['zip_code']
                record['application_record']['STATE_CD'] = random_georef['state_code']
                record['application_record']['STATE_NM'] = random_georef['state_name']
        
        updated_records.append(record)
    
    print(f"✅ Integrated georef data into {len(updated_records)} records")
    return updated_records

def save_integrated_data(integrated_data: List[Dict[str, Any]], output_file: str):
    """
    Save the integrated data to a new JSON file
    """
    print(f"💾 Saving integrated data to {output_file}...")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(integrated_data, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"✅ Integrated data saved successfully")
        
    except Exception as e:
        print(f"❌ Error saving integrated data: {e}")

def generate_integration_report(integrated_data: List[Dict[str, Any]], georef_data: List[Dict[str, str]]):
    """
    Generate a report on the integration
    """
    print("\n📊 INTEGRATION REPORT")
    print("=" * 50)
    
    # Count unique cities and zip codes used
    used_cities = set()
    used_zip_codes = set()
    used_states = set()
    
    for record in integrated_data:
        if 'aa_record' in record:
            used_cities.add(record['aa_record'].get('CITY_NM', ''))
            used_zip_codes.add(record['aa_record'].get('POSTAL_CD', ''))
            used_states.add(record['aa_record'].get('STATE_CD', ''))
    
    print(f"Total Georef Records Available: {len(georef_data)}")
    print(f"Total Comprehensive Records: {len(integrated_data)}")
    print(f"Unique Cities Used: {len(used_cities)}")
    print(f"Unique Zip Codes Used: {len(used_zip_codes)}")
    print(f"Unique States Used: {len(used_states)}")
    
    # Show sample of integrated data
    print("\n📋 SAMPLE INTEGRATED RECORDS:")
    print("-" * 30)
    for i, record in enumerate(integrated_data[:3]):
        if 'aa_record' in record:
            print(f"Record {i+1}:")
            print(f"  City: {record['aa_record'].get('CITY_NM', 'N/A')}")
            print(f"  Zip: {record['aa_record'].get('POSTAL_CD', 'N/A')}")
            print(f"  State: {record['aa_record'].get('STATE_CD', 'N/A')}")
            print(f"  County: {record['aa_record'].get('COUNTY_NM', 'N/A')}")
            print()

def main():
    """
    Main function to orchestrate the extraction and integration process
    """
    print("🚀 Starting Georef Data Extraction and Integration Process")
    print("=" * 60)
    
    # File paths
    georef_file = "/Applications/Mapping/chatbased_demo_app/test/georef-united-states-of-america-zc-point@public.json"
    comprehensive_file = "/Applications/Mapping/chatbased_demo_app/test/aa_comprehensive_test_data.json"
    output_file = "/Applications/Mapping/chatbased_demo_app/test/aa_comprehensive_test_data_with_georef.json"
    
    # Step 1: Extract georef data
    georef_data = extract_georef_data(georef_file)
    if not georef_data:
        print("❌ Failed to extract georef data. Exiting.")
        return
    
    # Step 2: Load comprehensive data
    comprehensive_data = load_comprehensive_data(comprehensive_file)
    if not comprehensive_data:
        print("❌ Failed to load comprehensive data. Exiting.")
        return
    
    # Step 3: Integrate the data
    integrated_data = integrate_georef_data(comprehensive_data, georef_data)
    
    # Step 4: Save integrated data
    save_integrated_data(integrated_data, output_file)
    
    # Step 5: Generate report
    generate_integration_report(integrated_data, georef_data)
    
    print("\n🎉 Georef data extraction and integration completed successfully!")
    print(f"📁 Output file: {output_file}")

if __name__ == "__main__":
    main()
