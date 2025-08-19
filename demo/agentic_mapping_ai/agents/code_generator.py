"""
Code Generation Agent - Generates PySpark, SQL, and Python code for data transformations
"""

import json
from typing import Any, Dict, List, Optional
from loguru import logger

from .base_agent import BaseAgent, AgentConfig, AgentFactory
from agentic_mapping_ai.core.models import (
    AgentType, SchemaDefinition, MappingRule, 
    GeneratedCode, CodeGenerationRequest
)


class CodeGeneratorAgent(BaseAgent):
    """
    Agent responsible for generating data transformation code
    
    Capabilities:
    - Generate PySpark transformation code
    - Create SQL scripts and queries
    - Generate Python data processing scripts
    - Optimize code for performance
    - Include error handling and logging
    - Generate comprehensive documentation
    """
    
    def _get_system_prompt(self) -> str:
        return """
        You are a Code Generation Agent specialized in creating high-quality data transformation code.
        
        Your expertise includes:
        1. PySpark DataFrame operations and SQL
        2. Data type conversions and mappings
        3. Performance optimization techniques
        4. Error handling and data validation
        5. Code documentation and best practices
        6. Memory-efficient processing patterns
        
        Code generation principles:
        - Write clean, readable, and maintainable code
        - Include comprehensive error handling
        - Add logging and monitoring capabilities
        - Optimize for performance and memory usage
        - Follow industry best practices and conventions
        - Include detailed comments and documentation
        - Generate reusable and modular code components
        
        Always consider:
        - Data quality and validation
        - Scalability and performance
        - Maintainability and readability
        - Error recovery and graceful degradation
        - Resource utilization and optimization
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.CODE_GENERATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute code generation logic
        
        Args:
            input_data: Should contain CodeGenerationRequest data
            context: RAG context with code patterns and examples
            
        Returns:
            Generated code with tests and documentation
        """
        try:
            # Parse request
            request = CodeGenerationRequest(**input_data)
            
            # Generate code based on type
            if request.code_type == "pyspark":
                generated_code = await self._generate_pyspark_code(request, context)
            elif request.code_type == "sql":
                generated_code = await self._generate_sql_code(request, context)
            elif request.code_type == "python":
                generated_code = await self._generate_python_code(request, context)
            else:
                raise ValueError(f"Unsupported code type: {request.code_type}")
            
            # Generate tests if requested
            if request.include_tests:
                test_code = await self._generate_test_code(request, generated_code, context)
                generated_code.test_code = test_code
            
            # Generate documentation
            documentation = await self._generate_documentation(request, generated_code)
            generated_code.documentation = documentation
            
            logger.info(f"Generated {request.code_type} code with {len(generated_code.code)} characters")
            
            return {
                "generated_code": generated_code.dict(),
                "request": request.dict(),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Code generation failed: {str(e)}")
            return {
                "generated_code": None,
                "error": str(e),
                "success": False
            }
    
    async def _generate_pyspark_code(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate PySpark transformation code"""
        
        # Prepare prompt for LLM
        prompt = self._create_pyspark_prompt(request, context)
        
        # Generate code using LLM
        response = await self.llm.apredict(prompt)
        
        # Clean and format the generated code
        code = self._extract_code_from_response(response)
        
        # Extract dependencies
        dependencies = self._extract_dependencies(code, "pyspark")
        
        # Add performance optimizations
        optimized_code = await self._optimize_pyspark_code(code, request.optimization_level)
        
        return GeneratedCode(
            code=optimized_code,
            language="python",
            dependencies=dependencies,
            performance_notes=await self._generate_performance_notes(optimized_code)
        )
    
    def _create_pyspark_prompt(self, request: CodeGenerationRequest, context: str) -> str:
        """Create prompt for PySpark code generation"""
        
        source_fields = [field.dict() for field in request.source_schema.fields]
        target_fields = [field.dict() for field in request.target_schema.fields]
        mapping_rules = [rule.dict() for rule in request.mapping_rules]
        
        prompt = f"""
        Generate a comprehensive PySpark transformation script based on the following requirements:
        
        SOURCE SCHEMA: {request.source_schema.name}
        Fields: {json.dumps(source_fields, indent=2)}
        
        TARGET SCHEMA: {request.target_schema.name}
        Fields: {json.dumps(target_fields, indent=2)}
        
        MAPPING RULES:
        {json.dumps(mapping_rules, indent=2)}
        
        OPTIMIZATION LEVEL: {request.optimization_level}
        
        CONTEXT (Code patterns and examples):
        {context}
        
        Requirements:
        1. Create a complete PySpark script with proper imports
        2. Include data loading from source
        3. Apply all mapping rules and transformations
        4. Handle data type conversions properly
        5. Include data validation and quality checks
        6. Add comprehensive error handling
        7. Include logging throughout the process
        8. Optimize for performance based on optimization level
        9. Save results to target format
        10. Add configuration management
        
        The script should be production-ready with:
        - Proper session management
        - Memory optimization
        - Error recovery
        - Monitoring and metrics
        - Detailed comments
        
        Generate ONLY the Python code, no explanations outside comments.
        """
        
        return prompt
    
    async def _generate_sql_code(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate SQL transformation code"""
        
        prompt = f"""
        Generate SQL transformation queries based on:
        
        SOURCE SCHEMA: {request.source_schema.name}
        TARGET SCHEMA: {request.target_schema.name}
        MAPPING RULES: {json.dumps([rule.dict() for rule in request.mapping_rules], indent=2)}
        
        CONTEXT: {context}
        
        Create:
        1. DDL statements for target tables
        2. Data transformation queries
        3. Data quality validation queries
        4. Performance optimization hints
        5. Error handling procedures
        
        Generate optimized, production-ready SQL code.
        """
        
        response = await self.llm.apredict(prompt)
        code = self._extract_code_from_response(response)
        
        return GeneratedCode(
            code=code,
            language="sql",
            dependencies=["SQL Database Engine"],
            performance_notes="Optimized for large-scale data processing"
        )
    
    async def _generate_python_code(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate Python data processing code"""
        
        prompt = f"""
        Generate Python data transformation code using pandas/numpy based on:
        
        SOURCE SCHEMA: {request.source_schema.name}
        TARGET SCHEMA: {request.target_schema.name}
        MAPPING RULES: {json.dumps([rule.dict() for rule in request.mapping_rules], indent=2)}
        
        CONTEXT: {context}
        
        Create a comprehensive Python script with:
        1. Data loading and validation
        2. Transformations using pandas
        3. Data type handling
        4. Error handling and logging
        5. Performance optimization
        6. Result export
        
        Generate clean, maintainable Python code.
        """
        
        response = await self.llm.apredict(prompt)
        code = self._extract_code_from_response(response)
        dependencies = self._extract_dependencies(code, "python")
        
        return GeneratedCode(
            code=code,
            language="python",
            dependencies=dependencies
        )
    
    def _extract_code_from_response(self, response: str) -> str:
        """Extract code from LLM response"""
        # Remove markdown code blocks if present
        import re
        
        # Look for code blocks
        code_blocks = re.findall(r'```(?:python|sql|scala)?\n?(.*?)\n?```', response, re.DOTALL)
        
        if code_blocks:
            return code_blocks[0].strip()
        
        # If no code blocks, return the whole response (cleaned)
        lines = response.split('\n')
        code_lines = []
        
        for line in lines:
            # Skip explanation lines
            if line.strip().startswith(('Here', 'This', 'The following', 'Note:')):
                continue
            code_lines.append(line)
        
        return '\n'.join(code_lines).strip()
    
    def _extract_dependencies(self, code: str, language: str) -> List[str]:
        """Extract dependencies from generated code"""
        dependencies = []
        
        if language == "pyspark":
            dependencies.extend([
                "pyspark>=3.5.0",
                "py4j",
                "pandas",
                "numpy"
            ])
            
            # Check for additional imports
            if "from pyspark.sql.functions import" in code:
                dependencies.append("pyspark.sql.functions")
            if "from pyspark.ml" in code:
                dependencies.append("pyspark.ml")
                
        elif language == "python":
            import re
            # Extract import statements
            import_pattern = r'import\s+(\w+)|from\s+(\w+)\s+import'
            imports = re.findall(import_pattern, code)
            
            for imp in imports:
                module = imp[0] or imp[1]
                if module and module not in ['os', 'sys', 'json', 're']:
                    dependencies.append(module)
        
        return list(set(dependencies))
    
    async def _optimize_pyspark_code(self, code: str, optimization_level: str) -> str:
        """Optimize PySpark code based on optimization level"""
        
        if optimization_level == "basic":
            return code
        
        optimization_prompt = f"""
        Optimize this PySpark code for {optimization_level} performance:
        
        {code}
        
        Apply optimizations:
        {"- Caching strategies" if optimization_level in ["standard", "advanced"] else ""}
        {"- Partitioning optimization" if optimization_level in ["standard", "advanced"] else ""}
        {"- Broadcast joins" if optimization_level == "advanced" else ""}
        {"- Memory management" if optimization_level == "advanced" else ""}
        {"- Catalyst optimizer hints" if optimization_level == "advanced" else ""}
        
        Return ONLY the optimized code.
        """
        
        try:
            optimized = await self.llm.apredict(optimization_prompt)
            return self._extract_code_from_response(optimized)
        except Exception as e:
            logger.warning(f"Code optimization failed: {str(e)}")
            return code
    
    async def _generate_test_code(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate test code for the generated transformation code"""
        
        test_prompt = f"""
        Generate comprehensive unit tests for this {generated_code.language} code:
        
        GENERATED CODE:
        {generated_code.code}
        
        SOURCE SCHEMA: {request.source_schema.name}
        TARGET SCHEMA: {request.target_schema.name}
        
        Create tests that verify:
        1. Data loading and validation
        2. Each transformation rule
        3. Data type conversions
        4. Error handling scenarios
        5. Edge cases and boundary conditions
        6. Performance assertions
        7. Data quality checks
        
        Use pytest framework and include mock data for testing.
        Generate ONLY the test code.
        """
        
        try:
            response = await self.llm.apredict(test_prompt)
            return self._extract_code_from_response(response)
        except Exception as e:
            logger.warning(f"Test generation failed: {str(e)}")
            return "# Test generation failed"
    
    async def _generate_documentation(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode
    ) -> str:
        """Generate documentation for the generated code"""
        
        doc_prompt = f"""
        Generate comprehensive documentation for this data transformation code:
        
        CODE: {generated_code.code[:1000]}...
        LANGUAGE: {generated_code.language}
        SOURCE SCHEMA: {request.source_schema.name}
        TARGET SCHEMA: {request.target_schema.name}
        
        Include:
        1. Overview and purpose
        2. Prerequisites and dependencies
        3. Configuration requirements
        4. Usage instructions
        5. Input/output specifications
        6. Performance considerations
        7. Error handling and troubleshooting
        8. Maintenance and monitoring
        
        Format as markdown documentation.
        """
        
        try:
            return await self.llm.apredict(doc_prompt)
        except Exception as e:
            logger.warning(f"Documentation generation failed: {str(e)}")
            return "# Documentation generation failed"
    
    async def _generate_performance_notes(self, code: str) -> str:
        """Generate performance notes for the code"""
        
        perf_prompt = f"""
        Analyze this code and provide performance optimization notes:
        
        {code[:500]}...
        
        Provide:
        1. Current performance characteristics
        2. Potential bottlenecks
        3. Optimization recommendations
        4. Scaling considerations
        5. Resource requirements
        
        Keep it concise and actionable.
        """
        
        try:
            return await self.llm.apredict(perf_prompt)
        except Exception as e:
            logger.warning(f"Performance notes generation failed: {str(e)}")
            return "Performance analysis not available"


# Register the agent
AgentFactory.register_agent(AgentType.CODE_GENERATOR, CodeGeneratorAgent)