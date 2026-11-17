@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "PYTHONUTF8=1"

if not exist ".venv\Scripts\python.exe" (
    echo The app is not set up yet. Run setup.bat first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" "%~dp0main.py"
if errorlevel 1 (
    echo.
    echo The app stopped with an error. See the messages above.
    pause
    exit /b 1
)
exit /b 0
