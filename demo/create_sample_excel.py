#!/usr/bin/env python3
"""
Create Sample Excel File for Metadata Validation Demo
Generates a realistic Excel file with field mappings for testing
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_sample_excel():
    """Create a sample Excel file with realistic banking field mappings"""
    
    # Sample data for banking field mappings
    sample_data = {
        'Physical Table': [
            'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY',
            'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY', 'ACCT_DLY',
            'CUST_DLY', 'CUST_DLY', 'CUST_DLY', 'CUST_DLY', 'CUST_DLY',
            'TXN_DLY', 'TXN_DLY', 'TXN_DLY', 'TXN_DLY', 'TXN_DLY'
        ],
        'Logical Name': [
            'Account Number', 'Account Balance', 'Currency Code', 'Account Status',
            'Opening Date', 'Account Type', 'Fee Amount', 'Interest Rate',
            'Customer ID', 'Customer Name', 'Customer Type', 'Customer Status',
            'Transaction ID', 'Transaction Amount', 'Transaction Type',
            'Transaction Date', 'Source System', 'Target System', 'Mapping Type',
            'Transformation Logic'
        ],
        'Physical Name': [
            'ACCT_NBR', 'ACCT_BAL', 'CURR_CD', 'ACCT_STAT_CD', 'OPEN_DT',
            'ACCT_TYP_CD', 'TXN_FEE_AMT', 'INT_RT', 'CUST_ID', 'CUST_NM',
            'CUST_TYP_CD', 'CUST_STAT_CD', 'TXN_ID', 'TXN_AMT', 'TXN_TYP_CD',
            'TXN_DT', 'SRC_SYS_CD', 'TGT_SYS_CD', 'MAPPING_TYP', 'TRANSFORM_LOGIC'
        ],
        'Data Type': [
            'String(20)', 'Decimal(15,2)', 'String(3)', 'String(1)', 'Date',
            'String(2)', 'Decimal(15,2)', 'Decimal(5,4)', 'String(20)', 'String(100)',
            'String(2)', 'String(1)', 'String(30)', 'Decimal(15,2)', 'String(2)',
            'Timestamp', 'String(10)', 'String(10)', 'String(20)', 'String(500)'
        ],
        'Source Table': [
            'EBS_ACCT', 'EBS_ACCT', 'EBS_ACCT', 'EBS_ACCT', 'EBS_ACCT',
            'EBS_ACCT', 'EBS_ACCT', 'EBS_ACCT', 'EBS_CUST', 'EBS_CUST',
            'EBS_CUST', 'EBS_CUST', 'EBS_TXN', 'EBS_TXN', 'EBS_TXN',
            'EBS_TXN', 'SYSTEM_CONFIG', 'SYSTEM_CONFIG', 'MAPPING_CONFIG', 'MAPPING_CONFIG'
        ],
        'Source Column': [
            'ACCOUNT_NUMBER', 'BALANCE', 'CURRENCY', 'STATUS', 'OPEN_DATE',
            'TYPE_CODE', 'FEE_AMOUNT', 'INTEREST_RATE', 'CUSTOMER_ID', 'CUSTOMER_NAME',
            'TYPE_CODE', 'STATUS_CODE', 'TRANSACTION_ID', 'AMOUNT', 'TYPE_CODE',
            'TRANSACTION_DATE', 'SOURCE_CODE', 'TARGET_CODE', 'MAPPING_TYPE', 'TRANSFORMATION'
        ],
        'Mapping Type': [
            'Direct', 'Direct', 'Direct', 'Direct', 'Direct',
            'Derived', 'Derived', 'Goldref', 'Direct', 'Direct',
            'Derived', 'Direct', 'Direct', 'Direct', 'Goldref',
            'Direct', 'Direct', 'Direct', 'Direct', 'Derived'
        ],
        'Transformation Logic': [
            '', '', '', '', '',
            'If ACCT_TYP_CD = "01" then "Savings" else "Checking"', 
            'TXN_FEE_AMT * 1.1', 
            'Lookup for standard interest rate from GOLDREF table',
            '', '', 
            'Case when CUST_TYP_CD = "01" then "Individual" else "Corporate"', 
            '', '', '', 
            'Lookup for transaction type description from GOLDREF table',
            '', '', '', '', 
            'UPPER(TRANSFORM_LOGIC)'
        ],
        'Description': [
            'Primary account identifier', 'Current account balance', 'Currency code (USD, EUR, etc.)',
            'Account status (A=Active, I=Inactive)', 'Date account was opened',
            'Account type classification', 'Transaction fee amount with 10% markup',
            'Interest rate from gold reference table', 'Customer identifier',
            'Customer full name', 'Customer type classification', 'Customer status',
            'Unique transaction identifier', 'Transaction amount', 'Transaction type from lookup',
            'Transaction timestamp', 'Source system identifier', 'Target system identifier',
            'Type of mapping applied', 'Applied transformation logic'
        ]
    }
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Create gold reference data
    goldref_data = {
        'Reference Table': [
            'GOLDREF_ACCT_TYPE', 'GOLDREF_ACCT_TYPE', 'GOLDREF_ACCT_TYPE',
            'GOLDREF_TXN_TYPE', 'GOLDREF_TXN_TYPE', 'GOLDREF_TXN_TYPE',
            'GOLDREF_INT_RATE', 'GOLDREF_INT_RATE', 'GOLDREF_INT_RATE'
        ],
        'Reference Code': [
            '01', '02', '03', '01', '02', '03', 'SAVINGS', 'CHECKING', 'LOAN'
        ],
        'Reference Value': [
            'Savings Account', 'Checking Account', 'Loan Account',
            'Debit Transaction', 'Credit Transaction', 'Transfer Transaction',
            '0.0250', '0.0100', '0.0750'
        ],
        'Description': [
            'Standard savings account type', 'Standard checking account type',
            'Standard loan account type', 'Debit from account', 'Credit to account',
            'Transfer between accounts', 'Standard savings interest rate',
            'Standard checking interest rate', 'Standard loan interest rate'
        ]
    }
    
    goldref_df = pd.DataFrame(goldref_data)
    
    # Create output directory
    output_dir = Path('data/input')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to Excel file
    excel_file = output_dir / 'ebs_IM_account_DATAhub_mapping_v8.0.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='datahub standard mapping', index=False)
        goldref_df.to_excel(writer, sheet_name='goldref', index=False)
    
    print(f"✅ Sample Excel file created: {excel_file}")
    print(f"📊 Main mapping sheet: {len(df)} rows")
    print(f"🥇 Gold reference sheet: {len(goldref_df)} rows")
    
    return excel_file

if __name__ == "__main__":
    create_sample_excel()
