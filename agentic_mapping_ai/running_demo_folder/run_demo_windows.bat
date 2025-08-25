@echo off
chcp 65001 >nul
echo ========================================
echo AGENTIC MAPPING AI - WINDOWS DEMO
echo ========================================
echo.
echo This script runs the Windows-compatible demo
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo Python found. Running demo...
echo.

REM Run the Windows-compatible demo
python working_demo_windows.py

echo.
echo ========================================
echo Demo completed!
echo ========================================
pause
