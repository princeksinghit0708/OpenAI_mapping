"""
Gold Reference Validator Agent - Validates data against gold reference standards
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from datetime import datetime
from loguru import logger

from ..core.base_agent import BaseAgent, AgentConfig
from ...core.models import (
    GoldReferenceDefinition, ValidationResult, FieldDefinition,
    TransformationRule
)


class GoldReferenceValidator(BaseAgent):
    """
    Gold Reference Validator Agent for ensuring data quality and standards compliance
    
    Capabilities:
    - Validate field values against gold reference data
    - Check lookup table consistency
    - Enforce business rules and standards
    - Generate compliance reports
    - Suggest corrections for non-compliant data
    """
    
    def __init__(self, config: AgentConfig, rag_engine=None, tools=None):
        super().__init__(config, rag_engine, tools)
        
        # Gold reference repository
        self.gold_references: Dict[str, GoldReferenceDefinition] = {}
        
        # Standard validation rules
        self.standard_validations = {
            'date_format': self._validate_date_format,
            'lookup_values': self._validate_lookup_values,
            'business_rules': self._validate_business_rules,
            'data_consistency': self._validate_data_consistency,
            'completeness': self._validate_completeness
        }
        
        # Reference data patterns (based on Excel screenshots)
        self.reference_patterns = {
            'branch_codes': {
                'pattern': r'^[A-Z0-9]{2,10}$',
                'description': 'Branch codes should be 2-10 alphanumeric characters'
            },
            'account_types': {
                'valid_values': ['SAVINGS', 'CHECKING', 'LOAN', 'CREDIT'],
                'description': 'Valid account types'
            },
            'currency_codes': {
                'pattern': r'^[A-Z]{3}$',
                'description': 'ISO 3-letter currency codes'
            },
            'date_formats': {
                'formats': ['YYYY-MM-DD', 'YYYYMMDD'],
                'description': 'Accepted date formats'
            }
        }
    
    async def register_gold_reference(self, gold_ref: GoldReferenceDefinition):
        """Register a gold reference definition"""
        try:
            logger.info(f"Registering gold reference: {gold_ref.name}")
            
            # Validate the gold reference itself
            validation = await self._validate_gold_reference_definition(gold_ref)
            
            if validation.is_valid:
                self.gold_references[gold_ref.name] = gold_ref
                logger.info(f"Successfully registered gold reference: {gold_ref.name}")
            else:
                logger.error(f"Invalid gold reference definition: {validation.errors}")
                raise ValueError(f"Invalid gold reference: {', '.join(validation.errors)}")
                
        except Exception as e:
            logger.error(f"Failed to register gold reference: {str(e)}")
            raise
    
    async def validate_field_against_goldref(self, 
                                           field_value: Any,
                                           field_def: FieldDefinition,
                                           gold_ref_name: str) -> ValidationResult:
        """Validate a field value against gold reference standards"""
        try:
            logger.info(f"Validating field {field_def.name} against gold reference {gold_ref_name}")
            
            if gold_ref_name not in self.gold_references:
                return ValidationResult(
                    is_valid=False,
                    errors=[f"Gold reference '{gold_ref_name}' not found"],
                    warnings=[],
                    suggestions=["Register the gold reference before validation"]
                )
            
            gold_ref = self.gold_references[gold_ref_name]
            errors = []
            warnings = []
            suggestions = []
            
            # Check against standard values
            if gold_ref.standard_values:
                if field_value not in gold_ref.standard_values.values():
                    errors.append(f"Value '{field_value}' not found in gold reference standards")
                    suggestions.append(f"Valid values: {list(gold_ref.standard_values.values())}")
            
            # Apply business rules
            for rule in gold_ref.business_rules:
                rule_validation = await self._apply_business_rule(field_value, rule, field_def)
                if not rule_validation.is_valid:
                    errors.extend(rule_validation.errors)
                    warnings.extend(rule_validation.warnings)
            
            # Check data type consistency
            type_validation = self._validate_data_type_consistency(field_value, field_def)
            if not type_validation.is_valid:
                errors.extend(type_validation.errors)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                metadata={
                    'gold_reference': gold_ref_name,
                    'field_name': field_def.name,
                    'validation_timestamp': datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Field validation failed: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
    
    async def validate_mapping_compliance(self, 
                                        field_mappings: List[Dict[str, Any]],
                                        gold_reference_template: str = "img_0241") -> ValidationResult:
        """Validate mapping compliance against gold reference template"""
        try:
            logger.info(f"Validating mapping compliance against template: {gold_reference_template}")
            
            errors = []
            warnings = []
            suggestions = []
            
            # Load gold reference template expectations
            template_requirements = await self._load_template_requirements(gold_reference_template)
            
            # Check each mapping
            for mapping in field_mappings:
                mapping_validation = await self._validate_single_mapping(mapping, template_requirements)
                
                if not mapping_validation.is_valid:
                    errors.extend(mapping_validation.errors)
                    warnings.extend(mapping_validation.warnings)
                    suggestions.extend(mapping_validation.suggestions)
            
            # Check for missing required mappings
            missing_mappings = self._check_missing_required_mappings(field_mappings, template_requirements)
            if missing_mappings:
                errors.extend([f"Missing required mapping: {mapping}" for mapping in missing_mappings])
            
            # Check for mapping consistency
            consistency_issues = self._check_mapping_consistency(field_mappings)
            warnings.extend(consistency_issues)
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                metadata={
                    'template': gold_reference_template,
                    'total_mappings': len(field_mappings),
                    'validation_timestamp': datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Mapping compliance validation failed: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Compliance validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
    
    async def _validate_gold_reference_definition(self, gold_ref: GoldReferenceDefinition) -> ValidationResult:
        """Validate a gold reference definition"""
        errors = []
        warnings = []
        
        # Check required fields
        if not gold_ref.name:
            errors.append("Gold reference name is required")
        
        if not gold_ref.lookup_table:
            errors.append("Lookup table is required")
        
        if not gold_ref.key_fields:
            warnings.append("No key fields specified")
        
        # Validate standard values format
        if gold_ref.standard_values:
            for key, value in gold_ref.standard_values.items():
                if not isinstance(key, str):
                    errors.append(f"Standard value key must be string: {key}")
        
        # Validate business rules syntax
        for rule in gold_ref.business_rules:
            rule_validation = self._validate_business_rule_syntax(rule)
            if not rule_validation:
                warnings.append(f"Potentially invalid business rule: {rule}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=[]
        )
    
    async def _apply_business_rule(self, 
                                 field_value: Any,
                                 rule: str,
                                 field_def: FieldDefinition) -> ValidationResult:
        """Apply a business rule to a field value"""
        errors = []
        warnings = []
        
        rule_lower = rule.lower()
        
        # Handle common business rule patterns
        if 'not null' in rule_lower:
            if field_value is None or field_value == '':
                errors.append(f"Field {field_def.name} cannot be null")
        
        if 'format' in rule_lower and 'date' in rule_lower:
            if not self._is_valid_date_format(field_value):
                errors.append(f"Invalid date format for field {field_def.name}")
        
        if 'length' in rule_lower:
            # Extract length requirement
            import re
            length_match = re.search(r'(\d+)', rule)
            if length_match and len(str(field_value)) > int(length_match.group(1)):
                errors.append(f"Field {field_def.name} exceeds maximum length")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=[]
        )
    
    def _validate_data_type_consistency(self, field_value: Any, field_def: FieldDefinition) -> ValidationResult:
        """Validate data type consistency"""
        errors = []
        
        expected_type = field_def.data_type.value
        
        # Type checking based on expected data type
        if expected_type == 'string' and not isinstance(field_value, str):
            if field_value is not None:
                errors.append(f"Expected string, got {type(field_value).__name__}")
        
        elif expected_type == 'integer' and not isinstance(field_value, int):
            try:
                int(field_value)
            except (ValueError, TypeError):
                errors.append(f"Cannot convert '{field_value}' to integer")
        
        elif expected_type == 'float' and not isinstance(field_value, (int, float)):
            try:
                float(field_value)
            except (ValueError, TypeError):
                errors.append(f"Cannot convert '{field_value}' to float")
        
        elif expected_type == 'boolean' and not isinstance(field_value, bool):
            if str(field_value).lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
                errors.append(f"Cannot convert '{field_value}' to boolean")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=[],
            suggestions=[]
        )
    
    async def _load_template_requirements(self, template_name: str) -> Dict[str, Any]:
        """Load requirements from gold reference template"""
        # This would typically load from a configuration file or database
        # For now, return basic requirements based on common patterns
        
        requirements = {
            'required_fields': [
                'physical_table',
                'logical_name', 
                'physical_name',
                'data_type',
                'mapping_type'
            ],
            'valid_mapping_types': ['Direct', 'Derived', 'Goldref', 'No Mapping'],
            'required_transformations': {
                'Derived': ['transformation logic required'],
                'Goldref': ['lookup table reference required']
            },
            'data_type_patterns': self.reference_patterns
        }
        
        return requirements
    
    async def _validate_single_mapping(self, 
                                     mapping: Dict[str, Any],
                                     requirements: Dict[str, Any]) -> ValidationResult:
        """Validate a single field mapping"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check required fields
        for required_field in requirements['required_fields']:
            if required_field not in mapping or not mapping[required_field]:
                errors.append(f"Required field missing: {required_field}")
        
        # Validate mapping type
        mapping_type = mapping.get('mapping_type', '')
        if mapping_type not in requirements['valid_mapping_types']:
            errors.append(f"Invalid mapping type: {mapping_type}")
        
        # Check transformation requirements
        if mapping_type in requirements['required_transformations']:
            for req in requirements['required_transformations'][mapping_type]:
                if 'transformation' not in mapping or not mapping['transformation']:
                    errors.append(f"Missing transformation for {mapping_type} mapping")
        
        # Validate data type
        data_type = mapping.get('data_type', '').lower()
        if data_type and data_type not in ['string', 'integer', 'decimal', 'date', 'boolean', 'char']:
            warnings.append(f"Non-standard data type: {data_type}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions
        )
    
    def _check_missing_required_mappings(self, 
                                       field_mappings: List[Dict[str, Any]],
                                       requirements: Dict[str, Any]) -> List[str]:
        """Check for missing required mappings"""
        # This would check against a comprehensive list of required fields
        # For now, return basic checks
        
        mapped_fields = {mapping.get('physical_name', '') for mapping in field_mappings}
        
        # Common required fields (would be loaded from template)
        required_fields = [
            'customer_id',
            'account_number', 
            'transaction_date',
            'amount'
        ]
        
        missing = []
        for required in required_fields:
            if required not in mapped_fields:
                missing.append(required)
        
        return missing
    
    def _check_mapping_consistency(self, field_mappings: List[Dict[str, Any]]) -> List[str]:
        """Check for mapping consistency issues"""
        warnings = []
        
        # Check for duplicate physical names
        physical_names = [mapping.get('physical_name', '') for mapping in field_mappings]
        duplicates = [name for name in set(physical_names) if physical_names.count(name) > 1 and name]
        
        if duplicates:
            warnings.append(f"Duplicate physical names found: {', '.join(duplicates)}")
        
        # Check for inconsistent data types for same logical names
        logical_types = {}
        for mapping in field_mappings:
            logical_name = mapping.get('logical_name', '')
            data_type = mapping.get('data_type', '')
            
            if logical_name and data_type:
                if logical_name in logical_types and logical_types[logical_name] != data_type:
                    warnings.append(f"Inconsistent data types for {logical_name}: {logical_types[logical_name]} vs {data_type}")
                logical_types[logical_name] = data_type
        
        return warnings
    
    def _validate_business_rule_syntax(self, rule: str) -> bool:
        """Validate business rule syntax"""
        try:
            # Basic syntax validation
            if not rule or not isinstance(rule, str):
                return False
            
            # Check for balanced parentheses
            if rule.count('(') != rule.count(')'):
                return False
            
            # Check for common patterns
            valid_patterns = ['not null', 'format', 'length', 'range', 'in', 'between']
            rule_lower = rule.lower()
            
            return any(pattern in rule_lower for pattern in valid_patterns)
            
        except Exception:
            return False
    
    def _is_valid_date_format(self, value: Any) -> bool:
        """Check if value matches valid date formats"""
        if not value:
            return False
        
        value_str = str(value)
        
        # Common date patterns
        import re
        date_patterns = [
            r'^\d{4}-\d{2}-\d{2}$',  # YYYY-MM-DD
            r'^\d{8}$',              # YYYYMMDD
            r'^\d{2}/\d{2}/\d{4}$',  # MM/DD/YYYY
            r'^\d{4}/\d{2}/\d{2}$'   # YYYY/MM/DD
        ]
        
        return any(re.match(pattern, value_str) for pattern in date_patterns)
    
    async def generate_compliance_report(self, 
                                       validation_results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate a comprehensive compliance report"""
        try:
            total_validations = len(validation_results)
            passed_validations = sum(1 for result in validation_results if result.is_valid)
            
            all_errors = []
            all_warnings = []
            all_suggestions = []
            
            for result in validation_results:
                all_errors.extend(result.errors)
                all_warnings.extend(result.warnings)
                all_suggestions.extend(result.suggestions)
            
            # Categorize issues
            error_categories = self._categorize_issues(all_errors)
            warning_categories = self._categorize_issues(all_warnings)
            
            report = {
                'summary': {
                    'total_validations': total_validations,
                    'passed_validations': passed_validations,
                    'failed_validations': total_validations - passed_validations,
                    'compliance_rate': (passed_validations / total_validations * 100) if total_validations > 0 else 0
                },
                'issues': {
                    'errors': {
                        'count': len(all_errors),
                        'categories': error_categories,
                        'details': all_errors
                    },
                    'warnings': {
                        'count': len(all_warnings),
                        'categories': warning_categories,
                        'details': all_warnings
                    }
                },
                'recommendations': all_suggestions,
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate compliance report: {str(e)}")
            return {
                'error': f"Report generation failed: {str(e)}",
                'generated_at': datetime.utcnow().isoformat()
            }
    
    def _categorize_issues(self, issues: List[str]) -> Dict[str, int]:
        """Categorize issues by type"""
        categories = {
            'data_type': 0,
            'missing_field': 0,
            'format': 0,
            'business_rule': 0,
            'consistency': 0,
            'other': 0
        }
        
        for issue in issues:
            issue_lower = issue.lower()
            
            if 'type' in issue_lower or 'convert' in issue_lower:
                categories['data_type'] += 1
            elif 'missing' in issue_lower or 'required' in issue_lower:
                categories['missing_field'] += 1
            elif 'format' in issue_lower:
                categories['format'] += 1
            elif 'rule' in issue_lower or 'null' in issue_lower:
                categories['business_rule'] += 1
            elif 'duplicate' in issue_lower or 'inconsistent' in issue_lower:
                categories['consistency'] += 1
            else:
                categories['other'] += 1
        
        return categories


def create_goldref_validator(config: AgentConfig = None) -> GoldReferenceValidator:
    """Factory function to create gold reference validator"""
    if config is None:
        config = AgentConfig(
            name="goldref_validator",
            description="Gold reference validator for data quality and standards compliance",
            capabilities=["gold_reference_validation", "compliance_checking", "data_quality"]
        )
    
    return GoldReferenceValidator(config)