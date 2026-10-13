#!/usr/bin/env python3
"""HP 键盘网页驱动离线版 —— 本地服务器。

WebHID 只在安全上下文（https 或 localhost）下可用，所以必须通过
http://127.0.0.1 打开，不能直接双击 index.html（file:// 不行）。

用法: python3 serve.py [端口]   默认端口 8787
"""
import http.server
import os
import sys
import threading
import webbrowser

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
_ports = [a for a in sys.argv[1:] if a.isdigit()]
PORT = int(_ports[0]) if _ports else 8787


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        # 单页应用：不存在的路径一律回退到 index.html
        path = self.translate_path(self.path)
        if not os.path.exists(path):
            self.path = "/index.html"
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def main():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"离线驱动已启动: {url}")
    print("请用 Chrome / Edge 打开（Firefox 不支持 WebHID）。按 Ctrl+C 退出。")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
