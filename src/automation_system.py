from __future__ import annotations
"""
Main automation system.
Orchestrates multiple browser instances for web automation.
"""
import logging
import threading
import time
from typing import Dict, List, Optional

from config_models import AutomationConfig
from browser_automation import WebDriverManager, ProcessManager

# Try to load local handlers, fall back to example handlers
try:
    from app_handlers import Page1Handler, Page2Handler
    logging.info("Loaded local handlers from app_handlers.py.")
except ImportError:
    logging.info("No local handlers found. Loading from example_app_handlers.py.")
    from example_app_handlers import Page1Handler, Page2Handler


class AutomationSystem:
    """Main class that coordinates browser automation."""

    def __init__(self, config: Optional[AutomationConfig] = None):
        self.config = config or AutomationConfig()
        self.driver_managers: List[WebDriverManager] = []
        self.threads: List[threading.Thread] = []
        self.is_running = False
        self.shutdown_event = threading.Event()

    def start_automation(self):
        """Start the complete automation system."""
        logging.info("Starting automation system...")

        try:
            # Initialize driver managers
            page1_driver = WebDriverManager(self.config.webdriver)
            page2_driver = WebDriverManager(self.config.webdriver)

            # Start drivers
            page1_driver.start_driver()
            page2_driver.start_driver()

            self.driver_managers = [page1_driver, page2_driver]

            # Determine test mode
            test_mode = hasattr(self.config, 'filters') and hasattr(self.config.filters, 'enabled') and not self.config.filters.enabled

            # Create page handlers with test_mode flag
            page1_handler = Page1Handler(page1_driver, self.config, test_mode=test_mode)
            page2_handler = Page2Handler(page2_driver, self.config, test_mode=test_mode)

            # Start automation threads
            self._start_automation_threads(page1_handler, page2_handler)

            self.is_running = True
            logging.info("Automation system started successfully")

        except Exception as e:
            logging.error(f"Failed to start automation: {e}", exc_info=True)
            self.cleanup()
            raise

    def _start_automation_threads(self, page1_handler: Page1Handler,
                                page2_handler: Page2Handler):
        """Start the main automation threads."""
        # Page 1 thread
        page1_thread = threading.Thread(
            target=self._run_page1_automation,
            args=(page1_handler,),
            name="Page1Automation"
        )

        # Page 2 thread
        page2_thread = threading.Thread(
            target=self._run_page2_automation,
            args=(page2_handler,),
            name="Page2Automation"
        )

        self.threads = [page1_thread, page2_thread]

        # Start threads
        for thread in self.threads:
            thread.start()

    def _run_page1_automation(self, handler: Page1Handler):
        """Run page 1 automation logic."""
        try:
            logging.info("Starting page 1 automation...")
            handler.navigate_and_setup()
            self.shutdown_event.wait()  # Keep the page open until shutdown is signaled

        except Exception as e:
            if not self.shutdown_event.is_set():
                logging.error(f"Error in page 1 automation: {e}", exc_info=True)

    def _run_page2_automation(self, handler: Page2Handler):
        """Run page 2 automation logic."""
        try:
            logging.info("Starting page 2 automation...")
            handler.navigate_and_setup()
            self.shutdown_event.wait()  # Keep the page open until shutdown is signaled

        except Exception as e:
            if not self.shutdown_event.is_set():
                logging.error(f"Error in page 2 automation: {e}", exc_info=True)

    def wait_for_completion(self):
        """Wait for all automation threads to complete."""
        try:
            while self.is_running:
                time.sleep(1)  # Just wait until cleanup is called
        except KeyboardInterrupt:
            logging.info("Received keyboard interrupt, shutting down...")
            # The cleanup is handled by the finally block in main.py

    def cleanup(self):
        """Clean up resources and terminate processes."""
        if not self.is_running:
            return

        logging.info("Cleaning up automation system...")
        self.shutdown_event.set()

        # Wait for automation threads to finish
        for thread in self.threads:
            thread.join()

        # Quit all drivers
        for driver_manager in self.driver_managers:
            driver_manager.quit_driver()

        # Terminate remaining ChromeDriver processes
        ProcessManager.terminate_remaining_chromedriver_processes()

        self.is_running = False
        logging.info("Cleanup completed")

    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            'is_running': self.is_running,
            'active_drivers': len([dm for dm in self.driver_managers if dm.driver]),
            'active_threads': len([t for t in self.threads if t.is_alive()]),
        }


def main():
    """Main entry point for the automation system."""
    # Create default configuration
    config = AutomationConfig()

    # You can customize configuration here or load from external source
    # Example of customizing URLs:
    # config.urls.base_url = "https://your-custom-system.com/app"
    # config.urls.page1_path = "/path/to/page1"
    # config.urls.page2_path = "/path/to/page2"

    # Create and start automation system
    automation_system = AutomationSystem(config)

    try:
        automation_system.start_automation()
        automation_system.wait_for_completion()
    except Exception as e:
        logging.error(f"Automation failed: {e}", exc_info=True)
    finally:
        automation_system.cleanup()
        logging.info("Automation system terminated")


if __name__ == "__main__":
    main()
