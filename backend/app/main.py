"""
FIT-DNA FastAPI Backend
메인 애플리케이션 진입점
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.core.config import settings
from app.routers import (
    auth,
    fitdna,
    daily_health,
    facilities,
    matching,
    reports,
)

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="FIT-DNA 체력 MBTI 플랫폼 API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS 설정 (개발 환경)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",  # 모든 origin 허용 (정규식)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["인증"])
app.include_router(fitdna.router, prefix="/api/fitdna", tags=["FIT-DNA 검사"])
app.include_router(daily_health.router, prefix="/api/daily", tags=["하루 건강 체크"])
app.include_router(facilities.router, prefix="/api/facilities", tags=["위치 기반 시설"])
app.include_router(matching.router, prefix="/api/matching", tags=["운동 메이트 매칭"])
app.include_router(reports.router, prefix="/api/reports", tags=["마이페이지 리포트"])


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "FIT-DNA API Server",
        "version": settings.VERSION,
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


# 정적 파일 서빙 (웹 디렉토리)
WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "web")
if os.path.exists(WEB_DIR):
    app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

    @app.get("/test")
    async def serve_test_page():
        """테스트 페이지 제공"""
        test_file = os.path.join(WEB_DIR, "test-integration.html")
        return FileResponse(test_file)
