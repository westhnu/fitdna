# 백엔드 프로젝트 구조

## 📁 전체 구조

```
project2/
├── backend/                          # FastAPI 백엔드
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # ✅ FastAPI 앱 진입점
│   │   ├── core/                    # 핵심 설정
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # ✅ 환경 변수 관리
│   │   │   └── security.py         # ⏳ JWT 인증 (예정)
│   │   ├── routers/                 # API 엔드포인트
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # ✅ 회원가입/로그인
│   │   │   ├── fitdna.py           # ✅ FIT-DNA 검사
│   │   │   ├── daily_health.py     # ✅ 하루 건강 체크
│   │   │   ├── facilities.py       # ✅ 위치 기반 시설
│   │   │   ├── matching.py         # ✅ 운동 메이트 매칭
│   │   │   └── reports.py          # ✅ 마이페이지 리포트
│   │   ├── models/                  # ⏳ DB 모델 (예정)
│   │   │   └── __init__.py
│   │   ├── schemas/                 # ⏳ Pydantic 스키마 (예정)
│   │   │   └── __init__.py
│   │   ├── services/                # ⏳ 비즈니스 로직 (예정)
│   │   │   └── __init__.py
│   │   └── utils/                   # ⏳ 유틸리티 (예정)
│   │       └── __init__.py
│   ├── requirements.txt             # ✅ Python 패키지
│   ├── .env.example                 # ✅ 환경 변수 템플릿
│   └── README.md                    # ✅ 백엔드 문서
│
├── web/                              # React 프론트엔드
│   ├── components/
│   │   ├── MyPage.tsx              # ✅ 마이페이지
│   │   ├── MonthlyReport.tsx       # ✅ 월간 리포트
│   │   └── ui/                      # ✅ shadcn/ui 컴포넌트
│   ├── data/
│   │   └── mockMonthlyReport.ts    # ✅ 임시 데이터
│   └── App.tsx                      # ✅ 앱 진입점
│
├── models/                           # 모델링 파일들
│   ├── fitdna_from_measurements.py # ✅ FIT-DNA 계산기
│   ├── fitdna_calculator.py        # ✅ 코어 계산 함수
│   ├── models_monthly_report.py    # ✅ 월간 리포트 생성
│   ├── phase2_exercise_recommendation.py  # ✅ 운동 추천
│   └── phase2_matching_algorithm.py       # ✅ 메이트 매칭
│
├── data/                             # 데이터 파일들
│   ├── fitdna_original_reference.pkl      # ✅ FIT-DNA 참조 테이블
│   ├── monthly_reports_mock_data.json     # ✅ 월간 리포트 임시 데이터
│   └── workout_sessions_mock_data.csv     # ✅ 운동 세션 임시 데이터
│
└── docs/                             # 문서
    ├── MONTHLY_REPORT_MODELING_GUIDE.md   # ✅ 월간 리포트 가이드
    └── BACKEND_STRUCTURE.md                # ✅ 이 파일
```

## 🎯 API 엔드포인트 개요

### 1. 인증 (`/api/auth`)
| 메서드 | 엔드포인트 | 설명 | 상태 |
|--------|-----------|------|------|
| POST | `/register` | 회원가입 | 🔨 스켈레톤 |
| POST | `/login` | 로그인 | 🔨 스켈레톤 |
| POST | `/logout` | 로그아웃 | 🔨 스켈레톤 |
| GET | `/me` | 내 정보 조회 | 🔨 스켈레톤 |

### 2. FIT-DNA 검사 (`/api/fitdna`)
| 메서드 | 엔드포인트 | 설명 | 연동 모델 | 상태 |
|--------|-----------|------|-----------|------|
| POST | `/basic-info` | 기본 정보 입력 | - | 🔨 스켈레톤 |
| POST | `/measurements` | 체력 측정값 입력 | - | 🔨 스켈레톤 |
| POST | `/survey` | 라이프스타일 설문 | - | 🔨 스켈레톤 |
| POST | `/calculate` | FIT-DNA 계산 | `fitdna_from_measurements.py` | ⏳ 예정 |
| GET | `/result/{user_id}` | 결과 조회 | - | 🔨 스켈레톤 |
| GET | `/types` | 모든 유형 정보 | - | 🔨 스켈레톤 |

### 3. 하루 건강 체크 (`/api/daily`)
| 메서드 | 엔드포인트 | 설명 | 상태 |
|--------|-----------|------|------|
| POST | `/condition` | 컨디션 체크 | 🔨 스켈레톤 |
| GET | `/injury-risk` | 부상 위험도 분석 | 🔨 스켈레톤 |
| GET | `/prevention-routine` | 예방 루틴 추천 | 🔨 스켈레톤 |
| GET | `/risk-history` | 위험도 이력 | 🔨 스켈레톤 |

### 4. 위치 기반 시설 (`/api/facilities`)
| 메서드 | 엔드포인트 | 설명 | 연동 API | 상태 |
|--------|-----------|------|----------|------|
| GET | `/nearby` | 주변 시설 조회 | 카카오맵 API | ⏳ 예정 |
| GET | `/{facility_id}` | 시설 상세 정보 | - | 🔨 스켈레톤 |
| GET | `/weather-recommendation` | 날씨 기반 추천 | 날씨 API | ⏳ 예정 |

### 5. 운동 메이트 매칭 (`/api/matching`)
| 메서드 | 엔드포인트 | 설명 | 연동 모델 | 상태 |
|--------|-----------|------|-----------|------|
| POST | `/preferences` | 매칭 선호도 설정 | - | 🔨 스켈레톤 |
| POST | `/request` | 매칭 요청 | `phase2_matching_algorithm.py` | ⏳ 예정 |
| GET | `/results` | 매칭 결과 | - | 🔨 스켈레톤 |
| GET | `/candidate/{id}` | 후보자 상세 | - | 🔨 스켈레톤 |
| POST | `/request/{id}` | 매칭 신청 | - | 🔨 스켈레톤 |
| POST | `/accept/{id}` | 매칭 수락 | - | 🔨 스켈레톤 |
| GET | `/my-matches` | 내 매칭 목록 | - | 🔨 스켈레톤 |

### 6. 마이페이지 리포트 (`/api/reports`)
| 메서드 | 엔드포인트 | 설명 | 연동 모델 | 상태 |
|--------|-----------|------|-----------|------|
| GET | `/monthly/{user_id}` | 월간 리포트 | `models_monthly_report.py` | ⏳ 예정 |
| POST | `/workout-sessions` | 운동 기록 저장 | - | 🔨 스켈레톤 |
| GET | `/workout-sessions/{user_id}` | 운동 기록 조회 | - | 🔨 스켈레톤 |
| GET | `/fitdna-history/{user_id}` | FIT-DNA 이력 | - | 🔨 스켈레톤 |
| POST | `/request-retest` | 재검 요청 | - | 🔨 스켈레톤 |
| GET | `/statistics/{user_id}` | 사용자 통계 | - | 🔨 스켈레톤 |
| GET | `/goals/{user_id}` | 목표 조회 | - | 🔨 스켈레톤 |

## 📊 데이터 흐름

```
사용자 입력
    ↓
[FastAPI 라우터]
    ↓
[Pydantic 검증] ← schemas/
    ↓
[비즈니스 로직] ← services/ + 모델링 파일
    ↓
[DB 조회/저장] ← models/ (SQLAlchemy)
    ↓
[응답 반환]
    ↓
프론트엔드
```

## 🔄 모델링 파일 연동 계획

### 1. FIT-DNA 계산 (`/api/fitdna/calculate`)
```python
# services/fitdna_service.py
from fitdna_from_measurements import calculate_fitdna_from_measurements, load_reference_table

ref_table = load_reference_table()

def calculate_user_fitdna(age, gender, measurements):
    result = calculate_fitdna_from_measurements(
        age=age,
        gender=gender,
        measurements=measurements,
        ref_table=ref_table
    )
    return result
```

### 2. 월간 리포트 생성 (`/api/reports/monthly`)
```python
# services/report_service.py
from models_monthly_report import generate_monthly_report

def get_monthly_report(user_id, year, month):
    sessions = fetch_user_sessions(user_id, year, month)
    measurements = fetch_user_measurements(user_id, year, month)

    report = generate_monthly_report(
        user_id=user_id,
        year=year,
        month=month,
        sessions=sessions,
        current_measurement=measurements[-1],
        previous_measurement=measurements[-2] if len(measurements) > 1 else None
    )
    return report
```

### 3. 운동 추천 (`/api/fitdna/result`)
```python
# services/exercise_service.py
import pandas as pd

recommendations_df = pd.read_csv('phase2_exercise_recommendation.csv')

def get_exercise_recommendations(fitdna_type):
    user_exercises = recommendations_df[
        recommendations_df['fitdna_type'] == fitdna_type
    ]
    return user_exercises.to_dict('records')
```

### 4. 메이트 매칭 (`/api/matching/request`)
```python
# services/matching_service.py
from phase2_matching_algorithm import calculate_matching_score

def find_matches(user_id, preferences):
    candidates = fetch_potential_candidates(preferences)

    matches = []
    for candidate in candidates:
        score = calculate_matching_score(
            user_fitdna=user.fitdna_type,
            candidate_fitdna=candidate.fitdna_type,
            user_zscores=user.zscores,
            candidate_zscores=candidate.zscores
        )
        matches.append({'candidate': candidate, 'score': score})

    return sorted(matches, key=lambda x: x['score'], reverse=True)
```

## 🚀 다음 단계

### Phase 1: 데이터베이스 설계 ⏳
- [ ] SQLAlchemy 모델 정의
- [ ] Alembic 마이그레이션 설정
- [ ] 초기 테이블 생성

### Phase 2: 인증 시스템 구현 ⏳
- [ ] JWT 토큰 생성/검증
- [ ] 비밀번호 해싱
- [ ] 사용자 CRUD

### Phase 3: 모델링 파일 연동 ⏳
- [ ] FIT-DNA 계산 서비스
- [ ] 월간 리포트 생성 서비스
- [ ] 운동 추천 서비스
- [ ] 메이트 매칭 서비스

### Phase 4: 외부 API 연동 ⏳
- [ ] 날씨 API
- [ ] 카카오맵 API
- [ ] 파일 업로드

### Phase 5: 테스트 및 배포 ⏳
- [ ] 단위 테스트
- [ ] 통합 테스트
- [ ] Docker 컨테이너화
- [ ] CI/CD 파이프라인

## 📝 참고 문서

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [월간 리포트 모델링 가이드](./MONTHLY_REPORT_MODELING_GUIDE.md)
