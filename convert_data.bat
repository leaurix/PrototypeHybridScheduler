@echo off
title Hybrid Scheduler — Data Converter
color 0B
cls

echo ============================================================
echo   HYBRID SCHEDULER — DATA CONVERTER
echo ============================================================
echo.
echo  This will convert your 3 Excel files into CSV files.
echo.

cd /d "%~dp0"

echo  Checking for openpyxl...
pip show openpyxl >nul 2>&1
if errorlevel 1 (
    echo  Installing openpyxl...
    pip install openpyxl
)

echo.
echo  Running converter...
echo ============================================================
echo.

python convert_data.py

echo.
pause
