#!/usr/bin/env python3
"""
AA Member Data Quality Test Scenarios
"""

import json
import random
from datetime import datetime, timedelta
from aa_test_generator import AAMemberTestDataGenerator

class AADataQualityTests(AAMemberTestDataGenerator):
    
    def generate_data_quality_scenarios(self):
        """Generate comprehensive data quality test scenarios"""
        scenarios = []
        
        # 1. Missing/Null Data Scenarios
        scenarios.extend(self.generate_null_data_scenarios())
        
        # 2. Invalid Format Scenarios
        scenarios.extend(self.generate_invalid_format_scenarios())
        
        # 3. Boundary Value Scenarios
        scenarios.extend(self.generate_boundary_value_scenarios())
        
        # 4. Special Character Scenarios
        scenarios.extend(self.generate_special_character_scenarios())
        
        # 5. Case Sensitivity Scenarios
        scenarios.extend(self.generate_case_sensitivity_scenarios())
        
        return scenarios
    
    def generate_null_data_scenarios(self):
        """Test scenarios with null/missing data"""
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
        
        return scenarios
    
    def generate_invalid_format_scenarios(self):
        """Test scenarios with invalid data formats"""
        scenarios = []
        
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
        
        # Invalid postal code format
        base_record = self.generate_base_record()
        base_record['POSTAL_CD'] = '1234'  # Too short
        scenarios.append({
            'scenario': 'DataQuality_InvalidPostalCode',
            'description': 'Test with invalid postal code',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        return scenarios
    
    def generate_boundary_value_scenarios(self):
        """Test scenarios with boundary values"""
        scenarios = []
        
        # Very long names
        base_record = self.generate_base_record()
        base_record['FIRST_NM'] = 'A' * 100  # Very long first name
        scenarios.append({
            'scenario': 'DataQuality_LongFirstName',
            'description': 'Test with very long first name',
            'aa_record': base_record,
            'expected_result': 'Data Quality Warning'
        })
        
        # Very long address
        base_record = self.generate_base_record()
        base_record['STREET_LINE_1_TXT'] = 'A' * 200  # Very long address
        scenarios.append({
            'scenario': 'DataQuality_LongAddress',
            'description': 'Test with very long address',
            'aa_record': base_record,
            'expected_result': 'Data Quality Warning'
        })
        
        # Future DOB
        base_record = self.generate_base_record()
        base_record['BIRTH_DT'] = '2030-01-01'  # Future date
        scenarios.append({
            'scenario': 'DataQuality_FutureDOB',
            'description': 'Test with future date of birth',
            'aa_record': base_record,
            'expected_result': 'Data Quality Error'
        })
        
        # Very old DOB
        base_record = self.generate_base_record()
        base_record['BIRTH_DT'] = '1900-01-01'  # Very old date
        scenarios.append({
            'scenario': 'DataQuality_OldDOB',
            'description': 'Test with very old date of birth',
            'aa_record': base_record,
            'expected_result': 'Data Quality Warning'
        })
        
        return scenarios
    
    def generate_special_character_scenarios(self):
        """Test scenarios with special characters"""
        scenarios = []
        
        # Names with special characters
        base_record = self.generate_base_record()
        base_record['FIRST_NM'] = "José-María"
        base_record['LAST_NM'] = "O'Connor-Smith"
        scenarios.append({
            'scenario': 'DataQuality_SpecialCharacters',
            'description': 'Test with special characters in names',
            'aa_record': base_record,
            'expected_result': 'Valid'
        })
        
        # Address with special characters
        base_record = self.generate_base_record()
        base_record['STREET_LINE_1_TXT'] = "123 Main St. #4B"
        base_record['STREET_LINE_2_TXT'] = "Apt. 2-C"
        scenarios.append({
            'scenario': 'DataQuality_AddressSpecialChars',
            'description': 'Test with special characters in address',
            'aa_record': base_record,
            'expected_result': 'Valid'
        })
        
        return scenarios
    
    def generate_case_sensitivity_scenarios(self):
        """Test scenarios with case sensitivity"""
        scenarios = []
        
        # Mixed case names
        base_record = self.generate_base_record()
        base_record['FIRST_NM'] = 'JOHN'
        base_record['LAST_NM'] = 'smith'
        scenarios.append({
            'scenario': 'DataQuality_CaseSensitivity',
            'description': 'Test case sensitivity in names',
            'aa_record': base_record,
            'expected_result': 'Valid'
        })
        
        # Mixed case email
        base_record = self.generate_base_record()
        base_record['EMAIL_ADDR_TXT'] = 'JOHN.SMITH@EXAMPLE.COM'
        scenarios.append({
            'scenario': 'DataQuality_EmailCaseSensitivity',
            'description': 'Test case sensitivity in email',
            'aa_record': base_record,
            'expected_result': 'Valid'
        })
        
        return scenarios

if __name__ == "__main__":
    generator = AADataQualityTests()
    print("AA Data Quality Tests initialized")
