#!/usr/bin/env python3
"""
Extract City Names and Zip Codes from Geographic JSON Data
For use with AA comprehensive generator
"""

import json
import csv
from pathlib import Path

def extract_city_zip_data(json_file_path, output_file_path=None):
    """
    Extract city names and zip codes from the geographic JSON file
    
    Args:
        json_file_path: Path to the input JSON file
        output_file_path: Path to save the extracted data (optional)
    
    Returns:
        List of dictionaries with city_name and zip_code
    """
    
    print(f"📖 Reading JSON file: {json_file_path}")
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Successfully loaded {len(data)} records")
        
        # Extract city names and zip codes
        extracted_data = []
        
        for record in data:
            city_zip_record = {
                "city_name": record.get("usps_city", ""),
                "zip_code": record.get("zip_code", ""),
                "state": record.get("stusps_code", ""),
                "state_name": record.get("ste_name", ""),
                "population": record.get("population", 0),
                "density": record.get("density", 0)
            }
            extracted_data.append(city_zip_record)
        
        print(f"📊 Extracted {len(extracted_data)} city-zip combinations")
        
        # Save to output file if specified
        if output_file_path:
            save_extracted_data(extracted_data, output_file_path)
        
        return extracted_data
        
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return []

def save_extracted_data(data, output_file_path):
    """Save extracted data to various formats"""
    
    output_path = Path(output_file_path)
    
    # Save as JSON
    json_path = output_path.with_suffix('.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved JSON: {json_path}")
    
    # Save as CSV
    csv_path = output_path.with_suffix('.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    print(f"💾 Saved CSV: {csv_path}")
    
    # Save as simple text format for easy copying
    txt_path = output_path.with_suffix('.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("# City Name and Zip Code Data\n")
        f.write("# Format: city_name, zip_code\n\n")
        for record in data:
            f.write(f"{record['city_name']}, {record['zip_code']}\n")
    print(f"💾 Saved TXT: {txt_path}")

def create_aa_generator_data(data, output_file_path):
    """Create data specifically formatted for AA comprehensive generator"""
    
    print("🏗️ Creating AA generator data format...")
    
    # Create a simplified format for AA generator
    aa_data = []
    
    for record in data:
        aa_record = {
            "city_nm": record["city_name"],
            "zip_code": record["zip_code"],
            "state": record["state"],
            "state_name": record["state_name"]
        }
        aa_data.append(aa_record)
    
    # Save AA-specific format
    aa_path = Path(str(output_file_path) + '_aa_generator.json')
    with open(aa_path, 'w', encoding='utf-8') as f:
        json.dump(aa_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved AA Generator data: {aa_path}")
    
    # Also create a Python dictionary format
    py_path = Path(str(output_file_path) + '_aa_generator.py')
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write("# AA Comprehensive Generator - City and Zip Code Data\n")
        f.write("# Generated from geographic JSON data\n\n")
        f.write("CITY_ZIP_DATA = [\n")
        
        for i, record in enumerate(aa_data):
            f.write(f"    {{\n")
            f.write(f"        'city_nm': '{record['city_nm']}',\n")
            f.write(f"        'zip_code': '{record['zip_code']}',\n")
            f.write(f"        'state': '{record['state']}',\n")
            f.write(f"        'state_name': '{record['state_name']}'\n")
            f.write(f"    }}{',' if i < len(aa_data) - 1 else ''}\n")
        
        f.write("]\n\n")
        f.write(f"# Total records: {len(aa_data)}\n")
        f.write("# Usage: from {py_path.stem} import CITY_ZIP_DATA\n")
    
    print(f"💾 Saved Python data: {py_path}")
    
    return aa_data

def main():
    """Main function"""
    print("🚀 City and Zip Code Extractor for AA Comprehensive Generator")
    print("=" * 60)
    
    # Input file path
    json_file = "chatbased_demo_app/test/georef-united-states-of-america-zc-point@public.json"
    
    # Check if file exists
    if not Path(json_file).exists():
        print(f"❌ JSON file not found: {json_file}")
        return
    
    # Extract data
    extracted_data = extract_city_zip_data(json_file)
    
    if not extracted_data:
        print("❌ No data extracted")
        return
    
    # Show sample data
    print("\n📋 Sample extracted data:")
    for i, record in enumerate(extracted_data[:5]):
        print(f"   {i+1}. {record['city_name']}, {record['zip_code']} ({record['state']})")
    
    # Save extracted data
    output_file = "extracted_city_zip_data"
    save_extracted_data(extracted_data, output_file)
    
    # Create AA generator specific data
    aa_data = create_aa_generator_data(extracted_data, output_file)
    
    print(f"\n✅ Extraction complete!")
    print(f"📊 Total records: {len(extracted_data)}")
    print(f"📁 Output files created with prefix: {output_file}")
    
    # Show statistics
    states = set(record['state'] for record in extracted_data)
    print(f"🗺️ States covered: {len(states)}")
    print(f"🏙️ Sample states: {', '.join(list(states)[:10])}")

if __name__ == "__main__":
    main()
