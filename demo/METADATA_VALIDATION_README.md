# 🔍 Hive Metadata Validation Demo

This demo showcases the **MetadataValidatorAgent** working with your existing Hive metadata JSON files in **agentic AI mode**.

## 🎯 What This Demo Shows

- **AI-Powered Validation**: The agent uses AI to analyze your Hive table metadata
- **Intelligent Field Analysis**: Automatically detects issues and provides insights
- **Banking-Specific Rules**: Validates against banking data standards
- **Comprehensive Reporting**: Detailed validation results for each table

## 📁 Files in This Demo

### Core Demo Files
- `hive_metadata_validation_demo.py` - Main demo script
- `test_metadata_agent.py` - Agent testing script
- `run_metadata_validation.py` - Easy launcher script

### Your Metadata Files (Required)
- `results/acct_dly_metadata.json` - Account daily table metadata
- `results/cust_dly_metadata.json` - Customer daily table metadata  
- `results/txn_dly_metadata.json` - Transaction daily table metadata

## 🚀 How to Run

### Option 1: Easy Launcher (Recommended)
```bash
cd demo
python run_metadata_validation.py
```

This gives you a menu to:
1. Test the agent first
2. Run the full demo
3. View metadata files
4. Exit

### Option 2: Test Agent First
```bash
cd demo
python test_metadata_agent.py
```

### Option 3: Run Full Demo Directly
```bash
cd demo
python hive_metadata_validation_demo.py
```

## 🔧 Prerequisites

1. **Python Environment**: Python 3.7+ with required packages
2. **agentic_mapping_ai**: The AI framework must be installed
3. **Metadata Files**: JSON files in `results/` directory
4. **LLM Access**: OpenAI API key or other LLM provider configured

## 📊 What the Agent Validates

### Schema Validation
- Table structure completeness
- Column definitions
- Data type consistency
- Naming conventions

### Banking-Specific Rules
- Account number formats
- Currency code compliance
- Date range validation
- Regulatory field requirements

### Field Analysis
- Required field presence
- Data type appropriateness
- Comment quality
- Business logic consistency

## 🤖 Agent Capabilities

The **MetadataValidatorAgent** demonstrates:

- **Intelligent Analysis**: Uses AI to understand your metadata structure
- **Context Awareness**: Knows this is banking data for EBS IM DataHub
- **Automated Detection**: Finds issues without manual rule definition
- **Actionable Insights**: Provides specific recommendations for fixes
- **Learning**: Improves validation over time

## 📈 Expected Output

The demo will show:

1. **Agent Initialization**: Confirms the agent is working
2. **File Processing**: Loads each metadata file
3. **AI Analysis**: Agent analyzes each table
4. **Validation Results**: Detailed findings for each table
5. **Summary Report**: Overall validation status

## 🎯 Demo Workflow

```
1. Load Hive Metadata Files
   ↓
2. Initialize MetadataValidatorAgent
   ↓
3. Process Each Table
   ↓
4. AI-Powered Validation
   ↓
5. Generate Validation Report
   ↓
6. Display Results & Insights
```

## 🔍 Sample Validation Output

```
🔍 [1/3] Validating: acct_dly_metadata.json
------------------------------------------------------------
📊 Table: acct_dly
🗄️  Database: ebs_im_datahub
📈 Rows: 15,000,000
📋 Columns: 10

🤖 Agent is analyzing the metadata...
   (This demonstrates the agent's AI-powered validation capabilities)

✅ AGENT VALIDATION COMPLETED
📊 Validation Status: VALIDATED

📝 Validation Details (5 checks):
   ✅ Schema Structure: PASS
   ✅ Field Definitions: PASS
   ✅ Data Types: PASS
   ✅ Banking Standards: PASS
   ✅ Naming Conventions: PASS

🔍 Field Analysis:
   📊 Total Fields: 10
   ✅ Valid Fields: 10
   ⚠️  Warnings: 0
   ❌ Errors: 0
```

## 🚀 Next Steps After Demo

1. **Review Validation Results**: Check what issues were found
2. **Fix Identified Problems**: Address any validation failures
3. **Run Validation Again**: Verify fixes resolved issues
4. **Integrate with Excel**: Use the agent to validate Excel mappings
5. **Automate Process**: Set up automated validation in your pipeline

## 🆘 Troubleshooting

### Common Issues

**Import Errors**
```bash
❌ Import error: No module named 'agentic_mapping_ai'
```
**Solution**: Make sure you're in the `demo` directory and the framework is installed

**No Metadata Files**
```bash
❌ No metadata files found in results/
```
**Solution**: Ensure your JSON metadata files are in the `results/` directory

**Agent Creation Failed**
```bash
❌ Agent creation failed: Invalid configuration
```
**Solution**: Check your LLM service configuration and API keys

### Getting Help

1. Run the test script first: `python test_metadata_agent.py`
2. Check the prerequisites section above
3. Verify your metadata files are valid JSON
4. Ensure you have proper LLM access configured

## 🎉 Success Indicators

You'll know the demo is working when you see:

- ✅ "MetadataValidatorAgent initialized successfully"
- ✅ "AGENT VALIDATION COMPLETED" for each table
- 📊 Detailed validation results with status indicators
- 🎯 Comprehensive summary at the end

## 🔗 Related Files

- `metadata_validator_demo.py` - Original metadata validation demo
- `enhanced_main.py` - Main application with Excel integration
- `setup_excel.py` - Excel file setup helper

---

**Ready to see your metadata validated by AI? Run the demo now!** 🚀
