@echo off
REM Demo Batch script for Script Runner Pro
echo Batch Script Demo
echo ================

echo Current directory: %CD%
echo Current user: %USERNAME%
echo Current date: %DATE%
echo Current time: %TIME%

echo.
echo Creating demo files...
echo Hello from batch script! > demo_output.txt
echo This is line 2 >> demo_output.txt
echo This is line 3 >> demo_output.txt

echo.
echo Contents of demo_output.txt:
type demo_output.txt

echo.
echo Cleaning up...
del demo_output.txt

echo.
echo Batch script completed successfully!
pause

