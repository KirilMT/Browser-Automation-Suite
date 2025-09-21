import http.server
import socketserver
import threading
import os
import sys
import logging

class TestEnvServerManager:
    """
    Manages an in-process HTTP server in a separate thread.
    """
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server_thread = None
        self.httpd = None

    def _get_pages_directory(self):
        """Determine the correct directory for the test pages."""
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running as a bundled executable
            return os.path.join(sys._MEIPASS, 'tests', 'pages')
        else:
            # Running in a normal Python environment
            return os.path.join(os.path.dirname(__file__), 'pages')

    def start(self):
        """Start the HTTP server in a background thread."""
        if self.server_thread and self.server_thread.is_alive():
            logging.warning("Test environment server is already running.")
            return

        pages_dir = self._get_pages_directory()
        if not os.path.isdir(pages_dir):
            logging.error(f"Test pages directory not found at: {pages_dir}")
            return

        # Custom handler to serve files from the correct directory
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=pages_dir, **kwargs)

        try:
            self.httpd = socketserver.TCPServer((self.host, self.port), Handler)
            self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.server_thread.start()
            logging.info(f"Test environment server started at http://{self.host}:{self.port}/, serving from {pages_dir}")
        except Exception as e:
            logging.error(f"Failed to start test environment server: {e}", exc_info=True)
            self.httpd = None

    def stop(self):
        """Stop the HTTP server."""
        if self.httpd:
            logging.info("Shutting down test environment server...")
            self.httpd.shutdown()  # Shuts down the server loop
            self.httpd.server_close()  # Closes the server socket
            self.httpd = None
            logging.info("Test environment server stopped.")
