# 데이터베이스 스키마 설계

## 📊 ERD (Entity Relationship Diagram)

```
┌─────────────────┐
│     USERS       │◄────────────┐
├─────────────────┤             │
│ id (PK)         │             │
│ email (UQ)      │             │
│ username (UQ)   │             │
│ hashed_password │             │
│ nickname        │             │
│ age             │             │
│ gender          │             │
│ height          │             │
│ weight          │             │
│ profile_image   │             │
│ current_fitdna  │             │
└─────────────────┘             │
         │                      │
         │ 1:N                  │
         ├──────────────────────┼─────────────────────┐
         │                      │                     │
         ▼                      ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│FITNESS_MEASUREMENTS│  │  FITDNA_RESULTS  │  │LIFESTYLE_SURVEYS │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ id (PK)          │  │ id (PK)          │  │ id (PK)          │
│ user_id (FK)     │  │ user_id (FK)     │  │ user_id (FK)     │
│ measurement_date │  │ test_date        │  │ survey_date      │
│ grip_right       │  │ fitdna_type      │  │ exercise_freq    │
│ grip_left        │  │ fitdna_name      │  │ activity_level   │
│ sit_up           │  │ strength_score   │  │ sleep_hours      │
│ sit_and_reach    │  │ flexibility_score│  │ stress_level     │
│ standing_long_jump│ │ endurance_score  │  └──────────────────┘
│ vo2max           │  │ strengths (JSON) │
│ shuttle_run      │  │ weaknesses (JSON)│
│ strength_zscore  │  │ recommended_ex   │
│ flex_zscore      │  │ is_current       │
│ endurance_zscore │  └──────────────────┘
└──────────────────┘

         │ 1:N
         ├──────────────────────┬─────────────────────┐
         │                      │                     │
         ▼                      ▼                     ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ WORKOUT_SESSIONS │  │ DAILY_CONDITIONS │  │   USER_GOALS     │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ id (PK)          │  │ id (PK)          │  │ id (PK)          │
│ user_id (FK)     │  │ user_id (FK)     │  │ user_id (FK)     │
│ date             │  │ date             │  │ goal_type        │
│ exercise_type    │  │ pain_areas (JSON)│  │ goal_name        │
│ exercises (JSON) │  │ fatigue_level    │  │ target_value     │
│ duration         │  │ tension_level    │  │ current_value    │
│ intensity        │  │ sleep_quality    │  │ unit             │
│ completed        │  │ overall_risk     │  │ start_date       │
│ notes            │  └────────┬─────────┘  │ deadline         │
└──────────────────┘           │            │ is_active        │
                               │ 1:N        │ is_achieved      │
                               ▼            └──────────────────┘
                    ┌──────────────────┐
                    │  INJURY_RISKS    │
                    ├──────────────────┤
                    │ id (PK)          │
                    │ condition_id (FK)│
                    │ body_part        │
                    │ risk_level       │
                    │ risk_score       │
                    │ warning_message  │
                    │ exercises_to_avoid│
                    │ recommended_rest │
                    └──────────────────┘

┌──────────────────┐
│   FACILITIES     │
├──────────────────┤
│ id (PK)          │
│ name             │
│ facility_type    │
│ address          │
│ latitude         │
│ longitude        │
│ phone            │
│ website          │
│ has_parking      │
│ has_shower       │
│ operating_hours  │
│ pricing (JSON)   │
│ programs (JSON)  │
│ average_rating   │
│ total_reviews    │
└────────┬─────────┘
         │ 1:N
         ├─────────────────────┐
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│FACILITY_REVIEWS  │  │FACILITY_CONGESTION│
├──────────────────┤  ├──────────────────┤
│ id (PK)          │  │ id (PK)          │
│ facility_id (FK) │  │ facility_id (FK) │
│ user_id (FK)     │  │ day_of_week      │
│ overall_rating   │  │ hour             │
│ cleanliness      │  │ congestion_level │
│ equipment        │  │ congestion_score │
│ staff            │  │ average_visitors │
│ value            │  └──────────────────┘
│ comment          │
│ helpful_count    │
└──────────────────┘

         USERS
           │ 1:1
           ▼
┌──────────────────────┐
│ MATCHING_PREFERENCES │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK) (UQ)    │
│ fitdna_similarity    │
│ exercise_types (JSON)│
│ preferred_times (JSON)│
│ location_radius_km   │
│ age_range (JSON)     │
│ gender_preference    │
└──────────────────────┘

         USERS
           │ N:M
           ▼
┌──────────────────┐
│     MATCHES      │
├──────────────────┤
│ id (PK)          │
│ user1_id (FK)    │
│ user2_id (FK)    │
│ compatibility    │
│ fitdna_similarity│
│ exercise_overlap │
│ time_overlap     │
│ common_exercises │
│ status           │
│ requester_id (FK)│
│ matched_date     │
│ ended_date       │
│ total_workouts   │
│ chat_room_id     │
└──────────────────┘

┌──────────────────┐
│ MATCH_REQUESTS   │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │
│ request_date     │
│ candidates (JSON)│
│ status           │
└──────────────────┘

┌──────────────────────┐
│ PREVENTION_ROUTINES  │
├──────────────────────┤
│ id (PK)              │
│ name                 │
│ target_area          │
│ difficulty           │
│ duration             │
│ description          │
│ steps (JSON)         │
│ image_url            │
│ video_url            │
└──────────────────────┘
```

---

## 📋 테이블 상세 설명

### 1. users (사용자)
회원 기본 정보 및 계정 관리

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | Integer | PK, Auto | 사용자 ID |
| email | String(255) | UNIQUE, NOT NULL | 이메일 |
| username | String(100) | UNIQUE, NOT NULL | 사용자명 |
| hashed_password | String(255) | NOT NULL | 해시된 비밀번호 |
| nickname | String(50) | NULL | 닉네임 |
| age | Integer | NULL | 나이 |
| gender | Enum('M','F') | NULL | 성별 |
| height | Float | NULL | 키 (cm) |
| weight | Float | NULL | 몸무게 (kg) |
| birth_date | Date | NULL | 생년월일 |
| profile_image | String(500) | NULL | 프로필 이미지 URL |
| bio | String(500) | NULL | 자기소개 |
| is_active | Boolean | DEFAULT TRUE | 활성 상태 |
| is_verified | Boolean | DEFAULT FALSE | 인증 여부 |
| joined_date | Date | NULL | 가입일 |
| current_fitdna_type | String(10) | NULL | 현재 FIT-DNA 유형 |
| created_at | DateTime | AUTO | 생성일시 |
| updated_at | DateTime | AUTO | 수정일시 |

---

### 2. fitness_measurements (체력 측정)
체력 측정값 기록

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | Integer | PK, Auto | 측정 ID |
| user_id | Integer | FK(users), NOT NULL | 사용자 ID |
| measurement_date | Date | NOT NULL | 측정 날짜 |
| grip_right | Float | NULL | 악력 (오른손) kg |
| grip_left | Float | NULL | 악력 (왼손) kg |
| sit_up | Integer | NULL | 윗몸일으키기 (회/분) |
| sit_and_reach | Float | NULL | 앉아윗몸앞으로굽히기 (cm) |
| standing_long_jump | Float | NULL | 제자리멀리뛰기 (cm) |
| vo2max | Float | NULL | 최대산소섭취량 |
| shuttle_run | Integer | NULL | 왕복오래달리기 (회) |
| strength_zscore | Float | NULL | 근력 Z-Score |
| flexibility_zscore | Float | NULL | 유연성 Z-Score |
| endurance_zscore | Float | NULL | 지구력 Z-Score |

---

### 3. fitdna_results (FIT-DNA 검사 결과)
FIT-DNA 유형 검사 결과

| 컬럼명 | 타입 | 제약조건 | 설명 |
|--------|------|----------|------|
| id | Integer | PK, Auto | 결과 ID |
| user_id | Integer | FK(users), NOT NULL | 사용자 ID |
| measurement_id | Integer | FK(measurements) | 측정 ID |
| test_date | Date | NOT NULL | 검사일 |
| fitdna_type | String(10) | NOT NULL | FIT-DNA 유형 (PFE, etc) |
| fitdna_name | String(100) | NOT NULL | 유형명 (파워 애슬리트) |
| strength_score | Float | NULL | 근력 점수 (0-10) |
| flexibility_score | Float | NULL | 유연성 점수 (0-10) |
| endurance_score | Float | NULL | 지구력 점수 (0-10) |
| strengths | JSON | NULL | 강점 목록 |
| weaknesses | JSON | NULL | 약점 목록 |
| recommended_exercises | JSON | NULL | 추천 운동 목록 |
| is_current | Integer | DEFAULT 1 | 현재 유형 여부 (1/0) |

---

### 4. lifestyle_surveys (라이프스타일 설문)
생활 습관 설문 기록

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 설문 ID |
| user_id | Integer FK | 사용자 ID |
| survey_date | Date | 설문일 |
| exercise_frequency | Integer | 주당 운동 횟수 |
| daily_activity_level | String(20) | 일상 활동량 (low/medium/high) |
| sleep_hours | Float | 평균 수면 시간 |
| stress_level | String(20) | 스트레스 수준 |
| additional_data | JSON | 추가 정보 |

---

### 5. workout_sessions (운동 세션)
일일 운동 기록

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 세션 ID |
| user_id | Integer FK | 사용자 ID |
| date | Date | 운동일 |
| exercise_type | String(20) | 운동 유형 (strength/flexibility/endurance) |
| exercises | JSON | 운동 목록 ["스쿼트", "푸시업"] |
| duration | Integer | 운동 시간 (분) |
| intensity | String(10) | 강도 (low/medium/high) |
| completed | Boolean | 완료 여부 |
| notes | String(500) | 메모 |

---

### 6. daily_conditions (일일 컨디션)
매일 건강 체크

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 컨디션 ID |
| user_id | Integer FK | 사용자 ID |
| date | Date | 날짜 |
| pain_areas | JSON | 통증 부위 ["허리", "무릎"] |
| fatigue_level | Integer | 피로도 (1-10) |
| tension_level | Integer | 긴장도 (1-10) |
| sleep_quality | Integer | 수면 질 (1-10) |
| overall_risk_score | Float | 전체 위험도 점수 |
| overall_risk_level | String(20) | 위험 수준 (낮음/보통/높음) |

---

### 7. injury_risks (부상 위험도)
부위별 부상 위험도 분석

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 위험도 ID |
| condition_id | Integer FK | 컨디션 ID |
| body_part | String(50) | 신체 부위 (lower_back, knee, etc) |
| risk_level | String(20) | 위험 수준 |
| risk_score | Float | 위험 점수 (0-10) |
| warning_message | String(500) | 경고 메시지 |
| exercises_to_avoid | JSON | 피해야 할 운동 목록 |
| recommended_rest | Integer | 휴식 권장 여부 (0/1) |

---

### 8. facilities (운동 시설)
운동 시설 정보

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 시설 ID |
| name | String(200) | 시설명 |
| facility_type | String(50) | 유형 (gym/pool/park/running) |
| address | String(500) | 주소 |
| latitude | Float | 위도 |
| longitude | Float | 경도 |
| phone | String(50) | 전화번호 |
| website | String(500) | 웹사이트 |
| has_parking | Boolean | 주차 가능 여부 |
| has_shower | Boolean | 샤워실 여부 |
| has_locker | Boolean | 락커 여부 |
| operating_hours | JSON | 운영 시간 |
| pricing | JSON | 가격 정보 |
| programs | JSON | 프로그램 정보 |
| average_rating | Float | 평균 평점 |
| total_reviews | Integer | 총 리뷰 수 |
| review_scores | JSON | 세부 평점 |
| thumbnail | String(500) | 썸네일 URL |
| is_active | Boolean | 활성 여부 |

---

### 9. matching_preferences (매칭 선호도)
운동 메이트 매칭 선호도

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 선호도 ID |
| user_id | Integer FK UNIQUE | 사용자 ID (1:1) |
| fitdna_similarity | Integer | FIT-DNA 유사도 (0-3) |
| exercise_types | JSON | 선호 운동 종목 |
| preferred_times | JSON | 선호 시간대 |
| location_radius_km | Float | 활동 반경 (km) |
| age_range | JSON | 나이 범위 {"min": 25, "max": 35} |
| gender_preference | String(10) | 성별 선호 (M/F/any) |

---

### 10. matches (매칭 결과)
운동 메이트 매칭

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| id | Integer PK | 매칭 ID |
| user1_id | Integer FK | 사용자1 ID |
| user2_id | Integer FK | 사용자2 ID |
| compatibility_score | Float | 호환성 점수 (0-100) |
| fitdna_similarity_score | Float | FIT-DNA 유사도 |
| exercise_overlap_score | Float | 운동 겹침 점수 |
| time_overlap_score | Float | 시간 겹침 점수 |
| location_distance_km | Float | 거리 (km) |
| common_exercises | JSON | 공통 운동 |
| status | Enum | 상태 (pending/accepted/active/ended) |
| requester_id | Integer FK | 신청자 ID |
| matched_date | Date | 매칭일 |
| ended_date | Date | 종료일 |
| total_workouts_together | Integer | 함께한 운동 횟수 |
| chat_room_id | String(100) | 채팅방 ID |

---

## 🔑 인덱스 전략

### 주요 조회 패턴 기반 인덱스

```sql
-- 사용자 조회
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- 날짜 기반 조회
CREATE INDEX idx_workout_sessions_user_date ON workout_sessions(user_id, date);
CREATE INDEX idx_daily_conditions_user_date ON daily_conditions(user_id, date);
CREATE INDEX idx_fitness_measurements_user_date ON fitness_measurements(user_id, measurement_date);

-- FIT-DNA 검사 조회
CREATE INDEX idx_fitdna_results_user_current ON fitdna_results(user_id, is_current);

-- 위치 기반 조회
CREATE INDEX idx_facilities_location ON facilities(latitude, longitude);
CREATE INDEX idx_facilities_type ON facilities(facility_type);

-- 매칭 조회
CREATE INDEX idx_matches_users ON matches(user1_id, user2_id);
CREATE INDEX idx_matches_status ON matches(status);
```

---

## 📊 데이터 타입 선택 이유

| 타입 | 사용 예 | 이유 |
|------|---------|------|
| JSON | exercises, pain_areas | 가변 길이 배열, 유연한 구조 |
| Float | measurements, scores | 소수점 정밀도 필요 |
| Enum | gender, status | 제한된 선택지 |
| Date | test_date, joined_date | 날짜만 필요 (시간 불필요) |
| DateTime | created_at | 정확한 타임스탬프 |

---

## 🚀 다음 단계

1. ✅ **스키마 설계 완료**
2. ⏳ **DB 마이그레이션** - Alembic 설정
3. ⏳ **초기 데이터** - 시드 데이터 생성
4. ⏳ **API 구현** - 모델 활용
5. ⏳ **테스트** - 관계 및 쿼리 검증
