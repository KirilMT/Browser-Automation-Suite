import http.server
import socketserver
import os
import sys
import logging

class TestEnvServer:
    """
    Simple HTTP server for serving tests/pages/ for browser automation testing.
    """
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.directory = os.path.join(os.path.dirname(__file__), 'pages')

    def run(self):
        os.chdir(self.directory)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            logging.info(f"Serving test environment at http://{self.host}:{self.port}/")
            logging.info(f"Serving files from: {self.directory}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logging.info("Server stopped by user.")
            except Exception as e:
                logging.error(f"Error: {e}", exc_info=True)
            finally:
                httpd.server_close()

if __name__ == "__main__":
    import argparse
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    parser = argparse.ArgumentParser(description="Launch local server for tests/pages/")
    parser.add_argument('--host', default='localhost', help='Host to bind (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind (default: 8000)')
    args = parser.parse_args()
    server = TestEnvServer(host=args.host, port=args.port)
    server.run()

