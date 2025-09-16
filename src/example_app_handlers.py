"""
Example application-specific page automation handlers.
This file serves as a template for creating your own `app_handlers.py`.
Copy this file to `app_handlers.py` and implement the specific automation
logic for your application. `app_handlers.py` is ignored by Git.
"""
from selenium.webdriver.common.by import By
from browser_automation import WebDriverManager
from config_models import AutomationConfig


class BasePageHandler:
    """Base class for page handlers."""

    def __init__(self, driver_manager: WebDriverManager, config: AutomationConfig):
        self.driver_manager = driver_manager
        self.config = config

    def setup_window_layout(self, x: int, y: int, width: int, height: int):
        """Setup window position and size for this page."""
        self.driver_manager.set_window_position_and_size(x, y, width, height)


class Page1Handler(BasePageHandler):
    """Handles automation for the SCADA alarms page."""

    def navigate_and_setup(self):
        """Navigate to alarms page and perform initial setup."""
        print("Navigating to Page 1...")
        self.driver_manager.navigate_to(self.config.urls.page1_url)
        # TODO: Implement page-specific setup logic here
        # self._close_menu()
        # self._configure_alarm_filters()
        self._setup_page1_window_layout()

    def _close_menu(self):
        """(Example) Close the navigation menu."""
        # self.driver_manager.click_element_safe(By.ID, "menu", timeout=30)
        print("Example: Closing menu (not implemented).")

    def _configure_alarm_filters(self):
        """(Example) Open config popup and apply filters."""
        print("Example: Configuring alarm filters (not implemented).")

    def _set_priority_filters(self):
        """(Example) Set minimum and maximum priority filters."""
        print("Example: Setting priority filters (not implemented).")

    def _set_category_filters(self):
        """(Example) Set category filters."""
        print("Example: Setting category filters (not implemented).")

    def _hide_filters_panel(self):
        """(Example) Hide the filters panel."""
        print("Example: Hiding filters panel (not implemented).")

    def _setup_page1_window_layout(self):
        """Setup window layout for alarms page."""
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        # y_position = (self.config.window.app_window_height - self.config.window.app_window_header_height - self.config.window.page1_header_height)
        # height = (screen_height - self.config.window.app_window_height + self.config.window.page1_header_height)
        # self.setup_window_layout(self.config.window.window_x_offset, y_position, screen_width, height)
        print("Example: Setting up Page 1 window layout (not implemented).")


class Page2Handler(BasePageHandler):
    """Handles automation for the SCADA overview page."""

    def navigate_and_setup(self):
        """Navigate to overview page and perform initial setup."""
        print("Navigating to Page 2...")
        self.driver_manager.navigate_to(self.config.urls.page2_url)
        # TODO: Implement page-specific setup logic here
        self._setup_page2_window_layout()

    def _setup_page2_window_layout(self):
        """Setup window layout for overview page."""
        import pyautogui
        screen_width, _ = pyautogui.size()
        # self.setup_window_layout(
        #     self.config.window.window_x_offset,
        #     -self.config.window.app_window_header_height,
        #     screen_width,
        #     self.config.window.app_window_height
        # )
        print("Example: Setting up Page 2 window layout (not implemented).")
