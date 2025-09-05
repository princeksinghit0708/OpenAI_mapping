#!/usr/bin/env python3
"""
AA Comprehensive Generator - City and Zip Code Integration (Fixed)
Uses extracted city and zip code data for AA member data generation
"""

import json
import random
from pathlib import Path

class AACityZipGenerator:
    """Generate AA member data with real city names and zip codes"""
    
    def __init__(self, json_file_path="extracted_city_zip_data_aa_generator.json"):
        self.json_file_path = json_file_path
        self.city_zip_data = []
        self.load_city_zip_data()
        
        if len(self.city_zip_data) == 0:
            print("⚠️ No city-zip data available")
        else:
            print(f"🏙️ Ready to generate AA data with {len(self.city_zip_data)} city-zip combinations")
    
    def load_city_zip_data(self):
        """Load city-zip data from JSON file"""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.city_zip_data = json.load(f)
            print(f"✅ Loaded {len(self.city_zip_data)} city-zip combinations from {self.json_file_path}")
        except FileNotFoundError:
            print(f"❌ JSON file not found: {self.json_file_path}")
            print("Please run extract_city_zip_from_json.py first")
        except Exception as e:
            print(f"❌ Error loading JSON file: {e}")
    
    def get_random_city_zip(self):
        """Get a random city and zip code combination"""
        if not self.city_zip_data:
            return {
                "city_nm": "Unknown City",
                "zip_code": "00000",
                "state": "XX",
                "state_name": "Unknown State"
            }
        
        return random.choice(self.city_zip_data)
    
    def get_city_zip_by_state(self, state_code):
        """Get city-zip data filtered by state"""
        filtered_data = [item for item in self.city_zip_data if item['state'] == state_code]
        if filtered_data:
            return random.choice(filtered_data)
        else:
            return self.get_random_city_zip()
    
    def generate_aa_member_address(self, member_id=None):
        """Generate a complete AA member address using real city-zip data"""
        city_zip = self.get_random_city_zip()
        
        # Generate a realistic street address
        street_numbers = [str(random.randint(100, 9999))]
        street_names = [
            "Main St", "Oak Ave", "First St", "Second St", "Park Ave", 
            "Washington St", "Lincoln Ave", "Jefferson St", "Madison Ave",
            "Broadway", "Elm St", "Pine St", "Cedar Ave", "Maple St"
        ]
        
        address = {
            "member_id": member_id or f"AA{random.randint(100000, 999999)}",
            "street_address": f"{random.choice(street_numbers)} {random.choice(street_names)}",
            "city_nm": city_zip["city_nm"],
            "zip_code": city_zip["zip_code"],
            "state": city_zip["state"],
            "state_name": city_zip["state_name"],
            "full_address": f"{random.choice(street_numbers)} {random.choice(street_names)}, {city_zip['city_nm']}, {city_zip['state']} {city_zip['zip_code']}"
        }
        
        return address
    
    def generate_multiple_addresses(self, count=10, state_filter=None):
        """Generate multiple AA member addresses"""
        addresses = []
        
        for i in range(count):
            if state_filter:
                city_zip = self.get_city_zip_by_state(state_filter)
            else:
                city_zip = self.get_random_city_zip()
            
            address = self.generate_aa_member_address(f"AA{i+1:06d}")
            addresses.append(address)
        
        return addresses
    
    def get_state_statistics(self):
        """Get statistics about available states"""
        states = {}
        for item in self.city_zip_data:
            state = item['state']
            if state not in states:
                states[state] = 0
            states[state] += 1
        
        return states
    
    def save_sample_data(self, count=100, filename="aa_sample_addresses.json"):
        """Generate and save sample AA address data"""
        print(f"🏗️ Generating {count} sample AA addresses...")
        
        addresses = self.generate_multiple_addresses(count)
        
        # Save to JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(addresses, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {count} addresses to {filename}")
        
        # Show sample
        print("\n📋 Sample generated addresses:")
        for i, addr in enumerate(addresses[:5]):
            print(f"   {i+1}. {addr['full_address']}")
        
        return addresses

def main():
    """Main function to demonstrate the AA city-zip generator"""
    print("🚀 AA Comprehensive Generator - City and Zip Code Integration")
    print("=" * 60)
    
    # Initialize generator
    generator = AACityZipGenerator()
    
    if len(generator.city_zip_data) == 0:
        print("❌ No data available. Please run extract_city_zip_from_json.py first")
        return
    
    # Show statistics
    stats = generator.get_state_statistics()
    print(f"\n📊 Data Statistics:")
    print(f"   Total city-zip combinations: {len(generator.city_zip_data)}")
    print(f"   States covered: {len(stats)}")
    print(f"   Top 10 states by city count:")
    
    sorted_states = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    for state, count in sorted_states[:10]:
        print(f"     {state}: {count} cities")
    
    # Generate sample data
    print(f"\n🎯 Generating sample AA member addresses...")
    sample_addresses = generator.save_sample_data(50, "aa_sample_addresses.json")
    
    # Show state-specific example
    print(f"\n🗺️ State-specific example (California):")
    ca_addresses = generator.generate_multiple_addresses(3, "CA")
    for addr in ca_addresses:
        print(f"   • {addr['full_address']}")
    
    print(f"\n✅ AA City-Zip Generator ready for use!")
    print(f"📁 Sample data saved to: aa_sample_addresses.json")
    print(f"🔧 Use this data in your AA comprehensive generator")

if __name__ == "__main__":
    main()
