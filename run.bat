@echo off
echo Starting Script Runner Pro...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if PyQt5 is installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo PyQt5 not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Run the application
python script-runner-gui.py

