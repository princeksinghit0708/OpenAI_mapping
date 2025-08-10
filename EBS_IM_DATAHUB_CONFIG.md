# EBS IM Account DataHub Mapping Configuration

## Overview

This configuration is specifically tailored for processing the `ebs_IM_account_DATAhub_mapping_v8.0.xlsx` file with specialized handling for DataHub standard mapping and goldref lookups.

## File Structure

### Excel File
- **File Name**: `ebs_IM_account_DATAhub_mapping_v8.0.xlsx`
- **Primary Sheet**: `datahub standard mapping`
- **Reference Sheet**: `goldref`

### Sheet Descriptions

#### 1. DataHub Standard Mapping Sheet
Contains the main mapping definitions with columns for:
- Source table and column information
- Target DataHub table and column specifications
- Mapping type classification
- Transformation logic

#### 2. Goldref Sheet
Contains reference transformations used when mapping type is "Derived goldref":
- Lookup tables and transformation rules
- Standard business logic patterns
- Reference data mappings

## Mapping Type Handling

The system recognizes these mapping types:

### Standard Types
- **`direct`**: Direct column-to-column mapping
- **`derived`**: Custom transformation logic required
- **`default`**: Use default/hardcoded values
- **`no mapping`**: Exclude from processing

### Special Type: Derived Goldref
- **`derived goldref`**: Use goldref sheet for transformation logic
- When this type is detected, the system:
  1. Searches the goldref sheet for matching entries
  2. Looks up transformation rules by source/target columns
  3. Applies goldref-specific business logic
  4. Generates appropriate PySpark transformation code

## Goldref Lookup Process

When a mapping has type "Derived goldref":

1. **Source Matching**: Find goldref entries matching source table/column
2. **Target Matching**: Match by target column name if source match fails
3. **Logic Extraction**: Extract transformation logic from goldref
4. **Code Generation**: Create PySpark code using goldref rules

### Example Goldref Lookup
```python
# If mapping type is "derived goldref"
# System searches goldref sheet for:
# - source_table: "EBS_ACCOUNTS"
# - source_column: "ACCOUNT_STATUS"
# - target_column: "account_status_cd"

# Generates code like:
"""
# Goldref transformation: 
# Map EBS account status codes to DataHub standard codes
# A=Active, I=Inactive, C=Closed -> 1=Active, 0=Inactive, 2=Closed
"""
```

## Configuration Files Updated

### Main Applications
- `main.py`: Updated to use EBS IM Excel file
- `enhanced_main.py`: Enhanced with goldref logic
- `run_application.py`: Updated default configuration

### Key Features
1. **Intelligent Sheet Detection**: Automatically finds mapping and goldref sheets
2. **Goldref Integration**: Special handling for "Derived goldref" mappings
3. **Fallback Logic**: Graceful handling when goldref data is unavailable
4. **Enhanced Context**: Includes goldref logic in code generation

## Usage

### Quick Start
```bash
# Run with EBS IM configuration
python enhanced_main.py
```

### Manual Configuration
```python
config = {
    'excel_file': 'ebs_IM_account_DATAhub_mapping_v8.0.xlsx',
    'results_dir': 'results',
    'output_dir': 'output'
}

app = EnhancedDataMappingApplication(config)
app.run_enhanced()
```

## Output

The system generates:
- **PySpark Code**: With goldref transformations included
- **Test Cases**: Covering goldref scenarios
- **Documentation**: Explaining goldref logic
- **Reports**: Highlighting goldref usage

## Goldref Logic Examples

### Simple Lookup
```python
# Goldref lookup: Map account_type to account_type_code
when(col("account_type") == "SAVINGS", "SAV")
.when(col("account_type") == "CHECKING", "CHK")
.otherwise("UNK")
```

### Complex Transformation
```python
# Goldref transformation: Calculate account_age_days
datediff(current_date(), col("account_open_date"))
```

This configuration ensures seamless processing of your EBS IM Account DataHub mapping requirements with full goldref support.
