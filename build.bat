@echo off
setlocal EnableExtensions
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo The app is not set up yet. Run setup.bat first.
    pause
    exit /b 1
)

echo Building dist\AOIHelpTools ...
".venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 goto :fail
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --windowed --name AOIHelpTools --add-data "settings.db;." main.py
if errorlevel 1 goto :fail
copy /Y "settings.db" "dist\AOIHelpTools\settings.db" >nul
echo.
echo Built dist\AOIHelpTools\AOIHelpTools.exe
echo Starting it...
start "" "dist\AOIHelpTools\AOIHelpTools.exe"
exit /b 0

:fail
echo.
echo Build failed. See the messages above.
pause
exit /b 1
