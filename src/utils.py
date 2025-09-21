"""
Utility functions for the automation suite.
"""
import logging
import os
import sys

def get_chromedriver_path() -> str:
    """Resolves the path to chromedriver.exe for both development and PyInstaller builds."""
    try:
        if getattr(sys, 'frozen', False):
            # Running as a PyInstaller bundle
            base_path = sys._MEIPASS
        else:
            # Running in development
            base_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

        # When running from src, the path is relative to the root, so go up one level
        if os.path.basename(base_path) == 'src':
            base_path = os.path.dirname(base_path)

        # Path within the src directory for both dev and bundled app
        chromedriver_rel_path = os.path.join('src', 'chromedriver.exe')

        # Check two possible locations: relative to root and within a 'src' subdir of root
        possible_paths = [
            os.path.join(base_path, chromedriver_rel_path),
            os.path.join(os.path.dirname(base_path), chromedriver_rel_path)
        ]

        for path in possible_paths:
            if os.path.exists(path):
                logging.debug(f"Resolved chromedriver.exe path: {path}")
                return path

        raise FileNotFoundError(f"chromedriver.exe not found in any expected location: {possible_paths}")

    except Exception as e:
        logging.error(f"Error resolving chromedriver path: {e}", exc_info=True)
        raise
