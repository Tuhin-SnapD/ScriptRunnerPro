@echo off
echo Installing Script Runner Pro...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install the application
echo Installing Script Runner Pro...
pip install -e .
if errorlevel 1 (
    echo Error: Failed to install Script Runner Pro
    pause
    exit /b 1
)

REM Create desktop shortcut (optional)
set /p create_shortcut="Create desktop shortcut? (y/n): "
if /i "%create_shortcut%"=="y" (
    echo Creating desktop shortcut...
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\Script Runner Pro.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '-m script_runner_gui'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Save()"
    echo Desktop shortcut created!
)

echo.
echo Installation completed successfully!
echo You can now run Script Runner Pro by typing: python script-runner-gui.py
echo.
pause

