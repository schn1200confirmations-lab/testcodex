from __future__ import annotations

import http.server
import os
import socketserver
import webbrowser
from pathlib import Path

PORT = int(os.environ.get('PORT', '8000'))
ROOT = Path(__file__).resolve().parent


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    os.chdir(ROOT)
    handler = http.server.SimpleHTTPRequestHandler
    with ReusableTCPServer(('', PORT), handler) as httpd:
        url = f'http://localhost:{PORT}/index.html'
        print(f'Serving Task Planner Dashboard from: {ROOT}')
        print(f'Open this URL in your browser: {url}')
        try:
            webbrowser.open(url)
        except Exception:
            pass
        httpd.serve_forever()
