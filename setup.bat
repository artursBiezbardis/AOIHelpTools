@echo off
setlocal EnableExtensions
cd /d "%~dp0"

REM AOI Help Tools needs Python 3.11. Newer versions cannot install the pinned libraries.
set "PY="
py -3.11 -c "import sys" >nul 2>&1
if not errorlevel 1 set "PY=py -3.11"
if not defined PY (
    python -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 11) else 1)" >nul 2>&1
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo Python 3.11 was not found.
    echo Install it from https://www.python.org/downloads/release/python-3119/
    echo In the installer, enable "py launcher", "Add python.exe to PATH", and "tcl/tk and IDLE".
    pause
    exit /b 1
)

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo Python 3.11 is installed, but tkinter is missing.
    echo Reinstall Python 3.11 and include "tcl/tk and IDLE".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating a virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :fail
)

echo Installing libraries...
set "PYTHONUTF8=1"
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :fail
".venv\Scripts\python.exe" -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto :fail

echo.
echo Setup finished. Starting AOI Help Tools...
call "%~dp0run.bat"
exit /b

:fail
echo.
echo Setup failed. See the messages above.
pause
exit /b 1
