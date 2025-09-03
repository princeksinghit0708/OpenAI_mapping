#!/usr/bin/env python3
"""
Ultimate AA Member Test Data Generator
Comprehensive system covering all scenarios: phone, postal, dates, special characters, emails
"""

import json
import random
from datetime import datetime
from aa_comprehensive_data_validator import AAComprehensiveDataValidator
from aa_enhanced_data_generator import AAEnhancedDataGenerator

class AAUltimateTestGenerator:
    def __init__(self):
        self.validator = AAComprehensiveDataValidator()
        self.enhanced_generator = AAEnhancedDataGenerator()
        
    def generate_ultimate_test_data(self, total_records=2000):
        """Generate ultimate comprehensive test dataset"""
        print("🚀 Generating ULTIMATE AA Member test data...")
        print("📞 Phone Numbers: 9, 10, 11 digits + invalid formats")
        print("📮 Postal Codes: 5, 6 digits + invalid formats")
        print("📅 Date Formats: ISO, US, EU, dot, dash + invalid formats")
        print("🔤 Special Characters: Valid/invalid names and addresses")
        print("📧 Email Formats: Standard, plus, dot, hyphen + invalid formats")
        print("🎯 All 11 AA Member Matching Criteria scenarios")
        
        all_test_data = []
        
        # Generate Match1 scenarios with all variations
        print("📊 Generating Match1 scenarios with all data variations...")
        all_test_data.extend(self.generate_match1_ultimate(200))
        
        # Generate Match2 scenarios with date variations
        print("📊 Generating Match2 scenarios with date format variations...")
        all_test_data.extend(self.generate_match2_date_variations(200))
        
        # Generate Match3 scenarios with special character variations
        print("📊 Generating Match3 scenarios with special character variations...")
        all_test_data.extend(self.generate_match3_special_char_variations(200))
        
        # Generate Match4 scenarios with email variations
        print("📊 Generating Match4 scenarios with email format variations...")
        all_test_data.extend(self.generate_match4_email_variations(200))
        
        # Generate remaining scenarios (Match5-Match10)
        print("📊 Generating Match5-Match10 scenarios...")
        all_test_data.extend(self.generate_remaining_scenarios(600))
        
        # Generate comprehensive date test scenarios
        print("📊 Generating comprehensive date test scenarios...")
        all_test_data.extend(self.generate_date_test_scenarios(200))
        
        # Generate special character test scenarios
        print("📊 Generating special character test scenarios...")
        all_test_data.extend(self.generate_special_char_test_scenarios(200))
        
        # Generate email test scenarios
        print("📊 Generating email test scenarios...")
        all_test_data.extend(self.generate_email_test_scenarios(200))
        
        # Generate phone test scenarios
        print("📊 Generating phone test scenarios...")
        all_test_data.extend(self.generate_phone_test_scenarios(200))
        
        # Generate postal test scenarios
        print("📊 Generating postal test scenarios...")
        all_test_data.extend(self.generate_postal_test_scenarios(200))
        
        # Generate data quality test scenarios
        print("📊 Generating comprehensive data quality test scenarios...")
        all_test_data.extend(self.generate_comprehensive_data_quality_scenarios())
        
        # Generate edge cases and boundary conditions
        print("📊 Generating ultimate edge cases...")
        all_test_data.extend(self.generate_ultimate_edge_cases(100))
        
        # Generate invalid scenarios
        print("📊 Generating invalid scenarios...")
        all_test_data.extend(self.generate_invalid_scenarios(100))
        
        print(f"✅ Generated {len(all_test_data)} ultimate test records")
        return all_test_data
    
    def generate_match1_ultimate(self, count=200):
        """Match1 with all possible data variations"""
        records = []
        date_formats = ['valid_iso', 'valid_us', 'valid_eu', 'valid_dot', 'valid_dash']
        name_types = ['valid', 'invalid']
        address_types = ['valid', 'invalid']
        email_formats = ['valid_standard', 'valid_plus', 'valid_dot', 'valid_hyphen']
        phone_types = ['valid_10_digit', 'valid_11_digit', 'valid_9_digit']
        postal_types = ['valid_5_digit', 'valid_6_digit']
        
        for i in range(count):
            date_format = random.choice(date_formats)
            name_type = random.choice(name_types)
            address_type = random.choice(address_types)
            email_format = random.choice(email_formats)
            phone_type = random.choice(phone_types)
            postal_type = random.choice(postal_types)
            
            base_record = self.validator.generate_comprehensive_test_record(
                date_format, name_type, address_type, email_format
            )
            
            # Override phone and postal with specific types
            phone_scenarios = self.enhanced_generator.generate_phone_scenarios()
            postal_scenarios = self.enhanced_generator.generate_postal_code_scenarios()
            base_record['PHONE_NBR'] = phone_scenarios[phone_type]
            base_record['POSTAL_CD'] = postal_scenarios[postal_type]
            
            records.append({
                'scenario': 'Match1',
                'description': f'Ultimate Match1 with {date_format} date, {name_type} names, {address_type} address, {email_format} email, {phone_type} phone, {postal_type} postal',
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
                'expected_result': 'Match1',
                'date_format': date_format,
                'name_type': name_type,
                'address_type': address_type,
                'email_format': email_format,
                'phone_type': phone_type,
                'postal_type': postal_type
            })
        
        return records
    
    def generate_match2_date_variations(self, count=200):
        """Match2 with date format variations"""
        records = []
        date_formats = ['valid_iso', 'valid_us', 'valid_eu', 'valid_dot', 'valid_dash', 
                       'invalid_format', 'invalid_future', 'invalid_past', 'invalid_leap']
        
        for i in range(count):
            date_format = random.choice(date_formats)
            base_record = self.validator.generate_comprehensive_test_record(date_format, 'valid', 'valid', 'valid_standard')
            
            records.append({
                'scenario': 'Match2',
                'description': f'Match2 with {date_format} date format',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.validator.special_characters['valid_names'][0],  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match2',
                'date_format': date_format
            })
        
        return records
    
    def generate_match3_special_char_variations(self, count=200):
        """Match3 with special character variations"""
        records = []
        name_types = ['valid', 'invalid']
        address_types = ['valid', 'invalid']
        
        for i in range(count):
            name_type = random.choice(name_types)
            address_type = random.choice(address_types)
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', name_type, address_type, 'valid_standard')
            
            records.append({
                'scenario': 'Match3',
                'description': f'Match3 with {name_type} names and {address_type} address',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.validator.special_characters['valid_names'][0],  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.validator.email_formats['valid_standard'],  # Different email
                    'PHONE_NBR': base_record['PHONE_NBR'],  # Same phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match3',
                'name_type': name_type,
                'address_type': address_type
            })
        
        return records
    
    def generate_match4_email_variations(self, count=200):
        """Match4 with email format variations"""
        records = []
        email_formats = ['valid_standard', 'valid_plus', 'valid_dot', 'valid_hyphen', 'valid_subdomain',
                        'invalid_no_at', 'invalid_no_domain', 'invalid_no_user', 'invalid_spaces', 'invalid_special']
        
        for i in range(count):
            email_format = random.choice(email_formats)
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', email_format)
            
            records.append({
                'scenario': 'Match4',
                'description': f'Match4 with {email_format} email format',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': self.validator.special_characters['valid_names'][0],  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.validator.email_formats['valid_standard'],  # Different email
                    'PHONE_NBR': self.enhanced_generator.generate_phone_scenarios()['valid_10_digit'],  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match4',
                'email_format': email_format
            })
        
        return records
    
    def generate_remaining_scenarios(self, count):
        """Generate Match5-Match10 scenarios"""
        scenarios = []
        
        for i in range(count):
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
            
            # Randomly select scenario type
            scenario_type = random.choice(['Match5', 'Match6', 'Match7', 'Match8', 'Match9', 'Match10'])
            
            if scenario_type in ['Match5', 'Match6']:
                # Invalid AA number, email match scenarios
                app_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'LYLTY_ACCT_ID': 'INVALID123',
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
                    'LYLTY_ACCT_ID': 'INVALID123',
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.validator.email_formats['valid_standard'],
                    'PHONE_NBR': base_record['PHONE_NBR'],
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
                    'LYLTY_ACCT_ID': 'INVALID123',
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': self.validator.email_formats['valid_standard'],
                    'PHONE_NBR': self.enhanced_generator.generate_phone_scenarios()['valid_10_digit'],
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
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
    
    def generate_date_test_scenarios(self, count=200):
        """Generate comprehensive date test scenarios"""
        records = []
        date_scenarios = self.validator.generate_date_scenarios()
        
        for date_format, date_value in date_scenarios.items():
            for i in range(count // len(date_scenarios)):
                base_record = self.validator.generate_comprehensive_test_record(date_format, 'valid', 'valid', 'valid_standard')
                
                records.append({
                    'scenario': f'DateTest_{date_format}',
                    'description': f'Date test scenario for {date_format} format',
                    'aa_record': base_record,
                    'application_record': {
                        'FIRST_NM': base_record['FIRST_NM'],
                        'LAST_NM': base_record['LAST_NM'],
                        'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                        'BIRTH_DT': date_value,
                        'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                        'PHONE_NBR': base_record['PHONE_NBR'],
                        'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                        'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                        'CITY_NM': base_record['CITY_NM'],
                        'POSTAL_CD': base_record['POSTAL_CD']
                    },
                    'expected_result': 'Valid' if 'valid' in date_format else 'Invalid',
                    'date_format': date_format,
                    'test_date': date_value
                })
        
        return records
    
    def generate_special_char_test_scenarios(self, count=200):
        """Generate special character test scenarios"""
        records = []
        special_scenarios = self.validator.generate_special_character_scenarios()
        
        for category, examples in special_scenarios.items():
            for example in examples:
                for i in range(count // (len(special_scenarios) * 2)):  # Divide by total examples
                    base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
                    
                    if 'name' in category:
                        base_record['FIRST_NM'] = example
                        field_type = 'name'
                    else:
                        base_record['STREET_LINE_1_TXT'] = example
                        field_type = 'address'
                    
                    records.append({
                        'scenario': f'SpecialCharTest_{category}',
                        'description': f'Special character test for {category}',
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
                        'expected_result': 'Valid' if 'valid' in category else 'Invalid',
                        'special_char_category': category,
                        'test_value': example,
                        'field_type': field_type
                    })
        
        return records
    
    def generate_email_test_scenarios(self, count=200):
        """Generate email test scenarios"""
        records = []
        email_scenarios = self.validator.generate_email_scenarios()
        
        for email_format, email_value in email_scenarios.items():
            for i in range(count // len(email_scenarios)):
                base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', email_format)
                
                records.append({
                    'scenario': f'EmailTest_{email_format}',
                    'description': f'Email test scenario for {email_format} format',
                    'aa_record': base_record,
                    'application_record': {
                        'FIRST_NM': base_record['FIRST_NM'],
                        'LAST_NM': base_record['LAST_NM'],
                        'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                        'BIRTH_DT': base_record['BIRTH_DT'],
                        'EMAIL_ADDR_TXT': email_value,
                        'PHONE_NBR': base_record['PHONE_NBR'],
                        'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                        'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                        'CITY_NM': base_record['CITY_NM'],
                        'POSTAL_CD': base_record['POSTAL_CD']
                    },
                    'expected_result': 'Valid' if 'valid' in email_format else 'Invalid',
                    'email_format': email_format,
                    'test_email': email_value
                })
        
        return records
    
    def generate_phone_test_scenarios(self, count=200):
        """Generate phone test scenarios"""
        records = []
        phone_scenarios = self.enhanced_generator.generate_phone_scenarios()
        
        for phone_type, phone_number in phone_scenarios.items():
            for i in range(count // len(phone_scenarios)):
                base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
                base_record['PHONE_NBR'] = phone_number
                
                records.append({
                    'scenario': f'PhoneTest_{phone_type}',
                    'description': f'Phone test scenario for {phone_type}',
                    'aa_record': base_record,
                    'application_record': {
                        'FIRST_NM': base_record['FIRST_NM'],
                        'LAST_NM': base_record['LAST_NM'],
                        'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                        'BIRTH_DT': base_record['BIRTH_DT'],
                        'EMAIL_ADDR_TXT': base_record['EMAIL_ADDR_TXT'],
                        'PHONE_NBR': phone_number,
                        'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],
                        'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                        'CITY_NM': base_record['CITY_NM'],
                        'POSTAL_CD': base_record['POSTAL_CD']
                    },
                    'expected_result': 'Valid' if 'valid' in phone_type else 'Invalid',
                    'phone_type': phone_type,
                    'test_phone': phone_number
                })
        
        return records
    
    def generate_postal_test_scenarios(self, count=200):
        """Generate postal test scenarios"""
        records = []
        postal_scenarios = self.enhanced_generator.generate_postal_code_scenarios()
        
        for postal_type, postal_code in postal_scenarios.items():
            for i in range(count // len(postal_scenarios)):
                base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
                base_record['POSTAL_CD'] = postal_code
                
                records.append({
                    'scenario': f'PostalTest_{postal_type}',
                    'description': f'Postal test scenario for {postal_type}',
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
                        'POSTAL_CD': postal_code
                    },
                    'expected_result': 'Valid' if 'valid' in postal_type else 'Invalid',
                    'postal_type': postal_type,
                    'test_postal': postal_code
                })
        
        return records
    
    def generate_comprehensive_data_quality_scenarios(self):
        """Generate comprehensive data quality test scenarios"""
        scenarios = []
        
        # Date quality tests
        date_scenarios = self.validator.generate_date_scenarios()
        for date_format, date_value in date_scenarios.items():
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
            base_record['BIRTH_DT'] = date_value
            
            scenarios.append({
                'scenario': f'DataQuality_Date_{date_format}',
                'description': f'Data quality test for {date_format} date format',
                'aa_record': base_record,
                'expected_result': 'Valid' if 'valid' in date_format else 'Data Quality Error'
            })
        
        # Special character quality tests
        special_scenarios = self.validator.generate_special_character_scenarios()
        for category, examples in special_scenarios.items():
            for example in examples[:2]:  # Limit to 2 examples per category
                base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
                
                if 'name' in category:
                    base_record['FIRST_NM'] = example
                else:
                    base_record['STREET_LINE_1_TXT'] = example
                
                scenarios.append({
                    'scenario': f'DataQuality_SpecialChar_{category}',
                    'description': f'Data quality test for {category} special characters',
                    'aa_record': base_record,
                    'expected_result': 'Valid' if 'valid' in category else 'Data Quality Error'
                })
        
        # Email quality tests
        email_scenarios = self.validator.generate_email_scenarios()
        for email_format, email_value in email_scenarios.items():
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
            base_record['EMAIL_ADDR_TXT'] = email_value
            
            scenarios.append({
                'scenario': f'DataQuality_Email_{email_format}',
                'description': f'Data quality test for {email_format} email format',
                'aa_record': base_record,
                'expected_result': 'Valid' if 'valid' in email_format else 'Data Quality Error'
            })
        
        return scenarios
    
    def generate_ultimate_edge_cases(self, count):
        """Generate ultimate edge cases"""
        scenarios = []
        
        for i in range(count):
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
            
            # Randomly select edge case type
            edge_case = random.choice([
                'unicode_names', 'very_long_address', 'very_short_address', 
                'special_chars_extreme', 'minimal_data', 'maximal_data',
                'mixed_formats', 'boundary_dates'
            ])
            
            if edge_case == 'unicode_names':
                base_record['FIRST_NM'] = "李小明"
                base_record['LAST_NM'] = "王"
                
            elif edge_case == 'very_long_address':
                base_record['STREET_LINE_1_TXT'] = 'A' * 100
                base_record['STREET_LINE_2_TXT'] = 'B' * 50
                
            elif edge_case == 'very_short_address':
                base_record['STREET_LINE_1_TXT'] = '123'
                base_record['STREET_LINE_2_TXT'] = ''
                
            elif edge_case == 'special_chars_extreme':
                base_record['FIRST_NM'] = "José-María O'Connor-Smith"
                base_record['LAST_NM'] = "Van Der Berg-García"
                
            elif edge_case == 'minimal_data':
                # Keep only required fields
                minimal_record = {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': base_record['LAST_NM'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID']
                }
                base_record = minimal_record
                
            elif edge_case == 'mixed_formats':
                base_record['BIRTH_DT'] = '25/12/2023'  # EU format
                base_record['PHONE_NBR'] = '1-800-555-0199'  # Formatted phone
                base_record['POSTAL_CD'] = '12345-6789'  # Extended postal
                
            elif edge_case == 'boundary_dates':
                base_record['BIRTH_DT'] = '1900-01-01'  # Very old
                base_record['PGM_ENROLL_DT'] = '2024-12-31'  # Recent
                
            scenarios.append({
                'scenario': f'UltimateEdgeCase_{edge_case}',
                'description': f'Ultimate edge case: {edge_case}',
                'aa_record': base_record,
                'expected_result': 'Edge Case'
            })
        
        return scenarios
    
    def generate_invalid_scenarios(self, count):
        """Generate invalid scenarios"""
        scenarios = []
        
        for i in range(count):
            base_record = self.validator.generate_comprehensive_test_record('valid_iso', 'valid', 'valid', 'valid_standard')
            
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
    
    def save_test_data(self, test_data, filename='aa_ultimate_test_data.json'):
        """Save ultimate test data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, default=str, ensure_ascii=False)
        print(f"💾 Ultimate test data saved to {filename}")
    
    def generate_ultimate_summary_report(self, test_data):
        """Generate ultimate summary report"""
        scenario_counts = {}
        date_format_counts = {}
        name_type_counts = {}
        address_type_counts = {}
        email_format_counts = {}
        phone_type_counts = {}
        postal_type_counts = {}
        
        for record in test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
            
            if 'date_format' in record:
                date_format = record['date_format']
                date_format_counts[date_format] = date_format_counts.get(date_format, 0) + 1
            
            if 'name_type' in record:
                name_type = record['name_type']
                name_type_counts[name_type] = name_type_counts.get(name_type, 0) + 1
            
            if 'address_type' in record:
                address_type = record['address_type']
                address_type_counts[address_type] = address_type_counts.get(address_type, 0) + 1
            
            if 'email_format' in record:
                email_format = record['email_format']
                email_format_counts[email_format] = email_format_counts.get(email_format, 0) + 1
            
            if 'phone_type' in record:
                phone_type = record['phone_type']
                phone_type_counts[phone_type] = phone_type_counts.get(phone_type, 0) + 1
            
            if 'postal_type' in record:
                postal_type = record['postal_type']
                postal_type_counts[postal_type] = postal_type_counts.get(postal_type, 0) + 1
        
        print("\n📈 ULTIMATE TEST DATA SUMMARY REPORT")
        print("=" * 70)
        print("SCENARIO DISTRIBUTION:")
        for scenario, count in sorted(scenario_counts.items()):
            print(f"  {scenario:<30}: {count:>4} records")
        
        if date_format_counts:
            print("\nDATE FORMAT DISTRIBUTION:")
            for date_format, count in sorted(date_format_counts.items()):
                print(f"  {date_format:<30}: {count:>4} records")
        
        if name_type_counts:
            print("\nNAME TYPE DISTRIBUTION:")
            for name_type, count in sorted(name_type_counts.items()):
                print(f"  {name_type:<30}: {count:>4} records")
        
        if address_type_counts:
            print("\nADDRESS TYPE DISTRIBUTION:")
            for address_type, count in sorted(address_type_counts.items()):
                print(f"  {address_type:<30}: {count:>4} records")
        
        if email_format_counts:
            print("\nEMAIL FORMAT DISTRIBUTION:")
            for email_format, count in sorted(email_format_counts.items()):
                print(f"  {email_format:<30}: {count:>4} records")
        
        if phone_type_counts:
            print("\nPHONE TYPE DISTRIBUTION:")
            for phone_type, count in sorted(phone_type_counts.items()):
                print(f"  {phone_type:<30}: {count:>4} records")
        
        if postal_type_counts:
            print("\nPOSTAL TYPE DISTRIBUTION:")
            for postal_type, count in sorted(postal_type_counts.items()):
                print(f"  {postal_type:<30}: {count:>4} records")
        
        print("=" * 70)
        print(f"Total Records: {len(test_data)}")

if __name__ == "__main__":
    generator = AAUltimateTestGenerator()
    
    # Generate ultimate test data
    test_data = generator.generate_ultimate_test_data(2000)
    
    # Save to file
    generator.save_test_data(test_data)
    
    # Generate summary report
    generator.generate_ultimate_summary_report(test_data)
    
    print("\n🎉 ULTIMATE AA Member test data generation completed!")
    print("📞 All phone number scenarios covered (9, 10, 11 digits)")
    print("📮 All postal code scenarios covered (5, 6 digits)")
    print("📅 All date format scenarios covered (ISO, US, EU, dot, dash)")
    print("🔤 All special character scenarios covered (valid/invalid)")
    print("📧 All email format scenarios covered (standard, plus, dot, hyphen)")
    print("🎯 All 11 AA Member Matching Criteria scenarios covered")
