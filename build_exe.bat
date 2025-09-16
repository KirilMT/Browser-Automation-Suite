@echo off
REM Kill any running main.exe before cleaning
taskkill /f /im main.exe >nul 2>&1
REM Build SCADA automation executable using PyInstaller
REM Uncomment and edit the next line if you use a virtual environment
REM call .\venv\Scripts\activate

REM Clean previous build artifacts
rmdir /s /q dist
rmdir /s /q build
if exist main.spec del main.spec

REM Build the executable and include chromedriver.exe
pyinstaller --onefile --add-data "src\chromedriver.exe;src" src\main.py