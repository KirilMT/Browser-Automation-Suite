"""
Automation System Entry Point
This script initializes and runs the browser automation system.
"""
import logging
import sys
from automation_system import AutomationSystem
from config_models import AutomationConfig
from logger_config import setup_logging

def main():
    """Main function that starts the automation system."""
    try:
        setup_logging()

        # Try to load local configuration, fall back to example config
        try:
            from config import LOCAL_APP_CONFIG
            logging.info("Loaded local configuration from config.py.")
        except ImportError:
            logging.info("No local configuration found. Loading from example_config.py.")
            from example_config import LOCAL_APP_CONFIG
        config_dict = LOCAL_APP_CONFIG

        # ... (rest of the configuration setup remains the same)
        test_env_host = config_dict.get("test_env_host", "localhost")
        test_env_port = config_dict.get("test_env_port", 8000)
        config = AutomationConfig(config_dict)

        # Launch test environment server if in test mode
        test_env_server = None
        if not config.filters.enabled:
            logging.info(f"Test environment detected: launching local test server at {test_env_host}:{test_env_port} ...")
            from tests.server_manager import TestEnvServerManager
            test_env_server = TestEnvServerManager(host=test_env_host, port=test_env_port)
            test_env_server.start()

        # Create and run the automation system
        automation_system = AutomationSystem(config)
        automation_system.start_automation()

        logging.info("Automation system is running. Press Ctrl+C to exit.")
        automation_system.wait_for_completion()

    except Exception:
        logging.exception("A critical error occurred during application execution.")
    finally:
        logging.info("Shutting down...")
        if 'automation_system' in locals() and automation_system:
            automation_system.cleanup()
        if 'test_env_server' in locals() and test_env_server:
            test_env_server.stop()
        
        # If running as a bundled executable, pause before exiting
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            input("Press Enter to exit...")

if __name__ == "__main__":
    main()
