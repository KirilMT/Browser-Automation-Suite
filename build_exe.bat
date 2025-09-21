@echo off

REM Define the path to the Python executable in the virtual environment
set PYTHON_EXE=%~dp0\.venv\Scripts\python.exe

REM Kill any running main.exe before cleaning
taskkill /F /IM main.exe /T > nul 2>&1

REM Remove previous build artifacts
rmdir /s /q dist > nul 2>&1
rmdir /s /q build > nul 2>&1
del main.spec > nul 2>&1

REM Build the executable
"%PYTHON_EXE%" -m PyInstaller --onefile src/main.py

echo.
echo Build complete.
pause
