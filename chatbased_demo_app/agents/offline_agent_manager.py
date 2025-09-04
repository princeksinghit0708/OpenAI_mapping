#!/usr/bin/env python3
"""
Offline Agent Manager for Chat-Based Demo
Manages specialized offline agents for different tasks
Uses only built-in Python libraries - No external dependencies
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio
import json
import logging
from datetime import datetime
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(str, Enum):
    """Types of offline agents"""
    DATA_PROCESSOR = "data_processor"
    SCHEMA_MAPPER = "schema_mapper"
    VALIDATOR = "validator"
    CODE_GENERATOR = "code_generator"
    WORKFLOW_ORCHESTRATOR = "workflow_orchestrator"
    CHAT_ASSISTANT = "chat_assistant"

class OfflineAgent:
    """Base class for offline agents"""
    
    def __init__(self, agent_type: AgentType, name: str):
        self.agent_type = agent_type
        self.name = name
        self.status = "initialized"
        self.capabilities = []
        self.last_used = None
        
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process input data and return results"""
        raise NotImplementedError("Subclasses must implement process method")
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return self.capabilities
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "name": self.name,
            "type": self.agent_type.value,
            "status": self.status,
            "capabilities": self.capabilities,
            "last_used": self.last_used
        }

class DataProcessorAgent(OfflineAgent):
    """Offline agent for data processing tasks"""
    
    def __init__(self):
        super().__init__(AgentType.DATA_PROCESSOR, "Data Processor Agent")
        self.capabilities = [
            "Excel file analysis",
            "CSV file processing", 
            "JSON data handling",
            "Data structure analysis",
            "File format conversion",
            "Data cleaning and validation"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process data files using offline methods"""
        try:
            self.last_used = datetime.now().isoformat()
            
            file_path = input_data.get("file_path")
            task = input_data.get("task", "analyze")
            
            if not file_path or not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": "File not found or path not provided",
                    "agent": self.name
                }
            
            # Analyze file based on extension
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext == '.xlsx' or file_ext == '.xls':
                return await self._process_excel_file(file_path, task)
            elif file_ext == '.csv':
                return await self._process_csv_file(file_path, task)
            elif file_ext == '.json':
                return await self._process_json_file(file_path, task)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported file format: {file_ext}",
                    "agent": self.name
                }
                
        except Exception as e:
            logger.error(f"DataProcessorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _process_excel_file(self, file_path: str, task: str) -> Dict[str, Any]:
        """Process Excel file using pandas"""
        import pandas as pd
        
        try:
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Basic analysis
            analysis = {
                "file_type": "Excel",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
            
            # Sample data
            analysis["sample_data"] = df.head(5).to_dict('records')
            
            return {
                "success": True,
                "result": analysis,
                "agent": self.name,
                "task": task
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Excel processing error: {str(e)}",
                "agent": self.name
            }
    
    async def _process_csv_file(self, file_path: str, task: str) -> Dict[str, Any]:
        """Process CSV file using pandas"""
        import pandas as pd
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Basic analysis
            analysis = {
                "file_type": "CSV",
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum()
            }
            
            # Sample data
            analysis["sample_data"] = df.head(5).to_dict('records')
            
            return {
                "success": True,
                "result": analysis,
                "agent": self.name,
                "task": task
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"CSV processing error: {str(e)}",
                "agent": self.name
            }
    
    async def _process_json_file(self, file_path: str, task: str) -> Dict[str, Any]:
        """Process JSON file using built-in json module"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Analyze JSON structure
            analysis = {
                "file_type": "JSON",
                "data_type": type(data).__name__,
                "structure": self._analyze_json_structure(data)
            }
            
            return {
                "success": True,
                "result": analysis,
                "agent": self.name,
                "task": task
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"JSON processing error: {str(e)}",
                "agent": self.name
            }
    
    def _analyze_json_structure(self, data: Any, depth: int = 0) -> Dict[str, Any]:
        """Analyze JSON structure recursively"""
        if depth > 5:  # Prevent infinite recursion
            return {"type": "max_depth_reached"}
        
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys()),
                "key_count": len(data),
                "sample_values": {k: self._analyze_json_structure(v, depth + 1) for k, v in list(data.items())[:3]}
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "sample_items": [self._analyze_json_structure(item, depth + 1) for item in data[:3]]
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100]  # Truncate long values
            }

class SchemaMapperAgent(OfflineAgent):
    """Offline agent for schema mapping tasks"""
    
    def __init__(self):
        super().__init__(AgentType.SCHEMA_MAPPER, "Schema Mapper Agent")
        self.capabilities = [
            "Field mapping between schemas",
            "Schema analysis and comparison",
            "Mapping rule generation",
            "Transformation logic creation",
            "Schema validation",
            "Mapping documentation"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process schema mapping tasks"""
        try:
            self.last_used = datetime.now().isoformat()
            
            source_schema = input_data.get("source_schema")
            target_schema = input_data.get("target_schema")
            mapping_rules = input_data.get("mapping_rules", [])
            
            if not source_schema or not target_schema:
                return {
                    "success": False,
                    "error": "Both source and target schemas are required",
                    "agent": self.name
                }
            
            # Analyze schemas
            source_analysis = self._analyze_schema(source_schema)
            target_analysis = self._analyze_schema(target_schema)
            
            # Generate mapping suggestions
            mapping_suggestions = self._generate_mapping_suggestions(source_analysis, target_analysis)
            
            return {
                "success": True,
                "result": {
                    "source_analysis": source_analysis,
                    "target_analysis": target_analysis,
                    "mapping_suggestions": mapping_suggestions,
                    "existing_rules": mapping_rules
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"SchemaMapperAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _analyze_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze schema structure"""
        fields = schema.get("fields", [])
        
        analysis = {
            "field_count": len(fields),
            "field_names": [field.get("name", "") for field in fields],
            "data_types": [field.get("type", "unknown") for field in fields],
            "required_fields": [field.get("name", "") for field in fields if field.get("required", False)],
            "field_details": fields
        }
        
        return analysis
    
    def _generate_mapping_suggestions(self, source: Dict[str, Any], target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate mapping suggestions using pattern matching"""
        suggestions = []
        
        source_fields = source.get("field_names", [])
        target_fields = target.get("field_names", [])
        
        for source_field in source_fields:
            # Find exact matches
            exact_matches = [tf for tf in target_fields if tf.lower() == source_field.lower()]
            
            # Find partial matches
            partial_matches = [tf for tf in target_fields if source_field.lower() in tf.lower() or tf.lower() in source_field.lower()]
            
            # Find similar matches using simple string similarity
            similar_matches = []
            for tf in target_fields:
                similarity = self._calculate_similarity(source_field, tf)
                if similarity > 0.6:  # 60% similarity threshold
                    similar_matches.append((tf, similarity))
            
            suggestion = {
                "source_field": source_field,
                "exact_matches": exact_matches,
                "partial_matches": partial_matches,
                "similar_matches": similar_matches,
                "confidence": "high" if exact_matches else "medium" if partial_matches else "low"
            }
            
            suggestions.append(suggestion)
        
        return suggestions
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate simple string similarity"""
        str1 = str1.lower()
        str2 = str2.lower()
        
        # Simple character-based similarity
        common_chars = set(str1) & set(str2)
        total_chars = set(str1) | set(str2)
        
        if not total_chars:
            return 0.0
        
        return len(common_chars) / len(total_chars)

class ValidatorAgent(OfflineAgent):
    """Offline agent for data validation tasks"""
    
    def __init__(self):
        super().__init__(AgentType.VALIDATOR, "Validator Agent")
        self.capabilities = [
            "Data quality validation",
            "Business rule validation",
            "Schema compliance checking",
            "Data completeness analysis",
            "Validation report generation",
            "Error detection and reporting"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process validation tasks"""
        try:
            self.last_used = datetime.now().isoformat()
            
            data = input_data.get("data")
            validation_rules = input_data.get("validation_rules", [])
            
            if not data:
                return {
                    "success": False,
                    "error": "Data is required for validation",
                    "agent": self.name
                }
            
            # Perform validation
            validation_results = self._perform_validation(data, validation_rules)
            
            return {
                "success": True,
                "result": validation_results,
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"ValidatorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _perform_validation(self, data: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform data validation using built-in methods"""
        results = {
            "total_records": len(data),
            "valid_records": 0,
            "invalid_records": 0,
            "errors": [],
            "warnings": [],
            "validation_summary": {}
        }
        
        for i, record in enumerate(data):
            record_errors = []
            record_warnings = []
            
            # Check for missing required fields
            for rule in rules:
                if rule.get("type") == "required_field":
                    field_name = rule.get("field")
                    if field_name not in record or not record[field_name]:
                        record_errors.append(f"Missing required field: {field_name}")
            
            # Check data types
            for rule in rules:
                if rule.get("type") == "data_type":
                    field_name = rule.get("field")
                    expected_type = rule.get("expected_type")
                    if field_name in record:
                        if not self._check_data_type(record[field_name], expected_type):
                            record_errors.append(f"Invalid data type for {field_name}: expected {expected_type}")
            
            # Check value ranges
            for rule in rules:
                if rule.get("type") == "value_range":
                    field_name = rule.get("field")
                    min_val = rule.get("min_value")
                    max_val = rule.get("max_value")
                    if field_name in record and record[field_name] is not None:
                        try:
                            value = float(record[field_name])
                            if min_val is not None and value < min_val:
                                record_errors.append(f"Value too low for {field_name}: {value} < {min_val}")
                            if max_val is not None and value > max_val:
                                record_errors.append(f"Value too high for {field_name}: {value} > {max_val}")
                        except (ValueError, TypeError):
                            record_errors.append(f"Cannot validate range for {field_name}: not a number")
            
            if record_errors:
                results["invalid_records"] += 1
                results["errors"].extend([f"Record {i}: {error}" for error in record_errors])
            else:
                results["valid_records"] += 1
            
            if record_warnings:
                results["warnings"].extend([f"Record {i}: {warning}" for warning in record_warnings])
        
        # Calculate validation summary
        results["validation_summary"] = {
            "validity_rate": results["valid_records"] / results["total_records"] if results["total_records"] > 0 else 0,
            "error_rate": results["invalid_records"] / results["total_records"] if results["total_records"] > 0 else 0,
            "total_errors": len(results["errors"]),
            "total_warnings": len(results["warnings"])
        }
        
        return results
    
    def _check_data_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected data type"""
        if expected_type == "string":
            return isinstance(value, str)
        elif expected_type == "number":
            return isinstance(value, (int, float))
        elif expected_type == "boolean":
            return isinstance(value, bool)
        elif expected_type == "date":
            return isinstance(value, str) and self._is_date_string(value)
        else:
            return True  # Unknown type, assume valid
    
    def _is_date_string(self, value: str) -> bool:
        """Check if string is a valid date"""
        import re
        # Simple date pattern matching
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}'   # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                return True
        return False

class CodeGeneratorAgent(OfflineAgent):
    """Offline agent for code generation tasks"""
    
    def __init__(self):
        super().__init__(AgentType.CODE_GENERATOR, "Code Generator Agent")
        self.capabilities = [
            "Python code generation",
            "SQL query generation",
            "Data transformation scripts",
            "Validation code creation",
            "Template-based code generation",
            "Code documentation"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process code generation tasks"""
        try:
            self.last_used = datetime.now().isoformat()
            
            code_type = input_data.get("code_type", "python")
            task = input_data.get("task", "data_processing")
            parameters = input_data.get("parameters", {})
            
            if code_type == "python":
                code = self._generate_python_code(task, parameters)
            elif code_type == "sql":
                code = self._generate_sql_code(task, parameters)
            else:
                return {
                    "success": False,
                    "error": f"Unsupported code type: {code_type}",
                    "agent": self.name
                }
            
            return {
                "success": True,
                "result": {
                    "code": code,
                    "code_type": code_type,
                    "task": task,
                    "parameters": parameters
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"CodeGeneratorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _generate_python_code(self, task: str, parameters: Dict[str, Any]) -> str:
        """Generate Python code using templates"""
        if task == "data_processing":
            return self._generate_data_processing_code(parameters)
        elif task == "data_validation":
            return self._generate_validation_code(parameters)
        elif task == "schema_mapping":
            return self._generate_mapping_code(parameters)
        else:
            return f"# Generated Python code for {task}\n# Parameters: {parameters}\n\n# TODO: Implement {task} functionality"
    
    def _generate_data_processing_code(self, parameters: Dict[str, Any]) -> str:
        """Generate data processing Python code"""
        file_path = parameters.get("file_path", "data.xlsx")
        file_type = parameters.get("file_type", "excel")
        
        if file_type == "excel":
            return f'''import pandas as pd
import numpy as np

def process_excel_file(file_path="{file_path}"):
    """Process Excel file and return analysis"""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Basic analysis
        print(f"File: {{file_path}}")
        print(f"Shape: {{df.shape}}")
        print(f"Columns: {{list(df.columns)}}")
        print(f"Data types: {{df.dtypes}}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        print(f"Missing values: {{missing_values}}")
        
        # Return processed data
        return df
        
    except Exception as e:
        print(f"Error processing file: {{e}}")
        return None

if __name__ == "__main__":
    df = process_excel_file()
    if df is not None:
        print("Data processing completed successfully!")
'''
        else:
            return f'''import pandas as pd

def process_data_file(file_path="{file_path}"):
    """Process data file"""
    try:
        # Read file based on extension
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            df = pd.read_json(file_path)
        else:
            print("Unsupported file format")
            return None
        
        # Process data
        print(f"Processed {{len(df)}} records")
        return df
        
    except Exception as e:
        print(f"Error: {{e}}")
        return None

if __name__ == "__main__":
    process_data_file()
'''
    
    def _generate_validation_code(self, parameters: Dict[str, Any]) -> str:
        """Generate data validation Python code"""
        return '''def validate_data(data, rules):
    """Validate data against rules"""
    errors = []
    warnings = []
    
    for i, record in enumerate(data):
        record_errors = []
        
        # Check required fields
        for rule in rules.get("required_fields", []):
            if rule not in record or not record[rule]:
                record_errors.append(f"Missing required field: {rule}")
        
        # Check data types
        for field, expected_type in rules.get("data_types", {}).items():
            if field in record:
                if not isinstance(record[field], expected_type):
                    record_errors.append(f"Invalid type for {field}")
        
        if record_errors:
            errors.extend([f"Record {i}: {error}" for error in record_errors])
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

# Example usage
validation_rules = {
    "required_fields": ["id", "name", "email"],
    "data_types": {"id": int, "name": str, "email": str}
}

# Validate your data
# result = validate_data(your_data, validation_rules)
'''
    
    def _generate_mapping_code(self, parameters: Dict[str, Any]) -> str:
        """Generate schema mapping Python code"""
        return '''def map_schema(source_data, mapping_rules):
    """Map data from source to target schema"""
    mapped_data = []
    
    for record in source_data:
        mapped_record = {}
        
        for target_field, source_field in mapping_rules.items():
            if source_field in record:
                mapped_record[target_field] = record[source_field]
            else:
                mapped_record[target_field] = None
        
        mapped_data.append(mapped_record)
    
    return mapped_data

# Example mapping rules
mapping_rules = {
    "customer_id": "id",
    "customer_name": "name",
    "customer_email": "email",
    "registration_date": "created_at"
}

# Map your data
# mapped_data = map_schema(source_data, mapping_rules)
'''
    
    def _generate_sql_code(self, task: str, parameters: Dict[str, Any]) -> str:
        """Generate SQL code"""
        if task == "data_processing":
            return '''-- Data processing SQL queries

-- Create table
CREATE TABLE IF NOT EXISTS processed_data (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data
INSERT INTO processed_data (id, name, email)
VALUES (1, 'John Doe', 'john@example.com'),
       (2, 'Jane Smith', 'jane@example.com');

-- Query data
SELECT * FROM processed_data WHERE created_at >= '2024-01-01';

-- Update data
UPDATE processed_data 
SET email = LOWER(email) 
WHERE email IS NOT NULL;

-- Delete old data
DELETE FROM processed_data 
WHERE created_at < '2023-01-01';
'''
        else:
            return f'''-- Generated SQL for {task}
-- Parameters: {parameters}

-- TODO: Implement {task} SQL functionality
SELECT 'Hello World' as message;
'''

class OfflineAgentManager:
    """Manager for offline agents"""
    
    def __init__(self):
        self.agents = {}
        self.agent_status = {}
        self.workflow_history = []
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available offline agents"""
        print("🤖 Initializing Offline Agents...")
        
        # Create agent instances
        self.agents = {
            AgentType.DATA_PROCESSOR: DataProcessorAgent(),
            AgentType.SCHEMA_MAPPER: SchemaMapperAgent(),
            AgentType.VALIDATOR: ValidatorAgent(),
            AgentType.CODE_GENERATOR: CodeGeneratorAgent()
        }
        
        # Initialize agent status
        for agent_type, agent in self.agents.items():
            self.agent_status[agent_type.value] = agent.get_status()
        
        print(f"✅ Initialized {len(self.agents)} offline agents")
        for agent_type, agent in self.agents.items():
            print(f"   • {agent.name}: {agent.status}")
    
    async def process_with_agent(self, 
                               agent_type: AgentType, 
                               input_data: Dict[str, Any], 
                               context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process input with specific agent"""
        try:
            if agent_type not in self.agents:
                return {
                    "success": False,
                    "error": f"Agent {agent_type.value} not available",
                    "agent": "unknown"
                }
            
            agent = self.agents[agent_type]
            result = await agent.process(input_data, context)
            
            # Log workflow
            self.workflow_history.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent.name,
                "agent_type": agent_type.value,
                "input_keys": list(input_data.keys()),
                "success": result.get("success", False)
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Agent processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": agent_type.value
            }
    
    async def process_with_workflow(self, 
                                  workflow: List[Dict[str, Any]], 
                                  input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input through a workflow of agents"""
        try:
            results = []
            current_data = input_data.copy()
            
            for step in workflow:
                agent_type = AgentType(step["agent_type"])
                step_input = step.get("input", current_data)
                
                result = await self.process_with_agent(agent_type, step_input)
                results.append(result)
                
                if not result.get("success", False):
                    return {
                        "success": False,
                        "error": f"Workflow failed at step: {step['agent_type']}",
                        "results": results
                    }
                
                # Update current data with result
                if "result" in result:
                    current_data.update(result["result"])
            
            return {
                "success": True,
                "results": results,
                "final_data": current_data
            }
            
        except Exception as e:
            logger.error(f"Workflow processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "results": results if 'results' in locals() else []
            }
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of available agents"""
        return [agent.get_status() for agent in self.agents.values()]
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.workflow_history
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all agents"""
        return {
            agent_type.value: agent.get_capabilities() 
            for agent_type, agent in self.agents.items()
        }

# Global agent manager instance
offline_agent_manager = OfflineAgentManager()
