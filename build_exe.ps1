# PowerShell script to build SCADA automation executable
# Kill any running main.exe before cleaning
Stop-Process -Name main -Force -ErrorAction SilentlyContinue
# Remove previous build artifacts
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item -Force main.spec -ErrorAction SilentlyContinue

# Build the executable and include chromedriver.exe
pyinstaller --onefile --add-data "src\chromedriver.exe;src" src\main.py
