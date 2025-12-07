# 월간 리포트 데이터 모델링 가이드

## 📋 개요

이 문서는 **FIT-DNA 월간 운동 리포트** 기능을 위한 데이터 모델링 및 계산 로직을 설명합니다.

## 🎯 주요 기능

1. **월간 운동 빈도/종류 분석** - 근력/유연성/지구력 운동 횟수
2. **체력 지표 변화 추적** - 전월 대비 측정값 비교
3. **꾸준함 점수 (Consistency Score)** - 운동 규칙성 점수화 (0-100점)

---

## 📊 데이터 모델

### 1. WorkoutSession (운동 세션)

```python
class WorkoutSession:
    user_id: int              # 사용자 ID
    date: str                 # 운동 날짜 (YYYY-MM-DD)
    exercise_type: str        # 'strength' | 'flexibility' | 'endurance'
    exercises: List[str]      # 수행한 운동 목록
    duration: int             # 운동 시간 (분)
    intensity: str            # 'low' | 'medium' | 'high'
    completed: bool           # 완료 여부
```

**예시:**
```json
{
  "user_id": 1,
  "date": "2025-11-15",
  "exercise_type": "strength",
  "exercises": ["스쿼트", "푸시업", "플랭크"],
  "duration": 60,
  "intensity": "high",
  "completed": true
}
```

### 2. FitnessMeasurement (체력 측정)

```python
class FitnessMeasurement:
    user_id: int              # 사용자 ID
    measurement_date: str     # 측정 날짜 (YYYY-MM-DD)
    age: int                  # 나이
    gender: str               # 'M' | 'F'
    measurements: Dict        # 측정값 딕셔너리
```

**측정 항목 (measurements):**
- `grip_right`: 악력 (오른손) - kg
- `grip_left`: 악력 (왼손) - kg
- `sit_up`: 윗몸일으키기 - 회/분
- `sit_and_reach`: 앉아윗몸앞으로굽히기 - cm
- `standing_long_jump`: 제자리멀리뛰기 - cm
- `vo2max`: 최대산소섭취량 - ml/kg/min
- `shuttle_run`: 왕복오래달리기 - 회

**예시:**
```json
{
  "user_id": 1,
  "measurement_date": "2025-11-15",
  "age": 28,
  "gender": "M",
  "measurements": {
    "grip_right": 41.2,
    "grip_left": 39.1,
    "sit_up": 48,
    "sit_and_reach": 15.8,
    "standing_long_jump": 205,
    "vo2max": 44.8,
    "shuttle_run": 48
  }
}
```

---

## 🧮 계산 로직

### 1. 월간 운동 요약 (Summary)

```python
def calculate_monthly_summary(sessions):
    total_workout_days = len(set(s.date for s in sessions))
    weekly_average = total_workout_days / 4  # 4주 기준
    total_duration = sum(s.duration for s in sessions)

    return {
        'total_workout_days': total_workout_days,
        'weekly_average': weekly_average,
        'total_duration': total_duration
    }
```

### 2. 운동 종류별 빈도

```python
def calculate_workout_frequency(sessions):
    frequency = {'strength': 0, 'flexibility': 0, 'endurance': 0}

    for session in sessions:
        frequency[session.exercise_type] += 1

    return frequency
```

### 3. 체력 지표 변화

```python
def calculate_metric_changes(previous, current):
    changes = []

    for metric_key in previous.measurements:
        prev_value = previous.measurements[metric_key]
        curr_value = current.measurements[metric_key]

        change = curr_value - prev_value
        change_percentage = (change / prev_value * 100)

        changes.append({
            'name': metric_key,
            'previous_month': prev_value,
            'current_month': curr_value,
            'change': change,
            'change_percentage': change_percentage
        })

    return changes
```

### 4. 꾸준함 점수 (Consistency Score)

**총점: 100점 만점**

#### 4.1 목표 달성률 (40점)
```python
achievement_rate = min((total_sessions / target_monthly_workouts) * 40, 40)
```
- 목표: 월 16회 (주 4회)
- 계산: 실제 운동 횟수 ÷ 목표 × 40

#### 4.2 운동 규칙성 (40점)
```python
# 운동 간격의 일관성 평가
intervals = [운동 날짜 간격 리스트]
ideal_interval = 2  # 이상적 간격 (2-3일)

interval_variance = sum(abs(interval - ideal_interval) for interval in intervals) / len(intervals)
regularity = max(40 - interval_variance * 5, 0)
```
- 운동 간격이 균일할수록 높은 점수
- 이상적: 2-3일 간격 (주 4회 기준)

#### 4.3 강도 유지도 (20점)
```python
intensity_scores = {'low': 1, 'medium': 2, 'high': 3}
avg_intensity = sum(intensity_scores[s.intensity] for s in sessions) / len(sessions)
intensity_maintenance = min(avg_intensity / 3 * 20, 20)
```
- 평균 운동 강도가 높을수록 높은 점수

#### 4.4 점수 등급
- **90-100점**: 최고 - "완벽해요!"
- **80-89점**: 우수 - "훌륭해요!"
- **70-79점**: 양호 - "잘하고 있어요!"
- **60-69점**: 보통 - "좋은 시작이에요"
- **0-59점**: 노력 필요 - "화이팅!"

---

## 📁 파일 구조

```
project2/
├── models_monthly_report.py          # 데이터 모델링 메인 파일
├── monthly_reports_mock_data.json    # 월간 리포트 임시 데이터 (JSON)
├── workout_sessions_mock_data.csv    # 운동 세션 임시 데이터 (CSV)
└── MONTHLY_REPORT_MODELING_GUIDE.md  # 이 문서
```

---

## 🚀 사용 방법

### 1. 임시 데이터 생성

```bash
python models_monthly_report.py
```

**출력:**
- `monthly_reports_mock_data.json` - 3개월치 월간 리포트 데이터
- `workout_sessions_mock_data.csv` - 운동 세션 상세 데이터

### 2. Python에서 사용

```python
from models_monthly_report import (
    generate_monthly_report,
    generate_mock_workout_sessions,
    generate_mock_fitness_measurement
)

# 운동 세션 생성
sessions = generate_mock_workout_sessions(
    user_id=1,
    year=2025,
    month=11,
    workout_days=18
)

# 체력 측정 생성
current_measurement = generate_mock_fitness_measurement(
    user_id=1,
    measurement_date='2025-11-15',
    age=28,
    gender='M'
)

# 월간 리포트 생성
report = generate_monthly_report(
    user_id=1,
    year=2025,
    month=11,
    sessions=sessions,
    current_measurement=current_measurement
)

print(f"꾸준함 점수: {report['consistency_score']['total_score']}점")
```

---

## 📊 JSON 데이터 구조

### 월간 리포트 (MonthlyReport)

```json
{
  "user_id": 1,
  "year": 2025,
  "month": 11,
  "summary": {
    "total_workout_days": 18,
    "weekly_average": 4.5,
    "total_duration": 1080,
    "total_sessions": 18
  },
  "workout_frequency": {
    "strength": 12,
    "flexibility": 8,
    "endurance": 10
  },
  "sessions": [
    {
      "user_id": 1,
      "date": "2025-11-01",
      "exercise_type": "strength",
      "exercises": ["스쿼트", "푸시업", "플랭크"],
      "duration": 60,
      "intensity": "high",
      "completed": true
    }
  ],
  "metric_changes": [
    {
      "name": "악력 (오른손)",
      "unit": "kg",
      "previous_month": 38.5,
      "current_month": 41.2,
      "change": 2.7,
      "change_percentage": 7.0
    }
  ],
  "consistency_score": {
    "total_score": 87,
    "breakdown": {
      "achievement_rate": 36.0,
      "regularity": 35.0,
      "intensity_maintenance": 16.0
    },
    "feedback": "훌륭해요! 이번 달 18회 꾸준히 운동하셨네요. 다음 달에도 화이팅!"
  }
}
```

---

## 🔄 백엔드 API 연동

### 필요한 API 엔드포인트

#### 1. 운동 기록 저장
```
POST /api/workouts/sessions
{
  "date": "2025-11-15",
  "exercise_type": "strength",
  "exercises": ["스쿼트", "푸시업"],
  "duration": 60,
  "intensity": "high"
}
```

#### 2. 월간 리포트 조회
```
GET /api/reports/monthly?year=2025&month=11
```

**응답:**
```json
{
  "summary": { ... },
  "workout_frequency": { ... },
  "metric_changes": [ ... ],
  "consistency_score": { ... }
}
```

#### 3. 체력 측정 기록
```
POST /api/measurements
{
  "measurement_date": "2025-11-15",
  "measurements": {
    "grip_right": 41.2,
    "sit_up": 48,
    ...
  }
}
```

---

## 📈 데이터베이스 스키마 (예정)

### workout_sessions 테이블
```sql
CREATE TABLE workout_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    exercise_type VARCHAR(20) NOT NULL,
    exercises JSONB,
    duration INTEGER,
    intensity VARCHAR(10),
    completed BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### fitness_measurements 테이블
```sql
CREATE TABLE fitness_measurements (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    measurement_date DATE NOT NULL,
    age INTEGER,
    gender CHAR(1),
    grip_right DECIMAL(5,2),
    grip_left DECIMAL(5,2),
    sit_up INTEGER,
    sit_and_reach DECIMAL(5,2),
    standing_long_jump DECIMAL(6,2),
    vo2max DECIMAL(5,2),
    shuttle_run INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### monthly_reports 테이블 (캐싱용)
```sql
CREATE TABLE monthly_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    report_data JSONB,
    generated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, year, month)
);
```

---

## 🧪 테스트 결과

### 9월 데이터
- 총 운동 일수: **12일**
- 주당 평균: **3.0회**
- 꾸준함 점수: **79점** (양호)

### 10월 데이터
- 총 운동 일수: **15일**
- 주당 평균: **3.8회**
- 꾸준함 점수: **87점** (우수)

### 11월 데이터
- 총 운동 일수: **18일**
- 주당 평균: **4.5회**
- 꾸준함 점수: **92점** (최고)

---

## 💡 다음 단계

1. ✅ **임시 데이터 모델링** - 완료
2. ⏳ **백엔드 API 구현** - FastAPI + PostgreSQL
3. ⏳ **프론트엔드 연동** - React 컴포넌트와 API 연결
4. ⏳ **실제 데이터 마이그레이션** - 기존 데이터 → 새 스키마

---

## 📞 문의

백엔드 개발 시 이 문서를 참고하여:
- DB 스키마 설계
- API 엔드포인트 구현
- 계산 로직 구현

추가 질문이나 수정사항이 있으면 언제든지 연락주세요!
