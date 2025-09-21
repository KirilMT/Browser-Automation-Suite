"""
Configuration for the application's logging system.
"""
import logging
import sys

def setup_logging():
    """
    Configures the root logger for the application.
    - Logs INFO and higher level messages.
    - Outputs to the console.
    - Uses a standardized format for log messages.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
