#!/usr/bin/env python3
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

CONFIG_FILE = 'config.json'
PORT = 8765

class ConfigHandler(SimpleHTTPRequestHandler):
    """HTTP Handler với endpoint API cho config"""
    
    def do_GET(self):
        """GET /api/config - Trả về config hiện tại"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/config':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = f.read()
            else:
                config = json.dumps({})
            
            self.wfile.write(config.encode())
            return
        
        # Mặc định phục vụ file tĩnh
        super().do_GET()
    
    def do_POST(self):
        """POST /api/config - Lưu config từ Chrome"""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/config':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                config = json.loads(body.decode('utf-8'))
                
                # Lưu vào file
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                # Trả response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok', 'message': 'Config saved'}).encode())
                
                print(f"[✓] Config saved to {CONFIG_FILE}")
                return
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}).encode())
                print(f"[!] Error: {e}")
                return
        
        super().do_POST()
    
    def do_OPTIONS(self):
        """CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """Thêm CORS headers vào tất cả responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        if '200' in format or '304' in format:
            print(f"[•] {args[0]}")
        elif '404' in format:
            print(f"[!] 404: {args[0]}")
        else:
            print(f"[*] {format % args}")

def main():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, ConfigHandler)
    
    print("\n" + "="*50)
    print(f"  OBS Sync Server - HIẾU BÙI BĐS 24H")
    print("="*50)
    print(f"\n  ✓ Server đang chạy tại:")
    print(f"    http://localhost:{PORT}\n")
    print(f"  📍 Trang chính (Chrome):")
    print(f"    http://localhost:{PORT}/ok_khung_live_v2.html\n")
    print(f"  📍 OBS Browser Source:")
    print(f"    http://localhost:{PORT}/ok_khung_live_v2.html?obs=1\n")
    print(f"  📍 API Config:")
    print(f"    GET  http://localhost:{PORT}/api/config")
    print(f"    POST http://localhost:{PORT}/api/config\n")
    print(f"  💾 File config: {os.path.abspath(CONFIG_FILE)}\n")
    print("="*50)
    print("  [!] Nhấn Ctrl+C để tắt server")
    print("="*50 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[✓] Server đã dừng.")
        sys.exit(0)

if __name__ == '__main__':
    main()
