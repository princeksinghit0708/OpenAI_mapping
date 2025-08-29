"""
Metadata Validation Agent - Validates document metadata and schema structures
"""

import json
from typing import Any, Dict, List, Optional
from loguru import logger

from ..core.base_agent import BaseAgent, AgentConfig, AgentFactory
from ...core.models import (
    AgentType, ValidationResult, FieldDefinition, 
    SchemaDefinition, DataType
)


class MetadataValidatorAgent(BaseAgent):
    """
    Agent responsible for validating document metadata and schema structures
    
    Converts the existing JSON field extraction logic into an intelligent agent
    that can:
    - Validate JSON/XML document structure
    - Extract and validate field definitions
    - Check data type consistency
    - Identify schema violations
    - Suggest corrections and improvements
    """
    
    def _get_system_prompt(self) -> str:
        return """
        You are a Metadata Validation Agent specialized in validating document schemas and field definitions.
        
        Your responsibilities:
        1. Analyze JSON/XML document structures
        2. Validate field definitions and data types
        3. Identify schema inconsistencies and violations
        4. Extract providedKey patterns and database names
        5. Suggest corrections and improvements
        6. Generate comprehensive validation reports
        
        Key validation rules:
        - Field definitions must have: providedKey, displayName, physicalName, dataType
        - ProvidedKey format: "database.table.field" or similar hierarchical structure
        - Data types must be consistent and valid
        - Required fields should be marked appropriately
        - Descriptions should be meaningful and complete
        
        You should be thorough, accurate, and provide actionable feedback.
        Always explain your reasoning and provide specific examples when identifying issues.
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.METADATA_VALIDATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute metadata validation logic
        
        Args:
            input_data: Should contain 'document' or 'schema' to validate
            context: RAG context for validation patterns
            
        Returns:
            Validation results with errors, warnings, and suggestions
        """
        try:
            # Extract input data
            document = input_data.get('document')
            schema = input_data.get('schema')
            validation_rules = input_data.get('validation_rules', [])
            
            if document:
                return await self._validate_document(document, context)
            elif schema:
                return await self._validate_schema(schema, validation_rules, context)
            else:
                raise ValueError("No document or schema provided for validation")
                
        except Exception as e:
            logger.error(f"Metadata validation failed: {str(e)}")
            return {
                "validation_result": ValidationResult(
                    is_valid=False,
                    errors=[f"Validation failed: {str(e)}"]
                ).dict(),
                "extracted_fields": [],
                "database_name": None
            }
    
    async def _validate_document(self, document: Dict[str, Any], context: str) -> Dict[str, Any]:
        """
        Validate a document structure and extract field definitions
        
        This method converts the existing extract_my_json_pandas.py logic
        into an intelligent agent-based approach
        """
        validation_result = ValidationResult(is_valid=True)
        extracted_fields = []
        database_name = None
        
        try:
            # Extract field definitions (similar to existing logic)
            fields = self._extract_field_definitions(document)
            
            # Find database name using intelligent extraction
            database_name = await self._extract_database_name(document, fields)
            
            # Validate each field
            for field in fields:
                field_validation = self._validate_field_definition(field)
                
                if not field_validation.is_valid:
                    validation_result.is_valid = False
                    validation_result.errors.extend(field_validation.errors)
                
                validation_result.warnings.extend(field_validation.warnings)
                validation_result.suggestions.extend(field_validation.suggestions)
                extracted_fields.append(field)
            
            # Global document validation
            document_validation = await self._validate_document_structure(document, context)
            validation_result.errors.extend(document_validation.get('errors', []))
            validation_result.warnings.extend(document_validation.get('warnings', []))
            validation_result.suggestions.extend(document_validation.get('suggestions', []))
            
            logger.info(f"Validated document with {len(extracted_fields)} fields")
            
        except Exception as e:
            validation_result.is_valid = False
            validation_result.errors.append(f"Document validation error: {str(e)}")
        
        return {
            "validation_result": validation_result.dict(),
            "extracted_fields": [field.dict() for field in extracted_fields],
            "database_name": database_name,
            "field_count": len(extracted_fields)
        }
    
    def _extract_field_definitions(self, document: Dict[str, Any]) -> List[FieldDefinition]:
        """
        Extract field definitions from document
        
        Enhanced version of the existing recursive search logic
        """
        fields = []
        required_keys = {'providedKey', 'displayName', 'physicalName', 'dataType'}
        
        def recursive_search(obj, path="root"):
            if isinstance(obj, dict):
                # Check if current dict is a field definition
                if required_keys.issubset(set(obj.keys())):
                    try:
                        field = FieldDefinition(
                            name=obj.get('displayName', obj.get('physicalName', 'unknown')),
                            data_type=self._normalize_data_type(obj.get('dataType', 'string')),
                            is_nullable=obj.get('isNullable', True),
                            description=obj.get('description'),
                            provided_key=obj.get('providedKey'),
                            physical_name=obj.get('physicalName'),
                            format=obj.get('format'),
                            constraints={
                                'extraction_path': path,
                                'original_data': obj
                            }
                        )
                        fields.append(field)
                    except Exception as e:
                        logger.warning(f"Failed to create field definition at {path}: {str(e)}")
                
                # Continue searching
                for key, value in obj.items():
                    recursive_search(value, f"{path}.{key}")
            
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_search(item, f"{path}[{i}]")
        
        recursive_search(document)
        return fields
    
    def _normalize_data_type(self, data_type_str: str) -> DataType:
        """Normalize data type string to enum"""
        type_mapping = {
            'character': DataType.STRING,
            'varchar': DataType.STRING,
            'string': DataType.STRING,
            'text': DataType.STRING,
            'integer': DataType.INTEGER,
            'int': DataType.INTEGER,
            'bigint': DataType.INTEGER,
            'float': DataType.FLOAT,
            'double': DataType.FLOAT,
            'decimal': DataType.FLOAT,
            'boolean': DataType.BOOLEAN,
            'bool': DataType.BOOLEAN,
            'date': DataType.DATE,
            'timestamp': DataType.TIMESTAMP,
            'datetime': DataType.TIMESTAMP,
            'array': DataType.ARRAY,
            'object': DataType.OBJECT,
            'json': DataType.OBJECT
        }
        
        normalized = type_mapping.get(data_type_str.lower(), DataType.STRING)
        return normalized
    
    async def _extract_database_name(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[str]:
        """
        Intelligently extract database name using multiple strategies
        
        Enhanced version of find_dictionary_name function
        """
        strategies = [
            self._extract_from_fields,
            self._extract_from_dictionary,
            self._extract_from_context,
            self._extract_using_llm
        ]
        
        for strategy in strategies:
            try:
                db_name = await strategy(document, fields)
                if db_name:
                    logger.info(f"Database name extracted using {strategy.__name__}: {db_name}")
                    return db_name
            except Exception as e:
                logger.warning(f"Strategy {strategy.__name__} failed: {str(e)}")
        
        logger.warning("Could not extract database name from document")
        return None
    
    async def _extract_from_fields(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[str]:
        """Extract database name from field providedKey"""
        for field in fields:
            if field.provided_key:
                parts = field.provided_key.split('.')
                if len(parts) >= 1:
                    # Get the last part (most likely to be database name)
                    db_name = parts[-1]
                    if db_name and db_name.strip():
                        return db_name.strip()
        return None
    
    async def _extract_from_dictionary(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[str]:
        """Extract from dictionary.providedKey pattern"""
        if 'dictionary' in document:
            dictionary_obj = document['dictionary']
            if isinstance(dictionary_obj, dict) and 'providedKey' in dictionary_obj:
                provided_key = dictionary_obj['providedKey']
                if provided_key:
                    parts = provided_key.split('.')
                    if len(parts) >= 1:
                        return parts[-1].strip()
        return None
    
    async def _extract_from_context(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[str]:
        """Extract from document context and patterns"""
        # Look for common database name patterns
        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key.lower() in ['database', 'db_name', 'database_name', 'schema']:
                        if isinstance(value, str) and value.strip():
                            return value.strip()
                    result = search_recursive(value, f"{path}.{key}")
                    if result:
                        return result
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    result = search_recursive(item, f"{path}[{i}]")
                    if result:
                        return result
            return None
        
        return search_recursive(document)
    
    async def _extract_using_llm(
        self, 
        document: Dict[str, Any], 
        fields: List[FieldDefinition]
    ) -> Optional[str]:
        """Use LLM to intelligently extract database name"""
        try:
            # Prepare context for LLM
            field_keys = [f.provided_key for f in fields if f.provided_key][:5]  # Sample
            
            prompt = f"""
            Analyze this document structure and extract the most likely database name.
            
            Sample field providedKey patterns:
            {json.dumps(field_keys, indent=2)}
            
            Document keys: {list(document.keys())[:10]}
            
            Based on the patterns, what is the most likely database name?
            Return only the database name, or "NONE" if unclear.
            
            Look for patterns like:
            - Last part of providedKey (e.g., "system.schema.database_name")
            - Dictionary.providedKey values
            - Common database naming conventions
            """
            
            response = await self.llm.apredict(prompt)
            
            # Clean up response
            db_name = response.strip().strip('"\'').strip()
            if db_name and db_name.upper() != "NONE":
                return db_name
                
        except Exception as e:
            logger.warning(f"LLM database name extraction failed: {str(e)}")
        
        return None
    
    def _validate_field_definition(self, field: FieldDefinition) -> ValidationResult:
        """Validate a single field definition"""
        result = ValidationResult(is_valid=True)
        
        # Required field checks
        if not field.name or field.name == 'unknown':
            result.errors.append(f"Field has no valid name: {field.name}")
            result.is_valid = False
        
        if not field.provided_key:
            result.warnings.append(f"Field '{field.name}' has no providedKey")
        
        if not field.description:
            result.warnings.append(f"Field '{field.name}' has no description")
        
        # Data type validation
        if field.data_type == DataType.STRING and field.format:
            if 'varchar' in field.format.lower():
                # Extract length if possible
                try:
                    import re
                    match = re.search(r'varchar\((\d+)\)', field.format.lower())
                    if match:
                        length = int(match.group(1))
                        if length > 4000:
                            result.suggestions.append(
                                f"Field '{field.name}' has very long varchar({length}), consider TEXT type"
                            )
                except:
                    pass
        
        # ProvidedKey format validation
        if field.provided_key:
            parts = field.provided_key.split('.')
            if len(parts) < 2:
                result.warnings.append(
                    f"Field '{field.name}' providedKey '{field.provided_key}' seems incomplete"
                )
            elif len(parts) > 5:
                result.warnings.append(
                    f"Field '{field.name}' providedKey '{field.provided_key}' seems overly complex"
                )
        
        return result
    
    async def _validate_document_structure(
        self, 
        document: Dict[str, Any], 
        context: str
    ) -> Dict[str, List[str]]:
        """Validate overall document structure using LLM"""
        try:
            prompt = f"""
            Analyze this document structure for metadata validation:
            
            Document sample: {json.dumps(dict(list(document.items())[:5]), indent=2)}
            
            Context: {context}
            
            Identify:
            1. Structural issues or inconsistencies
            2. Missing required metadata
            3. Potential improvements
            
            Return JSON with:
            {{
                "errors": ["list of critical issues"],
                "warnings": ["list of warnings"], 
                "suggestions": ["list of improvement suggestions"]
            }}
            """
            
            response = await self.llm.apredict(prompt)
            
            try:
                # Try to parse JSON response
                validation_data = json.loads(response)
                return {
                    "errors": validation_data.get("errors", []),
                    "warnings": validation_data.get("warnings", []),
                    "suggestions": validation_data.get("suggestions", [])
                }
            except json.JSONDecodeError:
                return {
                    "errors": [],
                    "warnings": [f"Could not parse LLM validation response: {response}"],
                    "suggestions": []
                }
                
        except Exception as e:
            return {
                "errors": [f"Document structure validation failed: {str(e)}"],
                "warnings": [],
                "suggestions": []
            }
    
    async def _validate_schema(
        self, 
        schema: SchemaDefinition, 
        validation_rules: List[str], 
        context: str
    ) -> Dict[str, Any]:
        """Validate a schema definition"""
        validation_result = ValidationResult(is_valid=True)
        
        # Basic schema validation
        if not schema.name:
            validation_result.errors.append("Schema has no name")
            validation_result.is_valid = False
        
        if not schema.fields:
            validation_result.errors.append("Schema has no fields")
            validation_result.is_valid = False
        
        # Validate each field
        for field in schema.fields:
            field_validation = self._validate_field_definition(field)
            if not field_validation.is_valid:
                validation_result.is_valid = False
                validation_result.errors.extend(field_validation.errors)
            validation_result.warnings.extend(field_validation.warnings)
            validation_result.suggestions.extend(field_validation.suggestions)
        
        return {
            "validation_result": validation_result.dict(),
            "schema_name": schema.name,
            "field_count": len(schema.fields)
        }


# Register the agent
AgentFactory.register_agent(AgentType.METADATA_VALIDATOR, MetadataValidatorAgent)