# FIT-DNA Backend API

FIT-DNA 체력 MBTI 플랫폼의 FastAPI 기반 백엔드 서버

## 📋 프로젝트 구조

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── core/
│   │   ├── config.py          # 설정 관리
│   │   └── security.py        # 인증/보안 (예정)
│   ├── routers/               # API 엔드포인트
│   │   ├── auth.py           # 인증 (회원가입/로그인)
│   │   ├── fitdna.py         # FIT-DNA 검사
│   │   ├── daily_health.py   # 하루 건강 체크
│   │   ├── facilities.py     # 위치 기반 시설
│   │   ├── matching.py       # 운동 메이트 매칭
│   │   └── reports.py        # 마이페이지 리포트
│   ├── models/                # DB 모델 (예정)
│   ├── schemas/               # Pydantic 스키마 (예정)
│   ├── services/              # 비즈니스 로직 (예정)
│   └── utils/                 # 유틸리티 함수 (예정)
├── requirements.txt
├── .env.example
└── README.md (이 파일)
```

## 🚀 빠른 시작

### 1. 가상환경 생성 및 활성화

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 수정 (DB 연결 정보, API 키 등)
```

### 4. 서버 실행

```bash
# 개발 모드 (auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. API 문서 확인

서버 실행 후 브라우저에서:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## 📚 API 엔드포인트

### 인증 (Authentication)
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃
- `GET /api/auth/me` - 내 정보 조회

### FIT-DNA 검사
- `POST /api/fitdna/basic-info` - 기본 정보 입력
- `POST /api/fitdna/measurements` - 체력 측정값 입력
- `POST /api/fitdna/survey` - 라이프스타일 설문
- `POST /api/fitdna/calculate` - FIT-DNA 계산
- `GET /api/fitdna/result/{user_id}` - 결과 조회
- `GET /api/fitdna/types` - 모든 유형 정보

### 하루 건강 체크
- `POST /api/daily/condition` - 컨디션 체크
- `GET /api/daily/injury-risk` - 부상 위험도 분석
- `GET /api/daily/prevention-routine` - 예방 루틴 추천
- `GET /api/daily/risk-history` - 위험도 이력

### 위치 기반 시설
- `GET /api/facilities/nearby` - 주변 시설 조회
- `GET /api/facilities/{facility_id}` - 시설 상세 정보
- `GET /api/facilities/weather-recommendation` - 날씨 기반 추천

### 운동 메이트 매칭
- `POST /api/matching/preferences` - 매칭 선호도 설정
- `POST /api/matching/request` - 매칭 요청
- `GET /api/matching/results` - 매칭 결과
- `GET /api/matching/candidate/{id}` - 후보자 상세
- `POST /api/matching/request/{id}` - 매칭 신청
- `POST /api/matching/accept/{id}` - 매칭 수락
- `GET /api/matching/my-matches` - 내 매칭 목록

### 마이페이지 리포트
- `GET /api/reports/monthly/{user_id}` - 월간 리포트
- `POST /api/reports/workout-sessions` - 운동 기록 저장
- `GET /api/reports/workout-sessions/{user_id}` - 운동 기록 조회
- `GET /api/reports/fitdna-history/{user_id}` - FIT-DNA 이력
- `POST /api/reports/request-retest` - 재검 요청
- `GET /api/reports/statistics/{user_id}` - 사용자 통계
- `GET /api/reports/goals/{user_id}` - 목표 조회

## 🔧 개발 상태

### ✅ 완료
- [x] 백엔드 프로젝트 구조 설계
- [x] API 엔드포인트 스켈레톤 생성
- [x] 임시 응답 데이터 구현

### 🚧 진행 중
- [ ] 데이터베이스 스키마 설계
- [ ] SQLAlchemy 모델 구현
- [ ] 인증 시스템 구현 (JWT)

### 📝 예정
- [ ] FIT-DNA 계산 로직 연동 (`fitdna_from_measurements.py`)
- [ ] 월간 리포트 생성 로직 연동 (`models_monthly_report.py`)
- [ ] 운동 추천 알고리즘 연동 (`phase2_exercise_recommendation.py`)
- [ ] 메이트 매칭 알고리즘 연동 (`phase2_matching_algorithm.py`)
- [ ] 외부 API 연동 (날씨, 지도)
- [ ] 파일 업로드 기능
- [ ] 단위 테스트 작성
- [ ] Docker 컨테이너화

## 🗄️ 데이터베이스

현재는 SQLite를 사용하지만, 프로덕션에서는 PostgreSQL 권장

### 마이그레이션 (예정)

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head
```

## 🔐 보안

- JWT 기반 인증
- 비밀번호 해싱 (bcrypt)
- CORS 설정
- Rate limiting (예정)

## 🧪 테스트

```bash
# 모든 테스트 실행
pytest

# 커버리지 포함
pytest --cov=app tests/
```

## 📦 배포

### Docker로 배포 (예정)

```bash
# Docker 이미지 빌드
docker build -t fitdna-backend .

# 컨테이너 실행
docker run -d -p 8000:8000 --env-file .env fitdna-backend
```

## 🤝 연동할 모델링 파일

프로젝트 루트 디렉토리에 있는 모델링 파일들:

1. **fitdna_from_measurements.py** - FIT-DNA 계산기
   - 사용자 측정값 → FIT-DNA 유형 계산

2. **models_monthly_report.py** - 월간 리포트 생성
   - 운동 세션 데이터 → 월간 통계 + 꾸준함 점수

3. **phase2_exercise_recommendation.py** - 운동 추천
   - FIT-DNA 유형 → 맞춤 운동 추천

4. **phase2_matching_algorithm.py** - 메이트 매칭
   - FIT-DNA + 선호도 → 최적 매칭

## 📄 라이선스

이 프로젝트는 비공개 프로젝트입니다.

## 📞 문의

백엔드 개발 관련 문의사항이 있으면 연락주세요!
