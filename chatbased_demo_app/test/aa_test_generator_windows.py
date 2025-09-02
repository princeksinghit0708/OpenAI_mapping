#!/usr/bin/env python3
"""
AA Member Test Data Generator - Windows Compatible
Generates clean test data with proper formatting for Windows systems
"""

import json
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import uuid
import re

fake = Faker()

class AAMemberTestDataGeneratorWindows:
    def __init__(self):
        self.test_scenarios = {
            'Match1': 'First Name + Last Name + AAdvantage Number + DOB match',
            'Match2': 'First Name + AAdvantage Number + Email + DOB match (Last Name mismatch)',
            'Match3': 'First Name + AAdvantage Number + Phone + DOB match (Last Name mismatch)',
            'Match4': 'First Name + AAdvantage Number + Address + DOB match (Last Name mismatch)',
            'Match5': 'First Name + Last Name + Email + DOB match (Invalid AA Number, Single Record)',
            'Match6': 'First Name + Last Name + Email + DOB match (Invalid AA Number, Multiple Records)',
            'Match7': 'First Name + Last Name + Phone + DOB match (Invalid AA Number, Single Record)',
            'Match8': 'First Name + Last Name + Phone + DOB match (Invalid AA Number, Multiple Records)',
            'Match9': 'First Name + Last Name + Address + DOB match (Invalid AA Number, Single Record)',
            'Match10': 'First Name + Last Name + Address + DOB match (Invalid AA Number, Multiple Records)',
            'Invalid': 'No matching criteria met'
        }
        
    def generate_clean_aa_id(self):
        """Generate a clean AAdvantage ID"""
        return fake.bothify(text='??#####').upper()
    
    def generate_clean_phone(self):
        """Generate a clean 10-digit phone number"""
        return fake.numerify(text='##########')
    
    def generate_clean_email(self):
        """Generate a clean email address"""
        return fake.email().lower()
    
    def generate_clean_postal_code(self):
        """Generate a clean 5-digit postal code"""
        return fake.numerify(text='#####')
    
    def generate_clean_date(self, start_date='-80y', end_date='-18y'):
        """Generate a clean date string"""
        return fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
    
    def generate_clean_name(self, name_type='first'):
        """Generate a clean name without special characters"""
        if name_type == 'first':
            name = fake.first_name()
        else:
            name = fake.last_name()
        
        # Remove any special characters that might cause issues
        name = re.sub(r'[^\w\s-]', '', name)
        return name.strip()
    
    def generate_clean_address(self):
        """Generate a clean address"""
        address = fake.street_address()
        # Clean up any problematic characters
        address = re.sub(r'[^\w\s#.-]', '', address)
        return address.strip()
    
    def generate_clean_city(self):
        """Generate a clean city name"""
        city = fake.city()
        # Clean up any problematic characters
        city = re.sub(r'[^\w\s-]', '', city)
        return city.strip()
        
    def generate_base_record(self):
        """Generate base AA member record with clean data"""
        return {
            "LYLTY_ACCT_ID": self.generate_clean_aa_id(),
            "LYLTY_LEVEL_IND": random.choice(['N', 'G', 'P', 'E', 'P']),
            "OPT_IN_ALL3_IND": random.choice(['Y', 'N']),
            "EMAIL_OPEN_RATE_12MO_PCT": round(random.uniform(0, 100), 3),
            "PGM_ENROLL_DT": self.generate_clean_date('-20y', 'today'),
            "AEM_CURR_QTY": random.randint(0, 10000),
            "LYLTY_PGM_ENROLL_SRC_CD": str(uuid.uuid4()).replace('-', '').upper()[:32],
            "PGM_TODT_AEM_QTY": random.randint(0, 1000),
            "AA_FLIGHT_SEG_24MO_QTY": random.randint(0, 500),
            "LYLTY_ACCT_LAST_ACTVTY_DT": self.generate_clean_date('-5y', 'today'),
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
            "LATEST_RES_CREATE_DT": self.generate_clean_date('-2y', 'today'),
            "RES_INACTVTY_DAY_QTY": random.randint(0, 1000),
            "LOUNGE_VISIT_12MO_QTY": random.randint(0, 50),
            "EXPD_CARD_QTY": random.randint(0, 5),
            "LATEST_FLIGHT_DT": self.generate_clean_date('-2y', 'today'),
            "LATEST_INTL_FLIGHT_DT": self.generate_clean_date('-5y', 'today'),
            "EXPD_PLAT_CARD_QTY": random.randint(0, 3),
            "FIRST_NM": self.generate_clean_name('first'),
            "LAST_NM": self.generate_clean_name('last'),
            "BIRTH_DT": self.generate_clean_date('-80y', '-18y'),
            "STREET_LINE_1_TXT": self.generate_clean_address(),
            "STREET_LINE_2_TXT": fake.secondary_address() or "",
            "CITY_NM": self.generate_clean_city(),
            "POSTAL_CD": self.generate_clean_postal_code(),
            "PHONE_NBR": self.generate_clean_phone(),
            "EMAIL_ADDR_TXT": self.generate_clean_email()
        }

if __name__ == "__main__":
    generator = AAMemberTestDataGeneratorWindows()
    print("AA Member Test Data Generator (Windows Compatible) initialized")
