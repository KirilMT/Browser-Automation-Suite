# 🚀 Generic Browser Automation Framework

A modular, reusable automation system built with Python and Selenium WebDriver. This system provides automated browser-based monitoring and interaction for web applications.

## 🖼️ Screenshots

*(Placeholder for screenshots of the application in action. You can add images of the browser automation, configuration files, or console output.)*

## ✨ Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, browser automation, and application-specific handlers.
- **Dual Browser Setup**: Simultaneously manages multiple browser instances for different tasks.
- **Configurable**: Easily customizable for different web applications through configuration files.
- **Thread-Safe**: Multi-threaded design for concurrent browser operations.
- **Error Handling**: Comprehensive error handling and graceful shutdown mechanisms.
- **Process Management**: Automatic cleanup of browser processes.
- **Automated EXE Build**: Batch and PowerShell scripts for packaging your automation as a standalone executable.

## 📁 Project Structure

```
SCADA/
├── src/
│   ├── config.py              # Configuration management classes
│   ├── browser_automation.py  # WebDriver and browser automation utilities
│   ├── app_handlers.py        # Application-specific page interaction handlers
│   ├── automation_system.py   # Main orchestration system
│   ├── main.py                # Entry point script
│   ├── example_config.py      # Example configuration templates
│   └── chromedriver.exe       # Chrome WebDriver executable
├── requirements.txt           # Python dependencies
├── README.md                  # This documentation
├── main.spec                  # PyInstaller spec file (ignored by git)
├── build_exe.bat              # Batch script for building EXE
├── build_exe.ps1              # PowerShell script for building EXE
└── .gitignore                 # Git ignore rules
```

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.7+
- Chrome browser
- ChromeDriver (included in project, must match your Chrome version)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourOrganization/SCADA.git
   cd SCADA
   ```

2. **Create a virtual environment (recommended):**
   ```powershell
   # On Windows (PowerShell)
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   ```bash
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:
   ```bash
   pip install selenium psutil pyautogui
   ```

4. **Setup:**
   - Ensure `chromedriver.exe` is in the `src/` directory.
   - Modify configuration in `src/main.py` or create a custom config based on `src/example_config.py`.

## 🚀 Quick Start

### Using the Entry Point Script

Simply run the main script:
```bash
cd src
python main.py
```

### Basic Usage Example

Create a script in the `src/` directory:

```python
# basic_usage.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

# noinspection PyUnresolvedReferences
from automation_system import AutomationSystem, AutomationConfig

# Create configuration
config = AutomationConfig()
config.urls.base_url = "https://your-target-system.com/app"
config.urls.page1_path = "/path/to/page1"
config.urls.page2_path = "/path/to/page2"

# Start automation
system = AutomationSystem(config)
try:
    system.start_automation()
    system.wait_for_completion()
finally:
    system.cleanup()
```

## 🔧 Configuration

The system uses a hierarchical configuration structure defined in `src/config.py`.

### Core Configuration Classes
- **WindowConfig**: Window positioning and sizing.
- **WebDriverConfig**: Chrome WebDriver settings.
- **AppUrls**: URL paths for different application pages.
- **FilterConfig**: Configuration for filtering elements.

### Example Configuration

You can customize parameters by creating an `AutomationConfig` object or loading from a dictionary.

```python
# configuration_example.py
# noinspection PyUnresolvedReferences
from config import AutomationConfig

config = AutomationConfig()

# Customize URLs
config.urls.base_url = "https://your-system.com/app"
config.urls.page1_path = "/page1"

# Window settings
config.window.app_window_height = 1200
config.window.window_x_offset = 0

# WebDriver settings
config.webdriver.headless_mode = True  # Run without GUI
config.webdriver.default_timeout = 15
```

### Test Server Configuration
You can control the test server's host and port via your config files (`config.py` or `example_config.py`):

```python
LOCAL_APP_CONFIG = {
    # ...existing config...
    "test_env_host": "localhost",  # Host for test server
    "test_env_port": 8000,          # Port for test server
}
```
- When `filters.enabled` is set to `False`, the test server will be launched automatically at the specified host and port.

## 🏗️ Building the Executable

You can automate EXE creation using either the batch or PowerShell script:

- **Batch (Windows CMD):**
  ```cmd
  build_exe.bat
  ```
- **PowerShell:**
  ```powershell
  .\build_exe.ps1
  ```
  > PowerShell script is recommended for better process cleanup and compatibility.

**Note:**
- Both scripts bundle `chromedriver.exe` using PyInstaller's `--add-data` option.
- The code automatically resolves the path to `chromedriver.exe` for both development and packaged execution.

## 🧪 Test Environment

A set of dummy HTML pages is provided in `src/test_env/pages/` for local testing.

### Launching the Local Test Server

To serve these pages for browser and Selenium testing:

```bash
cd src/test_env
python serve_test_env.py
```
- By default, the server runs at `http://localhost:8000/`.
- You can change the port with `--port`, e.g. `python serve_test_env.py --port 8080`.

## 🏛️ Architecture Overview

### Core Components

1. **AutomationSystem**: Main orchestrator that manages multiple browser instances.
2. **WebDriverManager**: Handles Chrome WebDriver lifecycle and interactions.
3. **Page Handlers** (`app_handlers.py`): Manages interactions on specific pages.
4. **ProcessManager**: Handles browser process cleanup.

### Key Design Principles

- **Separation of Concerns**: Each module has a specific responsibility.
- **Configurable**: All system parameters are externalized to configuration.
- **Extensible**: Easy to add new page handlers or automation workflows.
- **Resilient**: Comprehensive error handling and recovery mechanisms.

## 🚨 Troubleshooting

### Common Issues

1. **ChromeDriver Version Mismatch**:
   - Download the correct ChromeDriver for your Chrome browser from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
   - Replace `src/chromedriver.exe` with the new version.
   - Rebuild your executable.

2. **EXE Build Issues**:
   - Ensure no previous `.exe` process is running before building.
   - If you see `Access is denied`, terminate all related processes and retry.

3. **Window Layout Issues**:
   - Adjust window configuration parameters in `WindowConfig`.
   - Verify screen resolution compatibility.

4. **Import Errors**:
   - Ensure you're running scripts from the `src/` directory.
   - Install all dependencies: `pip install -r requirements.txt`.

### Debugging

Enable detailed logging by adding this to your script:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🤝 Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

1. Follow PEP 8 style guidelines.
2. Add comprehensive docstrings to new classes and methods.
3. Include error handling in all automation functions.
4. Update configuration examples when adding new features.

## 📝 License

This project is provided as-is for educational and development purposes. Ensure compliance with your organization's policies when using it with production systems.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above.
2. Review configuration examples in `example_config.py`.
3. Verify target system compatibility.
4. Test individual components separately.
