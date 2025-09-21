# PowerShell script to build Browser-Automation-Suite automation executable

# Define the path to the Python executable in the virtual environment
$pythonPath = Join-Path $PSScriptRoot ".venv/Scripts/python.exe"

# Kill any running main.exe before cleaning
Stop-Process -Name main -Force -ErrorAction SilentlyContinue

# Remove previous build artifacts
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue
Remove-Item -Force main.spec -ErrorAction SilentlyContinue

# Get the path to the chromedriver executable from webdriver-manager
Write-Host "Determining ChromeDriver path..."
$chromedriverPath = & $pythonPath -c "from webdriver_manager.chrome import ChromeDriverManager; print(ChromeDriverManager().install())" | Out-String | ForEach-Object { $_.Trim() }

if (-not (Test-Path $chromedriverPath)) {
    Write-Error "Could not determine the path to chromedriver.exe. Please ensure webdriver-manager is installed and working."
    exit 1
}

Write-Host "ChromeDriver found at: $chromedriverPath"

# Build the executable, adding necessary data and paths
Write-Host "Building executable with PyInstaller..."
& $pythonPath -m PyInstaller --onefile --add-binary "$chromedriverPath;." --add-data "./tests/pages;tests/pages" --paths "./src" --paths "./tests" src/main.py

Write-Host "Build complete."
