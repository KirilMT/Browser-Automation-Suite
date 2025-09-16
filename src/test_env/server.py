import http.server
import socketserver
import os

PORT = 8000
PAGES_DIR = os.path.join(os.path.dirname(__file__), 'pages')
os.makedirs(PAGES_DIR, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PAGES_DIR, **kwargs)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Starting local test server at http://localhost:{PORT}")
        print(f"Serving files from: {os.path.abspath(PAGES_DIR)}")
        print("Press Ctrl+C to stop the server.")
        httpd.serve_forever()
