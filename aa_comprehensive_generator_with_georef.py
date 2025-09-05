#!/usr/bin/env python3
"""
Enhanced AA Comprehensive Test Data Generator with Real Georef Data
Generates test cases using real city names and zip codes from georef data
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Any, Optional

class GeorefDataManager:
    """Manages georef data for city/zip code generation"""
    
    def __init__(self, georef_file_path: str):
        self.georef_file_path = georef_file_path
        self.georef_data = []
        self.load_georef_data()
    
    def load_georef_data(self):
        """Load georef data from JSON file"""
        try:
            with open(self.georef_file_path, 'r', encoding='utf-8') as f:
                self.georef_data = json.load(f)
            print(f"✅ Loaded {len(self.georef_data)} georef records")
        except Exception as e:
            print(f"❌ Error loading georef data: {e}")
            self.georef_data = []
    
    def get_random_city_zip(self) -> Dict[str, Any]:
        """Get a random city/zip combination from georef data"""
        if not self.georef_data:
            return self._get_fallback_data()
        
        # Filter for valid 5-digit zip codes
        valid_records = [record for record in self.georef_data 
                        if record.get('zip_code', '').isdigit() and len(record.get('zip_code', '')) == 5]
        
        if not valid_records:
            return self._get_fallback_data()
        
        georef_record = random.choice(valid_records)
        return {
            'city_name': georef_record.get('usps_city', 'Unknown City'),
            'zip_code': georef_record.get('zip_code', '00000'),
            'state_code': georef_record.get('stusps_code', 'XX'),
            'state_name': georef_record.get('ste_name', 'Unknown State'),
            'county_name': georef_record.get('primary_coty_name', 'Unknown County'),
            'population': georef_record.get('population', 0),
            'density': georef_record.get('density', 0),
            'timezone': georef_record.get('timezone', 'America/New_York'),
            'coordinates': georef_record.get('geo_point_2d', {})
        }
    
    def get_city_zip_by_state(self, state_code: str) -> Optional[Dict[str, Any]]:
        """Get a city/zip combination for a specific state"""
        if not self.georef_data:
            return self._get_fallback_data()
        
        # Filter for valid 5-digit zip codes in the specified state
        state_cities = [record for record in self.georef_data 
                       if (record.get('stusps_code') == state_code and 
                           record.get('zip_code', '').isdigit() and 
                           len(record.get('zip_code', '')) == 5)]
        
        if not state_cities:
            return self.get_random_city_zip()
        
        georef_record = random.choice(state_cities)
        return {
            'city_name': georef_record.get('usps_city', 'Unknown City'),
            'zip_code': georef_record.get('zip_code', '00000'),
            'state_code': georef_record.get('stusps_code', state_code),
            'state_name': georef_record.get('ste_name', 'Unknown State'),
            'county_name': georef_record.get('primary_coty_name', 'Unknown County'),
            'population': georef_record.get('population', 0),
            'density': georef_record.get('density', 0),
            'timezone': georef_record.get('timezone', 'America/New_York'),
            'coordinates': georef_record.get('geo_point_2d', {})
        }
    
    def _get_fallback_data(self) -> Dict[str, Any]:
        """Fallback data when georef data is not available"""
        return {
            'city_name': 'Test City',
            'zip_code': '12345',
            'state_code': 'XX',
            'state_name': 'Test State',
            'county_name': 'Test County',
            'population': 1000,
            'density': 10.0,
            'timezone': 'America/New_York',
            'coordinates': {'lon': 0.0, 'lat': 0.0}
        }

class AAComprehensiveTestGeneratorWithGeoref:
    """Enhanced comprehensive test generator with real georef data"""
    
    def __init__(self, georef_file_path: str):
        self.georef_manager = GeorefDataManager(georef_file_path)
        self.fake = None
        try:
            from faker import Faker
            self.fake = Faker()
        except ImportError:
            print("⚠️ Faker not available, using basic data generation")
    
    def generate_clean_name(self, name_type: str) -> str:
        """Generate clean name for testing"""
        if self.fake:
            if name_type == 'first':
                return self.fake.first_name()
            else:
                return self.fake.last_name()
        else:
            names = {
                'first': ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emily'],
                'last': ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
            }
            return random.choice(names[name_type])
    
    def generate_clean_email(self) -> str:
        """Generate clean email for testing"""
        if self.fake:
            return self.fake.email()
        else:
            domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
            name = self.generate_clean_name('first').lower()
            return f"{name}{random.randint(100, 999)}@{random.choice(domains)}"
    
    def generate_clean_phone(self) -> str:
        """Generate clean phone number for testing"""
        if self.fake:
            return self.fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        else:
            return f"{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    
    def generate_base_record(self) -> Dict[str, Any]:
        """Generate base AA member record with real georef data"""
        georef_data = self.georef_manager.get_random_city_zip()
        
        # Generate AAdvantage number
        aa_number = f"{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])}{random.randint(10000, 99999)}"
        
        # Generate birth date (18-80 years old)
        birth_year = random.randint(1944, 2006)
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        birth_date = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        
        # Generate enrollment date (after birth date)
        enroll_year = random.randint(birth_year + 18, 2024)
        enroll_month = random.randint(1, 12)
        enroll_day = random.randint(1, 28)
        enroll_date = f"{enroll_year}-{enroll_month:02d}-{enroll_day:02d}"
        
        # Generate street address
        street_number = random.randint(100, 9999)
        street_names = ['Main St', 'Oak Ave', 'First St', 'Second Ave', 'Park Rd', 'Elm St', 'Cedar Ln', 'Maple Dr']
        street_name = random.choice(street_names)
        
        return {
            'LYLTY_ACCT_ID': aa_number,
            'LYLTY_LEVEL_IND': random.choice(['E', 'G', 'P', 'S']),
            'OPT_IN_ALL3_IND': random.choice(['Y', 'N']),
            'EMAIL_OPEN_RATE_12MO_PCT': round(random.uniform(0, 100), 2),
            'PGM_ENROLL_DT': enroll_date,
            'AEM_CURR_QTY': random.randint(0, 50000),
            'LYLTY_PGM_ENROLL_SRC_CD': f"{random.randint(10000000, 99999999)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}{random.randint(10000000, 99999999)}",
            'PGM_TODT_AEM_QTY': random.randint(0, 1000),
            'AA_FLIGHT_SEG_24MO_QTY': random.randint(0, 500),
            'LYLTY_ACCT_LAST_ACTVTY_DT': f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'OA_FLIGHT_24MO_QTY': random.randint(0, 200),
            'FLIGHT_REDMPTN_TRANS_24MO_QTY': random.randint(0, 100),
            'TRIP_12MO_QTY': random.randint(0, 50),
            'REVNUE_TRIP_12MO_QTY': random.randint(0, 200),
            'AWD_TRIP_12MO_QTY': random.randint(0, 100),
            'REVNUE_OA_TRIP_12MO_QTY': random.randint(0, 100),
            'AWD_OA_TRIP_12MO_QTY': random.randint(0, 50),
            'DISCRETIONARY_TRIP_12MO_QTY': random.randint(0, 20),
            'NON_DISCRETIONARY_TRIP_12MO_QTY': random.randint(0, 100),
            'BLENDED_TRIP_12MO_QTY': random.randint(0, 50),
            'DIRECT_BKG_CHANL_TRIP_12MO_PCT': round(random.uniform(0, 100), 3),
            'MULTI_PARTY_TRIP_12MO_PCT': round(random.uniform(0, 100), 3),
            'REVNUE_AA_FUTURE_TRIP_QTY': random.randint(0, 20),
            'AWD_FUTURE_TRIP_QTY': random.randint(0, 20),
            'REVNUE_OA_FUTURE_TRIP_QTY': random.randint(0, 20),
            'AEM_EARN_24MO_QTY': random.randint(0, 10000),
            'NANB_EARN_AEM_12MO_QTY': random.randint(0, 1000),
            'AWD_FLIGHT_SEG_12MO_QTY': random.randint(0, 100),
            'NANE_PURCHS_AEM_12MO_IND': random.choice(['Yes', 'No']),
            'NANB_PARTNR_12MO_QTY': random.randint(0, 20),
            'NANB_TRANS_12MO_QTY': random.randint(0, 50),
            'LATEST_RES_CREATE_DT': f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'RES_INACTVTY_DAY_QTY': random.randint(0, 365),
            'LOUNGE_VISIT_12MO_QTY': random.randint(0, 100),
            'EXPD_CARD_QTY': random.randint(0, 10),
            'LATEST_FLIGHT_DT': f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'LATEST_INTL_FLIGHT_DT': f"{random.randint(2020, 2024)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'EXPD_PLAT_CARD_QTY': random.randint(0, 5),
            'FIRST_NM': self.generate_clean_name('first'),
            'LAST_NM': self.generate_clean_name('last'),
            'BIRTH_DT': birth_date,
            'STREET_LINE_1_TXT': f"{street_number} {street_name}",
            'STREET_LINE_2_TXT': random.choice(['', f"Apt {random.randint(1, 999)}", f"Suite {random.randint(1, 999)}", f"Unit {random.randint(1, 999)}"]),
            'CITY_NM': georef_data['city_name'],
            'POSTAL_CD': georef_data['zip_code'],
            'STATE_CD': georef_data['state_code'],
            'STATE_NM': georef_data['state_name'],
            'COUNTY_NM': georef_data['county_name'],
            'POPULATION': georef_data['population'],
            'DENSITY': georef_data['density'],
            'TIMEZONE': georef_data['timezone'],
            'COORDINATES': georef_data['coordinates'],
            'EMAIL_ADDR_TXT': self.generate_clean_email(),
            'PHONE_NBR': self.generate_clean_phone()
        }
    
    def generate_all_test_data(self, total_records=1000):
        """Generate comprehensive test dataset with real georef data"""
        print("🚀 Generating comprehensive AA Member test data with real georef data...")
        
        all_test_data = []
        
        # Generate Match1 scenarios (100 records)
        print("📊 Generating Match1 scenarios...")
        all_test_data.extend(self.generate_match1_scenario(100))
        
        # Generate Match2 scenarios (100 records)
        print("📊 Generating Match2 scenarios...")
        all_test_data.extend(self.generate_match2_scenario(100))
        
        # Generate Match3 scenarios (100 records)
        print("📊 Generating Match3 scenarios...")
        all_test_data.extend(self.generate_match3_scenario(100))
        
        # Generate Match4 scenarios (100 records)
        print("📊 Generating Match4 scenarios...")
        all_test_data.extend(self.generate_match4_scenario(100))
        
        # Generate remaining scenarios (Match5-Match10)
        print("📊 Generating Match5-Match10 scenarios...")
        all_test_data.extend(self.generate_remaining_scenarios(400))
        
        # Generate data quality test scenarios
        print("📊 Generating data quality test scenarios...")
        all_test_data.extend(self.generate_data_quality_scenarios())
        
        # Generate edge cases and boundary conditions
        print("📊 Generating edge cases...")
        all_test_data.extend(self.generate_edge_cases(100))
        
        # Generate invalid scenarios
        print("📊 Generating invalid scenarios...")
        all_test_data.extend(self.generate_invalid_scenarios(100))
        
        print(f"✅ Generated {len(all_test_data)} test records with real georef data")
        return all_test_data
    
    def generate_match1_scenario(self, count=100):
        """Match1: First Name + Last Name + AAdvantage Number + DOB match"""
        records = []
        for i in range(count):
            base_record = self.generate_base_record()
            # All fields match perfectly
            records.append({
                'scenario': 'Match1',
                'description': 'Perfect match - all key fields align',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                },
                'expected_result': 'Match1'
            })
        return records
    
    def generate_match2_scenario(self, count=100):
        """Match2: First Name + AAdvantage Number + Email + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.generate_base_record()
            # Last name is different, but other fields match
            records.append({
                'scenario': 'Match2',
                'description': 'Last name mismatch but other key fields match',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                },
                'expected_result': 'Match2'
            })
        return records
    
    def generate_match3_scenario(self, count=100):
        """Match3: First Name + AAdvantage Number + Phone + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.generate_base_record()
            # Last name and email are different, but phone matches
            records.append({
                'scenario': 'Match3',
                'description': 'Last name and email mismatch but phone matches',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.generate_clean_email(),  # Different email
                    'PHONE_NBR': base_record['PHONE_NBR'],  # Same phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                },
                'expected_result': 'Match3'
            })
        return records
    
    def generate_match4_scenario(self, count=100):
        """Match4: First Name + AAdvantage Number + Address + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.generate_base_record()
            # Last name, email, and phone are different, but address matches
            records.append({
                'scenario': 'Match4',
                'description': 'Only address matches with valid AA number',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.generate_clean_email(),  # Different email
                    'PHONE_NBR': self.generate_clean_phone(),  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                },
                'expected_result': 'Match4'
            })
        return records
    
    def generate_remaining_scenarios(self, count):
        """Generate Match5-Match10 scenarios"""
        scenarios = []
        
        for i in range(count):
            base_record = self.generate_base_record()
            
            # Randomly select scenario type
            scenario_type = random.choice(['Match5', 'Match6', 'Match7', 'Match8', 'Match9', 'Match10'])
            
            if scenario_type in ['Match5', 'Match6']:
                # Invalid AA number, email match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',  # Invalid AA number
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                }
                
            elif scenario_type in ['Match7', 'Match8']:
                # Invalid AA number, phone match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',  # Invalid AA number
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.generate_clean_email(),  # Different email
                    'PHONE_NBR': base_record['PHONE_NBR'],  # Same phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                }
                
            else:  # Match9, Match10
                # Invalid AA number, address match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',  # Invalid AA number
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.generate_clean_email(),  # Different email
                    'PHONE_NBR': self.generate_clean_phone(),  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD'],
                    'STATE_CD': base_record['STATE_CD'],
                    'STATE_NM': base_record['STATE_NM']
                }
            
            scenarios.append({
                'scenario': scenario_type,
                'description': f'{scenario_type} scenario with invalid AA number',
                'aa_record': base_record,
                'application_record': app_record,
                'expected_result': scenario_type
            })
        
        return scenarios
    
    def generate_data_quality_scenarios(self):
        """Generate data quality test scenarios"""
        scenarios = []
        
        # Null First Name
        base_record = self.generate_base_record()
        base_record['FIRST_NM'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullFirstName',
            'description': 'Test with null first name',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Null Last Name
        base_record = self.generate_base_record()
        base_record['LAST_NM'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullLastName',
            'description': 'Test with null last name',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Null DOB
        base_record = self.generate_base_record()
        base_record['BIRTH_DT'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullDOB',
            'description': 'Test with null date of birth',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Empty AAdvantage Number
        base_record = self.generate_base_record()
        base_record['LYLTY_ACCT_ID'] = ''
        scenarios.append({
            'scenario': 'DataQuality_EmptyAANumber',
            'description': 'Test with empty AAdvantage number',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid DOB format
        base_record = self.generate_base_record()
        base_record['BIRTH_DT'] = '03/03/1954'  # Wrong format
        scenarios.append({
            'scenario': 'DataQuality_InvalidDOBFormat',
            'description': 'Test with invalid DOB format',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid phone format
        base_record = self.generate_base_record()
        base_record['PHONE_NBR'] = '866-417-6210'  # With dashes
        scenarios.append({
            'scenario': 'DataQuality_InvalidPhoneFormat',
            'description': 'Test with invalid phone format',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid email format
        base_record = self.generate_base_record()
        base_record['EMAIL_ADDR_TXT'] = 'invalid-email'  # No @ symbol
        scenarios.append({
            'scenario': 'DataQuality_InvalidEmailFormat',
            'description': 'Test with invalid email format',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        return scenarios
    
    def generate_edge_cases(self, count):
        """Generate edge cases and boundary conditions"""
        scenarios = []
        
        for i in range(count):
            base_record = self.generate_base_record()
            
            # Randomly select edge case type
            edge_case = random.choice([
                'short_address', 'long_address', 'special_chars', 
                'unicode_names', 'minimal_data', 'maximal_data'
            ])
            
            if edge_case == 'short_address':
                base_record['STREET_LINE_1_TXT'] = '123 A'
                base_record['STREET_LINE_2_TXT'] = ''
                
            elif edge_case == 'long_address':
                base_record['STREET_LINE_1_TXT'] = 'A' * 50  # Reasonable length
                base_record['STREET_LINE_2_TXT'] = 'B' * 30
                
            elif edge_case == 'special_chars':
                base_record['FIRST_NM'] = "Jose-Maria"
                base_record['LAST_NM'] = "OConnor-Smith"
                
            elif edge_case == 'unicode_names':
                base_record['FIRST_NM'] = "Jose"
                base_record['LAST_NM'] = "Garcia"
                
            elif edge_case == 'minimal_data':
                # Keep only required fields
                minimal_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID']
                }
                base_record = minimal_record
                
            scenarios.append({
                'scenario': f'EdgeCase_{edge_case}',
                'description': f'Edge case: {edge_case}',
                'aa_record': base_record,
                'expected_result': 'Edge Case'
            })
        
        return scenarios
    
    def generate_invalid_scenarios(self, count):
        """Generate invalid scenarios that should not match"""
        scenarios = []
        
        for i in range(count):
            base_record = self.generate_base_record()
            
            # Create application record with no matching fields
            app_record = {
                'FIRST_NM': 'DifferentFirst',
                'LAST_NM': 'DifferentLast',
                'LYLTY_ACCT_ID': 'INVALID123',
                'BIRTH_DT': '1990-01-01',
                'EMAIL_ADDR_TXT': 'different@email.com',
                'PHONE_NBR': '1234567890',
                'STREET_LINE_1_TXT': '123 Different St',
                'STREET_LINE_2_TXT': 'Apt 1',
                'CITY_NM': 'Different City',
                'POSTAL_CD': '12345',
                'STATE_CD': 'XX',
                'STATE_NM': 'Different State'
            }
            
            scenarios.append({
                'scenario': 'Invalid',
                'description': 'No matching criteria met',
                'aa_record': base_record,
                'application_record': app_record,
                'expected_result': 'Invalid'
            })
        
        return scenarios
    
    def save_test_data(self, test_data, filename='aa_comprehensive_test_data_with_georef.json'):
        """Save test data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, default=str, ensure_ascii=False)
        print(f"💾 Test data saved to {filename}")
    
    def generate_summary_report(self, test_data):
        """Generate summary report of test data"""
        scenario_counts = {}
        for record in test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        print("\n📈 TEST DATA SUMMARY REPORT (With Real Georef Data)")
        print("=" * 60)
        for scenario, count in sorted(scenario_counts.items()):
            print(f"{scenario:<20}: {count:>4} records")
        print("=" * 60)
        print(f"Total Records: {len(test_data)}")
        
        # Show georef data usage
        unique_cities = set()
        unique_states = set()
        for record in test_data:
            if 'aa_record' in record:
                unique_cities.add(record['aa_record'].get('CITY_NM', ''))
                unique_states.add(record['aa_record'].get('STATE_CD', ''))
        
        print(f"Unique Cities Used: {len(unique_cities)}")
        print(f"Unique States Used: {len(unique_states)}")

if __name__ == "__main__":
    # File paths
    georef_file = "/Applications/Mapping/chatbased_demo_app/test/georef-united-states-of-america-zc-point@public.json"
    output_file = "/Applications/Mapping/chatbased_demo_app/test/aa_comprehensive_test_data_with_georef_enhanced.json"
    
    # Create generator with georef data
    generator = AAComprehensiveTestGeneratorWithGeoref(georef_file)
    
    # Generate comprehensive test data
    test_data = generator.generate_all_test_data(1000)
    
    # Save to file
    generator.save_test_data(test_data, output_file)
    
    # Generate summary report
    generator.generate_summary_report(test_data)
    
    print("\n🎉 Enhanced comprehensive AA Member test data generation completed!")
    print(f"📁 Output file: {output_file}")
