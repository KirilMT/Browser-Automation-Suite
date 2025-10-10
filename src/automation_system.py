"""
Main automation system.
Orchestrates multiple browser instances for web automation.
"""
import threading
from typing import Dict, List, Optional

from config_models import AutomationConfig
from browser_automation import WebDriverManager, ProcessManager

# Try to load local handlers, fall back to example handlers
try:
    from app_handlers import Page1Handler, Page2Handler
    print("Loaded local handlers from app_handlers.py.")
except ImportError:
    print("No local handlers found. Loading from example_app_handlers.py.")
    from example_app_handlers import Page1Handler, Page2Handler


class AutomationSystem:
    """Main class that coordinates browser automation."""

    def __init__(self, config: Optional[AutomationConfig] = None):
        self.config = config or AutomationConfig()
        self.driver_managers: List[WebDriverManager] = []
        self.threads: List[threading.Thread] = []
        self.monitor_threads: List[threading.Thread] = []
        self.is_running = False

    def start_automation(self):
        """Start the complete automation system."""
        print("Starting automation system...")

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

            # Start monitoring threads
            self._start_monitoring_threads()

            self.is_running = True
            print("Automation system started successfully")

        except Exception as e:
            print(f"Failed to start automation: {e}")
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

    def _start_monitoring_threads(self):
        """Start browser monitoring threads."""
        for i, driver_manager in enumerate(self.driver_managers):
            monitor_thread = threading.Thread(
                target=ProcessManager.monitor_browser_close,
                args=(driver_manager,),
                name=f"BrowserMonitor-{i+1}"
            )
            self.monitor_threads.append(monitor_thread)
            monitor_thread.start()

    def _run_page1_automation(self, handler: Page1Handler):
        """Run page 1 automation logic."""
        try:
            print("Starting page 1 automation...")
            handler.navigate_and_setup()

            # TODO: Add any continuous monitoring logic here
            # For now, just keep the page open

        except Exception as e:
            print(f"Error in page 1 automation: {e}")

    def _run_page2_automation(self, handler: Page2Handler):
        """Run page 2 automation logic."""
        try:
            print("Starting page 2 automation...")
            handler.navigate_and_setup()

            # TODO: Add any continuous monitoring logic here
            # For now, just keep the page open

        except Exception as e:
            print(f"Error in page 2 automation: {e}")

    def wait_for_completion(self):
        """Wait for all automation threads to complete."""
        if not self.is_running:
            print("Automation system is not running")
            return

        try:
            # Wait for monitoring threads to complete
            for monitor_thread in self.monitor_threads:
                monitor_thread.join()

            print("All browser windows have been closed")

        except KeyboardInterrupt:
            print("Received keyboard interrupt, shutting down...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources and terminate processes."""
        print("Cleaning up automation system...")

        # Quit all drivers
        for driver_manager in self.driver_managers:
            driver_manager.quit_driver()

        # Terminate remaining ChromeDriver processes
        ProcessManager.terminate_remaining_chromedriver_processes()

        self.is_running = False
        print("Cleanup completed")

    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            'is_running': self.is_running,
            'active_drivers': len([dm for dm in self.driver_managers if dm.driver]),
            'active_threads': len([t for t in self.threads if t.is_alive()]),
            'active_monitors': len([t for t in self.monitor_threads if t.is_alive()])
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
        print(f"Automation failed: {e}")
    finally:
        automation_system.cleanup()
        print("Automation system terminated")


if __name__ == "__main__":
    main()
