"""
Enhanced PySpark Code Generator - Generates production-ready PySpark code for complex transformations
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from loguru import logger
from datetime import datetime

from ...core.models import TransformationRule, FieldDefinition


class PySparkCodeGenerator:
    """
    Enhanced PySpark code generator for complex data transformations
    
    Generates production-ready PySpark code for:
    - Conditional transformations (If-Then-Else)
    - Lookup operations with multiple keys
    - Date format transformations
    - Numerical calculations
    - String manipulations
    - Data type conversions
    - Null handling
    """
    
    def __init__(self):
        self.imports = set()
        self.functions_used = set()
        
        # PySpark function mappings
        self.pyspark_functions = {
            'date_format': 'from pyspark.sql.functions import date_format',
            'when': 'from pyspark.sql.functions import when',
            'col': 'from pyspark.sql.functions import col',
            'lit': 'from pyspark.sql.functions import lit',
            'concat': 'from pyspark.sql.functions import concat',
            'concat_ws': 'from pyspark.sql.functions import concat_ws',
            'coalesce': 'from pyspark.sql.functions import coalesce',
            'isnull': 'from pyspark.sql.functions import isnull',
            'isnan': 'from pyspark.sql.functions import isnan',
            'regexp_replace': 'from pyspark.sql.functions import regexp_replace',
            'substring': 'from pyspark.sql.functions import substring',
            'length': 'from pyspark.sql.functions import length',
            'upper': 'from pyspark.sql.functions import upper',
            'lower': 'from pyspark.sql.functions import lower',
            'trim': 'from pyspark.sql.functions import trim',
            'cast': 'from pyspark.sql.functions import col',
            'sum': 'from pyspark.sql.functions import sum',
            'count': 'from pyspark.sql.functions import count',
            'avg': 'from pyspark.sql.functions import avg',
            'max': 'from pyspark.sql.functions import max',
            'min': 'from pyspark.sql.functions import min'
        }
    
    def generate_transformation_code(self, 
                                   rule: TransformationRule,
                                   source_df_name: str = "df",
                                   include_comments: bool = True,
                                   include_validation: bool = True) -> str:
        """Generate complete PySpark transformation code"""
        
        try:
            logger.info(f"Generating enhanced PySpark code for: {rule.name}")
            
            # Reset imports and functions for this generation
            self.imports.clear()
            self.functions_used.clear()
            
            # Analyze the transformation logic
            transformation_type = self._detect_transformation_type(rule.logic)
            
            # Generate code based on transformation type
            if transformation_type == 'conditional':
                code_body = self._generate_conditional_code(rule, source_df_name)
            elif transformation_type == 'lookup':
                code_body = self._generate_lookup_code(rule, source_df_name)
            elif transformation_type == 'date_format':
                code_body = self._generate_date_format_code(rule, source_df_name)
            elif transformation_type == 'calculation':
                code_body = self._generate_calculation_code(rule, source_df_name)
            elif transformation_type == 'string_manipulation':
                code_body = self._generate_string_manipulation_code(rule, source_df_name)
            elif transformation_type == 'null_handling':
                code_body = self._generate_null_handling_code(rule, source_df_name)
            elif transformation_type == 'direct':
                code_body = self._generate_direct_mapping_code(rule, source_df_name)
            else:
                code_body = self._generate_generic_transformation_code(rule, source_df_name)
            
            # Build complete code with imports and comments
            full_code = self._build_complete_code(
                rule, code_body, include_comments, include_validation
            )
            
            return full_code
            
        except Exception as e:
            logger.error(f"Failed to generate PySpark code: {str(e)}")
            return self._generate_error_code(rule, str(e))
    
    def _detect_transformation_type(self, logic: str) -> str:
        """Detect the type of transformation from logic text"""
        logic_lower = logic.lower()
        
        # Check for different transformation patterns
        if any(pattern in logic_lower for pattern in ['if', 'when', 'case', 'then', 'else']):
            return 'conditional'
        elif any(pattern in logic_lower for pattern in ['lookup', 'join', 'reference']):
            return 'lookup'
        elif any(pattern in logic_lower for pattern in ['date', 'format', 'yyyy', 'mm', 'dd']):
            return 'date_format'
        elif any(pattern in logic_lower for pattern in ['sum', 'count', 'avg', 'calculate', '+', '-', '*', '/']):
            return 'calculation'
        elif any(pattern in logic_lower for pattern in ['concat', 'substring', 'trim', 'upper', 'lower']):
            return 'string_manipulation'
        elif any(pattern in logic_lower for pattern in ['null', 'coalesce', 'nvl', 'isnull']):
            return 'null_handling'
        elif logic_lower in ['direct', 'copy', 'same', '']:
            return 'direct'
        else:
            return 'generic'
    
    def _generate_conditional_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for conditional transformations"""
        
        # Add required imports
        self._add_function('when')
        self._add_function('col')
        self._add_function('lit')
        
        # Parse conditional logic
        conditions = self._parse_conditional_logic(rule.logic)
        
        if not conditions:
            return f"# Unable to parse conditional logic: {rule.logic}"
        
        # Build when-otherwise chain
        when_chain = []
        
        for i, condition in enumerate(conditions):
            if i == 0:
                # First condition uses when()
                pyspark_condition = self._convert_condition_to_pyspark(condition['condition'])
                value_expr = self._convert_value_to_pyspark(condition['value'])
                when_chain.append(f"when({pyspark_condition}, {value_expr})")
            elif condition['condition'].lower() == 'else':
                # Else clause uses otherwise()
                value_expr = self._convert_value_to_pyspark(condition['value'])
                when_chain.append(f".otherwise({value_expr})")
            else:
                # Additional conditions use when()
                pyspark_condition = self._convert_condition_to_pyspark(condition['condition'])
                value_expr = self._convert_value_to_pyspark(condition['value'])
                when_chain.append(f".when({pyspark_condition}, {value_expr})")
        
        # Build the complete transformation
        transformation = '\n    '.join(when_chain)
        
        code = f"""
# Conditional transformation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    {transformation}
)"""
        
        return code.strip()
    
    def _generate_lookup_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for lookup transformations"""
        
        self._add_function('col')
        
        # Parse lookup information
        lookup_info = self._parse_lookup_logic(rule.logic)
        
        lookup_table = lookup_info.get('table', 'lookup_table')
        key_fields = lookup_info.get('key_fields', ['key_field'])
        lookup_field = lookup_info.get('lookup_field', rule.target_field)
        
        # Generate join conditions
        join_conditions = []
        for key_field in key_fields:
            join_conditions.append(f"{df_name}['{key_field}'] == lookup_df['{key_field}']")
        
        join_condition_str = ' & '.join([f"({condition})" for condition in join_conditions])
        
        code = f"""
# Lookup transformation for {rule.target_field}
# Load lookup table
lookup_df = spark.table('{lookup_table}')

# Perform lookup join
{df_name} = {df_name}.alias('main').join(
    lookup_df.alias('lookup').select(
        {', '.join([f"col('{field}')" for field in key_fields])},
        col('{lookup_field}').alias('{rule.target_field}_lookup')
    ),
    {join_condition_str},
    'left'
).select(
    'main.*',
    col('{rule.target_field}_lookup').alias('{rule.target_field}')
)"""
        
        return code.strip()
    
    def _generate_date_format_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for date format transformations"""
        
        self._add_function('date_format')
        self._add_function('col')
        self._add_function('to_date')
        
        # Parse date format requirements
        date_formats = self._parse_date_format_logic(rule.logic)
        
        source_format = date_formats.get('source_format', 'yyyy-MM-dd')
        target_format = date_formats.get('target_format', 'yyyyMMdd')
        source_field = rule.source_fields[0] if rule.source_fields else 'date_field'
        
        code = f"""
# Date format transformation for {rule.target_field}
from pyspark.sql.functions import date_format, to_date, col

{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    date_format(
        to_date(col('{source_field}'), '{source_format}'),
        '{target_format}'
    )
)"""
        
        return code.strip()
    
    def _generate_calculation_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for calculation transformations"""
        
        self._add_function('col')
        
        # Parse calculation logic
        calculation = self._parse_calculation_logic(rule.logic)
        
        if calculation['type'] == 'arithmetic':
            # Handle arithmetic operations
            expression = self._convert_arithmetic_to_pyspark(calculation['expression'])
        elif calculation['type'] == 'aggregation':
            # Handle aggregation functions
            self._add_function(calculation['function'])
            expression = f"{calculation['function']}(col('{calculation['field']}'))"
        else:
            # Generic expression
            expression = f"col('{rule.source_fields[0] if rule.source_fields else 'source_field'}')"
        
        code = f"""
# Calculation transformation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    {expression}
)"""
        
        return code.strip()
    
    def _generate_string_manipulation_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for string manipulation transformations"""
        
        # Parse string operation
        operation = self._parse_string_operation(rule.logic)
        
        if operation['type'] == 'concatenation':
            self._add_function('concat')
            self._add_function('col')
            
            fields = operation.get('fields', rule.source_fields)
            concat_fields = ', '.join([f"col('{field}')" for field in fields])
            
            code = f"""
# String concatenation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    concat({concat_fields})
)"""
        
        elif operation['type'] == 'substring':
            self._add_function('substring')
            self._add_function('col')
            
            source_field = rule.source_fields[0] if rule.source_fields else 'source_field'
            start_pos = operation.get('start', 1)
            length = operation.get('length', 10)
            
            code = f"""
# Substring transformation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    substring(col('{source_field}'), {start_pos}, {length})
)"""
        
        elif operation['type'] == 'case_conversion':
            func = operation.get('function', 'upper')
            self._add_function(func)
            self._add_function('col')
            
            source_field = rule.source_fields[0] if rule.source_fields else 'source_field'
            
            code = f"""
# Case conversion for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    {func}(col('{source_field}'))
)"""
        
        else:
            # Generic string operation
            self._add_function('col')
            source_field = rule.source_fields[0] if rule.source_fields else 'source_field'
            
            code = f"""
# String transformation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    col('{source_field}')  # Add specific string transformation here
)"""
        
        return code.strip()
    
    def _generate_null_handling_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for null handling transformations"""
        
        self._add_function('coalesce')
        self._add_function('col')
        self._add_function('lit')
        
        # Parse null handling logic
        null_logic = self._parse_null_handling_logic(rule.logic)
        
        source_field = rule.source_fields[0] if rule.source_fields else 'source_field'
        default_value = null_logic.get('default_value', 'NULL')
        
        if null_logic['type'] == 'coalesce':
            # Use coalesce for multiple fallback values
            coalesce_fields = [f"col('{field}')" for field in rule.source_fields]
            if default_value != 'NULL':
                coalesce_fields.append(f"lit('{default_value}')")
            
            expression = f"coalesce({', '.join(coalesce_fields)})"
        else:
            # Simple null check with default
            expression = f"coalesce(col('{source_field}'), lit('{default_value}'))"
        
        code = f"""
# Null handling transformation for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    {expression}
)"""
        
        return code.strip()
    
    def _generate_direct_mapping_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate PySpark code for direct field mapping"""
        
        self._add_function('col')
        
        source_field = rule.source_fields[0] if rule.source_fields else rule.target_field
        
        # Handle data type conversion if needed
        cast_expression = self._get_cast_expression(source_field, rule)
        
        code = f"""
# Direct mapping for {rule.target_field}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    {cast_expression}
)"""
        
        return code.strip()
    
    def _generate_generic_transformation_code(self, rule: TransformationRule, df_name: str) -> str:
        """Generate generic PySpark transformation code"""
        
        self._add_function('col')
        
        source_field = rule.source_fields[0] if rule.source_fields else 'source_field'
        
        code = f"""
# Generic transformation for {rule.target_field}  
# Logic: {rule.logic}
{df_name} = {df_name}.withColumn(
    '{rule.target_field}',
    col('{source_field}')  # TODO: Implement specific transformation logic
)

# Note: Manual implementation required for logic: {rule.logic}"""
        
        return code.strip()
    
    def _parse_conditional_logic(self, logic: str) -> List[Dict[str, str]]:
        """Parse conditional logic into structured conditions"""
        conditions = []
        
        # Handle If-Then-Else pattern
        if_pattern = r'if\s+(.+?)\s+then\s+[\'"](.+?)[\'"](?:\s+else\s+[\'"](.+?)[\'""])?'
        match = re.search(if_pattern, logic, re.IGNORECASE)
        
        if match:
            conditions.append({
                'condition': match.group(1).strip(),
                'value': match.group(2).strip()
            })
            
            if match.group(3):
                conditions.append({
                    'condition': 'else',
                    'value': match.group(3).strip()
                })
        
        return conditions
    
    def _parse_lookup_logic(self, logic: str) -> Dict[str, Any]:
        """Parse lookup logic to extract table and key information"""
        lookup_info = {
            'table': 'lookup_table',
            'key_fields': ['key_field'],
            'lookup_field': 'lookup_value'
        }
        
        # Extract table name
        if 'STANDARD_VAL' in logic:
            lookup_info['table'] = 'STANDARD_VAL_DESC'
        elif 'genesis' in logic.lower():
            lookup_info['table'] = 'genesis'
        
        # Extract key fields from parentheses
        key_match = re.search(r'\((.*?)\)', logic)
        if key_match:
            keys = [k.strip().strip("'\"") for k in key_match.group(1).split(',')]
            lookup_info['key_fields'] = keys
        
        return lookup_info
    
    def _parse_date_format_logic(self, logic: str) -> Dict[str, str]:
        """Parse date format requirements"""
        formats = {
            'source_format': 'yyyy-MM-dd',
            'target_format': 'yyyyMMdd'
        }
        
        # Look for format specifications
        if 'YYYYMMDD' in logic:
            formats['target_format'] = 'yyyyMMdd'
        elif 'YYYY-MM-DD' in logic:
            formats['target_format'] = 'yyyy-MM-dd'
        
        return formats
    
    def _parse_calculation_logic(self, logic: str) -> Dict[str, Any]:
        """Parse calculation logic"""
        calc_info = {
            'type': 'arithmetic',
            'expression': logic,
            'function': None,
            'field': None
        }
        
        # Check for aggregation functions
        agg_functions = ['sum', 'count', 'avg', 'max', 'min']
        for func in agg_functions:
            if func in logic.lower():
                calc_info['type'] = 'aggregation'
                calc_info['function'] = func
                break
        
        return calc_info
    
    def _parse_string_operation(self, logic: str) -> Dict[str, Any]:
        """Parse string operation logic"""
        operation = {
            'type': 'concatenation',
            'fields': [],
            'parameters': {}
        }
        
        logic_lower = logic.lower()
        
        if 'concat' in logic_lower:
            operation['type'] = 'concatenation'
        elif 'substring' in logic_lower:
            operation['type'] = 'substring'
        elif 'upper' in logic_lower:
            operation['type'] = 'case_conversion'
            operation['function'] = 'upper'
        elif 'lower' in logic_lower:
            operation['type'] = 'case_conversion'
            operation['function'] = 'lower'
        
        return operation
    
    def _parse_null_handling_logic(self, logic: str) -> Dict[str, Any]:
        """Parse null handling logic"""
        null_info = {
            'type': 'coalesce',
            'default_value': 'NULL'
        }
        
        # Extract default value if specified
        default_match = re.search(r'default[:\s]+[\'"](.+?)[\'"]', logic, re.IGNORECASE)
        if default_match:
            null_info['default_value'] = default_match.group(1)
        
        return null_info
    
    def _convert_condition_to_pyspark(self, condition: str) -> str:
        """Convert condition string to PySpark syntax"""
        # Replace comparison operators
        condition = re.sub(r'\s*=\s*', ' == ', condition)
        condition = re.sub(r'\s*<>\s*', ' != ', condition)
        condition = condition.replace(' AND ', ' & ')
        condition = condition.replace(' OR ', ' | ')
        condition = condition.replace(' NOT ', ' ~ ')
        
        # Convert field references to col() calls
        field_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_field(match):
            field_name = match.group(1)
            # Skip PySpark functions and keywords
            if field_name.lower() in ['true', 'false', 'null', 'and', 'or', 'not', 'col', 'lit']:
                return field_name
            # Skip numeric values
            if field_name.isdigit():
                return field_name
            # Convert to col() call
            return f"col('{field_name}')"
        
        condition = re.sub(field_pattern, replace_field, condition)
        
        return condition
    
    def _convert_value_to_pyspark(self, value: str) -> str:
        """Convert value to appropriate PySpark expression"""
        value = value.strip()
        
        # Handle different value types
        if value.lower() in ['null', 'none']:
            self._add_function('lit')
            return 'lit(None)'
        elif value.lower() in ['true', 'false']:
            self._add_function('lit')
            return f'lit({value.title()})'
        elif value.isdigit() or (value.replace('.', '', 1).isdigit() and value.count('.') <= 1):
            self._add_function('lit')
            return f'lit({value})'
        else:
            # String literal
            self._add_function('lit')
            return f"lit('{value}')"
    
    def _convert_arithmetic_to_pyspark(self, expression: str) -> str:
        """Convert arithmetic expression to PySpark"""
        # Simple field reference conversion
        field_pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_field(match):
            field_name = match.group(1)
            if field_name.lower() not in ['col', 'lit'] and not field_name.isdigit():
                return f"col('{field_name}')"
            return field_name
        
        expression = re.sub(field_pattern, replace_field, expression)
        return expression
    
    def _get_cast_expression(self, source_field: str, rule: TransformationRule) -> str:
        """Get appropriate cast expression for data type conversion"""
        # For now, return simple col() expression
        # This can be enhanced with actual data type conversion logic
        return f"col('{source_field}')"
    
    def _add_function(self, function_name: str):
        """Add function to the imports list"""
        if function_name in self.pyspark_functions:
            self.imports.add(self.pyspark_functions[function_name])
            self.functions_used.add(function_name)
    
    def _build_complete_code(self, 
                           rule: TransformationRule,
                           code_body: str,
                           include_comments: bool = True,
                           include_validation: bool = True) -> str:
        """Build complete PySpark code with imports and validation"""
        
        # Build imports section
        imports_section = '\n'.join(sorted(self.imports))
        
        # Build header comment
        header = ""
        if include_comments:
            header = f"""
# ============================================================================
# PySpark Transformation: {rule.name}
# Rule Type: {rule.rule_type}
# Target Field: {rule.target_field}
# Source Fields: {', '.join(rule.source_fields)}
# Logic: {rule.logic}
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================================================
"""
        
        # Build validation section
        validation_section = ""
        if include_validation:
            validation_section = f"""

# Validation: Check if transformation was successful
print(f"Transformation completed for field: {rule.target_field}")
print(f"Sample values: ")
{code_body.split('=')[0].strip()}.select('{rule.target_field}').show(5, truncate=False)
"""
        
        # Combine all sections
        complete_code = f"""{header}
{imports_section}

{code_body}{validation_section}
""".strip()
        
        return complete_code
    
    def _generate_error_code(self, rule: TransformationRule, error_message: str) -> str:
        """Generate error handling code"""
        return f"""
# ERROR: Failed to generate transformation code
# Rule: {rule.name}
# Error: {error_message}
# Manual implementation required

from pyspark.sql.functions import col, lit

# Placeholder transformation - REQUIRES MANUAL IMPLEMENTATION
df = df.withColumn(
    '{rule.target_field}',
    lit('ERROR: Manual implementation required')
)

# Original logic: {rule.logic}
"""


def generate_pyspark_transformation(rule: TransformationRule, 
                                  source_df_name: str = "df",
                                  include_comments: bool = True,
                                  include_validation: bool = True) -> str:
    """
    Convenience function to generate PySpark transformation code
    
    Args:
        rule: TransformationRule containing the transformation logic
        source_df_name: Name of the source DataFrame variable
        include_comments: Whether to include detailed comments
        include_validation: Whether to include validation code
        
    Returns:
        Complete PySpark transformation code as string
    """
    generator = PySparkCodeGenerator()
    return generator.generate_transformation_code(
        rule, source_df_name, include_comments, include_validation
    )