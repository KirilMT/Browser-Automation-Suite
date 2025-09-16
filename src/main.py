"""
Automation System Entry Point
This script initializes and runs the browser automation system.
"""

from automation_system import AutomationSystem
from config_models import AutomationConfig

def main():
    """Main function that starts the automation system."""
    # Try to load local configuration, fall back to example config
    try:
        from config import LOCAL_APP_CONFIG
        print("Loaded local configuration from config.py.")
        config = AutomationConfig(LOCAL_APP_CONFIG)
    except ImportError:
        print("No local configuration found. Loading from example_config.py.")
        from example_config import LOCAL_APP_CONFIG
        config = AutomationConfig(LOCAL_APP_CONFIG)

    # Create and run the automation system
    automation_system = AutomationSystem(config)

    try:
        print("Initializing automation system...")
        automation_system.start_automation()

        print("Automation system is running. Close browser windows to exit.")
        automation_system.wait_for_completion()

    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Shutting down gracefully...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation_system.cleanup()

if __name__ == "__main__":
    main()
