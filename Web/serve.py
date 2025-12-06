"""
간단한 HTTP 서버로 테스트 페이지 제공
CORS 문제 해결을 위해 file:// 대신 http://로 서빙
"""
import http.server
import socketserver
import os

PORT = 8002
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # CORS 헤더 추가
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"웹 서버 시작: http://localhost:{PORT}")
        print(f"테스트 페이지: http://localhost:{PORT}/test-integration.html")
        print("종료하려면 Ctrl+C를 누르세요")
        httpd.serve_forever()
