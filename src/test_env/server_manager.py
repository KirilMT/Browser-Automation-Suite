import subprocess
import sys
import os
import signal

class TestEnvServerManager:
    """
    Manages the test environment HTTP server as a subprocess.
    """
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.process = None
        self.script_path = os.path.join(os.path.dirname(__file__), 'serve_test_env.py')

    def start(self):
        if self.process is not None and self.process.poll() is None:
            print("Test environment server is already running.")
            return
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.script_path, '--host', self.host, '--port', str(self.port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(self.script_path)
            )
            print(f"Test environment server started at http://{self.host}:{self.port}/")
        except Exception as e:
            print(f"Failed to start test environment server: {e}")
            self.process = None

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                if sys.platform == 'win32':
                    self.process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    self.process.terminate()
                self.process.wait(timeout=5)
                print("Test environment server stopped.")
            except Exception as e:
                print(f"Failed to stop test environment server: {e}")
        self.process = None

