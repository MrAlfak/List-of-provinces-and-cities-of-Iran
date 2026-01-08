import http.server
import socketserver
import json
import os

PORT = 8000

class IranDataAPI(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/provinces':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open('iran_cities.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path.startswith('/api/province/'):
            # Example: /api/province/Tehran
            eng_name = self.path.split('/')[-1].lower()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            with open('iran_cities.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            result = next((p for p in data if p['english_name'].lower() == eng_name), None)
            if result:
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": "Province not found"}, ensure_ascii=False).encode('utf-8'))
        else:
            # Serve index.html or other files
            super().do_GET()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), IranDataAPI) as httpd:
        print(f"🚀 Iran Cities API Server running at http://localhost:{PORT}")
        print(f"📍 Provinces List: http://localhost:{PORT}/api/provinces")
        print(f"📍 Single Province: http://localhost:{PORT}/api/province/Tehran")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.server_close()
