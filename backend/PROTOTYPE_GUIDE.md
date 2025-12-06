# 프로토타입 실행 가이드

## 🎯 프로토타입 개요

이 프로토타입은 **단일 사용자 페르소나 (김체력, 28세 남성)**로 FIT-DNA 플랫폼의 전체 기능을 시연합니다.

**주요 특징:**
- ✅ 실제 로그인 없이 바로 시연 가능
- ✅ 3개월치 운동 기록 및 FIT-DNA 변화 추이
- ✅ 월간 리포트, 매칭, 시설 추천 등 전체 기능
- ✅ 필요 시 추가 데이터만 간단히 삽입

---

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
cd backend
pip install -r requirements.txt
```

### 2. 데이터베이스 초기화 + 시드 데이터 생성

```bash
python seed_data.py
```

**출력 예시:**
```
🌱 시드 데이터 생성 시작...

✅ 데이터베이스 테이블이 생성되었습니다.
✅ 사용자 생성: 김체력 (ID: 1)
✅ 체력 측정 기록 생성: 3개
✅ FIT-DNA 검사 결과 생성: 3개
✅ 운동 세션 생성: 45개
✅ 라이프스타일 설문 생성
✅ 일일 컨디션 및 부상 위험도 생성
✅ 사용자 목표 생성: 2개
✅ 매칭 선호도 생성
✅ 더미 파트너 및 매칭 생성: 3명

✅ 시드 데이터 생성 완료!

📊 데모 사용자 정보:
   - 이메일: demo@fitdna.com
   - 닉네임: 김체력
   - FIT-DNA: PFE (파워 애슬리트)
   - User ID: 1
```

### 3. 서버 실행

```bash
python run.py
```

또는

```bash
uvicorn app.main:app --reload
```

### 4. API 문서 확인

브라우저에서:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 👤 데모 사용자 페르소나

### 기본 정보
- **이름**: 김체력
- **나이**: 28세
- **성별**: 남성
- **키/몸무게**: 175cm / 72kg
- **직업**: 직장인
- **운동 빈도**: 주 4-5회
- **현재 FIT-DNA**: PFE (파워 애슬리트)

### FIT-DNA 변화 추이

| 날짜 | FIT-DNA | 유형명 | 특징 |
|------|---------|--------|------|
| 2025-09-15 | LSQ | 입문자형 | 기초 체력, 약점: 근력·유연성 |
| 2025-10-15 | PSE | 파워 러너 | 근력·지구력 우수, 약점: 유연성 |
| 2025-11-15 | **PFE** | **파워 애슬리트** | **균형 잡힌 체력, 전 영역 우수** |

### 운동 기록 (3개월)

| 월 | 운동 일수 | 주당 평균 | 꾸준함 점수 |
|----|-----------|-----------|-------------|
| 9월 | 12일 | 3.0회 | 79점 (양호) |
| 10월 | 15일 | 3.8회 | 87점 (우수) |
| 11월 | 18일 | 4.5회 | 92점 (최고) |

### 현재 목표
1. **주 4회 운동** - 진행률 75% (3/4회)
2. **벤치프레스 100kg** - 진행률 85% (85/100kg)

### 오늘의 컨디션
- **통증 부위**: 허리
- **피로도**: 6/10
- **부상 위험도**: 보통
- **허리 위험**: 높음 (데드리프트·스쿼트 피하기)

---

## 📊 생성된 데이터

### 데이터베이스 테이블별 레코드 수

| 테이블 | 레코드 수 | 설명 |
|--------|-----------|------|
| users | 4 | 데모 사용자 1명 + 더미 파트너 3명 |
| fitness_measurements | 3 | 3개월치 측정 기록 |
| fitdna_results | 3 | FIT-DNA 변화 추이 |
| workout_sessions | 45 | 운동 세션 기록 |
| lifestyle_surveys | 1 | 라이프스타일 설문 |
| daily_conditions | 1 | 오늘의 컨디션 |
| injury_risks | 2 | 부상 위험도 (허리, 무릎) |
| user_goals | 2 | 사용자 목표 |
| matching_preferences | 1 | 매칭 선호도 |
| matches | 1 | 활성 매칭 |

---

## 🧪 API 테스트

### 1. 월간 리포트 조회

```bash
curl http://localhost:8000/api/reports/monthly/1?year=2025&month=11
```

**응답:**
- 총 운동 일수: 18일
- 주당 평균: 4.5회
- 꾸준함 점수: 92점
- 체력 지표 변화 (전월 대비)

### 2. FIT-DNA 결과 조회

```bash
curl http://localhost:8000/api/fitdna/result/1
```

**응답:**
- FIT-DNA 유형: PFE (파워 애슬리트)
- 강점/약점 분석
- 추천 운동 목록
- 추천 루틴

### 3. 부상 위험도 분석

```bash
curl http://localhost:8000/api/daily/injury-risk?user_id=1
```

**응답:**
- 전체 위험도: 보통
- 부위별 위험도 (허리: 높음, 무릎: 낮음)
- 피해야 할 운동 목록

### 4. 매칭 결과 조회

```bash
curl http://localhost:8000/api/matching/results?user_id=1
```

**응답:**
- 매칭 후보 3명
- 호환성 점수
- 공통 운동 종목

---

## 🔧 추가 데이터 삽입

### 새로운 운동 세션 추가

```python
from app.core.database import SessionLocal
from app.models import WorkoutSession
from datetime import date

db = SessionLocal()

new_session = WorkoutSession(
    user_id=1,
    date=date.today(),
    exercise_type="strength",
    exercises=["벤치프레스", "데드리프트"],
    duration=90,
    intensity="high",
    completed=True,
    notes="PR 갱신!"
)

db.add(new_session)
db.commit()
db.close()
```

### 새로운 체력 측정 추가

```python
from app.models import FitnessMeasurement

measurement = FitnessMeasurement(
    user_id=1,
    measurement_date=date.today(),
    grip_right=42.0,
    grip_left=40.0,
    sit_up=50,
    sit_and_reach=16.5,
    standing_long_jump=210,
    vo2max=45.5,
    shuttle_run=50
)

db.add(measurement)
db.commit()
```

---

## 📱 프론트엔드 연동

### API Base URL 설정

```typescript
// web/src/config.ts
export const API_BASE_URL = 'http://localhost:8000/api';
```

### 사용자 ID 고정

프로토타입에서는 **User ID = 1** 고정

```typescript
// web/src/constants.ts
export const DEMO_USER_ID = 1;
```

### 예시: 월간 리포트 조회

```typescript
const fetchMonthlyReport = async (year: number, month: number) => {
  const response = await fetch(
    `${API_BASE_URL}/reports/monthly/${DEMO_USER_ID}?year=${year}&month=${month}`
  );
  return await response.json();
};
```

---

## 🗄️ 데이터베이스 위치

SQLite 데이터베이스 파일: `backend/fitdna.db`

### DB Browser로 확인

```bash
# DB Browser for SQLite 설치 후
# File > Open Database > backend/fitdna.db
```

---

## 🔄 데이터 초기화

데이터를 초기화하고 다시 생성하려면:

```bash
# 1. DB 파일 삭제
rm fitdna.db

# 2. 시드 데이터 재생성
python seed_data.py
```

---

## 📝 주요 API 엔드포인트 (프로토타입용)

| 엔드포인트 | 설명 | 파라미터 |
|-----------|------|----------|
| `GET /api/fitdna/result/1` | FIT-DNA 결과 | - |
| `GET /api/reports/monthly/1` | 월간 리포트 | year, month |
| `GET /api/reports/workout-sessions/1` | 운동 기록 | start_date, end_date |
| `GET /api/reports/fitdna-history/1` | FIT-DNA 이력 | - |
| `GET /api/reports/statistics/1` | 통계 | - |
| `GET /api/reports/goals/1` | 목표 | - |
| `GET /api/daily/injury-risk?user_id=1` | 부상 위험도 | - |
| `GET /api/matching/results?user_id=1` | 매칭 결과 | - |

---

## ✅ 프로토타입 시연 시나리오

### 1단계: 마이페이지
1. 사용자 프로필 조회 (`김체력, 28세, PFE`)
2. 월간 리포트 확인 (11월: 18일, 92점)
3. FIT-DNA 변화 추이 확인 (LSQ → PSE → PFE)

### 2단계: 하루 건강 체크
1. 오늘의 컨디션 입력 (허리 통증, 피로도 6)
2. 부상 위험도 분석 (허리: 높음)
3. 예방 루틴 추천 (허리 스트레칭)

### 3단계: 운동 메이트 매칭
1. 매칭 선호도 설정 (FIT-DNA 유사, 러닝/헬스)
2. 매칭 후보 조회 (3명)
3. 후보자 상세 정보 확인
4. 매칭 신청

### 4단계: 운동 추천
1. FIT-DNA 기반 운동 추천
2. 위치 기반 시설 추천
3. 날씨 기반 운동 추천

---

## 🐛 트러블슈팅

### Q: 시드 데이터 생성 시 에러 발생
**A:** 기존 DB 파일 삭제 후 재시도
```bash
rm fitdna.db
python seed_data.py
```

### Q: API 호출 시 404 에러
**A:** 서버가 실행 중인지 확인
```bash
curl http://localhost:8000/health
```

### Q: 데이터가 안 보임
**A:** User ID가 1인지 확인. 시드 데이터는 ID=1 사용자로 생성됨

---

## 📞 문의

프로토타입 실행 중 문제가 있으면 로그를 확인하거나 문의하세요!
