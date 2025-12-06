# FIT-DNA 체력 MBTI 플랫폼

FIT-DNA는 사용자의 체력 측정 데이터를 기반으로 8가지 체력 유형(MBTI)을 분석하고, 맞춤형 운동 추천과 건강 리포트를 제공하는 웹 플랫폼입니다.

## 주요 기능

### 1. FIT-DNA 검사 및 결과
- 근력(Power/Light), 유연성(Flexible/Stiff), 지구력(Endurance/Quick) 3가지 축으로 8가지 타입 분류
- Z-Score 기반 연령/성별 정규화 분석
- 맞춤형 운동 루틴 추천

### 2. 하루 건강 체크
- 일일 운동 기록 및 추적
- 오늘의 컨디션 체크
- 실시간 운동 추천

### 3. 위치 기반 운동 시설 검색
- GPS 기반 주변 체육관/헬스장/요가 스튜디오 검색
- 10만+ 시설 데이터베이스
- Haversine 공식 기반 거리 계산

### 4. 마이페이지 리포트
- 월간 운동 분석 리포트
- FIT-DNA 변화 추이 그래프
- 일관성 점수 및 피드백

### 5. 운동 메이트 매칭 (예정)
- FIT-DNA 기반 운동 파트너 추천
- 실시간 채팅

## 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite/PostgreSQL**: 데이터베이스
- **Pandas/NumPy/Scikit-learn**: 데이터 분석 및 ML

### Frontend
- **React + TypeScript**: UI 프레임워크
- **Vite**: 빌드 도구
- **shadcn/ui**: UI 컴포넌트 라이브러리
- **Tailwind CSS**: 스타일링
- **Recharts**: 데이터 시각화

## 프로젝트 구조

```
project2/
├── backend/              # FastAPI 백엔드
│   ├── app/
│   │   ├── routers/     # API 엔드포인트
│   │   ├── models/      # SQLAlchemy 모델
│   │   ├── services/    # 비즈니스 로직
│   │   ├── core/        # 설정 및 유틸리티
│   │   └── main.py      # FastAPI 앱
│   ├── scripts/         # 데이터 시드 스크립트
│   ├── requirements.txt
│   └── run.py           # 서버 실행
│
├── web/                 # React 프론트엔드
│   ├── components/      # React 컴포넌트
│   ├── services/        # API 클라이언트
│   ├── lib/            # 유틸리티
│   └── test-integration.html
│
├── fitdna_from_measurements.py    # FIT-DNA 계산 모델
├── models_monthly_report.py       # 월간 리포트 생성 모델
├── phase2_exercise_recommendation.csv
├── fitdna_original_reference.pkl
└── map_2k.html          # 시설 데이터 소스
```

## 로컬 개발 환경 설정

### 백엔드 실행

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화 및 시드 데이터
python scripts/init_db.py
python scripts/seed_data.py

# 서버 실행
python run.py
```

서버 실행 후:
- API: http://localhost:8001/api
- Swagger UI: http://localhost:8001/api/docs
- 테스트 페이지: http://localhost:8001/test

### 프론트엔드 실행 (선택)

```bash
cd web
npm install
npm run dev
```

프론트엔드: http://localhost:5173

## API 엔드포인트

### FIT-DNA
- `GET /api/fitdna/result/{user_id}` - FIT-DNA 결과 조회
- `POST /api/fitdna/calculate` - 측정값으로 FIT-DNA 계산

### 리포트
- `GET /api/reports/monthly/{user_id}` - 월간 리포트
- `GET /api/reports/workout-sessions/{user_id}` - 운동 세션 이력
- `GET /api/reports/fitdna-history/{user_id}` - FIT-DNA 변화 이력

### 시설 검색
- `GET /api/facilities/nearby` - 주변 시설 검색
  - Query: lat, lon, radius, limit

### 하루 건강 체크
- `GET /api/daily/check/{user_id}` - 오늘의 체크 조회
- `POST /api/daily/check` - 체크 기록

## 배포

[DEPLOYMENT.md](./DEPLOYMENT.md) 참조

### 추천 배포 방법
- **백엔드**: Render.com (무료)
- **프론트엔드**: Vercel (무료)
- **데이터베이스**: Render PostgreSQL (무료)

## 데이터 모델

### 주요 테이블
- `users` - 사용자 정보
- `fitdna_results` - FIT-DNA 검사 결과
- `workout_sessions` - 운동 세션 기록
- `daily_checks` - 일일 건강 체크
- `facilities` - 운동 시설 (100,821개)
- `exercise_recommendations` - 운동 추천

## 라이선스

MIT License

## 개발자

프로젝트 2 - FIT-DNA Team
