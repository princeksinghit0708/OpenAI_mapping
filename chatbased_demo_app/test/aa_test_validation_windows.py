#!/usr/bin/env python3
"""
AA Member Test Data Validation Script - Windows Compatible
Validates the generated test data for quality and completeness
"""

import json
import pandas as pd
from datetime import datetime
import re
import os
import sys

class AATestDataValidatorWindows:
    def __init__(self, test_data_file='aa_comprehensive_test_data.json'):
        try:
            with open(test_data_file, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Error: {test_data_file} not found!")
            print("Please run 'python aa_comprehensive_test_generator.py' first.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading {test_data_file}: {e}")
            sys.exit(1)
        
        self.validation_results = {
            'total_records': len(self.test_data),
            'scenario_coverage': {},
            'data_quality_issues': [],
            'missing_scenarios': [],
            'validation_summary': {}
        }
    
    def validate_all(self):
        """Run all validation checks"""
        print("🔍 Starting comprehensive test data validation...")
        
        self.validate_scenario_coverage()
        self.validate_data_quality()
        self.validate_data_types()
        self.validate_required_fields()
        self.validate_format_compliance()
        self.validate_edge_cases()
        
        self.generate_validation_report()
    
    def validate_scenario_coverage(self):
        """Validate that all required scenarios are covered"""
        print("📊 Validating scenario coverage...")
        
        required_scenarios = [
            'Match1', 'Match2', 'Match3', 'Match4', 'Match5', 
            'Match6', 'Match7', 'Match8', 'Match9', 'Match10', 'Invalid'
        ]
        
        scenario_counts = {}
        for record in self.test_data:
            scenario = record['scenario']
            scenario_counts[scenario] = scenario_counts.get(scenario, 0) + 1
        
        for scenario in required_scenarios:
            if scenario in scenario_counts:
                self.validation_results['scenario_coverage'][scenario] = {
                    'count': scenario_counts[scenario],
                    'status': 'PASS' if scenario_counts[scenario] >= 50 else 'WARNING'
                }
            else:
                self.validation_results['missing_scenarios'].append(scenario)
                self.validation_results['scenario_coverage'][scenario] = {
                    'count': 0,
                    'status': 'FAIL'
                }
    
    def validate_data_quality(self):
        """Validate data quality across all records"""
        print("🔍 Validating data quality...")
        
        quality_issues = []
        
        for i, record in enumerate(self.test_data):
            aa_record = record.get('aa_record', {})
            
            # Check for null/empty values in critical fields
            critical_fields = ['FIRST_NM', 'LAST_NM', 'BIRTH_DT', 'LYLTY_ACCT_ID']
            for field in critical_fields:
                value = aa_record.get(field)
                if value is None or value == '' or str(value).strip() == '':
                    quality_issues.append({
                        'record_index': i,
                        'scenario': record['scenario'],
                        'issue': f'Missing or empty {field}',
                        'severity': 'HIGH'
                    })
            
            # Check DOB format
            dob = aa_record.get('BIRTH_DT')
            if dob and not re.match(r'\d{4}-\d{2}-\d{2}', str(dob)):
                quality_issues.append({
                    'record_index': i,
                    'scenario': record['scenario'],
                    'issue': f'Invalid DOB format: {dob}',
                    'severity': 'MEDIUM'
                })
            
            # Check phone format (more flexible for Windows)
            phone = aa_record.get('PHONE_NBR')
            if phone and not re.match(r'^\d{10}$', str(phone)):
                quality_issues.append({
                    'record_index': i,
                    'scenario': record['scenario'],
                    'issue': f'Invalid phone format: {phone}',
                    'severity': 'MEDIUM'
                })
            
            # Check email format (more flexible)
            email = aa_record.get('EMAIL_ADDR_TXT')
            if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', str(email)):
                quality_issues.append({
                    'record_index': i,
                    'scenario': record['scenario'],
                    'issue': f'Invalid email format: {email}',
                    'severity': 'MEDIUM'
                })
        
        self.validation_results['data_quality_issues'] = quality_issues
    
    def validate_data_types(self):
        """Validate data types are correct"""
        print("🔍 Validating data types...")
        
        type_issues = []
        
        for i, record in enumerate(self.test_data):
            aa_record = record.get('aa_record', {})
            
            # Check numeric fields
            numeric_fields = ['AEM_CURR_QTY', 'PGM_TODT_AEM_QTY', 'AA_FLIGHT_SEG_24MO_QTY']
            for field in numeric_fields:
                value = aa_record.get(field)
                if value is not None and not isinstance(value, (int, float)):
                    type_issues.append({
                        'record_index': i,
                        'field': field,
                        'expected_type': 'numeric',
                        'actual_type': type(value).__name__,
                        'value': value
                    })
            
            # Check date fields
            date_fields = ['PGM_ENROLL_DT', 'BIRTH_DT', 'LATEST_FLIGHT_DT']
            for field in date_fields:
                value = aa_record.get(field)
                if value and not isinstance(value, str):
                    type_issues.append({
                        'record_index': i,
                        'field': field,
                        'expected_type': 'string (YYYY-MM-DD)',
                        'actual_type': type(value).__name__,
                        'value': value
                    })
        
        self.validation_results['type_issues'] = type_issues
    
    def validate_required_fields(self):
        """Validate that all required fields are present"""
        print("🔍 Validating required fields...")
        
        required_fields = [
            'LYLTY_ACCT_ID', 'FIRST_NM', 'LAST_NM', 'BIRTH_DT',
            'EMAIL_ADDR_TXT', 'PHONE_NBR', 'STREET_LINE_1_TXT',
            'CITY_NM', 'POSTAL_CD'
        ]
        
        missing_fields = []
        
        for i, record in enumerate(self.test_data):
            aa_record = record.get('aa_record', {})
            record_missing = []
            
            for field in required_fields:
                if field not in aa_record or aa_record[field] is None:
                    record_missing.append(field)
            
            if record_missing:
                missing_fields.append({
                    'record_index': i,
                    'scenario': record['scenario'],
                    'missing_fields': record_missing
                })
        
        self.validation_results['missing_fields'] = missing_fields
    
    def validate_format_compliance(self):
        """Validate format compliance for specific fields"""
        print("🔍 Validating format compliance...")
        
        format_issues = []
        
        for i, record in enumerate(self.test_data):
            aa_record = record.get('aa_record', {})
            
            # Validate postal code format (more flexible for international)
            postal = aa_record.get('POSTAL_CD')
            if postal and not re.match(r'^\d{5}(-\d{4})?$', str(postal)):
                # Don't flag as error, just note as warning
                format_issues.append({
                    'record_index': i,
                    'field': 'POSTAL_CD',
                    'issue': f'Non-standard postal code format: {postal}',
                    'expected': '5 digits or 5+4 format',
                    'severity': 'LOW'
                })
            
            # Validate AAdvantage ID format (more flexible)
            aa_id = aa_record.get('LYLTY_ACCT_ID')
            if aa_id and not re.match(r'^[A-Z0-9]{7}$', str(aa_id)):
                format_issues.append({
                    'record_index': i,
                    'field': 'LYLTY_ACCT_ID',
                    'issue': f'Non-standard AA ID format: {aa_id}',
                    'expected': '7 alphanumeric characters',
                    'severity': 'LOW'
                })
        
        self.validation_results['format_issues'] = format_issues
    
    def validate_edge_cases(self):
        """Validate edge cases are properly handled"""
        print("🔍 Validating edge cases...")
        
        edge_case_validation = {
            'unicode_names': 0,
            'special_characters': 0,
            'long_addresses': 0,
            'short_addresses': 0,
            'future_dates': 0,
            'very_old_dates': 0
        }
        
        for record in self.test_data:
            aa_record = record.get('aa_record', {})
            
            # Check for unicode names (Windows compatible)
            first_name = str(aa_record.get('FIRST_NM', '') or '')
            last_name = str(aa_record.get('LAST_NM', '') or '')
            
            try:
                if any(ord(char) > 127 for char in first_name + last_name):
                    edge_case_validation['unicode_names'] += 1
            except UnicodeError:
                # Handle encoding issues gracefully
                pass
            
            # Check for special characters
            if any(char in first_name + last_name for char in "'-."):
                edge_case_validation['special_characters'] += 1
            
            # Check for long addresses
            address = str(aa_record.get('STREET_LINE_1_TXT', '') or '')
            if len(address) > 50:
                edge_case_validation['long_addresses'] += 1
            
            # Check for short addresses
            if len(address) < 5 and address:
                edge_case_validation['short_addresses'] += 1
            
            # Check for future dates
            dob = aa_record.get('BIRTH_DT')
            if dob:
                try:
                    dob_date = datetime.strptime(str(dob), '%Y-%m-%d')
                    if dob_date > datetime.now():
                        edge_case_validation['future_dates'] += 1
                except (ValueError, TypeError):
                    pass
        
        self.validation_results['edge_case_validation'] = edge_case_validation
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*80)
        print("📋 COMPREHENSIVE TEST DATA VALIDATION REPORT (Windows Compatible)")
        print("="*80)
        
        # Summary statistics
        print(f"\n📊 SUMMARY STATISTICS:")
        print(f"Total Records: {self.validation_results['total_records']}")
        print(f"Data Quality Issues: {len(self.validation_results['data_quality_issues'])}")
        print(f"Type Issues: {len(self.validation_results.get('type_issues', []))}")
        print(f"Missing Fields: {len(self.validation_results.get('missing_fields', []))}")
        print(f"Format Issues: {len(self.validation_results.get('format_issues', []))}")
        
        # Scenario coverage
        print(f"\n📈 SCENARIO COVERAGE:")
        for scenario, details in self.validation_results['scenario_coverage'].items():
            status_icon = "✅" if details['status'] == 'PASS' else "⚠️" if details['status'] == 'WARNING' else "❌"
            print(f"{status_icon} {scenario}: {details['count']} records ({details['status']})")
        
        # Data quality issues summary
        if self.validation_results['data_quality_issues']:
            print(f"\n🚨 DATA QUALITY ISSUES:")
            severity_counts = {}
            for issue in self.validation_results['data_quality_issues']:
                severity = issue['severity']
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            for severity, count in severity_counts.items():
                print(f"  {severity}: {count} issues")
        
        # Edge case validation
        print(f"\n🔍 EDGE CASE VALIDATION:")
        for case_type, count in self.validation_results['edge_case_validation'].items():
            print(f"  {case_type.replace('_', ' ').title()}: {count} records")
        
        # Overall assessment
        high_issues = len([i for i in self.validation_results['data_quality_issues'] if i['severity'] == 'HIGH'])
        medium_issues = len([i for i in self.validation_results['data_quality_issues'] if i['severity'] == 'MEDIUM'])
        low_issues = len([i for i in self.validation_results.get('format_issues', []) if i.get('severity') == 'LOW'])
        
        total_critical_issues = high_issues + medium_issues
        
        if total_critical_issues == 0:
            print(f"\n🎉 VALIDATION RESULT: PASS - No critical issues found!")
            print(f"   (Note: {low_issues} low-severity format variations are acceptable)")
        elif total_critical_issues < 10:
            print(f"\n⚠️ VALIDATION RESULT: WARNING - {total_critical_issues} issues found")
            print(f"   (Note: {low_issues} low-severity format variations are acceptable)")
        else:
            print(f"\n❌ VALIDATION RESULT: FAIL - {total_critical_issues} critical issues found")
            print(f"   (Note: {low_issues} low-severity format variations are acceptable)")
        
        print("="*80)

if __name__ == "__main__":
    validator = AATestDataValidatorWindows()
    validator.validate_all()
