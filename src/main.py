"""
Automation System Entry Point
This script initializes and runs the browser automation system.
"""
import subprocess
import atexit

from automation_system import AutomationSystem
from config_models import AutomationConfig

def main():
    """Main function that starts the automation system."""
    server_process = None
    # Try to load local configuration, fall back to example config
    try:
        from config import LOCAL_APP_CONFIG
        print("Loaded local configuration from config.py.")
        config = AutomationConfig(LOCAL_APP_CONFIG)
    except ImportError:
        print("No local configuration found. Loading from example_config.py.")
        from example_config import LOCAL_APP_CONFIG
        config = AutomationConfig(LOCAL_APP_CONFIG)

    # If test environment is enabled, start the local server
    if not config.filters.enabled:
        try:
            server_command = ["python", "src/test_env/server.py"]
            server_process = subprocess.Popen(server_command)
            print("Local test server started.")

            def cleanup_server():
                if server_process:
                    print("Stopping local test server...")
                    server_process.terminate()
                    server_process.wait()
                    print("Local test server stopped.")

            atexit.register(cleanup_server)

        except FileNotFoundError:
            print("Could not start local test server. Make sure Python is in your PATH.")
        except Exception as e:
            print(f"An error occurred while starting the server: {e}")

    # Create and run the automation system
    automation_system = AutomationSystem(config)

    try:
        print("Initializing automation system...")
        automation_system.start_automation()

        print("Automation system is running. Close browser windows to exit.")
        automation_system.wait_for_completion()

    except KeyboardInterrupt:
        print("\nAutomation interrupted by user.")
    finally:
        print("Shutting down automation system.")
        # The atexit handler will take care of stopping the server.

if __name__ == "__main__":
    main()
