@echo off
echo Building Windows Installer for Script Runner Pro...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install cx_Freeze for creating Windows installer
echo Installing cx_Freeze...
pip install cx_Freeze
if errorlevel 1 (
    echo Error: Failed to install cx_Freeze
    pause
    exit /b 1
)

REM Create build directory
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM Build installer
echo Building installer...
python create_installer.py build
if errorlevel 1 (
    echo Error: Failed to build installer
    pause
    exit /b 1
)

REM Copy additional files to build directory
echo Copying additional files...
copy scripts.json build\exe.win-amd64-3.*\ >nul 2>&1
copy script-runner-icon.png build\exe.win-amd64-3.*\ >nul 2>&1

echo.
echo Installer build completed successfully!
echo Executable created in: build\exe.win-amd64-3.*\
echo.
echo You can now distribute the contents of the build directory.
pause

