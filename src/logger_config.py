"""
Configuration for the application's logging system.
"""
import logging
import sys

def setup_logging():
    """
    Configures the root logger for the application.
    This function is designed to be called multiple times, and will reset the
    logging configuration each time.
    """
    # Get the root logger
    root_logger = logging.getLogger()

    # Remove any existing handlers
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Configure the logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )

    # Set the logging level for noisy libraries to WARNING
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
