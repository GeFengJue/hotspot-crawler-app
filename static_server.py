#!/usr/bin/env python3
"""
静态文件服务器，用于提供前端页面
解决文件协议下的跨域限制问题
"""

import http.server
import socketserver
import webbrowser
import os
import threading
from datetime import datetime

class StaticFileHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 先调用父类方法处理请求
        result = super().do_GET()
        
        # 设置CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # 设置缓存控制
        if self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        else:
            self.send_header('Cache-Control', 'public, max-age=3600')
        
        return result
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - {self.address_string()} - {format % args}")

def start_static_server(port=8080):
    """启动静态文件服务器"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", port), StaticFileHandler) as httpd:
        print("=" * 60)
        print("静态文件服务器启动")
        print("=" * 60)
        print(f"服务器运行在: http://localhost:{port}")
        print(f"前端页面: http://localhost:{port}/index.html")
        print("=" * 60)
        print("按 Ctrl+C 停止服务器")
        
        # 在浏览器中打开页面
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{port}/index.html')).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    start_static_server(port)