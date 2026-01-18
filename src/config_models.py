"""
Configuration models for the automation system.
Contains all configuration data classes.
"""
import os
import sys
import logging
from dataclasses import dataclass, field
from typing import Dict, List


logger = logging.getLogger("config_models")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.handlers = [handler]


def get_chromedriver_path():
    """Return absolute path to chromedriver.exe, handling PyInstaller bundles."""
    if hasattr(sys, '_MEIPASS'):
        # If running in a PyInstaller bundle
        path = os.path.join(sys._MEIPASS, 'src', 'chromedriver.exe')
    else:
        # If running as a script
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'chromedriver.exe'))
    logger.debug(f"Resolved chromedriver.exe path: {path}")
    return path


@dataclass
class WindowConfig:
    """Configuration for window positioning and sizing."""
    app_window_height: int = 1100
    app_window_header_height: int = 210
    page1_header_height: int = 265
    page2_header_height: int = 265
    window_x_offset: int = -5


@dataclass
class WebDriverConfig:
    """Configuration for web driver settings."""
    chrome_driver_path: str = field(default_factory=get_chromedriver_path)
    headless_mode: bool = False
    default_timeout: int = 10


@dataclass
class AppUrls:
    """URL configurations for the target application."""
    base_url: str = "https://your-target-system.com/app"
    page1_path: str = "/path/to/page1"
    page2_path: str = "/path/to/page2"

    @property
    def page1_url(self) -> str:
        return f"{self.base_url}{self.page1_path}"

    @property
    def page2_url(self) -> str:
        return f"{self.base_url}{self.page2_path}"


@dataclass
class FilterConfig:
    """Configuration for element filters."""
    enabled: bool = False
    selectors: List[str] = field(default_factory=list)


class AutomationConfig:
    """Main configuration class combining all settings."""

    def __init__(self, config_dict: Dict = None):
        self.window = WindowConfig()
        self.webdriver = WebDriverConfig()
        self.urls = AppUrls()
        self.filters = FilterConfig()

        if config_dict:
            self._load_from_dict(config_dict)

    def _load_from_dict(self, config_dict: Dict):
        """Load configuration from dictionary."""
        for section, values in config_dict.items():
            if hasattr(self, section) and isinstance(values, dict):
                section_obj = getattr(self, section)
                for key, value in values.items():
                    if hasattr(section_obj, key):
                        setattr(section_obj, key, value)

    def to_dict(self) -> Dict:
        """Convert configuration to dictionary."""
        return {
            'window': self.window.__dict__,
            'webdriver': self.webdriver.__dict__,
            'urls': self.urls.__dict__,
            'filters': self.filters.__dict__
        }
