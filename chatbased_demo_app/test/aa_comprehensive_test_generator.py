#!/usr/bin/env python3
"""
Comprehensive AA Member Test Data Generator
Generates 1000+ test cases covering all scenarios
"""

import json
import random
from datetime import datetime
from aa_test_generator import AAMemberTestDataGenerator
from aa_scenario_generator import AAScenarioGenerator
from aa_data_quality_tests import AADataQualityTests

class AAComprehensiveTestGenerator:
    def __init__(self):
        self.base_generator = AAMemberTestDataGenerator()
        self.scenario_generator = AAScenarioGenerator()
        self.quality_tests = AADataQualityTests()
        
    def generate_all_test_data(self, total_records=1000):
        """Generate comprehensive test dataset"""
        print("🚀 Generating comprehensive AA Member test data...")
        
        all_test_data = []
        
        # Generate Match1 scenarios (100 records)
        print("📊 Generating Match1 scenarios...")
        all_test_data.extend(self.scenario_generator.generate_match1_scenario(100))
        
        # Generate Match2 scenarios (100 records)
        print("📊 Generating Match2 scenarios...")
        all_test_data.extend(self.scenario_generator.generate_match2_scenario(100))
        
        # Generate Match3 scenarios (100 records)
        print("📊 Generating Match3 scenarios...")
        all_test_data.extend(self.scenario_generator.generate_match3_scenario(100))
        
        # Generate Match4 scenarios (100 records)
        print("📊 Generating Match4 scenarios...")
        all_test_data.extend(self.scenario_generator.generate_match4_scenario(100))
        
        # Generate remaining scenarios (Match5-Match10)
        print("📊 Generating Match5-Match10 scenarios...")
        all_test_data.extend(self.generate_remaining_scenarios(400))
        
        # Generate data quality test scenarios
        print("📊 Generating data quality test scenarios...")
        all_test_data.extend(self.quality_tests.generate_data_quality_scenarios())
        
        # Generate edge cases and boundary conditions
        print("📊 Generating edge cases...")
        all_test_data.extend(self.generate_edge_cases(100))
        
        # Generate invalid scenarios
        print("📊 Generating invalid scenarios...")
        all_test_data.extend(self.generate_invalid_scenarios(100))
        
        print(f"✅ Generated {len(all_test_data)} test records")
        return all_test_data
    
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
                    'EMAIL_ADDR_TXT': 'different@email.com',  # Different email
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
                    'EMAIL_ADDR_TXT': 'different@email.com',  # Different email
                    'PHONE_NBR': '1234567890',  # Different phone
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
                base_record['STREET_LINE_1_TXT'] = 'A' * 100
                base_record['STREET_LINE_2_TXT'] = 'B' * 50
                
            elif edge_case == 'special_chars':
                base_record['FIRST_NM'] = "José-María"
                base_record['LAST_NM'] = "O'Connor-Smith"
                
            elif edge_case == 'unicode_names':
                base_record['FIRST_NM'] = "李小明"
                base_record['LAST_NM'] = "王"
                
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
    
    def save_test_data(self, test_data, filename='aa_comprehensive_test_data.json'):
        """Save test data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2, default=str)
        print(f"💾 Test data saved to {filename}")
    
    def generate_summary_report(self, test_data):
        """Generate summary report of test data"""
        scenario_counts = {}
        for record in test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        print("\n📈 TEST DATA SUMMARY REPORT")
        print("=" * 50)
        for scenario, count in sorted(scenario_counts.items()):
            print(f"{scenario:<20}: {count:>4} records")
        print("=" * 50)
        print(f"Total Records: {len(test_data)}")

if __name__ == "__main__":
    generator = AAComprehensiveTestGenerator()
    
    # Generate comprehensive test data
    test_data = generator.generate_all_test_data(1000)
    
    # Save to file
    generator.save_test_data(test_data)
    
    # Generate summary report
    generator.generate_summary_report(test_data)
    
    print("\n🎉 Comprehensive AA Member test data generation completed!")
