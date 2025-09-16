# Generic Browser Automation Framework

A modular, reusable automation system built with Python and Selenium WebDriver. This system provides automated browser-based monitoring and interaction for web applications.

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, browser automation, and application-specific handlers.
- **Dual Browser Setup**: Simultaneously manages multiple browser instances for different tasks.
- **Configurable**: Easily customizable for different web applications through configuration files
- **Thread-Safe**: Multi-threaded design for concurrent browser operations
- **Error Handling**: Comprehensive error handling and graceful shutdown mechanisms
- **Process Management**: Automatic cleanup of browser processes

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
```

## Installation

1. **Prerequisites**:
   - Python 3.7+
   - Chrome browser
   - ChromeDriver (included in project)

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

### Common Issues

1. **ChromeDriver Version Mismatch**:
   - Download a compatible ChromeDriver version for your Chrome browser.
   - Replace `chromedriver.exe` in the `src/` directory.
   - Update `webdriver.chrome_driver_path` in the configuration if needed.

2. **Element Not Found Errors**:
   - Verify that CSS selectors are correct for your target system.
   - Increase timeout values in the configuration.
   - Check if the page structure has changed.
   - Use browser developer tools to inspect elements.

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
