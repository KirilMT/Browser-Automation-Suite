import http.server
import socketserver
import os
import sys

class TestEnvServer:
    """
    Simple HTTP server for serving test_env/pages/ for browser automation testing.
    """
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.directory = os.path.join(os.path.dirname(__file__), 'pages')

    def run(self):
        os.chdir(self.directory)
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"Serving test environment at http://{self.host}:{self.port}/")
            print(f"Serving files from: {self.directory}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped by user.")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                httpd.server_close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Launch local server for test_env/pages/")
    parser.add_argument('--host', default='localhost', help='Host to bind (default: localhost)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind (default: 8000)')
    args = parser.parse_args()
    server = TestEnvServer(host=args.host, port=args.port)
    server.run()

