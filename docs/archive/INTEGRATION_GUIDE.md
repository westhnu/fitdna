# FIT-DNA 프론트엔드-백엔드 통합 가이드

## 📋 개요

React/TypeScript 프론트엔드와 FastAPI 백엔드를 연결하여 실제 데이터를 사용하는 통합 시스템입니다.

## 🎯 완료된 작업

### 백엔드 (FastAPI)
✅ **모델링 파일 통합**
- `fitdna_from_measurements.py` - FIT-DNA 계산
- `fitdna_calculator.py` - FIT-DNA 타입 분류
- `models_monthly_report.py` - 월간 리포트 생성 (간단한 버전으로 fallback)

✅ **API 엔드포인트**
- `/api/fitdna/result/{user_id}` - FIT-DNA 결과 조회
- `/api/reports/monthly/{user_id}` - 월간 리포트 조회
- `/api/facilities/nearby` - 주변 시설 검색
- `/api/reports/workout-sessions/{user_id}` - 운동 세션 조회

✅ **데이터베이스**
- SQLite: `backend/fitdna.db`
- 100,821개 시설 데이터
- 데모 사용자 (ID: 1, "김체력")
- 3개월치 FIT-DNA 진행 기록
- 18개 운동 세션

### 프론트엔드 (React/TypeScript)
✅ **API 클라이언트**
- `web/services/api.ts` - API 통신 레이어

✅ **통합 컴포넌트**
- `MyPageIntegrated.tsx` - 실제 API 연결된 마이페이지
- 자동 데이터 로딩
- 에러 처리 및 재시도
- 로딩 상태 표시

## 🚀 실행 방법

### 1. 백엔드 서버 시작

```bash
cd backend
python run.py
```

서버가 시작되면:
- API 서버: http://localhost:8000
- Swagger 문서: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 2. 프론트엔드 설정

#### Option A: 기존 App.tsx 교체
```bash
# web/App.tsx를 백업하고 통합 버전 사용
cd web
cp App.tsx App.tsx.backup
cp App.integrated.tsx App.tsx
```

#### Option B: import 경로만 변경
`web/App.tsx` 파일을 열어서:

```tsx
// 기존
import { MyPage } from './components/MyPage';

// 변경
import { MyPageIntegrated } from './components/MyPageIntegrated';

export default function App() {
  return <MyPageIntegrated />;
}
```

### 3. 프론트엔드 실행

```bash
cd web
npm install  # 처음 한 번만
npm run dev
```

## 📊 데이터 흐름

```
프론트엔드 (React)
    ↓
web/services/api.ts (API 클라이언트)
    ↓
FastAPI 백엔드 (http://localhost:8000/api)
    ↓
app/routers/*.py (라우터)
    ↓
app/services/*.py (비즈니스 로직)
    ↓
모델링 파일 (fitdna_*.py, models_*.py)
    ↓
SQLite DB (backend/fitdna.db)
```

## 🎨 주요 기능

### 1. 월간 리포트
- **데이터 소스**: `/api/reports/monthly/1?year=2024&month=11`
- **표시 내용**:
  - 총 운동 일수, 주당 평균, 총 운동 시간
  - 근력/유연성/지구력 운동 빈도
  - 체력 지표 변화 (전월 대비)
  - 꾸준함 점수 (0-100점)

### 2. FIT-DNA 결과
- **데이터 소스**: `/api/fitdna/result/1`
- **표시 내용**:
  - 현재 FIT-DNA 타입 (PFE - 파워 애슬리트)
  - 강점/약점 분석
  - 체력 점수 (근력 8.5, 유연성 7.2, 지구력 8.8)

### 3. 월별 데이터 전환
- 9월, 10월, 11월 버튼 클릭
- 자동으로 해당 월의 데이터 로드
- 로딩 상태 표시

## 🔧 API 타입 변환

백엔드 API는 snake_case, 프론트엔드는 camelCase를 사용합니다.

### 변환 함수 예시 (`MyPageIntegrated.tsx`)

```typescript
function convertAPIReportToFrontend(apiReport: MonthlyReportAPI): MonthlyReportType {
  return {
    year: apiReport.year,
    month: apiReport.month,
    summary: {
      totalWorkoutDays: apiReport.summary.total_workout_days,
      weeklyAverage: apiReport.summary.weekly_average,
      // ...
    },
    // ...
  };
}
```

## 🐛 문제 해결

### 백엔드 서버 연결 실패

**증상**: "데이터를 불러오는데 실패했습니다"

**해결**:
1. 백엔드 서버 실행 확인: `curl http://localhost:8000/`
2. 응답이 없으면 서버 재시작: `cd backend && python run.py`

### CORS 에러

**증상**: 브라우저 콘솔에 "CORS policy" 에러

**해결**: `backend/app/main.py`에 CORS 설정 확인
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    # ...
)
```

### 데이터가 비어있음

**증상**: 운동 일수 0, 세션 0

**해결**:
1. DB에 데이터 확인: `python backend/seed_data.py`
2. 해당 월에 데이터가 없을 수 있음 (9월, 10월, 11월만 데이터 있음)

## 📁 파일 구조

```
project2/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   │   ├── fitdna.py          # ✅ API 연결됨
│   │   │   ├── reports.py         # ✅ API 연결됨
│   │   │   └── facilities.py      # ✅ API 연결됨
│   │   ├── services/
│   │   │   ├── fitdna_service.py  # ✅ 모델링 파일 연결
│   │   │   └── report_service.py  # ✅ 간단한 버전 사용
│   │   └── models/                # DB 모델
│   ├── fitdna.db                  # SQLite 데이터베이스
│   └── run.py
│
├── web/
│   ├── services/
│   │   └── api.ts                 # ✅ 새로 추가됨
│   ├── components/
│   │   ├── MyPage.tsx             # 기존 (mock 데이터)
│   │   ├── MyPageIntegrated.tsx   # ✅ 새로 추가됨 (실제 API)
│   │   └── MonthlyReport.tsx      # 재사용
│   └── App.integrated.tsx         # ✅ 새로 추가됨
│
└── 모델링 파일/
    ├── fitdna_from_measurements.py
    ├── fitdna_calculator.py
    └── models_monthly_report.py
```

## 🎯 다음 단계

### 단기
1. ✅ 백엔드 API 통합 완료
2. ✅ 프론트엔드 API 클라이언트 생성
3. ✅ 월간 리포트 연결
4. ⏳ 운동 세션 상세 보기
5. ⏳ FIT-DNA 이력 전체 조회

### 중기
1. 시설 검색 기능 추가
2. 실시간 데이터 업데이트
3. 차트/그래프 추가
4. 매칭 기능 프론트엔드

### 장기
1. 인증/로그인 구현
2. 실제 사용자 지원
3. 모바일 반응형
4. PWA 변환

## 📝 참고사항

- 현재는 **데모 사용자 (ID: 1)** 로 고정
- pandas/numpy 에러로 인해 월간 리포트는 **간단한 버전** 사용
- 시설 데이터는 100,821개 로드되어 있으나 큰 반경 검색 시 성능 이슈 있음
- 프론트엔드는 shadcn/ui 사용 (Tailwind CSS 기반)

## 🔗 주요 링크

- 백엔드 API 문서: http://localhost:8000/api/docs
- GitHub Issues: https://github.com/anthropics/claude-code/issues
- Figma 디자인: https://www.figma.com/make/qGhKAF0DDWULUvaBAJDIKG

---

**Last Updated**: 2024-12-02
**Author**: Claude Code
