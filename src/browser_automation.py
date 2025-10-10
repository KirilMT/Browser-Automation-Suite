"""
Browser automation utilities.
Handles Chrome WebDriver initialization and common web interactions.
"""
import os
import subprocess
import sys
import time
import psutil
from typing import Optional, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from config_models import WebDriverConfig


class WebDriverManager:
    """Manages Chrome WebDriver lifecycle and common operations."""

    def __init__(self, config: WebDriverConfig):
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.service_process: Optional[subprocess.Popen] = None
        self.chrome_driver_path = self._resolve_chromedriver_path()

    def _resolve_chromedriver_path(self) -> str:
        """Resolves the path to chromedriver.exe for both development and PyInstaller builds."""
        try:
            if getattr(sys, 'frozen', False):
                # Running as a PyInstaller bundle
                base_path = sys._MEIPASS
            else:
                # Running in development
                base_path = os.path.dirname(__file__)
            # Try both possible locations
            possible_paths = [
                os.path.join(base_path, 'chromedriver.exe'),
                os.path.join(base_path, 'src', 'chromedriver.exe')
            ]
            for chromedriver_path in possible_paths:
                if os.path.exists(chromedriver_path):
                    print(f"[DEBUG] Resolved chromedriver.exe path: {chromedriver_path}")
                    return chromedriver_path
            raise FileNotFoundError(f"chromedriver.exe not found in any expected location: {possible_paths}")
        except Exception as e:
            print(f"Error resolving chromedriver path: {e}")
            raise

    def start_driver(self) -> Tuple[webdriver.Chrome, subprocess.Popen]:
        """Start Chrome WebDriver with configured options."""
        try:
            chrome_options = webdriver.ChromeOptions()

            if self.config.headless_mode:
                chrome_options.add_argument("--headless")

            # Setup startup info for Windows
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # Start ChromeDriver service
            self.service_process = subprocess.Popen(
                [self.chrome_driver_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startup_info
            )

            # Initialize WebDriver (Selenium 4.6+ recommended way)
            service = Service(self.chrome_driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)

            return self.driver, self.service_process

        except Exception as e:
            print(f"Failed to start Chrome WebDriver: {e}")
            raise

    def wait_for_element(self, by: By, value: str, timeout: int = None) -> Optional[any]:
        """Wait for element to be present and return it."""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")

        timeout = timeout or self.config.default_timeout

        try:
            # Ensure 'by' is a string if needed
            locator = (by.value if hasattr(by, 'value') else by, value)
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            print(f"Element with {by}='{value}' not found within {timeout} seconds.")
            return None

    def click_element_safe(self, by: By, value: str, timeout: int = None) -> bool:
        """Safely click an element with error handling."""
        element = self.wait_for_element(by, value, timeout)
        if element:
            try:
                element.click()
                return True
            except Exception as e:
                print(f"Failed to click element {by}='{value}': {e}")
                return False
        return False

    def move_to_element_and_click(self, by: By, value: str, timeout: int = None) -> bool:
        """Move to element and click with ActionChains."""
        element = self.wait_for_element(by, value, timeout)
        if element:
            try:
                actions = ActionChains(self.driver)
                actions.move_to_element(element).perform()

                if element.is_displayed():
                    element.click()
                    return True
                else:
                    print(f"Element {by}='{value}' is not visible")
                    return False
            except Exception as e:
                print(f"Failed to interact with element {by}='{value}': {e}")
                return False
        return False

    def set_window_position_and_size(self, x: int, y: int, width: int, height: int):
        """Set window position and size."""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")

        try:
            self.driver.set_window_position(x, y)
            self.driver.set_window_size(width, height)
        except Exception as e:
            print(f"Failed to set window position/size: {e}")

    def navigate_to(self, url: str):
        """Navigate to specified URL."""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")

        try:
            self.driver.get(url)
            print(f"Navigated to: {self.driver.title}")
        except Exception as e:
            print(f"Failed to navigate to {url}: {e}")

    def quit_driver(self):
        """Safely quit the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error occurred while closing browser: {e}")

        if self.service_process:
            try:
                self.service_process.terminate()
            except Exception as e:
                print(f"Error terminating ChromeDriver process: {e}")


class ProcessManager:
    """Manages browser processes and cleanup."""

    @staticmethod
    def terminate_remaining_chromedriver_processes():
        """Terminate any remaining ChromeDriver processes."""
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if 'chromedriver.exe' in process.info['name']:
                    print(f"Terminating remaining ChromeDriver process: {process.info['pid']}")
                    process.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    @staticmethod
    def monitor_browser_close(driver_manager: WebDriverManager):
        """Monitor browser window and close when all windows are closed."""
        try:
            while driver_manager.driver and driver_manager.driver.window_handles:
                time.sleep(1)
            driver_manager.quit_driver()
        except Exception as e:
            print(f"Error in browser monitoring: {e}")
            driver_manager.quit_driver()
