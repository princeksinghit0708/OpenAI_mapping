#!/usr/bin/env python3
"""
Hybrid Agent Manager for Chat-Based Demo
Uses llm_service.py for online LLM responses but removes Hugging Face dependencies
Maintains agentic approach with online LLM integration
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

# Add the parent directory to path for imports
sys.path.append('..')
sys.path.append('../agentic_mapping_ai')
sys.path.append('../demo')

# Import llm_service for online responses
try:
    from agentic_mapping_ai.llm_service import LLMService
    LLM_SERVICE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: LLM service not available: {e}")
    LLM_SERVICE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentType(str, Enum):
    """Types of hybrid agents"""
    DATA_PROCESSOR = "data_processor"
    SCHEMA_MAPPER = "schema_mapper"
    VALIDATOR = "validator"
    CODE_GENERATOR = "code_generator"
    WORKFLOW_ORCHESTRATOR = "workflow_orchestrator"
    CHAT_ASSISTANT = "chat_assistant"

class HybridAgent:
    """Base class for hybrid agents that can use both offline and online processing"""
    
    def __init__(self, agent_type: AgentType, name: str, use_llm: bool = True):
        self.agent_type = agent_type
        self.name = name
        self.use_llm = use_llm and LLM_SERVICE_AVAILABLE
        self.status = "initialized"
        self.capabilities = []
        self.last_used = None
        
        # Initialize LLM service if available
        if self.use_llm:
            try:
                self.llm_service = LLMService()
                self.status = "ready"
            except Exception as e:
                logger.warning(f"Could not initialize LLM service for {name}: {e}")
                self.use_llm = False
                self.status = "offline_only"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process input data and return results"""
        raise NotImplementedError("Subclasses must implement process method")
    
    async def _get_llm_response(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Get response from LLM service"""
        if not self.use_llm or not hasattr(self, 'llm_service'):
            return "LLM service not available"
        
        try:
            # Use the existing LLM service
            response = await self.llm_service.generate_response(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM service error: {e}")
            return f"LLM service error: {str(e)}"
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities"""
        return self.capabilities
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information"""
        return {
            "name": self.name,
            "type": self.agent_type.value,
            "status": self.status,
            "use_llm": self.use_llm,
            "capabilities": self.capabilities,
            "last_used": self.last_used
        }

class HybridDataProcessorAgent(HybridAgent):
    """Hybrid agent for data processing tasks with LLM integration"""
    
    def __init__(self, use_llm: bool = True):
        super().__init__(AgentType.DATA_PROCESSOR, "Hybrid Data Processor Agent", use_llm)
        self.capabilities = [
            "Excel file analysis with LLM insights",
            "CSV file processing with intelligent suggestions", 
            "JSON data handling with pattern recognition",
            "Data structure analysis with recommendations",
            "File format conversion with optimization tips",
            "Data cleaning and validation with AI guidance"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process data files using hybrid approach"""
        try:
            self.last_used = datetime.now().isoformat()
            
            file_path = input_data.get("file_path")
            task = input_data.get("task", "analyze")
            user_input = input_data.get("user_input", "")
            
            if not file_path or not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": "File not found or path not provided",
                    "agent": self.name
                }
            
            # Perform basic file analysis
            basic_analysis = await self._analyze_file_basic(file_path)
            
            # Get LLM insights if available
            llm_insights = ""
            if self.use_llm and user_input:
                llm_insights = await self._get_llm_insights(basic_analysis, user_input, task)
            
            # Combine results
            result = {
                **basic_analysis,
                "llm_insights": llm_insights,
                "analysis_method": "hybrid_llm" if self.use_llm else "basic_offline"
            }
            
            return {
                "success": True,
                "result": result,
                "agent": self.name,
                "task": task
            }
                
        except Exception as e:
            logger.error(f"HybridDataProcessorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    async def _analyze_file_basic(self, file_path: str) -> Dict[str, Any]:
        """Basic file analysis using pandas"""
        import pandas as pd
        
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.xlsx' or file_ext == '.xls':
                df = pd.read_excel(file_path)
            elif file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            else:
                return {"error": f"Unsupported file format: {file_ext}"}
            
            # Basic analysis
            analysis = {
                "file_type": file_ext[1:].upper(),
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "sample_data": df.head(5).to_dict('records')
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"File analysis error: {str(e)}"}
    
    async def _get_llm_insights(self, analysis: Dict[str, Any], user_input: str, task: str) -> str:
        """Get LLM insights for data analysis"""
        prompt = f"""
        As a data analysis expert, provide insights about this data file:
        
        File Analysis:
        - File Type: {analysis.get('file_type', 'Unknown')}
        - Rows: {analysis.get('rows', 0)}
        - Columns: {analysis.get('columns', 0)}
        - Column Names: {', '.join(analysis.get('column_names', []))}
        - Missing Values: {sum(analysis.get('missing_values', {}).values())}
        
        User Request: {user_input}
        Task: {task}
        
        Please provide:
        1. Key insights about the data structure
        2. Potential data quality issues
        3. Recommendations for next steps
        4. Specific suggestions based on the user's request
        
        Keep the response concise and actionable.
        """
        
        return await self._get_llm_response(prompt)

class HybridSchemaMapperAgent(HybridAgent):
    """Hybrid agent for schema mapping tasks with LLM integration"""
    
    def __init__(self, use_llm: bool = True):
        super().__init__(AgentType.SCHEMA_MAPPER, "Hybrid Schema Mapper Agent", use_llm)
        self.capabilities = [
            "Intelligent field mapping with LLM suggestions",
            "Schema analysis and comparison with AI insights",
            "Mapping rule generation with best practices",
            "Transformation logic creation with optimization",
            "Schema validation with intelligent recommendations",
            "Mapping documentation with detailed explanations"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process schema mapping tasks with LLM assistance"""
        try:
            self.last_used = datetime.now().isoformat()
            
            source_schema = input_data.get("source_schema")
            target_schema = input_data.get("target_schema")
            mapping_rules = input_data.get("mapping_rules", [])
            user_input = input_data.get("user_input", "")
            
            if not source_schema or not target_schema:
                return {
                    "success": False,
                    "error": "Both source and target schemas are required",
                    "agent": self.name
                }
            
            # Basic schema analysis
            source_analysis = self._analyze_schema(source_schema)
            target_analysis = self._analyze_schema(target_schema)
            
            # Generate basic mapping suggestions
            basic_mappings = self._generate_basic_mappings(source_analysis, target_analysis)
            
            # Get LLM-enhanced mappings if available
            llm_mappings = []
            if self.use_llm and user_input:
                llm_mappings = await self._get_llm_mappings(source_analysis, target_analysis, user_input)
            
            return {
                "success": True,
                "result": {
                    "source_analysis": source_analysis,
                    "target_analysis": target_analysis,
                    "basic_mappings": basic_mappings,
                    "llm_mappings": llm_mappings,
                    "existing_rules": mapping_rules,
                    "mapping_method": "hybrid_llm" if self.use_llm else "basic_offline"
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"HybridSchemaMapperAgent error: {e}")
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
    
    def _generate_basic_mappings(self, source: Dict[str, Any], target: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic mapping suggestions using pattern matching"""
        suggestions = []
        
        source_fields = source.get("field_names", [])
        target_fields = target.get("field_names", [])
        
        for source_field in source_fields:
            # Find exact matches
            exact_matches = [tf for tf in target_fields if tf.lower() == source_field.lower()]
            
            # Find partial matches
            partial_matches = [tf for tf in target_fields if source_field.lower() in tf.lower() or tf.lower() in source_field.lower()]
            
            suggestion = {
                "source_field": source_field,
                "exact_matches": exact_matches,
                "partial_matches": partial_matches,
                "confidence": "high" if exact_matches else "medium" if partial_matches else "low"
            }
            
            suggestions.append(suggestion)
        
        return suggestions
    
    async def _get_llm_mappings(self, source: Dict[str, Any], target: Dict[str, Any], user_input: str) -> List[Dict[str, Any]]:
        """Get LLM-enhanced mapping suggestions"""
        prompt = f"""
        As a data mapping expert, help create intelligent field mappings between these schemas:
        
        Source Schema:
        - Fields: {', '.join(source.get('field_names', []))}
        - Data Types: {', '.join(source.get('data_types', []))}
        - Required Fields: {', '.join(source.get('required_fields', []))}
        
        Target Schema:
        - Fields: {', '.join(target.get('field_names', []))}
        - Data Types: {', '.join(target.get('data_types', []))}
        - Required Fields: {', '.join(target.get('required_fields', []))}
        
        User Request: {user_input}
        
        Please provide:
        1. Recommended field mappings with confidence scores
        2. Transformation logic for each mapping
        3. Potential data quality considerations
        4. Best practices for the mapping
        
        Format as JSON with fields: source_field, target_field, confidence, transformation, notes
        """
        
        llm_response = await self._get_llm_response(prompt)
        
        # Try to parse LLM response as JSON, fallback to text
        try:
            return json.loads(llm_response)
        except:
            return [{"llm_insights": llm_response}]

class HybridValidatorAgent(HybridAgent):
    """Hybrid agent for data validation tasks with LLM integration"""
    
    def __init__(self, use_llm: bool = True):
        super().__init__(AgentType.VALIDATOR, "Hybrid Validator Agent", use_llm)
        self.capabilities = [
            "Intelligent data quality validation with LLM insights",
            "Business rule validation with AI recommendations",
            "Schema compliance checking with smart suggestions",
            "Data completeness analysis with optimization tips",
            "Validation report generation with detailed explanations",
            "Error detection and reporting with remediation guidance"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process validation tasks with LLM assistance"""
        try:
            self.last_used = datetime.now().isoformat()
            
            data = input_data.get("data")
            validation_rules = input_data.get("validation_rules", [])
            user_input = input_data.get("user_input", "")
            
            if not data:
                return {
                    "success": False,
                    "error": "Data is required for validation",
                    "agent": self.name
                }
            
            # Perform basic validation
            basic_validation = self._perform_basic_validation(data, validation_rules)
            
            # Get LLM insights if available
            llm_insights = ""
            if self.use_llm and user_input:
                llm_insights = await self._get_validation_insights(basic_validation, user_input)
            
            # Combine results
            result = {
                **basic_validation,
                "llm_insights": llm_insights,
                "validation_method": "hybrid_llm" if self.use_llm else "basic_offline"
            }
            
            return {
                "success": True,
                "result": result,
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"HybridValidatorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _perform_basic_validation(self, data: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform basic data validation"""
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
            
            if record_errors:
                results["invalid_records"] += 1
                results["errors"].extend([f"Record {i}: {error}" for error in record_errors])
            else:
                results["valid_records"] += 1
        
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
            return True
    
    def _is_date_string(self, value: str) -> bool:
        """Check if string is a valid date"""
        import re
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}'   # MM-DD-YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, value):
                return True
        return False
    
    async def _get_validation_insights(self, validation_results: Dict[str, Any], user_input: str) -> str:
        """Get LLM insights for validation results"""
        prompt = f"""
        As a data quality expert, analyze these validation results and provide insights:
        
        Validation Results:
        - Total Records: {validation_results.get('total_records', 0)}
        - Valid Records: {validation_results.get('valid_records', 0)}
        - Invalid Records: {validation_results.get('invalid_records', 0)}
        - Validity Rate: {validation_results.get('validation_summary', {}).get('validity_rate', 0):.2%}
        - Total Errors: {validation_results.get('validation_summary', {}).get('total_errors', 0)}
        
        User Request: {user_input}
        
        Please provide:
        1. Analysis of data quality issues
        2. Root cause analysis of errors
        3. Recommendations for data improvement
        4. Specific actions to fix the issues
        5. Prevention strategies for future data
        
        Keep the response actionable and specific.
        """
        
        return await self._get_llm_response(prompt)

class HybridCodeGeneratorAgent(HybridAgent):
    """Hybrid agent for code generation tasks with LLM integration"""
    
    def __init__(self, use_llm: bool = True):
        super().__init__(AgentType.CODE_GENERATOR, "Hybrid Code Generator Agent", use_llm)
        self.capabilities = [
            "Intelligent Python code generation with LLM assistance",
            "SQL query generation with optimization suggestions",
            "Data transformation scripts with best practices",
            "Validation code creation with comprehensive coverage",
            "Template-based code generation with AI enhancement",
            "Code documentation with detailed explanations"
        ]
        self.status = "ready"
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process code generation tasks with LLM assistance"""
        try:
            self.last_used = datetime.now().isoformat()
            
            code_type = input_data.get("code_type", "python")
            task = input_data.get("task", "data_processing")
            parameters = input_data.get("parameters", {})
            user_input = input_data.get("user_input", "")
            
            # Generate basic code template
            basic_code = self._generate_basic_code(code_type, task, parameters)
            
            # Get LLM-enhanced code if available
            enhanced_code = basic_code
            if self.use_llm and user_input:
                enhanced_code = await self._get_llm_enhanced_code(code_type, task, parameters, user_input, basic_code)
            
            return {
                "success": True,
                "result": {
                    "code": enhanced_code,
                    "basic_code": basic_code,
                    "code_type": code_type,
                    "task": task,
                    "parameters": parameters,
                    "generation_method": "hybrid_llm" if self.use_llm else "basic_offline"
                },
                "agent": self.name
            }
            
        except Exception as e:
            logger.error(f"HybridCodeGeneratorAgent error: {e}")
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _generate_basic_code(self, code_type: str, task: str, parameters: Dict[str, Any]) -> str:
        """Generate basic code template"""
        if code_type == "python":
            return self._generate_python_template(task, parameters)
        elif code_type == "sql":
            return self._generate_sql_template(task, parameters)
        else:
            return f"# Generated {code_type} code for {task}\n# Parameters: {parameters}\n\n# TODO: Implement {task} functionality"
    
    def _generate_python_template(self, task: str, parameters: Dict[str, Any]) -> str:
        """Generate Python code template"""
        if task == "data_processing":
            return '''import pandas as pd
import numpy as np

def process_data(file_path):
    """Process data file and return analysis"""
    try:
        # Read data file
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            print("Unsupported file format")
            return None
        
        # Basic analysis
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        print(f"Missing values: {missing_values}")
        
        return df
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Process your data file
    df = process_data("your_file.xlsx")
'''
        else:
            return f'''# Generated Python code for {task}
# Parameters: {parameters}

def {task.replace(' ', '_')}():
    """Implement {task} functionality"""
    # TODO: Add your implementation here
    pass

if __name__ == "__main__":
    {task.replace(' ', '_')}()
'''
    
    def _generate_sql_template(self, task: str, parameters: Dict[str, Any]) -> str:
        """Generate SQL code template"""
        return f'''-- Generated SQL for {task}
-- Parameters: {parameters}

-- TODO: Implement {task} SQL functionality
SELECT 'Hello World' as message;
'''
    
    async def _get_llm_enhanced_code(self, code_type: str, task: str, parameters: Dict[str, Any], user_input: str, basic_code: str) -> str:
        """Get LLM-enhanced code"""
        prompt = f"""
        As a software engineering expert, enhance this {code_type} code for {task}:
        
        Basic Code:
        ```{code_type}
        {basic_code}
        ```
        
        User Request: {user_input}
        Parameters: {parameters}
        
        Please provide:
        1. Enhanced, production-ready code
        2. Proper error handling
        3. Documentation and comments
        4. Best practices implementation
        5. Optimization suggestions
        
        Return only the enhanced code with proper formatting.
        """
        
        return await self._get_llm_response(prompt)

class HybridAgentManager:
    """Manager for hybrid agents that use both offline and online processing"""
    
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm and LLM_SERVICE_AVAILABLE
        self.agents = {}
        self.agent_status = {}
        self.workflow_history = []
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all available hybrid agents"""
        print("🤖 Initializing Hybrid Agents...")
        print(f"   🔗 LLM Service: {'Available' if self.use_llm else 'Not Available'}")
        
        # Create agent instances
        self.agents = {
            AgentType.DATA_PROCESSOR: HybridDataProcessorAgent(self.use_llm),
            AgentType.SCHEMA_MAPPER: HybridSchemaMapperAgent(self.use_llm),
            AgentType.VALIDATOR: HybridValidatorAgent(self.use_llm),
            AgentType.CODE_GENERATOR: HybridCodeGeneratorAgent(self.use_llm)
        }
        
        # Initialize agent status
        for agent_type, agent in self.agents.items():
            self.agent_status[agent_type.value] = agent.get_status()
        
        print(f"✅ Initialized {len(self.agents)} hybrid agents")
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
                "use_llm": agent.use_llm,
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

# Global hybrid agent manager instance
hybrid_agent_manager = HybridAgentManager()
