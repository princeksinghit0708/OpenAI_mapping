"""
GPT-4 Prompt Engine - Production Ready Prompt Engineering System
Uses advanced prompt engineering techniques for maximum effectiveness
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import tiktoken

class GPT4PromptEngine:
    """Advanced prompt engineering system for GPT-4 based data mapping operations"""
    
    def __init__(self, model="gpt-4", max_tokens=8000):
        self.model = model
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4")
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    # ===== MASTER PROMPTS FOR DIFFERENT OPERATIONS =====
    
    def get_mapping_analyzer_prompt(self, excel_data: Dict) -> str:
        """Generate prompt for analyzing mapping logic from Excel data"""
        return f"""You are an expert data engineer analyzing data mapping requirements. Your task is to provide a comprehensive analysis of the mapping logic.

**CONTEXT:**
I have an Excel file with mapping specifications that includes:
- Sheet 1: Mapping logic with columns (staging_table, column_name, mapping_type, transformation_logic, data_type)
- Sheet 2: Gold reference data for lookups
- Mapping types: derived, derived_goldref, direct, direct_map, no_mapping, blanks

**INPUT DATA:**
{json.dumps(excel_data, indent=2)}

**YOUR TASK:**
Analyze the mapping data and provide a structured response with:

1. **MAPPING SUMMARY**
   - Total mappings by type
   - Complexity assessment
   - Dependencies identified

2. **TRANSFORMATION ANALYSIS**
   For each mapping, identify:
   - Required transformations
   - Data quality concerns
   - Performance considerations

3. **GOLDREF REQUIREMENTS**
   - Which mappings need goldref lookups
   - Join keys and conditions
   - Handling missing references

4. **VALIDATION RULES**
   For each column, suggest:
   - Data type validations
   - Business rule validations
   - Null handling strategy

5. **OPTIMIZATION OPPORTUNITIES**
   - Suggest performance improvements
   - Identify reusable patterns
   - Recommend best practices

Provide your analysis in a structured JSON format for easy parsing."""

    def get_pyspark_generator_prompt(self, mapping_info: Dict, context: Dict) -> str:
        """Generate prompt for PySpark code generation with advanced patterns"""
        return f"""You are an expert PySpark developer. Generate production-ready, optimized PySpark code for the given data mapping.

**MAPPING DETAILS:**
{json.dumps(mapping_info, indent=2)}

**CONTEXT:**
- Environment: Production Spark cluster
- Expected data volume: {context.get('data_volume', 'Large scale')}
- Performance requirements: {context.get('performance', 'Optimized for speed')}
- Error handling: Comprehensive with logging

**CODE REQUIREMENTS:**

1. **TRANSFORMATION FUNCTION**
Generate a complete PySpark transformation function that:
- Handles the {mapping_info.get('mapping_type')} mapping type
- Implements proper error handling
- Includes data quality checks
- Optimizes for performance
- Adds comprehensive logging

2. **BEST PRACTICES TO FOLLOW:**
- Use broadcast joins for small lookup tables
- Implement proper null handling
- Add data validation before transformation
- Use appropriate Spark configurations
- Include clear documentation

3. **OUTPUT FORMAT:**
```python
def transform_{mapping_info.get('staging_table')}_{mapping_info.get('column_name')}(df, goldref_df=None):
    '''
    Production-ready transformation function
    
    Args:
        df: Input DataFrame
        goldref_df: Gold reference DataFrame (optional)
    
    Returns:
        Transformed DataFrame
    '''
    # Your optimized code here
```

4. **INCLUDE:**
- Input validation
- Transformation logic
- Error handling
- Performance optimizations
- Logging statements
- Return transformed DataFrame

Generate the complete, production-ready PySpark code:"""

    def get_test_generator_prompt(self, mapping_info: Dict) -> str:
        """Generate prompt for comprehensive test case generation"""
        return f"""You are a QA expert specializing in data validation. Generate comprehensive test cases for the data mapping validation.

**MAPPING TO TEST:**
{json.dumps(mapping_info, indent=2)}

**TEST REQUIREMENTS:**

1. **POSITIVE TEST CASES** (Valid scenarios)
   - Normal valid data
   - Boundary valid values
   - Different valid formats

2. **NEGATIVE TEST CASES** (Invalid scenarios)
   - Null values (for non-nullable)
   - Invalid data types
   - Out of range values
   - Invalid formats

3. **EDGE CASES**
   - Empty strings
   - Very long strings
   - Special characters
   - Unicode handling
   - Numeric boundaries

4. **PERFORMANCE TESTS**
   - Large dataset handling
   - Memory efficiency
   - Execution time benchmarks

5. **DATA QUALITY TESTS**
   - Completeness checks
   - Uniqueness validation
   - Referential integrity
   - Business rule compliance

**OUTPUT FORMAT:**
Provide test cases in this structure:
```json
{{
  "test_suite": {{
    "mapping_info": {{}},
    "test_cases": [
      {{
        "test_id": "TC001",
        "test_name": "descriptive_name",
        "test_type": "positive|negative|edge|performance",
        "description": "What this tests",
        "input_data": {{}},
        "expected_output": {{}},
        "validation_criteria": "",
        "pyspark_test_code": ""
      }}
    ],
    "test_data_generator": "Python code to generate test data",
    "execution_order": []
  }}
}}
```

Generate comprehensive test cases covering all scenarios:"""

    def get_validation_prompt(self, column_profile: Dict, mapping_info: Dict) -> str:
        """Generate prompt for data validation and quality analysis"""
        return f"""You are a data quality expert. Analyze the data profile and provide comprehensive validation recommendations.

**COLUMN PROFILE:**
{json.dumps(column_profile, indent=2)}

**MAPPING INFORMATION:**
{json.dumps(mapping_info, indent=2)}

**ANALYSIS REQUIRED:**

1. **DATA QUALITY ASSESSMENT**
   - Completeness score
   - Accuracy assessment
   - Consistency check
   - Validity verification
   - Uniqueness analysis

2. **ANOMALY DETECTION**
   - Identify patterns
   - Detect outliers
   - Find inconsistencies
   - Spot data quality issues

3. **VALIDATION RULES**
   Generate PySpark validation code for:
   - Data type validation
   - Range validation
   - Format validation
   - Business rule validation
   - Referential integrity

4. **CLEANSING RECOMMENDATIONS**
   - Null handling strategy
   - Outlier treatment
   - Standardization needs
   - Deduplication approach

5. **MONITORING METRICS**
   - Key quality indicators
   - Threshold definitions
   - Alert conditions
   - Trending metrics

**OUTPUT FORMAT:**
```json
{{
  "quality_score": 0.0-1.0,
  "issues_found": [],
  "validation_rules": [
    {{
      "rule_name": "",
      "description": "",
      "severity": "critical|high|medium|low",
      "pyspark_code": ""
    }}
  ],
  "cleansing_steps": [],
  "monitoring_setup": {{}}
}}
```

Provide comprehensive validation analysis and actionable recommendations:"""

    def get_recommendation_prompt(self, analysis_results: Dict) -> str:
        """Generate prompt for intelligent recommendations"""
        return f"""You are a senior data architect providing expert recommendations for data mapping implementation.

**ANALYSIS RESULTS:**
{json.dumps(analysis_results, indent=2)}

**PROVIDE RECOMMENDATIONS FOR:**

1. **ARCHITECTURE DECISIONS**
   - Optimal processing strategy
   - Resource allocation
   - Parallelization approach
   - Caching strategy

2. **PERFORMANCE OPTIMIZATION**
   - Spark configuration tuning
   - Partition strategy
   - Broadcast vs shuffle joins
   - Memory optimization

3. **DATA QUALITY IMPROVEMENTS**
   - Critical issues to address
   - Quality gates to implement
   - Monitoring requirements
   - SLA definitions

4. **IMPLEMENTATION ROADMAP**
   - Priority order
   - Dependencies
   - Risk mitigation
   - Timeline estimation

5. **BEST PRACTICES**
   - Coding standards
   - Documentation needs
   - Testing strategy
   - Deployment approach

**OUTPUT FORMAT:**
```json
{{
  "executive_summary": "",
  "critical_recommendations": [
    {{
      "priority": 1-5,
      "category": "",
      "recommendation": "",
      "impact": "",
      "effort": "",
      "implementation_steps": []
    }}
  ],
  "optimization_config": {{
    "spark_settings": {{}},
    "processing_strategy": "",
    "resource_allocation": {{}}
  }},
  "risk_assessment": [],
  "success_metrics": []
}}
```

Provide actionable, prioritized recommendations:"""

    def get_code_optimizer_prompt(self, generated_code: str, performance_metrics: Dict) -> str:
        """Generate prompt for code optimization"""
        return f"""You are a PySpark performance expert. Optimize the provided code for production use.

**CURRENT CODE:**
```python
{generated_code}
```

**PERFORMANCE METRICS:**
{json.dumps(performance_metrics, indent=2)}

**OPTIMIZATION GOALS:**
1. Reduce execution time by 30%+
2. Minimize memory usage
3. Improve scalability
4. Enhance error recovery

**OPTIMIZATION TECHNIQUES TO CONSIDER:**
- Predicate pushdown
- Column pruning  
- Broadcast joins for small tables
- Partition optimization
- Cache strategic DataFrames
- Avoid shuffle operations
- Use efficient aggregations
- Optimize UDFs or avoid them

**OUTPUT REQUIREMENTS:**
1. Optimized code with comments explaining changes
2. Performance improvement estimates
3. Trade-offs and considerations
4. Configuration recommendations

Generate the optimized PySpark code:"""

    def get_documentation_prompt(self, project_context: Dict) -> str:
        """Generate prompt for comprehensive documentation"""
        return f"""You are a technical writer creating production-ready documentation for a data mapping system.

**PROJECT CONTEXT:**
{json.dumps(project_context, indent=2)}

**DOCUMENTATION REQUIREMENTS:**

1. **TECHNICAL SPECIFICATION**
   - System architecture
   - Data flow diagrams
   - Component descriptions
   - API documentation

2. **OPERATIONAL GUIDE**
   - Deployment procedures
   - Configuration management
   - Monitoring setup
   - Troubleshooting guide

3. **USER MANUAL**
   - How to add new mappings
   - Running transformations
   - Interpreting results
   - Common use cases

4. **MAINTENANCE GUIDE**
   - Update procedures
   - Performance tuning
   - Backup/recovery
   - Version management

Generate comprehensive documentation in Markdown format:"""

    def create_chain_of_thought_prompt(self, task: str, context: Dict) -> str:
        """Create a chain-of-thought prompt for complex reasoning"""
        return f"""Let's approach this step-by-step.

**TASK:** {task}

**CONTEXT:**
{json.dumps(context, indent=2)}

**REASONING STEPS:**
1. First, let me understand the requirements...
2. Next, I'll identify the key components...
3. Then, I'll design the solution...
4. Finally, I'll implement with best practices...

Please think through this systematically and provide your detailed reasoning followed by the solution."""

    def create_few_shot_prompt(self, task: str, examples: List[Dict]) -> str:
        """Create few-shot learning prompt with examples"""
        examples_text = "\n\n".join([
            f"**Example {i+1}:**\nInput: {ex['input']}\nOutput: {ex['output']}"
            for i, ex in enumerate(examples)
        ])
        
        return f"""Here are some examples of the task:

{examples_text}

**Now, for your task:**
{task}

Following the same pattern as the examples above, provide your solution:"""

    def optimize_prompt_for_tokens(self, prompt: str, max_tokens: int = 4000) -> str:
        """Optimize prompt to fit within token limits"""
        current_tokens = self.count_tokens(prompt)
        
        if current_tokens <= max_tokens:
            return prompt
        
        # Intelligently truncate while preserving structure
        lines = prompt.split('\n')
        optimized_lines = []
        running_tokens = 0
        
        # Priority sections to keep
        priority_markers = ['**TASK**', '**OUTPUT', '**REQUIREMENTS**', '**FORMAT**']
        
        for line in lines:
            line_tokens = self.count_tokens(line)
            if running_tokens + line_tokens > max_tokens:
                if any(marker in line for marker in priority_markers):
                    optimized_lines.append(line)
                    running_tokens += line_tokens
                else:
                    break
            else:
                optimized_lines.append(line)
                running_tokens += line_tokens
        
        return '\n'.join(optimized_lines) 