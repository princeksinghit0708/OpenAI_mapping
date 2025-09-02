#!/usr/bin/env python3
"""
Comprehensive AA Member Test Data Generator - Windows Compatible
Generates 1000+ test cases with clean data for Windows systems
"""

import json
import random
from datetime import datetime
from aa_test_generator_windows import AAMemberTestDataGeneratorWindows
from faker import Faker

fake = Faker()

class AAComprehensiveTestGeneratorWindows:
    def __init__(self):
        self.base_generator = AAMemberTestDataGeneratorWindows()
        
    def generate_all_test_data(self, total_records=1000):
        """Generate comprehensive test dataset with clean data"""
        print("🚀 Generating comprehensive AA Member test data (Windows Compatible)...")
        
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
        
        print(f"✅ Generated {len(all_test_data)} test records")
        return all_test_data
    
    def generate_match1_scenario(self, count=100):
        """Match1: First Name + Last Name + AAdvantage Number + DOB match"""
        records = []
        for i in range(count):
            base_record = self.base_generator.generate_base_record()
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
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match1'
            })
        return records
    
    def generate_match2_scenario(self, count=100):
        """Match2: First Name + AAdvantage Number + Email + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.base_generator.generate_base_record()
            # Last name is different, but other fields match
            records.append({
                'scenario': 'Match2',
                'description': 'Last name mismatch but other key fields match',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.base_generator.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match2'
            })
        return records
    
    def generate_match3_scenario(self, count=100):
        """Match3: First Name + AAdvantage Number + Phone + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.base_generator.generate_base_record()
            # Last name and email are different, but phone matches
            records.append({
                'scenario': 'Match3',
                'description': 'Last name and email mismatch but phone matches',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.base_generator.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.base_generator.generate_clean_email(),  # Different email
                    'PHONE_NBR': base_record['PHONE_NBR'],  # Same phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match3'
            })
        return records
    
    def generate_match4_scenario(self, count=100):
        """Match4: First Name + AAdvantage Number + Address + DOB match (Last Name mismatch)"""
        records = []
        for i in range(count):
            base_record = self.base_generator.generate_base_record()
            # Last name, email, and phone are different, but address matches
            records.append({
                'scenario': 'Match4',
                'description': 'Only address matches with valid AA number',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.base_generator.generate_clean_name('last'),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.base_generator.generate_clean_email(),  # Different email
                    'PHONE_NBR': self.base_generator.generate_clean_phone(),  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match4'
            })
        return records
    
    def generate_remaining_scenarios(self, count):
        """Generate Match5-Match10 scenarios"""
        scenarios = []
        
        for i in range(count):
            base_record = self.base_generator.generate_base_record()
            
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
                    'POSTAL_CD': base_record['POSTAL_CD']
                }
                
            elif scenario_type in ['Match7', 'Match8']:
                # Invalid AA number, phone match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',  # Invalid AA number
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.base_generator.generate_clean_email(),  # Different email
                    'PHONE_NBR': base_record['PHONE_NBR'],  # Same phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                }
                
            else:  # Match9, Match10
                # Invalid AA number, address match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',  # Invalid AA number
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.base_generator.generate_clean_email(),  # Different email
                    'PHONE_NBR': self.base_generator.generate_clean_phone(),  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
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
        base_record = self.base_generator.generate_base_record()
        base_record['FIRST_NM'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullFirstName',
            'description': 'Test with null first name',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Null Last Name
        base_record = self.base_generator.generate_base_record()
        base_record['LAST_NM'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullLastName',
            'description': 'Test with null last name',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Null DOB
        base_record = self.base_generator.generate_base_record()
        base_record['BIRTH_DT'] = None
        scenarios.append({
            'scenario': 'DataQuality_NullDOB',
            'description': 'Test with null date of birth',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Empty AAdvantage Number
        base_record = self.base_generator.generate_base_record()
        base_record['LYLTY_ACCT_ID'] = ''
        scenarios.append({
            'scenario': 'DataQuality_EmptyAANumber',
            'description': 'Test with empty AAdvantage number',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid DOB format
        base_record = self.base_generator.generate_base_record()
        base_record['BIRTH_DT'] = '03/03/1954'  # Wrong format
        scenarios.append({
            'scenario': 'DataQuality_InvalidDOBFormat',
            'description': 'Test with invalid DOB format',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid phone format
        base_record = self.base_generator.generate_base_record()
        base_record['PHONE_NBR'] = '866-417-6210'  # With dashes
        scenarios.append({
            'scenario': 'DataQuality_InvalidPhoneFormat',
            'description': 'Test with invalid phone format',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Invalid email format
        base_record = self.base_generator.generate_base_record()
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
            base_record = self.base_generator.generate_base_record()
            
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
            base_record = self.base_generator.generate_base_record()
            
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
                'POSTAL_CD': '12345'
            }
            
            scenarios.append({
                'scenario': 'Invalid',
                'description': 'No matching criteria met',
                'aa_record': base_record,
                'application_record': app_record,
                'expected_result': 'Invalid'
            })
        
        return scenarios
    
    def save_test_data(self, test_data, filename='aa_comprehensive_test_data_windows.json'):
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
        
        print("\n📈 TEST DATA SUMMARY REPORT (Windows Compatible)")
        print("=" * 50)
        for scenario, count in sorted(scenario_counts.items()):
            print(f"{scenario:<20}: {count:>4} records")
        print("=" * 50)
        print(f"Total Records: {len(test_data)}")

if __name__ == "__main__":
    generator = AAComprehensiveTestGeneratorWindows()
    
    # Generate comprehensive test data
    test_data = generator.generate_all_test_data(1000)
    
    # Save to file
    generator.save_test_data(test_data)
    
    # Generate summary report
    generator.generate_summary_report(test_data)
    
    print("\n🎉 Comprehensive AA Member test data generation completed (Windows Compatible)!")
