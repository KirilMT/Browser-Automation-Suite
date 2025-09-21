"""
Automation System Entry Point
This script initializes and runs the browser automation system.
"""
import logging
from automation_system import AutomationSystem
from config_models import AutomationConfig
from logger_config import setup_logging

def main():
    """Main function that starts the automation system."""
    setup_logging()

    # Try to load local configuration, fall back to example config
    try:
        from config import LOCAL_APP_CONFIG
        logging.info("Loaded local configuration from config.py.")
    except ImportError:
        logging.info("No local configuration found. Loading from example_config.py.")
        from example_config import LOCAL_APP_CONFIG
    config_dict = LOCAL_APP_CONFIG

    # Ensure filters and enabled exist
    if "filters" not in config_dict:
        logging.warning("'filters' section missing in config. Setting default.")
        config_dict["filters"] = {"enabled": True, "selectors": []}
    if "enabled" not in config_dict["filters"]:
        logging.warning("'enabled' flag missing in filters. Setting default True.")
        config_dict["filters"]["enabled"] = True

    # Ensure test_env_host and test_env_port exist
    test_env_host = config_dict.get("test_env_host", "localhost")
    test_env_port = config_dict.get("test_env_port", 8000)

    config = AutomationConfig(config_dict)

    # Launch test environment server if in test mode
    test_env_server = None
    if hasattr(config, 'filters') and hasattr(config.filters, 'enabled') and config.filters.enabled is False:
        logging.info(f"Test environment detected: launching local test server at {test_env_host}:{test_env_port} ...")
        from test_env.server_manager import TestEnvServerManager
        test_env_server = TestEnvServerManager(host=test_env_host, port=test_env_port)
        test_env_server.start()

    # Create and run the automation system
    automation_system = AutomationSystem(config)

    try:
        logging.info("Initializing automation system...")
        automation_system.start_automation()

        # Re-apply logging configuration to override selenium's settings
        setup_logging()

        logging.info("Automation system is running. Press Ctrl+C to exit.")
        automation_system.wait_for_completion()

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
    finally:
        logging.info("Shutting down...")
        automation_system.cleanup()
        if test_env_server:
            test_env_server.stop()

if __name__ == "__main__":
    main()
