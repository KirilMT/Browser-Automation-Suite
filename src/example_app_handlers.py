"""
Example application-specific page automation handlers.
This file serves as a template for creating your own `app_handlers.py`.
Copy this file to `app_handlers.py` and implement the specific automation
logic for your application. `app_handlers.py` is ignored by Git.
"""
from selenium.webdriver.common.by import By
from browser_automation import WebDriverManager
from config_models import AutomationConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def page1_logic(driver, config):
    """Handles the automation logic for the first page."""
    full_url = f"{config.urls.base_url}{config.urls.page1_path}"
    driver.get(full_url)
    print(f"Navigated to: {driver.title}")

    if not config.filters.enabled:
        print("Test environment detected. Skipping production UI interactions for page 1.")
        try:
            WebDriverWait(driver, config.webdriver.default_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print("Test page for 'Page 1' loaded successfully.")
        except Exception as e:
            print(f"Could not verify test page for page 1: {e}")
        return

    # --- Production Logic ---
    # Example: Close a menu, apply filters, etc.
    # Replace with your actual production automation steps.
    print("Running production logic for page 1...")
    # try:
    #     wait_until_element_loaded(driver, By.ID, "menu", timeout=30).click()
    #     print("Menu closed.")
    # except Exception as e:
    #     print(f"Could not close menu: {e}")
    #
    # # Example of further interactions
    # print("Page 1 automation complete.")


def page2_logic(driver, config):
    """Handles the automation logic for the second page."""
    full_url = f"{config.urls.base_url}{config.urls.page2_path}"
    driver.get(full_url)
    print(f"Navigated to: {driver.title}")

    if not config.filters.enabled:
        print("Test environment detected. Skipping production UI interactions for page 2.")
        try:
            WebDriverWait(driver, config.webdriver.default_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print("Test page for 'Page 2' loaded successfully.")
        except Exception as e:
            print(f"Could not verify test page for page 2: {e}")
        return

    # --- Production Logic ---
    # Example: Set window size and position.
    # Replace with your actual production automation steps.
    print("Running production logic for page 2...")
    # try:
    #     import pyautogui
    #     screen_width, _ = pyautogui.size()
    #     driver.set_window_position(0, 0)
    #     driver.set_window_size(screen_width, 1080)
    #     print("Window for page 2 resized.")
    # except Exception as e:
    #     print(f"Could not set window size for page 2: {e}")
    #
    # print("Page 2 automation complete.")
