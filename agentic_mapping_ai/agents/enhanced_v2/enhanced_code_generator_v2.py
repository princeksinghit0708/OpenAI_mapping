"""
Enhanced Code Generator v2 - Production Ready with LangChain + LiteLLM
Generates high-quality PySpark, SQL, and Python code with advanced AI capabilities
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime

from agents.enhanced_agent_v2 import EnhancedBaseAgent, EnhancedAgentConfig, create_enhanced_agent
from core.models import (
    AgentType, SchemaDefinition, MappingRule, 
    GeneratedCode, CodeGenerationRequest
)


class EnhancedCodeGenerator(EnhancedBaseAgent):
    """
    Production-ready code generator with advanced AI capabilities
    
    Features:
    - Multi-model code generation (GPT-4 for complex, Claude for analysis)
    - Advanced PySpark optimization
    - Comprehensive test generation
    - Performance-aware code patterns
    - LangChain + LiteLLM integration
    """
    
    def __init__(self, config: EnhancedAgentConfig, rag_engine=None, tools=None):
        # Ensure this is configured as a code generator
        config.agent_type = "code_generator"
        
        super().__init__(config, rag_engine, tools)
        
        # Code generation specific tracking
        self.generation_stats = {
            "total_generations": 0,
            "code_types": {},
            "average_complexity": 0.0,
            "optimization_levels": {}
        }
        
        self.logger.info("Enhanced Code Generator initialized")
    
    def _get_system_prompt(self) -> str:
        return """
        You are an Enhanced Code Generation Agent specialized in creating high-quality data transformation code.
        
        Your advanced capabilities:
        1. **Multi-Language Expertise**: PySpark, SQL, Python with deep understanding
        2. **Performance Optimization**: Generate code optimized for large-scale data processing
        3. **Best Practices Integration**: Include industry standards and patterns
        4. **Context-Aware Generation**: Use metadata and schemas for intelligent code creation
        5. **Comprehensive Testing**: Generate thorough test suites automatically
        
        Code generation principles:
        - Write production-ready, maintainable code
        - Include comprehensive error handling and logging
        - Optimize for performance, memory efficiency, and scalability
        - Follow language-specific best practices and conventions
        - Generate modular, reusable components
        - Include detailed documentation and comments
        
        PySpark Expertise:
        - DataFrame operations, SQL, and RDD transformations
        - Catalyst optimizer utilization
        - Memory management and caching strategies
        - Partitioning and shuffling optimization
        - Integration with various data sources
        
        SQL Expertise:
        - Complex queries with CTEs and window functions
        - Performance optimization with indexes and hints
        - Database-specific optimizations
        - Data quality and validation queries
        
        Python Expertise:
        - Pandas DataFrame operations
        - Memory-efficient processing
        - Async/await patterns where applicable
        - Type hints and documentation
        
        Always consider:
        - Data volume and processing requirements
        - Error scenarios and edge cases
        - Monitoring and observability
        - Code maintainability and readability
        - Resource utilization and optimization
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.CODE_GENERATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """Enhanced code generation logic"""
        try:
            # Parse request
            if isinstance(input_data, dict) and 'source_schema' in input_data:
                # Direct CodeGenerationRequest
                request = CodeGenerationRequest(**input_data)
            else:
                # Wrapped request
                request_data = input_data.get("code_request", input_data)
                request = CodeGenerationRequest(**request_data)
            
            self.logger.info("Starting enhanced code generation", 
                           code_type=request.code_type,
                           optimization_level=request.optimization_level,
                           include_tests=request.include_tests)
            
            # Generate code based on type with AI enhancement
            if request.code_type == "pyspark":
                generated_code = await self._generate_pyspark_enhanced(request, context)
            elif request.code_type == "sql":
                generated_code = await self._generate_sql_enhanced(request, context)
            elif request.code_type == "python":
                generated_code = await self._generate_python_enhanced(request, context)
            else:
                raise ValueError(f"Unsupported code type: {request.code_type}")
            
            # Generate comprehensive tests if requested
            if request.include_tests:
                test_code = await self._generate_comprehensive_tests(request, generated_code, context)
                generated_code.test_code = test_code
            
            # Generate enhanced documentation
            documentation = await self._generate_enhanced_documentation(request, generated_code, context)
            generated_code.documentation = documentation
            
            # Add performance analysis
            performance_analysis = await self._analyze_code_performance(generated_code, request)
            generated_code.performance_notes = performance_analysis
            
            # Update statistics
            self.generation_stats["total_generations"] += 1
            self.generation_stats["code_types"][request.code_type] = \
                self.generation_stats["code_types"].get(request.code_type, 0) + 1
            self.generation_stats["optimization_levels"][request.optimization_level] = \
                self.generation_stats["optimization_levels"].get(request.optimization_level, 0) + 1
            
            self.logger.info("Enhanced code generation completed", 
                           code_length=len(generated_code.code),
                           test_code_length=len(generated_code.test_code or ""),
                           has_documentation=bool(generated_code.documentation))
            
            return {
                "generated_code": generated_code.dict(),
                "request": request.dict(),
                "generation_stats": self.generation_stats.copy(),
                "success": True,
                "ai_enhancement_used": True
            }
            
        except Exception as e:
            self.logger.error("Enhanced code generation failed", error=str(e))
            return {
                "generated_code": None,
                "error": str(e),
                "success": False,
                "ai_enhancement_used": False
            }
    
    async def _generate_pyspark_enhanced(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate enhanced PySpark code with AI optimization"""
        
        # Prepare comprehensive prompt
        prompt = await self._create_enhanced_pyspark_prompt(request, context)
        
        # Use best model for code generation (GPT-4 preferred)
        messages = [
            {
                "role": "system",
                "content": "You are a PySpark expert. Generate production-ready, optimized code."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        try:
            # Generate with primary model
            response = await self.llm_provider.generate(messages, max_tokens=3000)
            code = self._extract_and_clean_code(response["content"])
            
            # AI-powered optimization
            optimized_code = await self._ai_optimize_pyspark_code(code, request.optimization_level)
            
            # Extract dependencies intelligently
            dependencies = await self._extract_dependencies_ai(optimized_code, "pyspark")
            
            return GeneratedCode(
                code=optimized_code,
                language="python",
                dependencies=dependencies,
                performance_notes="AI-optimized PySpark code with advanced patterns"
            )
            
        except Exception as e:
            self.logger.error("PySpark generation failed", error=str(e))
            # Fallback to simpler generation
            return await self._generate_pyspark_fallback(request)
    
    async def _create_enhanced_pyspark_prompt(self, request: CodeGenerationRequest, context: str) -> str:
        """Create comprehensive PySpark generation prompt"""
        
        source_schema = request.source_schema
        target_schema = request.target_schema
        mapping_rules = request.mapping_rules
        
        prompt = f"""
        Generate a production-ready PySpark transformation script with the following requirements:
        
        **SOURCE SCHEMA: {source_schema.name}**
        Fields ({len(source_schema.fields)} total):
        {self._format_schema_for_prompt(source_schema)}
        
        **TARGET SCHEMA: {target_schema.name}**
        Fields ({len(target_schema.fields)} total):
        {self._format_schema_for_prompt(target_schema)}
        
        **MAPPING RULES ({len(mapping_rules)} rules):**
        {self._format_mapping_rules_for_prompt(mapping_rules)}
        
        **OPTIMIZATION LEVEL:** {request.optimization_level}
        
        **CONTEXT & PATTERNS:**
        {context[:800]}
        
        **REQUIREMENTS:**
        1. Complete PySpark script with all necessary imports
        2. Proper SparkSession configuration with optimization settings
        3. Data loading with schema enforcement and validation
        4. All mapping transformations with proper data type handling
        5. Advanced error handling with logging and monitoring
        6. Performance optimizations based on optimization level
        7. Data quality checks and validation
        8. Memory management and caching where appropriate
        9. Comprehensive comments explaining complex operations
        10. Save results with proper partitioning and compression
        
        **OPTIMIZATION REQUIREMENTS:**
        {self._get_optimization_requirements(request.optimization_level)}
        
        **OUTPUT FORMAT:**
        Generate ONLY the Python code with detailed comments. 
        Make it production-ready with proper error handling, logging, and performance optimizations.
        """
        
        return prompt
    
    def _format_schema_for_prompt(self, schema: SchemaDefinition) -> str:
        """Format schema for prompt"""
        field_lines = []
        for field in schema.fields[:10]:  # Limit to avoid token overflow
            field_lines.append(f"  - {field.name}: {field.data_type.value} ({'nullable' if field.is_nullable else 'required'})")
            if field.description:
                field_lines.append(f"    Description: {field.description[:100]}")
        
        if len(schema.fields) > 10:
            field_lines.append(f"  ... and {len(schema.fields) - 10} more fields")
        
        return "\n".join(field_lines)
    
    def _format_mapping_rules_for_prompt(self, mapping_rules: List[MappingRule]) -> str:
        """Format mapping rules for prompt"""
        rule_lines = []
        for rule in mapping_rules[:15]:  # Limit to avoid overflow
            transformation = f" -> {rule.transformation}" if rule.transformation else ""
            rule_lines.append(f"  - {rule.source_field} -> {rule.target_field}{transformation}")
            if rule.description:
                rule_lines.append(f"    Note: {rule.description}")
        
        if len(mapping_rules) > 15:
            rule_lines.append(f"  ... and {len(mapping_rules) - 15} more rules")
        
        return "\n".join(rule_lines)
    
    def _get_optimization_requirements(self, level: str) -> str:
        """Get optimization requirements based on level"""
        if level == "basic":
            return """
            - Basic DataFrame operations
            - Simple caching for reused DataFrames
            - Standard error handling
            """
        elif level == "standard":
            return """
            - Efficient DataFrame operations with proper column selection
            - Strategic caching and checkpointing
            - Partitioning optimization for joins
            - Adaptive query execution settings
            - Memory management for large datasets
            """
        else:  # advanced
            return """
            - Advanced optimization patterns (broadcast joins, bucketing)
            - Custom partitioning strategies
            - Memory management with spill detection
            - Catalyst optimizer hints and advanced settings
            - Performance monitoring and metrics collection
            - Resource allocation optimization
            """
    
    def _extract_and_clean_code(self, response: str) -> str:
        """Extract and clean code from AI response"""
        import re
        
        # Look for code blocks
        code_blocks = re.findall(r'```(?:python|pyspark)?\n?(.*?)\n?```', response, re.DOTALL)
        
        if code_blocks:
            return code_blocks[0].strip()
        
        # If no code blocks, try to extract Python-like content
        lines = response.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            # Skip explanation lines at the start
            if not in_code and any(line.strip().startswith(prefix) for prefix in 
                                 ['Here', 'This', 'The following', 'I', 'Let', 'Now', 'First']):
                continue
            
            # Start of code detection
            if any(keyword in line for keyword in ['import', 'from', 'def', 'class', 'if __name__']):
                in_code = True
            
            if in_code:
                code_lines.append(line)
        
        return '\n'.join(code_lines).strip()
    
    async def _ai_optimize_pyspark_code(self, code: str, optimization_level: str) -> str:
        """AI-powered PySpark code optimization"""
        
        if optimization_level == "basic":
            return code  # No additional optimization needed
        
        try:
            optimization_prompt = f"""
            Optimize this PySpark code for {optimization_level} performance:
            
            ```python
            {code}
            ```
            
            Apply these optimizations:
            {self._get_optimization_requirements(optimization_level)}
            
            Return ONLY the optimized Python code with improvement comments.
            Focus on performance, memory efficiency, and scalability.
            """
            
            messages = [
                {
                    "role": "system", 
                    "content": "You are a PySpark performance optimization expert."
                },
                {
                    "role": "user",
                    "content": optimization_prompt
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=3000)
            optimized = self._extract_and_clean_code(response["content"])
            
            if len(optimized) > 100:  # Sanity check
                return optimized
            else:
                return code  # Fallback to original if optimization failed
                
        except Exception as e:
            self.logger.warning("AI optimization failed", error=str(e))
            return code
    
    async def _extract_dependencies_ai(self, code: str, language: str) -> List[str]:
        """AI-powered dependency extraction"""
        try:
            messages = [
                {
                    "role": "system",
                    "content": f"Extract all dependencies needed for this {language} code. Return ONLY a JSON list of package names."
                },
                {
                    "role": "user",
                    "content": f"Code:\n```python\n{code[:1000]}\n```\n\nList all required packages:"
                }
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=200)
            
            try:
                deps = json.loads(response["content"])
                if isinstance(deps, list):
                    return deps
            except json.JSONDecodeError:
                pass
                
        except Exception as e:
            self.logger.warning("AI dependency extraction failed", error=str(e))
        
        # Fallback to pattern-based extraction
        return self._extract_dependencies_pattern(code, language)
    
    def _extract_dependencies_pattern(self, code: str, language: str) -> List[str]:
        """Pattern-based dependency extraction"""
        dependencies = []
        
        if language == "pyspark":
            base_deps = ["pyspark>=3.5.0", "py4j", "pandas", "numpy"]
            dependencies.extend(base_deps)
            
            # Check for specific imports
            if "from pyspark.sql.functions import" in code:
                dependencies.append("pyspark.sql.functions")
            if "from pyspark.ml" in code:
                dependencies.append("pyspark.ml")
            if "import logging" in code:
                dependencies.append("logging")
                
        return list(set(dependencies))
    
    async def _generate_pyspark_fallback(self, request: CodeGenerationRequest) -> GeneratedCode:
        """Fallback PySpark generation"""
        # Simple template-based generation
        code = f"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import logging

# Initialize Spark Session
spark = SparkSession.builder \\
    .appName("{request.source_schema.name}_to_{request.target_schema.name}") \\
    .config("spark.sql.adaptive.enabled", "true") \\
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("INFO")
logger = logging.getLogger(__name__)

try:
    # Load source data
    source_df = spark.read.parquet("input_path")
    
    # Apply transformations
    transformed_df = source_df.select(
        # Add your transformations here
        col("*")
    )
    
    # Save results
    transformed_df.write.mode("overwrite").parquet("output_path")
    
    logger.info("Transformation completed successfully")
    
except Exception as e:
    logger.error(f"Transformation failed: {{e}}")
    raise
finally:
    spark.stop()
"""
        
        return GeneratedCode(
            code=code,
            language="python",
            dependencies=["pyspark>=3.5.0", "py4j"],
            performance_notes="Basic PySpark template - requires customization"
        )
    
    async def _generate_sql_enhanced(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate enhanced SQL code"""
        
        prompt = f"""
        Generate optimized SQL transformation queries for:
        
        SOURCE: {request.source_schema.name}
        TARGET: {request.target_schema.name}
        MAPPINGS: {len(request.mapping_rules)} rules
        
        Context: {context[:500]}
        
        Create:
        1. DDL for target tables with proper constraints
        2. Optimized transformation queries with CTEs
        3. Data quality validation queries
        4. Performance optimization hints
        5. Error handling procedures
        
        Focus on performance, readability, and maintainability.
        """
        
        messages = [
            {"role": "system", "content": "You are a SQL optimization expert."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_provider.generate(messages, max_tokens=2000)
            code = self._extract_and_clean_code(response["content"])
            
            return GeneratedCode(
                code=code,
                language="sql",
                dependencies=["SQL Database Engine"],
                performance_notes="Optimized SQL with performance hints"
            )
            
        except Exception as e:
            self.logger.error("SQL generation failed", error=str(e))
            return GeneratedCode(
                code="-- SQL generation failed",
                language="sql",
                dependencies=[],
                performance_notes="Generation failed"
            )
    
    async def _generate_python_enhanced(
        self, 
        request: CodeGenerationRequest, 
        context: str
    ) -> GeneratedCode:
        """Generate enhanced Python code"""
        
        prompt = f"""
        Generate optimized Python data transformation code using pandas:
        
        SOURCE: {request.source_schema.name}
        TARGET: {request.target_schema.name}
        MAPPINGS: {len(request.mapping_rules)} transformations
        
        Context: {context[:500]}
        
        Requirements:
        1. Efficient pandas operations
        2. Memory optimization for large datasets
        3. Type hints and documentation
        4. Error handling and validation
        5. Progress monitoring
        6. Modular, reusable functions
        
        Generate clean, maintainable Python code.
        """
        
        messages = [
            {"role": "system", "content": "You are a Python data processing expert."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = await self.llm_provider.generate(messages, max_tokens=2000)
            code = self._extract_and_clean_code(response["content"])
            dependencies = await self._extract_dependencies_ai(code, "python")
            
            return GeneratedCode(
                code=code,
                language="python",
                dependencies=dependencies,
                performance_notes="Optimized pandas operations"
            )
            
        except Exception as e:
            self.logger.error("Python generation failed", error=str(e))
            return GeneratedCode(
                code="# Python generation failed",
                language="python", 
                dependencies=["pandas", "numpy"],
                performance_notes="Generation failed"
            )
    
    async def _generate_comprehensive_tests(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate comprehensive test suite"""
        
        test_prompt = f"""
        Generate comprehensive unit tests for this {generated_code.language} transformation code:
        
        Generated Code:
        ```{generated_code.language}
        {generated_code.code[:1500]}
        ```
        
        Requirements:
        1. Test all transformation functions
        2. Test edge cases and error conditions
        3. Test data quality validations
        4. Performance tests for large datasets
        5. Mock data generation for testing
        6. Integration test scenarios
        
        Use pytest framework with fixtures and parametrized tests.
        Generate comprehensive, maintainable test code.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a test automation expert."},
                {"role": "user", "content": test_prompt}
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=2000)
            return self._extract_and_clean_code(response["content"])
            
        except Exception as e:
            self.logger.warning("Test generation failed", error=str(e))
            return "# Test generation failed - please add tests manually"
    
    async def _generate_enhanced_documentation(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode,
        context: str
    ) -> str:
        """Generate enhanced documentation"""
        
        doc_prompt = f"""
        Generate comprehensive documentation for this data transformation code:
        
        Code Type: {generated_code.language}
        Source: {request.source_schema.name} 
        Target: {request.target_schema.name}
        Optimization Level: {request.optimization_level}
        
        Code Preview:
        {generated_code.code[:500]}...
        
        Create documentation including:
        1. Overview and purpose
        2. Prerequisites and setup
        3. Configuration options
        4. Usage examples
        5. Performance considerations
        6. Troubleshooting guide
        7. Maintenance notes
        
        Format as markdown with clear sections.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a technical documentation expert."},
                {"role": "user", "content": doc_prompt}
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=1500)
            return response["content"]
            
        except Exception as e:
            self.logger.warning("Documentation generation failed", error=str(e))
            return "# Documentation generation failed"
    
    async def _analyze_code_performance(
        self, 
        generated_code: GeneratedCode, 
        request: CodeGenerationRequest
    ) -> str:
        """Analyze code performance characteristics"""
        
        analysis_prompt = f"""
        Analyze the performance characteristics of this {generated_code.language} code:
        
        {generated_code.code[:800]}
        
        Provide analysis on:
        1. Time complexity and scalability
        2. Memory usage patterns
        3. I/O efficiency
        4. Optimization opportunities
        5. Potential bottlenecks
        6. Resource requirements
        
        Keep analysis concise and actionable.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a performance analysis expert."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            response = await self.llm_provider.generate(messages, max_tokens=500)
            return response["content"]
            
        except Exception as e:
            self.logger.warning("Performance analysis failed", error=str(e))
            return "Performance analysis not available"


# Factory function for easy creation
def create_enhanced_code_generator(
    enable_multi_provider: bool = None,
    rag_engine=None,
    **kwargs
) -> EnhancedCodeGenerator:
    """Create enhanced code generator with smart defaults"""
    
    config = create_enhanced_agent(
        agent_type="code_generator",
        name="Enhanced Code Generator v2",
        description="Production-ready code generator with LangChain + LiteLLM", 
        enable_multi_provider=enable_multi_provider,
        primary_model="gpt-4",  # Best for code generation
        fallback_models=["claude-3-sonnet", "gpt-3.5-turbo"],
        temperature=0.1,  # Low temperature for consistent code
        max_tokens=3000,  # Higher limit for code generation
        **kwargs
    )
    
    return EnhancedCodeGenerator(config, rag_engine)