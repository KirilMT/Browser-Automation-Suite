"""
Example configuration file for the automation system.
Copy this file to config.py and modify it for your specific application requirements.
config.py is ignored by Git, so your settings will remain local.
"""

import os

# Example configuration dictionary.
# This dictionary is loaded by AutomationConfig in main.py.
LOCAL_APP_CONFIG = {
    "window": {
        "app_window_height": 1080,
        "app_window_header_height": 200,
        "page1_header_height": 250,
        "window_x_offset": 0
    },
    "webdriver": {
        "chrome_driver_path": os.path.join(os.path.dirname(__file__), "chromedriver.exe"),
        "headless_mode": False,
        "default_timeout": 10
    },
    "urls": {
        "base_url": "http://localhost:8000",
        "page1_path": "/page1.html",
        "page2_path": "/page2.html"
    },
    "filters": {
        "enabled": False,
        "selectors": [
            # Example selector: "#app > div > ul > li:nth-child(1)"
        ]
    },
    "test_env_host": "localhost",
    "test_env_port": 8000
}
