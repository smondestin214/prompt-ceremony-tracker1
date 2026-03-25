"""
Prompt Engineering Ceremony Tracker — Shared Server
Zero dependencies. Run with: python3 server.py
Team members connect to http://<your-ip>:8080
"""

import json
import os
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared-data.json")
PORT = 8080
lock = threading.Lock()


def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            directory=os.path.dirname(os.path.abspath(__file__)),
            **kwargs,
        )

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/projects":
            with lock:
                data = read_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/projects":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                if not isinstance(data, list):
                    raise ValueError("Expected a list")
                with lock:
                    write_data(data)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True}).encode())
            except (json.JSONDecodeError, ValueError) as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Quieter logging — only show API calls
        if "/api/" in str(args[0]):
            super().log_message(format, *args)


if __name__ == "__main__":
    print(f"Starting Ceremony Tracker server on port {PORT}...")
    print(f"Data file: {DATA_FILE}")
    print()

    # Show local network IPs for sharing
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
        print(f"Share with your team:")
        print(f"  http://{local_ip}:{PORT}")
    except socket.gaierror:
        pass
    print(f"  http://localhost:{PORT}")
    print()
    print("Press Ctrl+C to stop.")
    print()

    server = HTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
