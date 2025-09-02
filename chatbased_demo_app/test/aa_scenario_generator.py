#!/usr/bin/env python3
"""
AA Member Matching Scenarios Generator
"""

import json
import random
from datetime import datetime, timedelta
from aa_test_generator import AAMemberTestDataGenerator
from faker import Faker

fake = Faker()

class AAScenarioGenerator(AAMemberTestDataGenerator):
    
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
                    'POSTAL_CD': base_record['POSTAL_CD']
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
                    'LAST_NM': fake.last_name(),  # Different last name
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
            base_record = self.generate_base_record()
            # Last name and email are different, but phone matches
            records.append({
                'scenario': 'Match3',
                'description': 'Last name and email mismatch but phone matches',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': fake.last_name(),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': fake.email(),  # Different email
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
            base_record = self.generate_base_record()
            # Last name, email, and phone are different, but address matches
            records.append({
                'scenario': 'Match4',
                'description': 'Only address matches with valid AA number',
                'aa_record': base_record,
                'application_record': {
                    'FIRST_NM': base_record['FIRST_NM'],
                    'LAST_NM': fake.last_name(),  # Different last name
                    'LYLTY_ACCT_ID': base_record['LYLTY_ACCT_ID'],
                    'BIRTH_DT': base_record['BIRTH_DT'],
                    'EMAIL_ADDR_TXT': fake.email(),  # Different email
                    'PHONE_NBR': fake.numerify(text='##########'),  # Different phone
                    'STREET_LINE_1_TXT': base_record['STREET_LINE_1_TXT'],  # Same address
                    'STREET_LINE_2_TXT': base_record['STREET_LINE_2_TXT'],
                    'CITY_NM': base_record['CITY_NM'],
                    'POSTAL_CD': base_record['POSTAL_CD']
                },
                'expected_result': 'Match4'
            })
        return records

if __name__ == "__main__":
    generator = AAScenarioGenerator()
    print("AA Scenario Generator initialized")
