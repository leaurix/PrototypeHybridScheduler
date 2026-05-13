@echo off
title Hybrid Scheduler — Builder
color 0A
cls

echo ============================================================
echo   HYBRID SCHEDULER — AUTO BUILD
echo ============================================================
echo.

:: Go to the folder where this .bat file lives
cd /d "%~dp0"

echo [1/3] Installing / updating dependencies...
pip install --upgrade pyinstaller openpyxl ortools pandas
echo.

echo [2/3] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist\HybridScheduler.exe" del /f /q "dist\HybridScheduler.exe"
echo.

echo [3/3] Building HybridScheduler.exe ...
python -m PyInstaller scheduler_gui.spec --noconfirm
echo.

echo ============================================================
if exist "dist\HybridScheduler.exe" (
    echo   BUILD SUCCESSFUL!
    echo   Launching HybridScheduler.exe ...
    echo ============================================================
    echo.
    start "" "dist\HybridScheduler.exe"
) else (
    color 0C
    echo   BUILD FAILED - check the output above for errors.
    echo ============================================================
)

pause
