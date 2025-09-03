#!/usr/bin/env python3
"""
Ultimate AA Member Test Data Validator
Comprehensive validation system for all test scenarios
"""

import json
import re
from datetime import datetime
from aa_comprehensive_data_validator import AAComprehensiveDataValidator

class AAUltimateValidator:
    def __init__(self, json_file='aa_ultimate_test_data.json'):
        self.json_file = json_file
        self.test_data = []
        self.validator = AAComprehensiveDataValidator()
        self.validation_results = {
            'total_records': 0,
            'passed': 0,
            'failed': 0,
            'errors': [],
            'scenario_results': {},
            'data_quality_issues': [],
            'format_issues': [],
            'edge_case_issues': []
        }
        self.load_data()
    
    def load_data(self):
        """Load test data from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
            print(f"📊 Loaded {len(self.test_data)} test records from {self.json_file}")
        except FileNotFoundError:
            print(f"❌ File {self.json_file} not found!")
            return
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return
    
    def validate_all_records(self):
        """Validate all test records comprehensively"""
        print("🔍 Starting comprehensive validation of all test records...")
        
        if not self.test_data:
            print("❌ No test data available for validation!")
            return
        
        self.validation_results['total_records'] = len(self.test_data)
        
        for i, record in enumerate(self.test_data):
            try:
                self.validate_single_record(record, i + 1)
            except Exception as e:
                self.validation_results['errors'].append({
                    'record_id': i + 1,
                    'scenario': record.get('scenario', 'Unknown'),
                    'error': str(e)
                })
                self.validation_results['failed'] += 1
        
        self.generate_validation_report()
    
    def validate_single_record(self, record, record_id):
        """Validate a single test record"""
        scenario = record.get('scenario', 'Unknown')
        aa_record = record.get('aa_record', {})
        app_record = record.get('application_record', {})
        
        validation_passed = True
        issues = []
        
        # Validate AA record if present
        if aa_record:
            aa_validation = self.validate_aa_record(aa_record)
            if not aa_validation['valid']:
                validation_passed = False
                issues.extend(aa_validation['issues'])
        
        # Validate application record if present
        if app_record:
            app_validation = self.validate_application_record(app_record)
            if not app_validation['valid']:
                validation_passed = False
                issues.extend(app_validation['issues'])
        
        # Validate scenario-specific logic
        scenario_validation = self.validate_scenario_logic(record)
        if not scenario_validation['valid']:
            validation_passed = False
            issues.extend(scenario_validation['issues'])
        
        # Update results
        if validation_passed:
            self.validation_results['passed'] += 1
        else:
            self.validation_results['failed'] += 1
            self.validation_results['data_quality_issues'].append({
                'record_id': record_id,
                'scenario': scenario,
                'issues': issues
            })
        
        # Track scenario results
        if scenario not in self.validation_results['scenario_results']:
            self.validation_results['scenario_results'][scenario] = {'passed': 0, 'failed': 0}
        
        if validation_passed:
            self.validation_results['scenario_results'][scenario]['passed'] += 1
        else:
            self.validation_results['scenario_results'][scenario]['failed'] += 1
    
    def validate_aa_record(self, aa_record):
        """Validate AA member record"""
        issues = []
        
        # Validate required fields
        required_fields = ['FIRST_NM', 'LAST_NM', 'LYLTY_ACCT_ID', 'BIRTH_DT']
        for field in required_fields:
            if field not in aa_record or not aa_record[field]:
                issues.append(f"Missing required field: {field}")
        
        # Validate AAdvantage ID format
        if 'LYLTY_ACCT_ID' in aa_record:
            aa_id_validation = self.validator.validate_aa_id_format(aa_record['LYLTY_ACCT_ID'])
            if not aa_id_validation['valid']:
                issues.append(f"AAdvantage ID validation failed: {aa_id_validation['error']}")
        
        # Validate date format
        if 'BIRTH_DT' in aa_record:
            date_validation = self.validate_date_field(aa_record['BIRTH_DT'])
            if not date_validation['valid']:
                issues.append(f"Birth date validation failed: {date_validation['error']}")
        
        # Validate name fields
        if 'FIRST_NM' in aa_record:
            name_validation = self.validator.validate_special_characters(aa_record['FIRST_NM'], 'name')
            if not name_validation['valid']:
                issues.append(f"First name validation failed: {name_validation['error']}")
        
        if 'LAST_NM' in aa_record:
            name_validation = self.validator.validate_special_characters(aa_record['LAST_NM'], 'name')
            if not name_validation['valid']:
                issues.append(f"Last name validation failed: {name_validation['error']}")
        
        # Validate email format
        if 'EMAIL_ADDR_TXT' in aa_record:
            email_validation = self.validator.validate_email_format(aa_record['EMAIL_ADDR_TXT'])
            if not email_validation['valid']:
                issues.append(f"Email validation failed: {email_validation['error']}")
        
        # Validate phone format
        if 'PHONE_NBR' in aa_record:
            phone_validation = self.validator.validate_phone_format(aa_record['PHONE_NBR'])
            if not phone_validation['valid']:
                issues.append(f"Phone validation failed: {phone_validation['error']}")
        
        # Validate postal format
        if 'POSTAL_CD' in aa_record:
            postal_validation = self.validator.validate_postal_format(aa_record['POSTAL_CD'])
            if not postal_validation['valid']:
                issues.append(f"Postal code validation failed: {postal_validation['error']}")
        
        # Validate address fields
        if 'STREET_LINE_1_TXT' in aa_record:
            address_validation = self.validator.validate_special_characters(aa_record['STREET_LINE_1_TXT'], 'address')
            if not address_validation['valid']:
                issues.append(f"Address validation failed: {address_validation['error']}")
        
        if 'CITY_NM' in aa_record:
            city_validation = self.validator.validate_special_characters(aa_record['CITY_NM'], 'city')
            if not city_validation['valid']:
                issues.append(f"City validation failed: {city_validation['error']}")
        
        return {'valid': len(issues) == 0, 'issues': issues}
    
    def validate_application_record(self, app_record):
        """Validate application record"""
        issues = []
        
        # Validate required fields
        required_fields = ['FIRST_NM', 'LAST_NM', 'BIRTH_DT']
        for field in required_fields:
            if field not in app_record or not app_record[field]:
                issues.append(f"Missing required application field: {field}")
        
        # Validate date format
        if 'BIRTH_DT' in app_record:
            date_validation = self.validate_date_field(app_record['BIRTH_DT'])
            if not date_validation['valid']:
                issues.append(f"Application birth date validation failed: {date_validation['error']}")
        
        # Validate name fields
        if 'FIRST_NM' in app_record:
            name_validation = self.validator.validate_special_characters(app_record['FIRST_NM'], 'name')
            if not name_validation['valid']:
                issues.append(f"Application first name validation failed: {name_validation['error']}")
        
        if 'LAST_NM' in app_record:
            name_validation = self.validator.validate_special_characters(app_record['LAST_NM'], 'name')
            if not name_validation['valid']:
                issues.append(f"Application last name validation failed: {name_validation['error']}")
        
        # Validate email format if present
        if 'EMAIL_ADDR_TXT' in app_record:
            email_validation = self.validator.validate_email_format(app_record['EMAIL_ADDR_TXT'])
            if not email_validation['valid']:
                issues.append(f"Application email validation failed: {email_validation['error']}")
        
        # Validate phone format if present
        if 'PHONE_NBR' in app_record:
            phone_validation = self.validator.validate_phone_format(app_record['PHONE_NBR'])
            if not phone_validation['valid']:
                issues.append(f"Application phone validation failed: {phone_validation['error']}")
        
        # Validate postal format if present
        if 'POSTAL_CD' in app_record:
            postal_validation = self.validator.validate_postal_format(app_record['POSTAL_CD'])
            if not postal_validation['valid']:
                issues.append(f"Application postal code validation failed: {postal_validation['error']}")
        
        return {'valid': len(issues) == 0, 'issues': issues}
    
    def validate_date_field(self, date_string):
        """Validate date field with multiple format support"""
        if not date_string:
            return {'valid': False, 'error': 'Date is empty'}
        
        # Try different date formats
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y']
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_string, date_format)
                if parsed_date > datetime.now():
                    return {'valid': False, 'error': 'Future date not allowed'}
                if parsed_date.year < 1900:
                    return {'valid': False, 'error': 'Date too old'}
                return {'valid': True, 'parsed_date': parsed_date}
            except ValueError:
                continue
        
        return {'valid': False, 'error': 'Invalid date format'}
    
    def validate_scenario_logic(self, record):
        """Validate scenario-specific logic"""
        issues = []
        scenario = record.get('scenario', 'Unknown')
        expected_result = record.get('expected_result', 'Unknown')
        
        # Validate that test scenarios have expected results
        if scenario.startswith('Match') or scenario == 'Invalid':
            if expected_result == 'Unknown':
                issues.append(f"Missing expected result for {scenario}")
        
        # Validate that data quality tests have appropriate test values
        if 'DataQuality' in scenario or 'Test' in scenario:
            if 'aa_record' not in record:
                issues.append(f"Missing AA record for {scenario}")
        
        # Validate edge cases have appropriate descriptions
        if 'UltimateEdgeCase' in scenario:
            if 'description' not in record or not record['description']:
                issues.append(f"Missing description for edge case {scenario}")
        
        return {'valid': len(issues) == 0, 'issues': issues}
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*70)
        print("🔍 ULTIMATE AA MEMBER TEST DATA VALIDATION REPORT")
        print("="*70)
        
        # Overall statistics
        total = self.validation_results['total_records']
        passed = self.validation_results['passed']
        failed = self.validation_results['failed']
        
        print(f"📊 OVERALL STATISTICS:")
        print(f"  Total Records: {total}")
        if total > 0:
            print(f"  Passed: {passed} ({passed/total*100:.1f}%)")
            print(f"  Failed: {failed} ({failed/total*100:.1f}%)")
        else:
            print(f"  Passed: {passed} (0.0%)")
            print(f"  Failed: {failed} (0.0%)")
        print(f"  Errors: {len(self.validation_results['errors'])}")
        
        # Scenario results
        print(f"\n📈 SCENARIO RESULTS:")
        for scenario, results in sorted(self.validation_results['scenario_results'].items()):
            total_scenario = results['passed'] + results['failed']
            pass_rate = results['passed'] / total_scenario * 100 if total_scenario > 0 else 0
            print(f"  {scenario:<30}: {results['passed']:>3}/{total_scenario:<3} ({pass_rate:>5.1f}%)")
        
        # Data quality issues summary
        if self.validation_results['data_quality_issues']:
            print(f"\n⚠️  DATA QUALITY ISSUES: {len(self.validation_results['data_quality_issues'])} records")
            
            # Group issues by type
            issue_types = {}
            for issue_record in self.validation_results['data_quality_issues']:
                for issue in issue_record['issues']:
                    issue_type = issue.split(':')[0] if ':' in issue else 'Other'
                    issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
            
            print("  Issue Types:")
            for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
                print(f"    {issue_type:<30}: {count:>3} issues")
        
        # Top failing scenarios
        failing_scenarios = [(scenario, results['failed']) for scenario, results in self.validation_results['scenario_results'].items() if results['failed'] > 0]
        if failing_scenarios:
            print(f"\n❌ TOP FAILING SCENARIOS:")
            for scenario, failed_count in sorted(failing_scenarios, key=lambda x: x[1], reverse=True)[:10]:
                print(f"    {scenario:<30}: {failed_count:>3} failures")
        
        # Validation conclusion
        print(f"\n🎯 VALIDATION CONCLUSION:")
        if total == 0:
            print("  ❌ NO DATA - No test records available for validation")
        elif failed == 0:
            print("  ✅ ALL TESTS PASSED - Data quality is excellent!")
        elif failed < total * 0.05:  # Less than 5% failure rate
            print("  ✅ EXCELLENT - Data quality is very good with minimal issues")
        elif failed < total * 0.10:  # Less than 10% failure rate
            print("  ⚠️  GOOD - Data quality is acceptable with some issues to review")
        else:
            print("  ❌ NEEDS ATTENTION - Data quality issues need to be addressed")
        
        print("="*70)
        
        # Save detailed report
        self.save_validation_report()
    
    def save_validation_report(self):
        """Save detailed validation report to file"""
        report_data = {
            'validation_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_records': self.validation_results['total_records'],
                'passed': self.validation_results['passed'],
                'failed': self.validation_results['failed'],
                'error_count': len(self.validation_results['errors'])
            },
            'scenario_results': self.validation_results['scenario_results'],
            'data_quality_issues': self.validation_results['data_quality_issues'][:50],  # Limit to first 50
            'errors': self.validation_results['errors'][:50]  # Limit to first 50
        }
        
        with open('aa_ultimate_validation_report.json', 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"💾 Detailed validation report saved to: aa_ultimate_validation_report.json")

if __name__ == "__main__":
    validator = AAUltimateValidator()
    validator.validate_all_records()
