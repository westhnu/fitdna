"""
백엔드 서버 실행 스크립트
"""

import uvicorn
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("FIT-DNA Backend Server Starting...")
    print("API Docs: http://localhost:8001/api/docs")
    print("ReDoc: http://localhost:8001/api/redoc")
    print("\n")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,  # Django와 충돌 방지를 위해 8001 사용
        reload=True,  # 개발 모드: 파일 변경 시 자동 재시작
        log_level="info"
    )
