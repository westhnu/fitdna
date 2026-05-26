"""
애플리케이션 설정
환경 변수 및 설정 관리
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # 프로젝트 정보
    PROJECT_NAME: str = "FIT-DNA API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FIT-DNA 체력 MBTI 플랫폼"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "null",  # 로컬 파일 (file://)에서 접근 허용
    ]

    # 데이터베이스
    DATABASE_URL: str = "sqlite:///./fitdna.db"  # 개발용 SQLite
    # PostgreSQL 예시: "postgresql://user:password@localhost/fitdna"

    # JWT 인증 — SECRET_KEY는 환경변수로 반드시 설정. 미설정 시 startup에서 raise.
    SECRET_KEY: str = ""  # set via env (.env or process env)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    # 파일 업로드
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # 외부 API (날씨, 지도 등)
    WEATHER_API_KEY: str = ""
    KAKAO_REST_API_KEY: str = ""

    # 모델 파일 경로 (data/ 로 이동됨)
    FITDNA_REFERENCE_TABLE: str = "../data/fitdna_original_reference.pkl"
    EXERCISE_RECOMMENDATION_FILE: str = "../data/phase2_classified_exercise_database.csv"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Fail fast — production 에서는 절대 startup 가능 X
if not settings.SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY가 비어있습니다. backend/.env 또는 환경변수로 설정하세요. "
        "예: SECRET_KEY=$(openssl rand -hex 32)"
    )
