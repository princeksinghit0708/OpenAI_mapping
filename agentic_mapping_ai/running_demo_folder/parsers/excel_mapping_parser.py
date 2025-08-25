"""
Excel Mapping Parser - Processes Excel files containing field mappings and transformations
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import re
from loguru import logger

from core.models import FieldDefinition, MappingRule, DataType


@dataclass
class ExcelFieldMapping:
    """Enhanced field mapping with Excel-specific attributes"""
    physical_table: str
    logical_name: str
    physical_name: str
    data_type: str
    source_name: Optional[str] = None
    column_name: Optional[str] = None
    mapping_type: str = "Direct"  # Direct, No Mapping, Derived, Goldref
    transformation: Optional[str] = None
    description: Optional[str] = None
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExcelGoldReference:
    """Gold reference data structure from lookup tables"""
    key_fields: List[str]
    lookup_table: str
    standard_values: Dict[str, Any]
    description: str
    processing_rules: List[str] = field(default_factory=list)


@dataclass
class ExcelMappingSchema:
    """Complete mapping schema from Excel"""
    name: str
    field_mappings: List[ExcelFieldMapping]
    gold_references: List[ExcelGoldReference]
    transformation_rules: Dict[str, str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExcelMappingParser:
    """
    Parser for Excel mapping files containing field definitions and transformations
    
    Expected Excel structure:
    - Column A: Physical table/entity name
    - Column B: Logical name
    - Column C: Physical field name  
    - Column D: Data type
    - Column G: Source name/context
    - Column H: Column name/default
    - Column I: Mapping type (Direct/No Mapping/Derived/Goldref)
    - Column J: Transformation/Derivation logic
    """
    
    def __init__(self):
        self.data_type_mapping = {
            'string': DataType.STRING,
            'date': DataType.DATE,
            'decimal': DataType.FLOAT,
            'integer': DataType.INTEGER,
            'int': DataType.INTEGER,
            'char': DataType.STRING,
            'varchar': DataType.STRING,
            'timestamp': DataType.TIMESTAMP,
            'boolean': DataType.BOOLEAN,
            'bool': DataType.BOOLEAN
        }
    
    def parse_excel_file(self, file_path: str, sheet_name: str = 'Sheet1') -> ExcelMappingSchema:
        """Parse Excel mapping file into structured schema"""
        try:
            logger.info(f"Parsing Excel mapping file: {file_path}")
            
            # Read Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Clean column names and data
            df = self._clean_dataframe(df)
            
            # Extract field mappings
            field_mappings = self._extract_field_mappings(df)
            
            # Extract gold references
            gold_references = self._extract_gold_references(df)
            
            # Extract transformation rules
            transformation_rules = self._extract_transformation_rules(df)
            
            # Create schema name from file
            schema_name = Path(file_path).stem
            
            return ExcelMappingSchema(
                name=schema_name,
                field_mappings=field_mappings,
                gold_references=gold_references,
                transformation_rules=transformation_rules,
                metadata={
                    'source_file': file_path,
                    'sheet_name': sheet_name,
                    'parsed_at': pd.Timestamp.now().isoformat(),
                    'total_fields': len(field_mappings)
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to parse Excel file {file_path}: {str(e)}")
            raise
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize dataframe"""
        # Define expected column mappings based on the Excel screenshots
        column_mapping = {
            0: 'physical_table',      # Column A
            1: 'logical_name',        # Column B  
            2: 'physical_name',       # Column C
            3: 'data_type',          # Column D
            6: 'source_name',        # Column G
            7: 'column_name',        # Column H
            8: 'mapping_type',       # Column I
            9: 'transformation'      # Column J
        }
        
        # Rename columns based on position
        new_columns = {}
        for i, col in enumerate(df.columns):
            if i in column_mapping:
                new_columns[col] = column_mapping[i]
        
        df = df.rename(columns=new_columns)
        
        # Fill NaN values with appropriate defaults
        df = df.fillna({
            'physical_table': '',
            'logical_name': '',
            'physical_name': '',
            'data_type': 'string',
            'source_name': '',
            'column_name': '',
            'mapping_type': 'Direct',
            'transformation': ''
        })
        
        # Convert to string and strip whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        return df
    
    def _extract_field_mappings(self, df: pd.DataFrame) -> List[ExcelFieldMapping]:
        """Extract field mappings from dataframe"""
        field_mappings = []
        
        for _, row in df.iterrows():
            # Skip empty rows
            if not row.get('physical_name') or row.get('physical_name') == '':
                continue
            
            # Parse constraints from data type
            constraints = self._parse_data_type_constraints(row.get('data_type', ''))
            
            # Create field mapping
            mapping = ExcelFieldMapping(
                physical_table=row.get('physical_table', ''),
                logical_name=row.get('logical_name', ''),
                physical_name=row.get('physical_name', ''),
                data_type=self._normalize_data_type(row.get('data_type', 'string')),
                source_name=row.get('source_name', ''),
                column_name=row.get('column_name', ''),
                mapping_type=row.get('mapping_type', 'Direct'),
                transformation=row.get('transformation', ''),
                constraints=constraints,
                metadata={
                    'row_index': row.name,
                    'original_data_type': row.get('data_type', '')
                }
            )
            
            field_mappings.append(mapping)
        
        logger.info(f"Extracted {len(field_mappings)} field mappings")
        return field_mappings
    
    def _extract_gold_references(self, df: pd.DataFrame) -> List[ExcelGoldReference]:
        """Extract gold reference patterns from dataframe"""
        gold_references = []
        
        # Look for Goldref mapping types
        goldref_rows = df[df['mapping_type'].str.contains('Goldref', case=False, na=False)]
        
        for _, row in goldref_rows.iterrows():
            transformation = row.get('transformation', '')
            
            # Parse lookup instructions from transformation
            lookup_info = self._parse_lookup_transformation(transformation)
            
            if lookup_info:
                gold_ref = ExcelGoldReference(
                    key_fields=lookup_info.get('key_fields', []),
                    lookup_table=lookup_info.get('table', ''),
                    standard_values=lookup_info.get('values', {}),
                    description=f"Gold reference for {row.get('logical_name', '')}",
                    processing_rules=lookup_info.get('rules', [])
                )
                gold_references.append(gold_ref)
        
        logger.info(f"Extracted {len(gold_references)} gold references")
        return gold_references
    
    def _extract_transformation_rules(self, df: pd.DataFrame) -> Dict[str, str]:
        """Extract transformation rules from dataframe"""
        transformation_rules = {}
        
        for _, row in df.iterrows():
            physical_name = row.get('physical_name', '')
            transformation = row.get('transformation', '')
            
            if physical_name and transformation and transformation != 'Direct':
                transformation_rules[physical_name] = transformation
        
        logger.info(f"Extracted {len(transformation_rules)} transformation rules")
        return transformation_rules
    
    def _normalize_data_type(self, data_type_str: str) -> str:
        """Normalize data type string to standard format"""
        if not data_type_str:
            return 'string'
        
        # Extract base type (handle cases like "Decimal(15,2)")
        base_type = re.match(r'^([a-zA-Z]+)', data_type_str.lower())
        if base_type:
            base_type = base_type.group(1)
            return self.data_type_mapping.get(base_type, 'string')
        
        return 'string'
    
    def _parse_data_type_constraints(self, data_type_str: str) -> Dict[str, Any]:
        """Parse constraints from data type string"""
        constraints = {}
        
        if not data_type_str:
            return constraints
        
        # Handle Decimal(precision, scale)
        decimal_match = re.match(r'decimal\((\d+),(\d+)\)', data_type_str.lower())
        if decimal_match:
            constraints['precision'] = int(decimal_match.group(1))
            constraints['scale'] = int(decimal_match.group(2))
        
        # Handle Char(length)
        char_match = re.match(r'char\((\d+)\)', data_type_str.lower())
        if char_match:
            constraints['max_length'] = int(char_match.group(1))
        
        return constraints
    
    def _parse_lookup_transformation(self, transformation: str) -> Optional[Dict[str, Any]]:
        """Parse lookup transformation instructions"""
        if not transformation or 'lookup' not in transformation.lower():
            return None
        
        lookup_info = {
            'key_fields': [],
            'table': '',
            'values': {},
            'rules': []
        }
        
        # Extract table name and key fields from transformation text
        # Example: "Lookup for the genesis STANDARD_VAL_DESC using the lookup keys"
        if 'STANDARD_VAL' in transformation:
            lookup_info['table'] = 'STANDARD_VAL_DESC'
            lookup_info['rules'].append(transformation)
        
        # Extract conditional logic
        if 'if' in transformation.lower():
            lookup_info['rules'].append(transformation)
        
        return lookup_info
    
    def to_standard_models(self, excel_schema: ExcelMappingSchema) -> Tuple[List[FieldDefinition], List[MappingRule]]:
        """Convert Excel schema to standard Pydantic models"""
        field_definitions = []
        mapping_rules = []
        
        for mapping in excel_schema.field_mappings:
            # Create field definition
            field_def = FieldDefinition(
                name=mapping.logical_name or mapping.physical_name,
                data_type=DataType(mapping.data_type),
                is_nullable=mapping.mapping_type != 'Direct',
                description=mapping.description,
                constraints=mapping.constraints,
                provided_key=mapping.source_name,
                physical_name=mapping.physical_name
            )
            field_definitions.append(field_def)
            
            # Create mapping rule if transformation exists
            if mapping.transformation and mapping.transformation not in ['Direct', '']:
                mapping_rule = MappingRule(
                    source_field=mapping.physical_name,
                    target_field=mapping.logical_name or mapping.physical_name,
                    transformation=mapping.transformation,
                    description=f"{mapping.mapping_type} mapping"
                )
                mapping_rules.append(mapping_rule)
        
        return field_definitions, mapping_rules


def parse_excel_mappings(file_path: str, sheet_name: str = 'Sheet1') -> ExcelMappingSchema:
    """Convenience function to parse Excel mappings"""
    parser = ExcelMappingParser()
    return parser.parse_excel_file(file_path, sheet_name)