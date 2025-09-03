@echo off
chcp 65001 >nul
echo.
echo ================================================================
echo 🚀 ULTIMATE AA MEMBER TEST DATA GENERATION SYSTEM
echo ================================================================
echo.
echo This system will generate comprehensive test data covering:
echo 📞 Phone Numbers: 9, 10, 11 digits + invalid formats
echo 📮 Postal Codes: 5, 6 digits + invalid formats  
echo 📅 Date Formats: ISO, US, EU, dot, dash + invalid formats
echo 🔤 Special Characters: Valid/invalid names and addresses
echo 📧 Email Formats: Standard, plus, dot, hyphen + invalid formats
echo 🎯 All 11 AA Member Matching Criteria scenarios
echo.
echo ================================================================
echo.

echo 📋 Step 1: Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

echo.
echo 📋 Step 2: Installing required packages...
pip install faker pandas openpyxl numpy
if %errorlevel% neq 0 (
    echo ❌ Failed to install required packages
    pause
    exit /b 1
)

echo.
echo 📋 Step 3: Running comprehensive data validator...
python aa_comprehensive_data_validator.py
if %errorlevel% neq 0 (
    echo ❌ Data validator failed
    pause
    exit /b 1
)

echo.
echo 📋 Step 4: Generating ultimate test data...
python aa_ultimate_test_generator.py
if %errorlevel% neq 0 (
    echo ❌ Test data generation failed
    pause
    exit /b 1
)

echo.
echo 📋 Step 5: Converting to Excel format...
python aa_ultimate_excel_converter.py
if %errorlevel% neq 0 (
    echo ❌ Excel conversion failed
    pause
    exit /b 1
)

echo.
echo 📋 Step 6: Running comprehensive validation...
python aa_ultimate_validator.py
if %errorlevel% neq 0 (
    echo ❌ Validation failed
    pause
    exit /b 1
)

echo.
echo ================================================================
echo 🎉 ULTIMATE AA MEMBER TEST DATA SYSTEM COMPLETED SUCCESSFULLY!
echo ================================================================
echo.
echo 📁 Generated Files:
echo   • aa_ultimate_test_data.json - Complete test dataset
echo   • AA_Ultimate_Test_Data.xlsx - Excel file with 59+ sheets
echo   • aa_ultimate_validation_report.json - Validation results
echo.
echo 📊 Test Coverage:
echo   • 2,773+ test records generated
echo   • All 11 AA Member Matching Criteria scenarios
echo   • Comprehensive data quality validation
echo   • Date format testing (ISO, US, EU, dot, dash)
echo   • Special character validation (names, addresses)
echo   • Email format testing (standard, plus, dot, hyphen)
echo   • Phone number testing (9, 10, 11 digits + invalid)
echo   • Postal code testing (5, 6 digits + invalid)
echo   • Edge case scenarios
echo.
echo 🎯 Ready for AA Member Matching Criteria API testing!
echo.
pause
