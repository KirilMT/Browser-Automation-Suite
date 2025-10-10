# Generic Browser Automation Framework

A modular, reusable automation system built with Python and Selenium WebDriver. This system provides automated browser-based monitoring and interaction for web applications.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, browser automation, and application-specific handlers.
- **Dual Browser Setup**: Simultaneously manages multiple browser instances for different tasks.
- **Configurable**: Easily customizable for different web applications through configuration files
- **Thread-Safe**: Multi-threaded design for concurrent browser operations
- **Error Handling**: Comprehensive error handling and graceful shutdown mechanisms
- **Process Management**: Automatic cleanup of browser processes
- **Automated EXE Build**: Batch and PowerShell scripts for packaging your automation as a standalone executable

## Project Structure

```
src/
├── config.py              # Configuration management classes
├── browser_automation.py  # WebDriver and browser automation utilities
├── app_handlers.py        # Application-specific page interaction handlers
├── automation_system.py   # Main orchestration system
├── main.py                # Entry point script
├── example_config.py      # Example configuration templates
└── chromedriver.exe       # Chrome WebDriver executable
requirements.txt           # Python dependencies
README.md                  # This documentation
main.spec                  # PyInstaller spec file (ignored by git)
build_exe.bat              # Batch script for building EXE
build_exe.ps1              # PowerShell script for building EXE
.gitignore                 # Git ignore rules
```

## Installation

1. **Prerequisites**:
   - Python 3.7+
   - Chrome browser
   - ChromeDriver (included in project, must match your Chrome version)

2. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:
   ```bash
   pip install selenium psutil pyautogui
   ```

3. **Setup**:
   - Clone or download the project
   - Navigate to the project directory
   - Ensure `chromedriver.exe` is in the `src/` directory
   - Modify configuration in `src/main.py` or create a custom config.

## Building the Executable

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
- If you see a ChromeDriver version mismatch error, update `chromedriver.exe` in `src/` to match your installed Chrome version (see Troubleshooting).

## .gitignore

- All PyInstaller spec files are ignored using `*.spec`.
- Build artifacts and local configuration files are also ignored.

## Quick Start

### Basic Usage

Create a script in the `src/` directory:

```python
# basic_usage.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

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

### Using the Entry Point Script

Simply run the main script:
```bash
cd src
python main.py
```

### Using Configuration File

```python
# custom_config_usage.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import AutomationConfig
from example_config import APP_CONFIG
from automation_system import AutomationSystem

# Load from configuration dictionary
config = AutomationConfig(APP_CONFIG)
system = AutomationSystem(config)
```

## Configuration

### AutomationConfig Class

The system uses a hierarchical configuration structure:

- **WindowConfig**: Window positioning and sizing.
- **WebDriverConfig**: Chrome WebDriver settings.
- **AppUrls**: URL paths for different application pages.
- **FilterConfig**: Configuration for filtering elements.

### Example Configuration

```python
# configuration_example.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from config import AutomationConfig

config = AutomationConfig()

# Customize URLs
config.urls.base_url = "https://your-system.com/app"
config.urls.page1_path = "/page1"
config.urls.page2_path = "/dashboard"

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
- If these options are missing, defaults (`localhost:8000`) will be used.
- Warnings will be printed if any required config section is missing, and sensible defaults will be set automatically.

## Architecture Overview

### Core Components

1. **AutomationSystem**: Main orchestrator that manages multiple browser instances and coordinates automation workflows.

2. **WebDriverManager**: Handles Chrome WebDriver lifecycle, element interactions, and window management.

3. **Page Handlers**:
   - `Page1Handler`: Manages interactions on the first page.
   - `Page2Handler`: Manages setup and monitoring on the second page.

4. **ProcessManager**: Handles browser process cleanup and monitoring

### Key Design Principles

- **Separation of Concerns**: Each module has a specific responsibility
- **Configurable**: All system parameters are externalized to configuration
- **Extensible**: Easy to add new page handlers or automation workflows
- **Resilient**: Comprehensive error handling and recovery mechanisms

## Extending the System

### Adding New Page Handlers

Create a new handler by extending the base class:

```python
# custom_handler_example.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app_handlers import BasePageHandler

class CustomPageHandler(BasePageHandler):
    def navigate_and_setup(self):
        self.driver_manager.navigate_to("https://your-custom-page.com")
        # Add your custom automation logic here
        self._setup_custom_layout()
    
    def _setup_custom_layout(self):
        # Custom implementation
        pass
```

### Custom Configuration

Extend the configuration system:

```python
# extended_config_example.py
import sys
import os
sys.path.append(os.path.dirname(__file__))

from dataclasses import dataclass
from config import AutomationConfig

@dataclass
class CustomConfig:
    custom_setting: str = "default_value"
    retry_count: int = 3

class ExtendedAutomationConfig(AutomationConfig):
    def __init__(self, config_dict=None):
        super().__init__(config_dict)
        self.custom = CustomConfig()
```

## Error Handling

The system includes comprehensive error handling:

- **WebDriver Errors**: Automatic retry logic and fallback mechanisms
- **Element Not Found**: Timeout-based waiting with configurable timeouts
- **Process Management**: Automatic cleanup of orphaned browser processes
- **Graceful Shutdown**: Proper resource cleanup on interruption

## Threading Model

- **Main Thread**: Orchestration and user interaction
- **Automation Threads**: One per browser instance for page-specific automation
- **Monitor Threads**: Browser window monitoring and automatic cleanup

## Troubleshooting

### ChromeDriver Version Mismatch
- Download the correct ChromeDriver for your Chrome browser from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/).
- Replace `src/chromedriver.exe` with the new version.
- Rebuild your executable using the provided script.

### EXE Build Issues
- Ensure no previous `main.exe` process is running before building (run scripts as administrator if needed).
- If you see `Access is denied` or `file is in use`, terminate all related processes and retry.

3. **Window Layout Issues**:
   - Adjust window configuration parameters in `WindowConfig`
   - Verify screen resolution compatibility
   - Test with different screen resolutions

4. **Import Errors**:
   - Ensure you're running scripts from the `src/` directory
   - Add proper path setup: `sys.path.append(os.path.dirname(__file__))`
   - Install all dependencies: `pip install -r requirements.txt`

### Debugging

Enable detailed logging by adding this to your script:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Running Tests

Test the system configuration:

```bash
cd src
python -c "from config import AutomationConfig; print('Configuration loaded successfully')"
python -c "from automation_system import AutomationSystem; print('Main system loaded successfully')"
```

## PyInstaller Packaging Notes

- `chromedriver.exe` is bundled using `--add-data`.
- The code uses `sys._MEIPASS` to resolve the driver path when running as an executable.
- No manual path configuration is needed in your config.
- Update `chromedriver.exe` whenever Chrome updates to avoid compatibility errors.

## Security Considerations

- Store sensitive URLs and credentials in environment variables.
- Use HTTPS for all system connections.
- Regularly update ChromeDriver and dependencies.
- Consider running in headless mode for production deployments.
- Implement proper authentication handling for your target system.

## Performance Optimization

- Use headless mode (`config.webdriver.headless_mode = True`) for better performance
- Adjust timeout values based on your network conditions
- Consider implementing connection pooling for multiple target systems
- Monitor system resources when running multiple browser instances

## Development Workflow

1. **Initial Setup**:
   ```bash
   cd src
   python main.py  # Test with default configuration
   ```

2. **Custom Configuration**:
   - Copy `example_config.py` to your own config file.
   - Modify URLs and settings for your target system.
   - Test with: `python your_custom_script.py`

3. **Adding Features**:
   - Extend page handlers for new functionality.
   - Add new configuration sections as needed.
   - Test thoroughly with your target system.

## Test Environment

A set of dummy HTML pages is provided in `src/test_env/pages/` for local testing and development:

- `index.html`: Main entry page with navigation links and a button.
- `page1.html`: Contains a button and a link back to index.
- `page2.html`: Contains a simple form and a link back to index.

### Launching the Local Test Server

To serve these pages for browser and Selenium testing, use the provided Python server:

```bash
cd src/test_env
python serve_test_env.py
```

- By default, the server runs at [http://localhost:8000/](http://localhost:8000/).
- Access your test pages at:
  - http://localhost:8000/index.html
  - http://localhost:8000/page1.html
  - http://localhost:8000/page2.html
- You can change the port with `--port`, e.g. `python serve_test_env.py --port 8080`

**Usage:**
- Open these pages in your browser for manual testing.
- Use Selenium automation scripts to interact with buttons, links, and forms for development and debugging.
- Update or extend these pages as needed for more complex test scenarios.

Example (Python Selenium):
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# Point to local test page served by the test server
driver = webdriver.Chrome()
driver.get('http://localhost:8000/index.html')

# Interact with elements
index_btn = driver.find_element(By.ID, 'index-btn')
index_btn.click()

link_page1 = driver.find_element(By.ID, 'link-page1')
link_page1.click()

# ... continue with your tests ...
driver.quit()
```

## License

This project is provided as-is for educational and development purposes. Ensure compliance with your organization's policies when using it with production systems.

## Contributing

1. Follow PEP 8 style guidelines
2. Add comprehensive docstrings to new classes and methods
3. Include error handling in all automation functions
4. Update configuration examples when adding new features
5. Test with multiple system configurations

## Support

For issues and questions:
1. Check the troubleshooting section above.
2. Review configuration examples in `example_config.py`.
3. Verify target system compatibility.
4. Test individual components separately.
