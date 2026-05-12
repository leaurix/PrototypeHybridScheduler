@echo off
:: ============================================================
::  build.bat  —  builds HybridScheduler.exe
::  Run this once from inside PrototypeHybridScheduler-main\
:: ============================================================

echo Installing / upgrading PyInstaller...
pip install --upgrade pyinstaller ortools pandas

echo.
echo Building HybridScheduler.exe ...
pyinstaller scheduler_gui.spec --clean --noconfirm

echo.
if exist "dist\HybridScheduler.exe" (
    echo  BUILD SUCCESSFUL
    echo  Your EXE is at:  dist\HybridScheduler.exe
    echo  Double-click it to launch the scheduler.
) else (
    echo  BUILD FAILED — check the output above for errors.
)
pause
