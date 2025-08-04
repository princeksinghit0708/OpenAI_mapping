"""
PySpark Code Generation Template
This template provides a comprehensive structure for generating PySpark transformation code
"""

PYSPARK_TEMPLATE = """
#!/usr/bin/env python3
'''
Generated PySpark Transformation Script
Source Schema: {source_schema_name}
Target Schema: {target_schema_name}
Generated: {timestamp}
Optimization Level: {optimization_level}
'''

import sys
import logging
from datetime import datetime
from typing import Dict, Any, List
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *
import pyspark.sql.functions as F

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformation:
    '''Main transformation class for {source_schema_name} to {target_schema_name}'''
    
    def __init__(self, spark_session: SparkSession = None):
        self.spark = spark_session or self._create_spark_session()
        self.source_schema = self._get_source_schema()
        self.target_schema = self._get_target_schema()
        
    def _create_spark_session(self) -> SparkSession:
        '''Create optimized Spark session'''
        builder = SparkSession.builder \\
            .appName("{source_schema_name}_to_{target_schema_name}_transformation") \\
            .config("spark.sql.adaptive.enabled", "true") \\
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        
        {optimization_configs}
        
        return builder.getOrCreate()
    
    def _get_source_schema(self) -> StructType:
        '''Define source schema structure'''
        return StructType([
            {source_schema_fields}
        ])
    
    def _get_target_schema(self) -> StructType:
        '''Define target schema structure'''
        return StructType([
            {target_schema_fields}
        ])
    
    def load_source_data(self, source_path: str) -> DataFrame:
        '''Load source data with validation'''
        try:
            logger.info(f"Loading source data from: {{source_path}}")
            
            # Load data with schema enforcement
            df = self.spark.read \\
                .schema(self.source_schema) \\
                .option("multiline", "true") \\
                .json(source_path)
            
            # Data quality checks
            self._validate_source_data(df)
            
            logger.info(f"Successfully loaded {{df.count()}} records")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load source data: {{str(e)}}")
            raise
    
    def _validate_source_data(self, df: DataFrame) -> None:
        '''Validate source data quality'''
        # Check for empty dataset
        if df.count() == 0:
            raise ValueError("Source dataset is empty")
        
        # Check required fields
        required_fields = {required_fields}
        missing_fields = set(required_fields) - set(df.columns)
        if missing_fields:
            raise ValueError(f"Missing required fields: {{missing_fields}}")
        
        # Check for null values in critical fields
        critical_fields = {critical_fields}
        for field in critical_fields:
            if field in df.columns:
                null_count = df.filter(col(field).isNull()).count()
                if null_count > 0:
                    logger.warning(f"Field '{{field}}' has {{null_count}} null values")
    
    def transform_data(self, source_df: DataFrame) -> DataFrame:
        '''Apply all transformations'''
        try:
            logger.info("Starting data transformation")
            
            # Apply transformations step by step
            df = source_df.alias("source")
            
            {transformation_steps}
            
            # Final validation
            self._validate_transformed_data(df)
            
            logger.info("Data transformation completed successfully")
            return df
            
        except Exception as e:
            logger.error(f"Data transformation failed: {{str(e)}}")
            raise
    
    {transformation_methods}
    
    def _validate_transformed_data(self, df: DataFrame) -> None:
        '''Validate transformed data'''
        # Check schema compliance
        expected_columns = set([field.name for field in self.target_schema.fields])
        actual_columns = set(df.columns)
        
        missing_columns = expected_columns - actual_columns
        extra_columns = actual_columns - expected_columns
        
        if missing_columns:
            raise ValueError(f"Missing target columns: {{missing_columns}}")
        
        if extra_columns:
            logger.warning(f"Extra columns in result: {{extra_columns}}")
        
        logger.info("Data validation completed successfully")
    
    def save_transformed_data(self, df: DataFrame, output_path: str) -> None:
        '''Save transformed data with optimization'''
        try:
            logger.info(f"Saving transformed data to: {{output_path}}")
            
            # Apply final optimizations
            {save_optimizations}
            
            # Save data
            df.write \\
                .mode("overwrite") \\
                .option("compression", "snappy") \\
                .parquet(output_path)
            
            logger.info("Data saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save data: {{str(e)}}")
            raise
    
    def run_transformation(self, source_path: str, output_path: str) -> Dict[str, Any]:
        '''Run complete transformation pipeline'''
        start_time = datetime.now()
        
        try:
            # Load source data
            source_df = self.load_source_data(source_path)
            
            # Transform data
            transformed_df = self.transform_data(source_df)
            
            # Save results
            self.save_transformed_data(transformed_df, output_path)
            
            # Generate metrics
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            metrics = {{
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration,
                "source_record_count": source_df.count(),
                "target_record_count": transformed_df.count(),
                "success": True
            }}
            
            logger.info(f"Transformation completed successfully in {{duration:.2f}} seconds")
            return metrics
            
        except Exception as e:
            error_metrics = {{
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "error": str(e),
                "success": False
            }}
            
            logger.error(f"Transformation failed: {{str(e)}}")
            return error_metrics
        
        finally:
            # Cleanup
            if hasattr(self, 'spark'):
                self.spark.stop()


def main():
    '''Main execution function'''
    if len(sys.argv) != 3:
        print("Usage: python transformation_script.py <source_path> <output_path>")
        sys.exit(1)
    
    source_path = sys.argv[1]
    output_path = sys.argv[2]
    
    # Run transformation
    transformer = DataTransformation()
    metrics = transformer.run_transformation(source_path, output_path)
    
    print("Transformation Metrics:")
    for key, value in metrics.items():
        print(f"  {{key}}: {{value}}")
    
    if not metrics.get("success", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
"""

# Template variables and their descriptions
TEMPLATE_VARIABLES = {
    "source_schema_name": "Name of the source schema",
    "target_schema_name": "Name of the target schema", 
    "timestamp": "Generation timestamp",
    "optimization_level": "Code optimization level (basic/standard/advanced)",
    "optimization_configs": "Spark configuration optimizations",
    "source_schema_fields": "Source schema field definitions",
    "target_schema_fields": "Target schema field definitions", 
    "required_fields": "List of required field names",
    "critical_fields": "List of critical field names that cannot be null",
    "transformation_steps": "Step-by-step transformation logic",
    "transformation_methods": "Individual transformation method definitions",
    "save_optimizations": "Data saving optimizations"
}

# Optimization configurations by level
OPTIMIZATION_CONFIGS = {
    "basic": """
        # Basic optimizations
        .config("spark.sql.adaptive.coalescePartitions.minPartitionNum", "1")
    """,
    
    "standard": """
        # Standard optimizations
        .config("spark.sql.adaptive.coalescePartitions.minPartitionNum", "1") \\
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \\
        .config("spark.sql.adaptive.localShuffleReader.enabled", "true")
    """,
    
    "advanced": """
        # Advanced optimizations
        .config("spark.sql.adaptive.coalescePartitions.minPartitionNum", "1") \\
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \\
        .config("spark.sql.adaptive.localShuffleReader.enabled", "true") \\
        .config("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB") \\
        .config("spark.sql.adaptive.advisoryPartitionSizeInBytes", "128MB") \\
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \\
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
    """
}