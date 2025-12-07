# FIT-DNA 체력 MBTI 플랫폼

사용자의 체력 측정 데이터를 기반으로 8가지 체력 유형을 분석하고, 맞춤형 운동 추천과 건강 리포트를 제공하는 웹 플랫폼입니다.

## 🏗️ 프로젝트 구조

```
fitdna/
├── backend/                # FastAPI 백엔드 서버
│   ├── app/               # 애플리케이션 코드
│   ├── data/              # 모델 데이터 파일
│   ├── requirements.txt
│   ├── runtime.txt
│   └── run.py
├── frontend/              # React 프론트엔드
│   ├── components/
│   ├── services/
│   └── test-integration.html
├── docs/                  # 프로젝트 문서
│   ├── DEPLOYMENT.md     # 배포 가이드
│   ├── DATABASE_SCHEMA.md
│   └── archive/          # 과거 문서
└── scripts/              # 유틸리티 스크립트
```

## 🚀 빠른 시작

### 백엔드 실행

```bash
cd backend
pip install -r requirements.txt
python seed_data.py  # 시드 데이터 생성
python run.py        # 서버 시작
```

서버 실행 후:
- API: http://localhost:8001/api
- Swagger UI: http://localhost:8001/api/docs
- 테스트 페이지: http://localhost:8001/test

### 프론트엔드 (선택)

```bash
cd frontend
npm install
npm run dev
```

## 📋 주요 기능

1. **FIT-DNA 검사** - 8가지 체력 유형 분석 (P/L × F/S × E/Q)
2. **월간 리포트** - 운동 기록 분석 및 진척도 추적
3. **위치 기반 시설 검색** - GPS 기반 주변 체육 시설 검색
4. **운동 추천** - 체력 유형별 맞춤 운동 루틴

## 🔧 기술 스택

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL/SQLite
- **Frontend**: React, TypeScript, Tailwind CSS
- **Data Science**: Pandas, NumPy, Scikit-learn

## 📦 배포

배포 가이드는 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)를 참조하세요.

**추천 플랫폼:**
- Backend: [Render.com](https://render.com) (무료)
- Frontend: [Vercel](https://vercel.com) (무료)

## 📚 문서

- [배포 가이드](docs/DEPLOYMENT.md)
- [데이터베이스 스키마](docs/DATABASE_SCHEMA.md)
- [추가 문서](docs/archive/)

## 📄 라이선스

MIT License

## 👥 개발팀

FIT-DNA Team
