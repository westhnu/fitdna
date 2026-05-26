# FIT-DNA 배포 가이드

## 방법 1: Render.com (추천 - 완전 무료)

### 장점
- ✅ 완전 무료 (Hobby tier)
- ✅ FastAPI + PostgreSQL 모두 지원
- ✅ GitHub 자동 배포
- ✅ HTTPS 자동 설정
- ✅ 무료 PostgreSQL 데이터베이스
- ✅ CORS 문제 없음

### 배포 단계

#### 1. GitHub에 코드 업로드

```bash
cd C:\Users\User\PycharmProjects\project2
git init
git add .
git commit -m "Initial commit: FIT-DNA backend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fitdna.git
git push -u origin main
```

#### 2. Render 계정 생성
- https://render.com 접속
- GitHub 계정으로 가입

#### 3. PostgreSQL 데이터베이스 생성
1. Dashboard → New → PostgreSQL
2. Name: `fitdna-db`
3. Database: `fitdna`
4. User: `fitdna_user`
5. Region: Singapore (가장 가까움)
6. **Free** 플랜 선택
7. Create Database

#### 4. Web Service 생성
1. Dashboard → New → Web Service
2. GitHub 저장소 연결: `YOUR_USERNAME/fitdna`
3. 설정:
   - **Name**: `fitdna-backend`
   - **Region**: Singapore
   - **Branch**: main
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

#### 5. 환경 변수 설정
Environment → Add Environment Variable:
```
DATABASE_URL = [PostgreSQL 데이터베이스의 External URL 복사]
SECRET_KEY = your-super-secret-key-here-change-this
ALLOWED_ORIGINS = https://your-frontend.vercel.app
```

#### 6. 배포 완료!
- 자동으로 배포가 시작됩니다
- 완료되면 URL: `https://fitdna-backend.onrender.com`

---

## 방법 2: Railway.app (무료 $5 크레딧)

### 장점
- ✅ 매달 $5 무료 크레딧
- ✅ 빠른 배포 속도
- ✅ PostgreSQL, Redis 등 지원

### 배포 단계

1. https://railway.app 가입
2. New Project → Deploy from GitHub
3. `fitdna` 저장소 선택
4. Add Variables:
   ```
   DATABASE_URL = (자동 생성)
   SECRET_KEY = your-secret-key
   ```
5. 배포 완료: `https://fitdna-backend.up.railway.app`

---

## 방법 3: Vercel (프론트엔드용)

프론트엔드(React)는 Vercel에 배포하는 것이 가장 좋습니다.

### 배포 단계

```bash
cd web
npm install
npm run build

# Vercel CLI 설치
npm i -g vercel

# 배포
vercel --prod
```

배포 완료: `https://fitdna.vercel.app`

---

## 전체 아키텍처 (배포 후)

```
프론트엔드 (Vercel)
https://fitdna.vercel.app
        ↓
백엔드 API (Render)
https://fitdna-backend.onrender.com/api
        ↓
PostgreSQL DB (Render)
postgres://fitdna_user:***@dpg-***.singapore-postgres.render.com/fitdna
```

---

## 데이터베이스 마이그레이션

Render PostgreSQL에 시드 데이터 추가:

```bash
# 로컬에서 PostgreSQL URL로 연결
export DATABASE_URL="postgres://..."

# 시드 데이터 실행
python -c "from app.database import init_db; init_db()"
python scripts/seed_data.py
```

---

## 프론트엔드 API URL 변경

`web/services/api.ts`:
```typescript
// 로컬
const API_BASE_URL = 'http://localhost:8001/api';

// 배포 후
const API_BASE_URL = 'https://fitdna-backend.onrender.com/api';
```

또는 환경 변수 사용:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001/api';
```

`web/.env`:
```
VITE_API_URL=https://fitdna-backend.onrender.com/api
```

---

## 주의사항

1. **Render 무료 플랜의 제약**:
   - 15분 동안 요청이 없으면 서버가 sleep 상태로 전환
   - 첫 요청 시 30초 정도 걸릴 수 있음
   - 해결: 무료 UptimeRobot으로 5분마다 핑 보내기

2. **보안**:
   - `.env` 파일은 절대 Git에 커밋하지 말 것
   - `SECRET_KEY`는 반드시 강력한 비밀키로 변경
   - CORS `ALLOWED_ORIGINS`에 실제 프론트엔드 URL만 추가

3. **데이터베이스**:
   - Render 무료 PostgreSQL은 90일 후 삭제됨
   - 중요 데이터는 정기적으로 백업

---

## 다음 단계

배포 후 테스트:
1. https://fitdna-backend.onrender.com/health → `{"status": "healthy"}`
2. https://fitdna-backend.onrender.com/api/docs → Swagger UI
3. 프론트엔드에서 API 호출 테스트

문제 발생 시:
- Render Dashboard → Logs 확인
- Environment Variables 재확인
