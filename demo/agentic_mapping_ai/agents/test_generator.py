"""
Test Generation Agent - Specialized agent for generating comprehensive test suites
"""

import json
from typing import Any, Dict, List, Optional
from loguru import logger

from agents.base_agent import BaseAgent, AgentConfig, AgentFactory
from core.models import (
    AgentType, SchemaDefinition, MappingRule, 
    GeneratedCode, CodeGenerationRequest, ValidationResult
)


class TestGeneratorAgent(BaseAgent):
    """
    Agent specialized in generating comprehensive test suites for data transformations
    
    Capabilities:
    - Generate unit tests for PySpark transformations
    - Create integration test scenarios
    - Generate data quality validation tests
    - Create performance benchmark tests
    - Generate mock data for testing
    - Create test documentation and reports
    """
    
    def _get_system_prompt(self) -> str:
        return """
        You are a Test Generation Agent specialized in creating comprehensive test suites for data transformation code.
        
        Your expertise includes:
        1. Unit testing for PySpark DataFrame operations
        2. Integration testing for end-to-end data pipelines
        3. Data quality validation testing
        4. Performance and load testing scenarios
        5. Mock data generation for realistic testing
        6. Edge case and boundary condition testing
        7. Error handling and exception testing
        8. Test automation and CI/CD integration
        
        Test generation principles:
        - Generate comprehensive test coverage (>90%)
        - Include positive and negative test scenarios
        - Create realistic mock data for testing
        - Test all transformation business logic
        - Include performance benchmarks
        - Add data quality assertions
        - Generate maintainable and readable tests
        - Follow pytest best practices
        - Include proper test documentation
        
        Always ensure tests are:
        - Isolated and independent
        - Deterministic and repeatable
        - Fast and efficient
        - Clear and well-documented
        - Comprehensive in coverage
        """
    
    def get_agent_type(self) -> AgentType:
        return AgentType.TEST_GENERATOR
    
    async def _execute_core_logic(
        self, 
        input_data: Dict[str, Any], 
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Execute test generation logic
        
        Args:
            input_data: Should contain code_generation_request and generated_code
            context: RAG context for test patterns
            
        Returns:
            Test generation results
        """
        try:
            request_data = input_data.get("code_generation_request", {})
            generated_code_data = input_data.get("generated_code", {})
            test_type = input_data.get("test_type", "comprehensive")
            
            # Parse the request
            if isinstance(request_data, dict):
                code_request = CodeGenerationRequest(**request_data)
            else:
                code_request = request_data
            
            if isinstance(generated_code_data, dict):
                generated_code = GeneratedCode(**generated_code_data)
            else:
                generated_code = generated_code_data
            
            logger.info(f"Generating {test_type} tests for {generated_code.language} code")
            
            # Generate different types of tests based on request
            test_results = {}
            
            if test_type in ["comprehensive", "unit"]:
                test_results["unit_tests"] = await self._generate_unit_tests(
                    code_request, generated_code, context
                )
            
            if test_type in ["comprehensive", "integration"]:
                test_results["integration_tests"] = await self._generate_integration_tests(
                    code_request, generated_code, context
                )
            
            if test_type in ["comprehensive", "performance"]:
                test_results["performance_tests"] = await self._generate_performance_tests(
                    code_request, generated_code, context
                )
            
            if test_type in ["comprehensive", "data_quality"]:
                test_results["data_quality_tests"] = await self._generate_data_quality_tests(
                    code_request, generated_code, context
                )
            
            # Generate mock data
            test_results["mock_data"] = await self._generate_mock_data(
                code_request, generated_code, context
            )
            
            # Generate test documentation
            test_results["test_documentation"] = await self._generate_test_documentation(
                code_request, test_results
            )
            
            return {
                "success": True,
                "test_results": test_results,
                "test_type": test_type,
                "coverage_estimate": self._estimate_coverage(test_results),
                "message": f"Successfully generated {test_type} test suite"
            }
            
        except Exception as e:
            logger.error(f"Test generation failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Test generation failed"
            }
    
    async def _generate_unit_tests(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate comprehensive unit tests"""
        
        unit_test_prompt = f"""
        Generate comprehensive unit tests for this {generated_code.language} transformation code:
        
        GENERATED CODE:
        ```{generated_code.language}
        {generated_code.code}
        ```
        
        SOURCE SCHEMA: {request.source_schema.name}
        TARGET SCHEMA: {request.target_schema.name}
        
        MAPPING RULES: {len(request.mapping_rules)} rules defined
        
        Generate unit tests that cover:
        1. **Data Loading Tests**:
           - Test successful data loading from various sources
           - Test handling of missing or corrupted data
           - Test schema validation on input data
        
        2. **Transformation Logic Tests**:
           - Test each mapping rule individually
           - Test data type conversions
           - Test null value handling
           - Test business logic calculations
        
        3. **Data Validation Tests**:
           - Test output schema compliance
           - Test data quality constraints
           - Test referential integrity
        
        4. **Edge Case Tests**:
           - Test empty datasets
           - Test single row datasets
           - Test large datasets (performance)
           - Test malformed input data
        
        5. **Error Handling Tests**:
           - Test exception scenarios
           - Test recovery mechanisms
           - Test error logging
        
        Use pytest framework with:
        - Proper fixtures for test data
        - Parametrized tests for multiple scenarios
        - Clear test naming conventions
        - Comprehensive assertions
        - Setup and teardown methods
        
        Generate ONLY the test code with proper imports and structure.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a test automation expert specializing in data transformation testing."},
                {"role": "user", "content": unit_test_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=3000,
                llm_provider="azure"
            )
            
            return self._clean_test_code(response)
            
        except Exception as e:
            logger.warning(f"Unit test generation failed: {str(e)}")
            return "# Unit test generation failed - please add tests manually"
    
    async def _generate_integration_tests(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate integration tests for end-to-end scenarios"""
        
        integration_test_prompt = f"""
        Generate integration tests for this data transformation pipeline:
        
        CODE: {generated_code.code[:1000]}...
        
        Create integration tests that verify:
        1. **End-to-End Pipeline Tests**:
           - Full data flow from source to target
           - Multi-stage transformation pipelines
           - Data persistence and retrieval
        
        2. **System Integration Tests**:
           - Database connectivity tests
           - File system integration tests
           - External service integration
        
        3. **Data Pipeline Tests**:
           - Batch processing scenarios
           - Streaming data scenarios
           - Error recovery and retry logic
        
        4. **Environment Tests**:
           - Different data volumes
           - Different cluster configurations
           - Resource utilization tests
        
        Use pytest with realistic test scenarios and proper test isolation.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are an integration testing specialist."},
                {"role": "user", "content": integration_test_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=2000,
                llm_provider="azure"
            )
            
            return self._clean_test_code(response)
            
        except Exception as e:
            logger.warning(f"Integration test generation failed: {str(e)}")
            return "# Integration test generation failed"
    
    async def _generate_performance_tests(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate performance and load tests"""
        
        performance_test_prompt = f"""
        Generate performance tests for this data transformation:
        
        CODE: {generated_code.code[:800]}...
        
        Create performance tests that measure:
        1. **Execution Time Benchmarks**:
           - Small dataset (1K rows)
           - Medium dataset (100K rows)  
           - Large dataset (10M+ rows)
        
        2. **Memory Usage Tests**:
           - Memory consumption monitoring
           - Memory leak detection
           - Garbage collection impact
        
        3. **Scalability Tests**:
           - Linear scaling verification
           - Cluster resource utilization
           - Bottleneck identification
        
        4. **Optimization Tests**:
           - Cache effectiveness
           - Partition optimization
           - Query optimization
        
        Use pytest-benchmark and include performance thresholds.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a performance testing expert."},
                {"role": "user", "content": performance_test_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=2000,
                llm_provider="azure"
            )
            
            return self._clean_test_code(response)
            
        except Exception as e:
            logger.warning(f"Performance test generation failed: {str(e)}")
            return "# Performance test generation failed"
    
    async def _generate_data_quality_tests(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate data quality validation tests"""
        
        data_quality_prompt = f"""
        Generate data quality tests for this transformation:
        
        SOURCE SCHEMA: {request.source_schema.dict()}
        TARGET SCHEMA: {request.target_schema.dict()}
        
        Create data quality tests that verify:
        1. **Data Completeness**:
           - No missing required fields
           - Expected record counts
           - Data freshness checks
        
        2. **Data Accuracy**:
           - Business rule compliance
           - Calculation accuracy
           - Reference data validation
        
        3. **Data Consistency**:
           - Cross-field validations
           - Referential integrity
           - Format consistency
        
        4. **Data Validity**:
           - Data type validation
           - Range and constraint checks
           - Pattern matching validation
        
        Include specific assertions for banking data quality requirements.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a data quality specialist."},
                {"role": "user", "content": data_quality_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=2000,
                llm_provider="azure"
            )
            
            return self._clean_test_code(response)
            
        except Exception as e:
            logger.warning(f"Data quality test generation failed: {str(e)}")
            return "# Data quality test generation failed"
    
    async def _generate_mock_data(
        self, 
        request: CodeGenerationRequest, 
        generated_code: GeneratedCode, 
        context: str
    ) -> str:
        """Generate realistic mock data for testing"""
        
        mock_data_prompt = f"""
        Generate realistic mock data generation code for testing:
        
        SOURCE SCHEMA: {request.source_schema.dict()}
        TARGET SCHEMA: {request.target_schema.dict()}
        
        Create mock data generators that produce:
        1. **Realistic Test Data**:
           - Valid business scenarios
           - Representative data distributions
           - Proper data relationships
        
        2. **Edge Case Data**:
           - Boundary value scenarios
           - Null and empty values
           - Invalid data scenarios
        
        3. **Volume Test Data**:
           - Small datasets for unit tests
           - Large datasets for performance tests
           - Streaming data scenarios
        
        Use libraries like Faker, factory_boy for realistic data generation.
        Include both positive and negative test data scenarios.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a test data generation expert."},
                {"role": "user", "content": mock_data_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.2,
                max_tokens=2000,
                llm_provider="azure"
            )
            
            return self._clean_test_code(response)
            
        except Exception as e:
            logger.warning(f"Mock data generation failed: {str(e)}")
            return "# Mock data generation failed"
    
    async def _generate_test_documentation(
        self, 
        request: CodeGenerationRequest, 
        test_results: Dict[str, str]
    ) -> str:
        """Generate comprehensive test documentation"""
        
        doc_prompt = f"""
        Generate comprehensive test documentation for this test suite:
        
        TEST COMPONENTS:
        - Unit Tests: {'✓' if 'unit_tests' in test_results else '✗'}
        - Integration Tests: {'✓' if 'integration_tests' in test_results else '✗'}
        - Performance Tests: {'✓' if 'performance_tests' in test_results else '✗'}
        - Data Quality Tests: {'✓' if 'data_quality_tests' in test_results else '✗'}
        - Mock Data: {'✓' if 'mock_data' in test_results else '✗'}
        
        Create documentation that includes:
        1. **Test Suite Overview**
        2. **Test Categories and Coverage**
        3. **Running the Tests** (commands and setup)
        4. **Test Data Requirements**
        5. **Expected Results and Thresholds**
        6. **Troubleshooting Guide**
        7. **Maintenance Instructions**
        
        Format as markdown documentation.
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a technical documentation specialist."},
                {"role": "user", "content": doc_prompt}
            ]
            
            response = self.llm_service.query_llm(
                model="gpt-4",
                messages=messages,
                temperature=0.1,
                max_tokens=1500,
                llm_provider="azure"
            )
            
            return response
            
        except Exception as e:
            logger.warning(f"Test documentation generation failed: {str(e)}")
            return "# Test documentation generation failed"
    
    def _clean_test_code(self, code: str) -> str:
        """Clean and format test code"""
        # Remove markdown code blocks if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
        
        return code.strip()
    
    def _estimate_coverage(self, test_results: Dict[str, str]) -> int:
        """Estimate test coverage percentage"""
        coverage = 0
        
        if "unit_tests" in test_results:
            coverage += 40
        if "integration_tests" in test_results:
            coverage += 25
        if "performance_tests" in test_results:
            coverage += 15
        if "data_quality_tests" in test_results:
            coverage += 15
        if "mock_data" in test_results:
            coverage += 5
        
        return min(coverage, 95)  # Cap at 95%


# Register the agent
AgentFactory.register_agent(AgentType.TEST_GENERATOR, TestGeneratorAgent)
