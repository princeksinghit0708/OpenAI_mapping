#!/usr/bin/env python3
"""
Comprehensive AA Member Data Validator
Validates date formats, special characters, and all data quality aspects
"""

import re
import json
from datetime import datetime, timedelta
from faker import Faker
import random
import uuid

fake = Faker()

class AAComprehensiveDataValidator:
    def __init__(self):
        self.date_formats = {
            'valid_iso': '%Y-%m-%d',  # 2023-12-25
            'valid_us': '%m/%d/%Y',   # 12/25/2023
            'valid_eu': '%d/%m/%Y',   # 25/12/2023
            'valid_dot': '%d.%m.%Y',  # 25.12.2023
            'valid_dash': '%d-%m-%Y', # 25-12-2023
            'invalid_format': 'invalid',
            'invalid_future': 'future',
            'invalid_past': 'past',
            'invalid_leap': 'leap'
        }
        
        self.special_characters = {
            'valid_names': ['José', 'María', "O'Connor", 'Smith-Jones', 'Van Der Berg'],
            'valid_addresses': ['123 Main St. #4B', 'Apt. 2-C', 'Suite 100-A'],
            'invalid_names': ['José@María', 'O\'Connor<script>', 'Smith<>Jones'],
            'invalid_addresses': ['123 Main St. <script>', 'Apt. 2-C; DROP TABLE', 'Suite 100-A OR 1=1']
        }
        
        self.email_formats = {
            'valid_standard': 'user@example.com',
            'valid_plus': 'user+tag@example.com',
            'valid_dot': 'user.name@example.com',
            'valid_hyphen': 'user-name@example.com',
            'valid_subdomain': 'user@sub.example.com',
            'invalid_no_at': 'userexample.com',
            'invalid_no_domain': 'user@',
            'invalid_no_user': '@example.com',
            'invalid_spaces': 'user @example.com',
            'invalid_special': 'user@example.com<script>'
        }
        
    def generate_date_scenarios(self):
        """Generate all date format scenarios"""
        date_scenarios = {}
        
        # Valid ISO format
        date_scenarios['valid_iso'] = fake.date_between(start_date='-80y', end_date='-18y').strftime('%Y-%m-%d')
        
        # Valid US format
        date_scenarios['valid_us'] = fake.date_between(start_date='-80y', end_date='-18y').strftime('%m/%d/%Y')
        
        # Valid EU format
        date_scenarios['valid_eu'] = fake.date_between(start_date='-80y', end_date='-18y').strftime('%d/%m/%Y')
        
        # Valid dot format
        date_scenarios['valid_dot'] = fake.date_between(start_date='-80y', end_date='-18y').strftime('%d.%m.%Y')
        
        # Valid dash format
        date_scenarios['valid_dash'] = fake.date_between(start_date='-80y', end_date='-18y').strftime('%d-%m-%Y')
        
        # Invalid format
        date_scenarios['invalid_format'] = '25/13/2023'  # Invalid month
        
        # Future date
        date_scenarios['invalid_future'] = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        
        # Too old date
        date_scenarios['invalid_past'] = '1800-01-01'
        
        # Invalid leap year
        date_scenarios['invalid_leap'] = '2023-02-29'  # 2023 is not a leap year
        
        return date_scenarios
    
    def generate_special_character_scenarios(self):
        """Generate special character scenarios"""
        return {
            'valid_names': self.special_characters['valid_names'],
            'valid_addresses': self.special_characters['valid_addresses'],
            'invalid_names': self.special_characters['invalid_names'],
            'invalid_addresses': self.special_characters['invalid_addresses']
        }
    
    def generate_email_scenarios(self):
        """Generate email format scenarios"""
        return self.email_formats
    
    def validate_date_format(self, date_string, expected_format):
        """Validate date format and return validation result"""
        try:
            if expected_format == 'valid_iso':
                parsed_date = datetime.strptime(date_string, '%Y-%m-%d')
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date'}
                if parsed_date.year < 1900:
                    return {'valid': False, 'error': 'Date too old'}
                return {'valid': True, 'parsed_date': parsed_date}
            
            elif expected_format == 'valid_us':
                parsed_date = datetime.strptime(date_string, '%m/%d/%Y')
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date'}
                return {'valid': True, 'parsed_date': parsed_date}
            
            elif expected_format == 'valid_eu':
                parsed_date = datetime.strptime(date_string, '%d/%m/%Y')
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date'}
                return {'valid': True, 'parsed_date': parsed_date}
            
            elif expected_format == 'valid_dot':
                parsed_date = datetime.strptime(date_string, '%d.%m.%Y')
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date'}
                return {'valid': True, 'parsed_date': parsed_date}
            
            elif expected_format == 'valid_dash':
                parsed_date = datetime.strptime(date_string, '%d-%m-%Y')
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date'}
                return {'valid': True, 'parsed_date': parsed_date}
            
            elif expected_format == 'invalid_format':
                return {'valid': False, 'error': 'Invalid date format'}
            
            elif expected_format == 'invalid_future':
                return {'valid': False, 'error': 'Future date not allowed'}
            
            elif expected_format == 'invalid_past':
                return {'valid': False, 'error': 'Date too old'}
            
            elif expected_format == 'invalid_leap':
                return {'valid': False, 'error': 'Invalid leap year date'}
            
        except ValueError as e:
            return {'valid': False, 'error': f'Date parsing error: {str(e)}'}
        
        return {'valid': False, 'error': 'Unknown format'}
    
    def validate_special_characters(self, text, field_type):
        """Validate special characters in text fields"""
        if field_type == 'name':
            # Allow common name characters: letters (including accented), spaces, hyphens, apostrophes, dots
            if re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", text):
                return {'valid': True, 'error': None}
            else:
                return {'valid': False, 'error': 'Invalid characters in name'}
        
        elif field_type == 'address':
            # Allow common address characters: letters, numbers, spaces, hyphens, dots, hash, comma
            if re.match(r"^[a-zA-Z0-9\s\-\.#\,]+$", text):
                return {'valid': True, 'error': None}
            else:
                return {'valid': False, 'error': 'Invalid characters in address'}
        
        elif field_type == 'city':
            # Allow common city characters: letters, spaces, hyphens, dots
            if re.match(r"^[a-zA-Z\s\-\.]+$", text):
                return {'valid': True, 'error': None}
            else:
                return {'valid': False, 'error': 'Invalid characters in city'}
        
        return {'valid': False, 'error': 'Unknown field type'}
    
    def validate_email_format(self, email):
        """Validate email format"""
        # Basic email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(email_pattern, email):
            # Additional checks
            if ' ' in email:
                return {'valid': False, 'error': 'Email contains spaces'}
            if email.count('@') != 1:
                return {'valid': False, 'error': 'Email must contain exactly one @'}
            if email.startswith('.') or email.endswith('.'):
                return {'valid': False, 'error': 'Email cannot start or end with dot'}
            return {'valid': True, 'error': None}
        else:
            return {'valid': False, 'error': 'Invalid email format'}
    
    def validate_phone_format(self, phone):
        """Validate phone number format"""
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', phone)
        
        if len(digits_only) == 10:
            return {'valid': True, 'format': '10-digit', 'error': None}
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return {'valid': True, 'format': '11-digit', 'error': None}
        elif len(digits_only) == 9:
            return {'valid': True, 'format': '9-digit', 'error': None}
        elif len(digits_only) < 9:
            return {'valid': False, 'format': 'short', 'error': 'Phone number too short'}
        elif len(digits_only) > 11:
            return {'valid': False, 'format': 'long', 'error': 'Phone number too long'}
        else:
            return {'valid': False, 'format': 'invalid', 'error': 'Invalid phone number format'}
    
    def validate_postal_format(self, postal):
        """Validate postal code format"""
        # Remove all non-digit characters for validation
        digits_only = re.sub(r'\D', '', postal)
        
        if len(digits_only) == 5:
            return {'valid': True, 'format': '5-digit', 'error': None}
        elif len(digits_only) == 6:
            return {'valid': True, 'format': '6-digit', 'error': None}
        elif len(digits_only) < 5:
            return {'valid': False, 'format': 'short', 'error': 'Postal code too short'}
        elif len(digits_only) > 6:
            return {'valid': False, 'format': 'long', 'error': 'Postal code too long'}
        else:
            return {'valid': False, 'format': 'invalid', 'error': 'Invalid postal code format'}
    
    def validate_aa_id_format(self, aa_id):
        """Validate AAdvantage ID format"""
        if not aa_id:
            return {'valid': False, 'error': 'AAdvantage ID is empty'}
        
        if len(aa_id) != 7:
            return {'valid': False, 'error': 'AAdvantage ID must be 7 characters'}
        
        if not re.match(r'^[A-Z0-9]{7}$', aa_id):
            return {'valid': False, 'error': 'AAdvantage ID must contain only uppercase letters and numbers'}
        
        return {'valid': True, 'error': None}
    
    def generate_comprehensive_test_record(self, date_format='valid_iso', name_type='valid', 
                                         address_type='valid', email_format='valid_standard'):
        """Generate a comprehensive test record with specified validation scenarios"""
        
        # Generate base record
        record = {
            "LYLTY_ACCT_ID": fake.bothify(text='??#####').upper(),
            "LYLTY_LEVEL_IND": random.choice(['N', 'G', 'P', 'E', 'P']),
            "OPT_IN_ALL3_IND": random.choice(['Y', 'N']),
            "EMAIL_OPEN_RATE_12MO_PCT": round(random.uniform(0, 100), 3),
            "PGM_ENROLL_DT": fake.date_between(start_date='-20y', end_date='today').strftime('%Y-%m-%d'),
            "AEM_CURR_QTY": random.randint(0, 10000),
            "LYLTY_PGM_ENROLL_SRC_CD": str(uuid.uuid4()).replace('-', '').upper()[:32],
            "PGM_TODT_AEM_QTY": random.randint(0, 1000),
            "AA_FLIGHT_SEG_24MO_QTY": random.randint(0, 500),
            "LYLTY_ACCT_LAST_ACTVTY_DT": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            "OA_FLIGHT_24MO_QTY": random.randint(0, 300),
            "FLIGHT_REDMPTN_TRANS_24MO_QTY": random.randint(0, 200),
            "TRIP_12MO_QTY": random.randint(0, 50),
            "REVNUE_TRIP_12MO_QTY": random.randint(0, 100),
            "AWD_TRIP_12MO_QTY": random.randint(0, 20),
            "REVNUE_OA_TRIP_12MO_QTY": random.randint(0, 50),
            "AWD_OA_TRIP_12MO_QTY": random.randint(0, 30),
            "DISCRETIONARY_TRIP_12MO_QTY": random.randint(0, 40),
            "NON_DISCRETIONARY_TRIP_12MO_QTY": random.randint(0, 60),
            "BLENDED_TRIP_12MO_QTY": random.randint(0, 50),
            "DIRECT_BKG_CHANL_TRIP_12MO_PCT": round(random.uniform(0, 100), 3),
            "MULTI_PARTY_TRIP_12MO_PCT": round(random.uniform(0, 50), 3),
            "REVNUE_AA_FUTURE_TRIP_QTY": random.randint(0, 20),
            "AWD_FUTURE_TRIP_QTY": random.randint(0, 15),
            "REVNUE_OA_FUTURE_TRIP_QTY": random.randint(0, 10),
            "AEM_EARN_24MO_QTY": random.randint(0, 5000),
            "NANB_EARN_AEM_12MO_QTY": random.randint(0, 2000),
            "AWD_FLIGHT_SEG_12MO_QTY": random.randint(0, 100),
            "NANE_PURCHS_AEM_12MO_IND": random.choice(['Yes', 'No']),
            "NANB_PARTNR_12MO_QTY": random.randint(0, 50),
            "NANB_TRANS_12MO_QTY": random.randint(0, 100),
            "LATEST_RES_CREATE_DT": fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            "RES_INACTVTY_DAY_QTY": random.randint(0, 1000),
            "LOUNGE_VISIT_12MO_QTY": random.randint(0, 50),
            "EXPD_CARD_QTY": random.randint(0, 5),
            "LATEST_FLIGHT_DT": fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
            "LATEST_INTL_FLIGHT_DT": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            "EXPD_PLAT_CARD_QTY": random.randint(0, 3),
            "STREET_LINE_2_TXT": fake.secondary_address() or "",
            "CITY_NM": fake.city(),
            "POSTAL_CD": fake.numerify(text='#####'),
            "PHONE_NBR": fake.numerify(text='##########')
        }
        
        # Apply date format
        date_scenarios = self.generate_date_scenarios()
        record["BIRTH_DT"] = date_scenarios[date_format]
        
        # Apply name format
        if name_type == 'valid':
            record["FIRST_NM"] = random.choice(self.special_characters['valid_names'])
            record["LAST_NM"] = random.choice(self.special_characters['valid_names'])
        else:
            record["FIRST_NM"] = random.choice(self.special_characters['invalid_names'])
            record["LAST_NM"] = random.choice(self.special_characters['invalid_names'])
        
        # Apply address format
        if address_type == 'valid':
            record["STREET_LINE_1_TXT"] = random.choice(self.special_characters['valid_addresses'])
        else:
            record["STREET_LINE_1_TXT"] = random.choice(self.special_characters['invalid_addresses'])
        
        # Apply email format
        record["EMAIL_ADDR_TXT"] = self.email_formats[email_format]
        
        return record

if __name__ == "__main__":
    validator = AAComprehensiveDataValidator()
    
    print("🔍 Comprehensive AA Member Data Validator")
    print("=" * 50)
    
    # Test date scenarios
    print("\n📅 Date Format Scenarios:")
    date_scenarios = validator.generate_date_scenarios()
    for format_type, date_value in date_scenarios.items():
        validation = validator.validate_date_format(date_value, format_type)
        status = "✅" if validation['valid'] else "❌"
        print(f"  {status} {format_type}: {date_value} - {validation.get('error', 'Valid')}")
    
    # Test special character scenarios
    print("\n🔤 Special Character Scenarios:")
    special_scenarios = validator.generate_special_character_scenarios()
    for category, examples in special_scenarios.items():
        print(f"  {category}:")
        for example in examples[:2]:  # Show first 2 examples
            if 'name' in category:
                validation = validator.validate_special_characters(example, 'name')
            else:
                validation = validator.validate_special_characters(example, 'address')
            status = "✅" if validation['valid'] else "❌"
            print(f"    {status} {example} - {validation.get('error', 'Valid')}")
    
    # Test email scenarios
    print("\n📧 Email Format Scenarios:")
    email_scenarios = validator.generate_email_scenarios()
    for format_type, email_value in email_scenarios.items():
        validation = validator.validate_email_format(email_value)
        status = "✅" if validation['valid'] else "❌"
        print(f"  {status} {format_type}: {email_value} - {validation.get('error', 'Valid')}")
    
    print("\n🎉 Comprehensive data validator initialized successfully!")
