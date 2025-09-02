#!/usr/bin/env python3
"""
AA Member Matching Criteria Test Data Generator
Senior Test Principal Architect Approach
"""

import json
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker
import uuid

fake = Faker()

class AAMemberTestDataGenerator:
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
        
    def generate_base_record(self):
        """Generate base AA member record"""
        return {
            "LYLTY_ACCT_ID": fake.bothify(text='??#####'),
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
            "FIRST_NM": fake.first_name(),
            "LAST_NM": fake.last_name(),
            "BIRTH_DT": fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
            "STREET_LINE_1_TXT": fake.street_address(),
            "STREET_LINE_2_TXT": fake.secondary_address(),
            "CITY_NM": fake.city(),
            "POSTAL_CD": fake.postcode(),
            "PHONE_NBR": fake.numerify(text='##########'),
            "EMAIL_ADDR_TXT": fake.email()
        }

if __name__ == "__main__":
    generator = AAMemberTestDataGenerator()
    print("AA Member Test Data Generator initialized")
