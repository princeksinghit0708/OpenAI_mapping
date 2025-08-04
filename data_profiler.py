"""
Production-Ready Data Profiler
Analyzes data quality and generates profiles for validation
"""
import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, min as spark_min, 
    max as spark_max, stddev, length, when, isnan, isnull
)
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import re

class DataProfiler:
    """Production-ready data profiler for mapping validation"""
    
    def __init__(self, spark_session: Optional[SparkSession] = None):
        """Initialize profiler with Spark session"""
        if spark_session is None:
            self.spark = SparkSession.builder \
                .appName("DataMappingProfiler") \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                .getOrCreate()
        else:
            self.spark = spark_session
    
    def profile_dataframe(self, df: DataFrame, sample_size: int = 10000) -> Dict[str, Any]:
        """Generate comprehensive profile for entire DataFrame"""
        profile = {
            "timestamp": datetime.now().isoformat(),
            "total_rows": df.count(),
            "total_columns": len(df.columns),
            "columns": {},
            "data_quality_score": 0.0
        }
        
        # Sample for detailed analysis if dataset is large
        if profile["total_rows"] > sample_size:
            sample_df = df.sample(fraction=sample_size/profile["total_rows"])
        else:
            sample_df = df
        
        # Profile each column
        quality_scores = []
        for column in df.columns:
            col_profile = self.profile_column(df, column, sample_df)
            profile["columns"][column] = col_profile
            quality_scores.append(col_profile.get("quality_score", 0))
        
        # Calculate overall quality score
        profile["data_quality_score"] = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return profile
    
    def profile_column(self, df: DataFrame, column_name: str, sample_df: DataFrame = None) -> Dict[str, Any]:
        """Generate detailed profile for a single column"""
        if sample_df is None:
            sample_df = df
        
        # Get data type
        data_type = dict(df.dtypes)[column_name]
        
        # Basic statistics
        stats = self._calculate_basic_stats(df, column_name, data_type)
        
        # Pattern analysis
        patterns = self._analyze_patterns(sample_df, column_name, data_type)
        
        # Quality metrics
        quality_metrics = self._calculate_quality_metrics(stats, patterns)
        
        # Anomalies
        anomalies = self._detect_anomalies(stats, patterns, data_type)
        
        return {
            "column_name": column_name,
            "data_type": data_type,
            "stats": stats,
            "patterns": patterns,
            "quality_metrics": quality_metrics,
            "anomalies": anomalies,
            "quality_score": quality_metrics.get("overall_quality", 0)
        }
    
    def _calculate_basic_stats(self, df: DataFrame, column_name: str, data_type: str) -> Dict[str, Any]:
        """Calculate basic statistics for a column"""
        total_count = df.count()
        
        # Null statistics
        null_count = df.filter(col(column_name).isNull() | isnan(col(column_name))).count()
        
        # Distinct count
        distinct_count = df.select(column_name).distinct().count()
        
        stats = {
            "total_count": total_count,
            "null_count": null_count,
            "null_percentage": (null_count / total_count * 100) if total_count > 0 else 0,
            "distinct_count": distinct_count,
            "distinct_percentage": (distinct_count / total_count * 100) if total_count > 0 else 0,
            "cardinality": "high" if distinct_count > total_count * 0.95 else "medium" if distinct_count > total_count * 0.5 else "low"
        }
        
        # Type-specific statistics
        if data_type in ["int", "bigint", "float", "double", "decimal"]:
            numeric_stats = df.select(
                avg(col(column_name)).alias("mean"),
                spark_min(col(column_name)).alias("min"),
                spark_max(col(column_name)).alias("max"),
                stddev(col(column_name)).alias("std_dev")
            ).collect()[0]
            
            stats.update({
                "mean": float(numeric_stats["mean"]) if numeric_stats["mean"] else None,
                "min": float(numeric_stats["min"]) if numeric_stats["min"] else None,
                "max": float(numeric_stats["max"]) if numeric_stats["max"] else None,
                "std_dev": float(numeric_stats["std_dev"]) if numeric_stats["std_dev"] else None
            })
            
        elif data_type == "string":
            string_stats = df.select(
                avg(length(col(column_name))).alias("avg_length"),
                spark_min(length(col(column_name))).alias("min_length"),
                spark_max(length(col(column_name))).alias("max_length")
            ).filter(col(column_name).isNotNull()).collect()
            
            if string_stats:
                stats.update({
                    "avg_length": float(string_stats[0]["avg_length"]) if string_stats[0]["avg_length"] else 0,
                    "min_length": int(string_stats[0]["min_length"]) if string_stats[0]["min_length"] else 0,
                    "max_length": int(string_stats[0]["max_length"]) if string_stats[0]["max_length"] else 0
                })
            
            # Top values
            top_values = df.groupBy(column_name).count() \
                .orderBy(col("count").desc()) \
                .limit(10) \
                .collect()
            
            stats["top_values"] = [(row[column_name], row["count"]) for row in top_values]
        
        return stats
    
    def _analyze_patterns(self, df: DataFrame, column_name: str, data_type: str) -> Dict[str, Any]:
        """Analyze patterns in column data"""
        patterns = {
            "has_leading_spaces": False,
            "has_trailing_spaces": False,
            "has_special_chars": False,
            "detected_formats": []
        }
        
        if data_type == "string":
            # Sample data for pattern analysis
            sample_data = df.select(column_name).filter(col(column_name).isNotNull()).limit(1000).collect()
            values = [row[column_name] for row in sample_data]
            
            if values:
                # Check for spaces
                patterns["has_leading_spaces"] = any(val.startswith(" ") for val in values if val)
                patterns["has_trailing_spaces"] = any(val.endswith(" ") for val in values if val)
                
                # Check for special characters
                special_char_pattern = r'[!@#$%^&*(),.?":{}|<>]'
                patterns["has_special_chars"] = any(re.search(special_char_pattern, val) for val in values if val)
                
                # Detect common formats
                formats_detected = []
                
                # Email pattern
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if any(re.match(email_pattern, val) for val in values[:100]):
                    formats_detected.append("email")
                
                # Phone pattern
                phone_pattern = r'^\+?1?\d{9,15}$'
                if any(re.match(phone_pattern, val.replace("-", "").replace(" ", "")) for val in values[:100] if val):
                    formats_detected.append("phone")
                
                # Date patterns
                date_patterns = [
                    (r'^\d{4}-\d{2}-\d{2}$', "YYYY-MM-DD"),
                    (r'^\d{2}/\d{2}/\d{4}$', "MM/DD/YYYY"),
                    (r'^\d{8}$', "YYYYMMDD")
                ]
                
                for pattern, format_name in date_patterns:
                    if any(re.match(pattern, val) for val in values[:100] if val):
                        formats_detected.append(f"date_{format_name}")
                
                patterns["detected_formats"] = formats_detected
        
        return patterns
    
    def _calculate_quality_metrics(self, stats: Dict, patterns: Dict) -> Dict[str, Any]:
        """Calculate data quality metrics"""
        metrics = {}
        
        # Completeness (inverse of null percentage)
        metrics["completeness"] = 100 - stats.get("null_percentage", 0)
        
        # Uniqueness
        metrics["uniqueness"] = stats.get("distinct_percentage", 0)
        
        # Validity (basic check - no special characters for certain fields)
        validity_score = 100
        if patterns.get("has_special_chars") and not any(fmt in patterns.get("detected_formats", []) for fmt in ["email"]):
            validity_score -= 20
        if patterns.get("has_leading_spaces") or patterns.get("has_trailing_spaces"):
            validity_score -= 10
        metrics["validity"] = validity_score
        
        # Consistency (based on format detection)
        if patterns.get("detected_formats"):
            metrics["consistency"] = 90  # Has consistent format
        else:
            metrics["consistency"] = 70  # No specific format detected
        
        # Overall quality score
        metrics["overall_quality"] = (
            metrics["completeness"] * 0.3 +
            metrics["uniqueness"] * 0.2 +
            metrics["validity"] * 0.3 +
            metrics["consistency"] * 0.2
        ) / 100
        
        return metrics
    
    def _detect_anomalies(self, stats: Dict, patterns: Dict, data_type: str) -> List[Dict[str, Any]]:
        """Detect data anomalies"""
        anomalies = []
        
        # High null percentage
        if stats.get("null_percentage", 0) > 50:
            anomalies.append({
                "type": "high_null_percentage",
                "severity": "high",
                "value": stats["null_percentage"],
                "description": f"Column has {stats['null_percentage']:.1f}% null values"
            })
        
        # Low cardinality for supposedly unique fields
        if stats.get("cardinality") == "low" and stats.get("distinct_count", 0) < 10:
            anomalies.append({
                "type": "low_cardinality",
                "severity": "medium",
                "value": stats["distinct_count"],
                "description": f"Column has only {stats['distinct_count']} unique values"
            })
        
        # Numeric outliers
        if data_type in ["int", "bigint", "float", "double"] and stats.get("std_dev"):
            if stats["std_dev"] > abs(stats.get("mean", 0)) * 2:
                anomalies.append({
                    "type": "high_variance",
                    "severity": "medium",
                    "description": "High standard deviation indicates potential outliers"
                })
        
        # String length anomalies
        if data_type == "string" and "max_length" in stats:
            if stats["max_length"] > stats.get("avg_length", 0) * 10:
                anomalies.append({
                    "type": "extreme_length_values",
                    "severity": "low",
                    "description": f"Maximum length ({stats['max_length']}) is much higher than average ({stats.get('avg_length', 0):.1f})"
                })
        
        return anomalies
    
    def generate_validation_code(self, profile: Dict, mapping_info: Dict) -> str:
        """Generate PySpark validation code based on profile"""
        column_name = mapping_info.get("column_name", "")
        data_type = mapping_info.get("data_type", "string")
        
        validation_code = f'''
def validate_{column_name}(df):
    """
    Validation function for {column_name}
    Generated based on data profiling results
    """
    from pyspark.sql.functions import col, when, isnan, isnull, length, regexp_extract
    
    # Initialize validation results
    validation_results = {{}}
    
    # Null check
    null_count = df.filter(col("{column_name}").isNull() | isnan(col("{column_name}"))).count()
    total_count = df.count()
    null_percentage = (null_count / total_count * 100) if total_count > 0 else 0
    
    validation_results["null_check"] = {{
        "passed": null_percentage <= {profile.get('stats', {}).get('null_percentage', 0) + 5},
        "null_percentage": null_percentage,
        "threshold": {profile.get('stats', {}).get('null_percentage', 0) + 5}
    }}
'''
        
        # Add type-specific validations
        if data_type == "string":
            validation_code += f'''
    
    # Length validation
    length_stats = df.select(
        avg(length(col("{column_name}"))).alias("avg_length"),
        max(length(col("{column_name}"))).alias("max_length")
    ).collect()[0]
    
    validation_results["length_check"] = {{
        "passed": length_stats["max_length"] <= {profile.get('stats', {}).get('max_length', 1000) * 1.5},
        "max_length": length_stats["max_length"],
        "threshold": {profile.get('stats', {}).get('max_length', 1000) * 1.5}
    }}
'''
        
        elif data_type in ["int", "bigint", "float", "double"]:
            validation_code += f'''
    
    # Range validation
    range_stats = df.select(
        min(col("{column_name}")).alias("min_val"),
        max(col("{column_name}")).alias("max_val")
    ).collect()[0]
    
    validation_results["range_check"] = {{
        "passed": (
            range_stats["min_val"] >= {profile.get('stats', {}).get('min', 0) * 0.9} and
            range_stats["max_val"] <= {profile.get('stats', {}).get('max', 1000000) * 1.1}
        ),
        "min_val": range_stats["min_val"],
        "max_val": range_stats["max_val"],
        "expected_range": [{profile.get('stats', {}).get('min', 0) * 0.9}, {profile.get('stats', {}).get('max', 1000000) * 1.1}]
    }}
'''
        
        validation_code += '''
    
    # Return validation results
    return validation_results
'''
        
        return validation_code
    
    def save_profile(self, profile: Dict, output_path: str) -> None:
        """Save profile to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(profile, f, indent=2, default=str) 