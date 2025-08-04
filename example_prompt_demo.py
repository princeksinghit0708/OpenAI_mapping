"""
Demonstration: How GPT-4 Prompt Engineering Handles Complex Mappings
This shows the actual prompt generated for your ACCT_DLY example
"""

# Example mapping from your data
complex_mapping = {
    "staging_table": "ACCT_DLY",
    "column_name": "LAST_PYMT_DT",
    "data_type": "String",
    "source_table": "im_s061_static_dly\nim_dynamic_dly",
    "source_column": "d_date_last_stmt\nn_rate_ptr\nv_hifi_indicator",
    "mapping_type": "Derived",
    "transformation_logic": """if
im_dynamic_dly_HIFI-INDICATOR>0 or im_dynamic_dly-RATE-PTR>0 then CM-IMPMSTR2-DATE-LAST-STMT else null"""
}

# Context enrichment from FAISS and metadata
context = {
    "data_volume": "10M+ records daily",
    "table_metadata": {
        "im_dynamic_dly": {
            "columns": [
                {"name": "v_hifi_indicator", "type": "integer"},
                {"name": "n_rate_ptr", "type": "integer"}
            ]
        }
    },
    "similar_patterns": [
        {
            "column_name": "EFFECTIVE_DT",
            "transformation_logic": "case when indicator > 0 then date_col else null",
            "pyspark_code": "when(col('indicator') > 0, col('date_col')).otherwise(lit(None))"
        }
    ]
}

# The actual prompt that gets generated
generated_prompt = f"""You are an expert PySpark developer. Generate production-ready, optimized PySpark code for the given data mapping.

**MAPPING DETAILS:**
- Table: ACCT_DLY
- Column: LAST_PYMT_DT (String)
- Type: Derived mapping
- Source Tables: im_s061_static_dly, im_dynamic_dly
- Source Columns: d_date_last_stmt, n_rate_ptr, v_hifi_indicator
- Transformation Logic: if im_dynamic_dly_HIFI-INDICATOR>0 or im_dynamic_dly-RATE-PTR>0 then CM-IMPMSTR2-DATE-LAST-STMT else null

**CONTEXT:**
- Environment: Production Spark cluster
- Expected data volume: 10M+ records daily
- Table Metadata Available: Yes (column types known)

**SIMILAR PATTERN FOUND:**
A similar conditional date transformation was implemented:
```python
when(col('indicator') > 0, col('date_col')).otherwise(lit(None))
```

**CODE REQUIREMENTS:**

1. **TRANSFORMATION FUNCTION**
Generate a complete PySpark transformation function that:
- Implements the conditional logic: if HIFI_INDICATOR > 0 OR RATE_PTR > 0
- Handles joins between im_s061_static_dly and im_dynamic_dly tables
- Returns d_date_last_stmt when condition is true, null otherwise
- Includes proper null handling for all source columns
- Optimizes the join operation for 10M+ daily records

2. **SPECIFIC REQUIREMENTS FOR THIS MAPPING:**
- Handle the multi-table join efficiently
- Ensure date format consistency
- Add data quality checks for the indicator columns
- Use broadcast join if reference data is small
- Include logging for debugging

3. **OUTPUT FORMAT:**
```python
def transform_ACCT_DLY_LAST_PYMT_DT(staging_df, im_s061_df, im_dynamic_df):
    '''
    Transform LAST_PYMT_DT for ACCT_DLY table
    
    Business Logic: Set payment date based on HIFI indicator or rate pointer
    
    Args:
        staging_df: Main staging DataFrame
        im_s061_df: Static daily data with d_date_last_stmt
        im_dynamic_df: Dynamic daily data with indicators
    
    Returns:
        DataFrame with LAST_PYMT_DT column added
    '''
    # Your optimized implementation here
```

Generate the complete, production-ready PySpark code:"""

print("GENERATED PROMPT:")
print("=" * 80)
print(generated_prompt)
print("=" * 80)

# What GPT-4 would generate based on this prompt:
expected_output = '''
def transform_ACCT_DLY_LAST_PYMT_DT(staging_df, im_s061_df, im_dynamic_df):
    """
    Transform LAST_PYMT_DT for ACCT_DLY table
    
    Business Logic: Set payment date based on HIFI indicator or rate pointer
    
    Args:
        staging_df: Main staging DataFrame  
        im_s061_df: Static daily data with d_date_last_stmt
        im_dynamic_df: Dynamic daily data with indicators
    
    Returns:
        DataFrame with LAST_PYMT_DT column added
    """
    from pyspark.sql.functions import col, when, lit, coalesce, trim
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("Starting LAST_PYMT_DT transformation")
    
    try:
        # Step 1: Data quality checks
        logger.info("Performing data quality checks")
        
        # Check for required columns
        required_cols_dynamic = ['v_hifi_indicator', 'n_rate_ptr']
        required_cols_static = ['d_date_last_stmt']
        
        for col_name in required_cols_dynamic:
            if col_name not in im_dynamic_df.columns:
                raise ValueError(f"Missing required column: {col_name} in im_dynamic_df")
                
        for col_name in required_cols_static:
            if col_name not in im_s061_df.columns:
                raise ValueError(f"Missing required column: {col_name} in im_s061_df")
        
        # Step 2: Optimize small table for broadcast
        dynamic_count = im_dynamic_df.count()
        static_count = im_s061_df.count()
        
        logger.info(f"Dynamic table size: {dynamic_count}, Static table size: {static_count}")
        
        # Step 3: Join strategy based on data volume
        if dynamic_count < 1000000:  # If less than 1M records, broadcast
            im_dynamic_df = im_dynamic_df.hint("broadcast")
            logger.info("Using broadcast join for im_dynamic_df")
            
        # Step 4: Perform joins and transformation
        result_df = staging_df \
            .join(im_dynamic_df, staging_df.account_id == im_dynamic_df.account_id, "left") \
            .join(im_s061_df, staging_df.account_id == im_s061_df.account_id, "left") \
            .withColumn(
                "LAST_PYMT_DT",
                when(
                    (coalesce(col("v_hifi_indicator"), lit(0)) > 0) | 
                    (coalesce(col("n_rate_ptr"), lit(0)) > 0),
                    trim(col("d_date_last_stmt"))
                ).otherwise(lit(None))
            )
        
        # Step 5: Clean up - drop intermediate columns
        cols_to_drop = ['v_hifi_indicator', 'n_rate_ptr', 'd_date_last_stmt']
        result_df = result_df.drop(*cols_to_drop)
        
        # Step 6: Data quality validation
        null_count = result_df.filter(col("LAST_PYMT_DT").isNull()).count()
        total_count = result_df.count()
        
        logger.info(f"Transformation complete. Null percentage: {(null_count/total_count)*100:.2f}%")
        
        return result_df
        
    except Exception as e:
        logger.error(f"Error in LAST_PYMT_DT transformation: {str(e)}")
        raise
'''

print("\nEXPECTED GPT-4 OUTPUT:")
print("=" * 80)
print(expected_output)
print("=" * 80)

# Key features of the prompt engineering:
print("\n🔑 KEY PROMPT ENGINEERING FEATURES:")
print("""
1. **Context Awareness**: Includes table metadata and data volumes
2. **Pattern Matching**: Shows similar transformations for learning
3. **Specific Requirements**: Addresses exact business logic
4. **Performance Hints**: Suggests optimization strategies
5. **Error Handling**: Requires comprehensive error management
6. **Documentation**: Enforces clear code documentation
7. **Best Practices**: Embeds Spark optimization techniques
""") 