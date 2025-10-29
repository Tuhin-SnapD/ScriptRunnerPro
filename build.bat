@echo off
echo Building Script Runner Pro for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Install PyInstaller for building executable
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo Error: Failed to install PyInstaller
    pause
    exit /b 1
)

REM Create build directory
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Build executable
echo Building executable...
pyinstaller --onefile --windowed --name "ScriptRunnerPro" --icon=script-runner-icon.png script-runner-gui.py
if errorlevel 1 (
    echo Error: Failed to build executable
    pause
    exit /b 1
)

REM Copy additional files
echo Copying additional files...
copy scripts.json dist\ >nul 2>&1
copy script-runner-icon.png dist\ >nul 2>&1

echo.
echo Build completed successfully!
echo Executable created: dist\ScriptRunnerPro.exe
echo.
echo You can now distribute the contents of the 'dist' folder.
pause

