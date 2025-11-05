#!/usr/bin/env python3
"""
Simple HTTP server to serve the Tech Momentum Arbitrage Engine frontend
Run with: python3 server.py
Access at: http://localhost:8000
"""

import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print("=" * 80)
        print("TECH MOMENTUM ARBITRAGE ENGINE - FRONTEND SERVER")
        print("=" * 80)
        print(f"\n✅ Server running at: http://localhost:{PORT}")
        print(f"📊 Dashboard: http://localhost:{PORT}/index.html")
        print(f"\n🛑 Press Ctrl+C to stop\n")
        print("=" * 80)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped")
