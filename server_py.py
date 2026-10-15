#!/usr/bin/env python3
"""Finanzas server: static files + borradores API on port 3001"""
import http.server, json, os
from pathlib import Path

BASE       = Path(__file__).parent
PUBLIC     = BASE / 'public'
BORRADORES = BASE.parent / 'Estados de cuenta' / 'borradores.json'
PORT       = 3001

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors(); self.end_headers()

    def do_GET(self):
        if self.path == '/api/borradores':
            try:
                data = json.loads(BORRADORES.read_text('utf-8')) if BORRADORES.exists() else []
            except Exception:
                data = []
            self._json(200, data)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/borradores':
            length = int(self.headers.get('Content-Length', 0))
            try:
                data = json.loads(self.rfile.read(length))
                BORRADORES.write_text(json.dumps(data, ensure_ascii=False, indent=2), 'utf-8')
                self._json(200, {'ok': True, 'count': len(data)})
            except Exception as e:
                self._json(500, {'ok': False, 'error': str(e)})
        else:
            self.send_error(404)

    def _json(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self._cors()
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def log_message(self, fmt, *args):
        pass  # silencioso

if __name__ == '__main__':
    server = http.server.HTTPServer(('', PORT), Handler)
    print(f'Finanzas → http://localhost:{PORT}')
    server.serve_forever()
