@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Script Runner Pro - Windows Edition
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    echo.
    pause
    exit /b 1
)

echo [✓] Python found
python --version
echo.

REM Set venv directory
set VENV_DIR=venv

REM Check if virtual environment exists, create if not
if not exist "%VENV_DIR%" (
    echo [*] Creating virtual environment...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
    echo.
) else (
    echo [✓] Virtual environment found
    echo.
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated
echo.

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [✓] Pip upgraded
echo.

REM Check if dependencies are installed
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [✓] Dependencies installed
    echo.
) else (
    echo [✓] Dependencies already installed
    echo.
)

REM Run the application
echo ========================================
echo   Starting Script Runner Pro...
echo ========================================
echo.
python script-runner-gui.py

REM Deactivate virtual environment on exit
call deactivate >nul 2>&1

endlocal
