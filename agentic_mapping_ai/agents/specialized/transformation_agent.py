"""
Transformation Agent - Specialized agent for handling complex field transformations and gold reference validations
"""

import re
import ast
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
from loguru import logger

from agents.base_agent import BaseAgent, AgentConfig
from core.models import (
    TransformationRule, GoldReferenceDefinition, MappingRule,
    ValidationResult, TaskStatus
)


class TransformationAgent(BaseAgent):
    """
    Transformation Agent specialized in processing complex field transformations
    
    Capabilities:
    - Parse and execute conditional transformations (If-Then-Else logic)
    - Handle gold reference lookups and validations
    - Process derivations and calculations
    - Validate business rules
    - Generate transformation code
    """
    
    def __init__(self, config: AgentConfig, rag_engine=None, tools=None):
        super().__init__(config, rag_engine, tools)
        
        # Transformation patterns and templates
        self.transformation_patterns = {
            'conditional': r'if\s+(.+?)\s+then\s+[\'"](.+?)[\'"](?:\s+else\s+[\'"](.+?)[\'"])?',
            'lookup': r'lookup.*?using.*?keys?\s*\((.*?)\)',
            'date_format': r'date\s+format.*?([YMDH-]+)',
            'null_check': r'is\s+not\s+null\s+or\s+not\s+0',
            'range_check': r'>\s*(\d+)',
            'equality_check': r'=\s*[\'"]([^\'\"]+)[\'"]'
        }
        
        # Gold reference cache
        self.gold_reference_cache: Dict[str, GoldReferenceDefinition] = {}
        
        # Supported transformation types
        self.supported_transformations = {
            'conditional',
            'lookup',
            'derivation',
            'calculation',
            'validation',
            'formatting'
        }
    
    async def analyze_transformation(self, transformation_text: str) -> Dict[str, Any]:
        """Analyze transformation text and extract components"""
        try:
            logger.info(f"Analyzing transformation: {transformation_text[:100]}...")
            
            analysis = {
                'type': 'unknown',
                'components': {},
                'dependencies': [],
                'complexity': 'simple',
                'execution_order': 1
            }
            
            # Detect transformation type
            analysis['type'] = self._detect_transformation_type(transformation_text)
            
            # Extract components based on type
            if analysis['type'] == 'conditional':
                analysis['components'] = self._parse_conditional_transformation(transformation_text)
            elif analysis['type'] == 'lookup':
                analysis['components'] = self._parse_lookup_transformation(transformation_text)
            elif analysis['type'] == 'derivation':
                analysis['components'] = self._parse_derivation_transformation(transformation_text)
            
            # Determine dependencies
            analysis['dependencies'] = self._extract_field_dependencies(transformation_text)
            
            # Assess complexity
            analysis['complexity'] = self._assess_complexity(transformation_text, analysis['components'])
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze transformation: {str(e)}")
            return {
                'type': 'error',
                'error': str(e),
                'components': {},
                'dependencies': [],
                'complexity': 'unknown'
            }
    
    def _detect_transformation_type(self, text: str) -> str:
        """Detect the type of transformation"""
        text_lower = text.lower()
        
        if 'if' in text_lower and ('then' in text_lower or 'else' in text_lower):
            return 'conditional'
        elif 'lookup' in text_lower:
            return 'lookup'
        elif any(op in text_lower for op in ['calculate', 'sum', 'count', 'avg']):
            return 'calculation'
        elif 'derive' in text_lower or 'concatenate' in text_lower:
            return 'derivation'
        elif 'format' in text_lower:
            return 'formatting'
        elif any(check in text_lower for check in ['validate', 'check', 'must be']):
            return 'validation'
        else:
            return 'direct'
    
    def _parse_conditional_transformation(self, text: str) -> Dict[str, Any]:
        """Parse conditional (if-then-else) transformation"""
        components = {
            'condition': '',
            'then_value': '',
            'else_value': '',
            'fields_used': []
        }
        
        # Extract condition and values using regex
        match = re.search(self.transformation_patterns['conditional'], text, re.IGNORECASE)
        if match:
            components['condition'] = match.group(1).strip()
            components['then_value'] = match.group(2).strip()
            components['else_value'] = match.group(3).strip() if match.group(3) else 'NULL'
        
        # Extract field references from condition
        field_refs = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', components['condition'])
        components['fields_used'] = list(set(field_refs))
        
        return components
    
    def _parse_lookup_transformation(self, text: str) -> Dict[str, Any]:
        """Parse lookup transformation"""
        components = {
            'lookup_table': '',
            'key_fields': [],
            'target_field': '',
            'conditions': []
        }
        
        # Extract table name
        if 'STANDARD_VAL' in text:
            components['lookup_table'] = 'STANDARD_VAL_DESC'
        elif 'genesis' in text.lower():
            components['lookup_table'] = 'genesis'
        
        # Extract key fields from parentheses
        key_match = re.search(r'\((.*?)\)', text)
        if key_match:
            keys = [k.strip().strip("'\"") for k in key_match.group(1).split(',')]
            components['key_fields'] = keys
        
        # Extract conditions
        if 'using' in text.lower():
            conditions_part = text.split('using')[-1]
            components['conditions'].append(conditions_part.strip())
        
        return components
    
    def _parse_derivation_transformation(self, text: str) -> Dict[str, Any]:
        """Parse derivation transformation"""
        components = {
            'operation': '',
            'source_fields': [],
            'parameters': {}
        }
        
        # Detect concatenation
        if 'concatenate' in text.lower():
            components['operation'] = 'concatenate'
        elif 'derive' in text.lower():
            components['operation'] = 'derive'
        
        # Extract field references
        field_refs = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', text)
        components['source_fields'] = list(set(field_refs))
        
        return components
    
    def _extract_field_dependencies(self, text: str) -> List[str]:
        """Extract field dependencies from transformation text"""
        dependencies = []
        
        # Common field patterns
        field_patterns = [
            r'[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_][a-zA-Z0-9_]*',  # table.field
            r'[a-zA-Z_][a-zA-Z0-9_]*',  # simple field names
        ]
        
        for pattern in field_patterns:
            matches = re.findall(pattern, text)
            dependencies.extend(matches)
        
        # Filter out common keywords
        keywords = {'if', 'then', 'else', 'and', 'or', 'not', 'null', 'true', 'false'}
        dependencies = [dep for dep in dependencies if dep.lower() not in keywords]
        
        return list(set(dependencies))
    
    def _assess_complexity(self, text: str, components: Dict[str, Any]) -> str:
        """Assess transformation complexity"""
        complexity_indicators = 0
        
        # Check for nested conditions
        if text.count('if') > 1:
            complexity_indicators += 2
        
        # Check for multiple operations
        if 'and' in text.lower() or 'or' in text.lower():
            complexity_indicators += 1
        
        # Check for lookups
        if 'lookup' in text.lower():
            complexity_indicators += 2
        
        # Check for calculations
        if any(op in text.lower() for op in ['sum', 'count', 'avg', 'calculate']):
            complexity_indicators += 1
        
        # Check for date operations
        if 'date' in text.lower():
            complexity_indicators += 1
        
        if complexity_indicators >= 4:
            return 'complex'
        elif complexity_indicators >= 2:
            return 'moderate'
        else:
            return 'simple'
    
    async def generate_transformation_code(self, rule: TransformationRule, language: str = 'pyspark') -> str:
        """Generate executable code for transformation rule"""
        try:
            logger.info(f"Generating {language} code for transformation: {rule.name}")
            
            if language == 'pyspark':
                # Use enhanced PySpark code generator
                from agents.pyspark_code_generator import generate_pyspark_transformation
                return generate_pyspark_transformation(
                    rule, 
                    source_df_name="df",
                    include_comments=True,
                    include_validation=True
                )
            elif language == 'sql':
                return self._generate_sql_code(rule)
            elif language == 'python':
                return self._generate_python_code(rule)
            else:
                raise ValueError(f"Unsupported language: {language}")
                
        except Exception as e:
            logger.error(f"Failed to generate transformation code: {str(e)}")
            return f"# Error generating code: {str(e)}"
    
    def _generate_sql_code(self, rule: TransformationRule) -> str:
        """Generate SQL transformation code"""
        # Analyze the transformation first
        analysis = asyncio.run(self.analyze_transformation(rule.logic))
        
        if analysis['type'] == 'conditional':
            return self._generate_sql_conditional(rule, analysis['components'])
        elif analysis['type'] == 'lookup':
            return self._generate_sql_lookup(rule, analysis['components'])
        elif analysis['type'] == 'direct':
            return f"-- Direct mapping\nSELECT *, {rule.source_fields[0] if rule.source_fields else rule.target_field} AS {rule.target_field} FROM source_table"
        else:
            return f"-- Generic transformation for {rule.target_field}\n-- Logic: {rule.logic}\n-- TODO: Implement SQL transformation"
    
    def _generate_sql_conditional(self, rule: TransformationRule, components: Dict[str, Any]) -> str:
        """Generate SQL conditional transformation"""
        condition = components['condition']
        then_value = components['then_value']
        else_value = components['else_value']
        
        # Convert condition to SQL syntax
        sql_condition = self._convert_condition_to_sql(condition)
        
        code = f"""
-- Conditional transformation for {rule.target_field}
SELECT *,
    CASE 
        WHEN {sql_condition} THEN '{then_value}'
        ELSE '{else_value}'
    END AS {rule.target_field}
FROM source_table
"""
        
        return code.strip()
    
    def _generate_pyspark_lookup(self, rule: TransformationRule, components: Dict[str, Any]) -> str:
        """Generate PySpark lookup transformation"""
        lookup_table = components['lookup_table']
        key_fields = components['key_fields']
        
        code = f"""
# Lookup transformation for {rule.target_field}
from pyspark.sql.functions import col

# Load lookup table
lookup_df = spark.table('{lookup_table}')

# Perform lookup join
join_conditions = [{' & '.join([f"df.{field} == lookup_df.{field}" for field in key_fields])}]
df = df.join(
    lookup_df.select({', '.join([f"'{field}'" for field in key_fields] + ["'standard_value'"])}),
    join_conditions,
    'left'
).withColumnRenamed('standard_value', '{rule.target_field}')
""".strip()
        
        return code
    
    def _generate_pyspark_derivation(self, rule: TransformationRule, components: Dict[str, Any]) -> str:
        """Generate PySpark derivation transformation"""
        operation = components['operation']
        source_fields = components['source_fields']
        
        if operation == 'concatenate':
            fields_concat = ', '.join([f"col('{field}')" for field in source_fields])
            code = f"""
# Derivation transformation for {rule.target_field}
from pyspark.sql.functions import concat, col

df = df.withColumn(
    '{rule.target_field}',
    concat({fields_concat})
)
""".strip()
        else:
            code = f"# Derivation code for {rule.target_field} - {operation}"
        
        return code
    
    def _convert_condition_to_pyspark(self, condition: str) -> str:
        """Convert condition text to PySpark syntax"""
        # Handle common patterns
        condition = condition.replace(' = ', ' == ')
        condition = condition.replace(' AND ', ' & ')
        condition = condition.replace(' OR ', ' | ')
        
        # Convert field references to col() calls
        field_refs = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', condition)
        for field in field_refs:
            if field.lower() not in ['null', 'true', 'false', 'and', 'or', 'not']:
                condition = condition.replace(field, f"col('{field}')")
        
        return condition
    
    async def validate_transformation(self, rule: TransformationRule, sample_data: Dict[str, Any] = None) -> ValidationResult:
        """Validate a transformation rule"""
        try:
            logger.info(f"Validating transformation rule: {rule.name}")
            
            errors = []
            warnings = []
            suggestions = []
            
            # Analyze the transformation
            analysis = await self.analyze_transformation(rule.logic)
            
            # Check for syntax errors
            if analysis['type'] == 'error':
                errors.append(f"Syntax error in transformation: {analysis['error']}")
            
            # Check for missing dependencies
            for field in analysis['dependencies']:
                if field not in rule.source_fields:
                    warnings.append(f"Field '{field}' referenced but not in source fields")
            
            # Check complexity
            if analysis['complexity'] == 'complex':
                suggestions.append("Consider breaking down complex transformation into simpler steps")
            
            # Validate conditional logic
            if analysis['type'] == 'conditional':
                condition_validation = self._validate_conditional_logic(analysis['components'])
                errors.extend(condition_validation.get('errors', []))
                warnings.extend(condition_validation.get('warnings', []))
            
            is_valid = len(errors) == 0
            
            return ValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                metadata={
                    'transformation_type': analysis['type'],
                    'complexity': analysis['complexity'],
                    'dependencies_count': len(analysis['dependencies'])
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to validate transformation: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
    
    def _validate_conditional_logic(self, components: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate conditional logic components"""
        validation = {
            'errors': [],
            'warnings': []
        }
        
        condition = components.get('condition', '')
        
        # Check for balanced parentheses
        if condition.count('(') != condition.count(')'):
            validation['errors'].append("Unbalanced parentheses in condition")
        
        # Check for valid operators
        invalid_ops = re.findall(r'[^a-zA-Z0-9_\s\(\)><=!&|\'\".-]', condition)
        if invalid_ops:
            validation['warnings'].append(f"Potentially invalid operators: {', '.join(set(invalid_ops))}")
        
        return validation
    
    async def create_transformation_rule(self, 
                                       name: str,
                                       source_fields: List[str],
                                       target_field: str,
                                       logic: str,
                                       description: str = None) -> TransformationRule:
        """Create a new transformation rule"""
        
        # Analyze the transformation
        analysis = await self.analyze_transformation(logic)
        
        rule = TransformationRule(
            name=name,
            rule_type=analysis['type'],
            source_fields=source_fields,
            target_field=target_field,
            logic=logic,
            description=description,
            parameters={
                'complexity': analysis['complexity'],
                'dependencies': analysis['dependencies']
            }
        )
        
        return rule


def create_transformation_agent(config: AgentConfig = None) -> TransformationAgent:
    """Factory function to create transformation agent"""
    if config is None:
        config = AgentConfig(
            name="transformation_agent",
            description="Specialized agent for complex field transformations",
            capabilities=["conditional_logic", "lookups", "derivations", "validations"]
        )
    
    return TransformationAgent(config)