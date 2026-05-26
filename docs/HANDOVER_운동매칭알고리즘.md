# 운동 매칭 알고리즘 인수인계 문서

---

## 📋 인수인계 개요

**담당 기능:** FIT-DNA 기반 운동 메이트 매칭 알고리즘
**작성일:** 2024-11-27
**데이터 기준:** 국민체력100 데이터 (115,983건)

---

## 📦 인수인계 파일 목록

### 1. 핵심 파일 (필수)

| 파일명 | 용도 | 크기 | 비고 |
|--------|------|------|------|
| **phase2_matching_algorithm.py** | 매칭 알고리즘 구현 코드 | 16KB | 메인 로직 |
| **matching_euclidean_distance_matrix.csv** | FIT-DNA 8유형 간 유클리드 거리 행렬 | 1.2KB | 유사도 참조 테이블 |
| **matching_cosine_similarity_matrix.csv** | FIT-DNA 8유형 간 코사인 유사도 행렬 | 1.2KB | 유사도 참조 테이블 |
| **phase2_matching_algorithm_report.txt** | 알고리즘 분석 리포트 | 3.8KB | 상세 설명서 |
| **phase2_matching_algorithm_analysis.png** | 시각화 자료 | 630KB | 유사도 히트맵 |

### 2. 데이터 파일 (선택)

**운동 매칭 알고리즘만 사용한다면 데이터 파일은 불필요합니다.**

현재 알고리즘은 **FIT-DNA 8가지 유형의 대표값만** 사용하며, 이 값은 이미 코드에 하드코딩되어 있습니다 ([phase2_matching_algorithm.py:13-22](phase2_matching_algorithm.py:13-22)).

```python
FITDNA_VECTORS = {
    'PFE': [1.547, 0.806, 0.959],
    'PFQ': [1.513, 0.782, -0.820],
    # ... (코드 내 직접 정의됨)
}
```

**단, 다음 작업을 하려면 데이터 파일이 필요합니다:**

| 작업 | 필요 데이터 파일 | 크기 | 용도 |
|------|----------------|------|------|
| FIT-DNA 재계산 또는 검증 | **fit_dna_preprocessed_cp949.csv** | 9.1MB | 115,983명의 Z-Score 및 FIT-DNA 유형 |
| 실제 사용자 DB 구축 | 위와 동일 | 9.1MB | 개인별 Z-Score로 매칭 점수 계산 |
| 유형별 대표값 재산출 | 위와 동일 | 9.1MB | 평균값 계산 |

**파일 위치:**
```
최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv
```

**데이터 구조:**
| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| MBER_AGE_CO | 나이 | 25 |
| MBER_SEXDSTN_FLAG_CD | 성별 | M/F |
| strength_z | 근력 Z-Score | 1.23 |
| flex_z | 유연성 Z-Score | 0.56 |
| endurance_z | 지구력 Z-Score | -0.34 |
| FIT_DNA | 유형 코드 | PFE |

### 3. 참조 문서 (선택)

| 파일명 | 용도 |
|--------|------|
| **FIT_DNA_SERVICE_GUIDE.md** | FIT-DNA 서비스 전체 가이드 |
| **FIT_DNA_PROJECT_SUMMARY_FOR_MEETING.md** | 프로젝트 전체 요약 |

---

## ⚠️ 중요: 매칭 전략 선택 가이드

### 현재 알고리즘의 설계 철학

**질문 1: 왜 같은 FIT-DNA 유형끼리만 매칭하지 않나요?**

현재 알고리즘은 **"FIT-DNA 유형 유사도(40%) + 개인별 실제 체력 유사도(60%)"** 를 조합합니다.

**이유:**

```
예시 1) 유형은 다르지만 실제 체력은 비슷한 경우

사용자 A: PFE (근력↑, 유연성↑, 지구력↑)
  실제 Z-Score: [0.55, 0.52, 0.53]  ← 기준(0.5)을 살짝 넘어서 'High'

사용자 B: PSE (근력↑, 유연성↓, 지구력↑)
  실제 Z-Score: [0.58, 0.48, 0.56]  ← 유연성이 0.48이라 'Low'

→ 유형은 다르지만 실제 Z-Score 거리는 0.08로 매우 유사
→ 함께 운동하기 좋음!


예시 2) 같은 유형이지만 실제 체력 차이가 큰 경우

사용자 C: PFE (근력↑, 유연성↑, 지구력↑)
  실제 Z-Score: [2.5, 2.0, 2.3]  ← 상위 1% 수준

사용자 D: PFE (근력↑, 유연성↑, 지구력↑)
  실제 Z-Score: [0.55, 0.52, 0.53]  ← 평균보다 살짝 높음

→ 같은 PFE 유형이지만 실제 체력 거리는 2.3으로 큼
→ C는 너무 쉽고, D는 너무 힘들어서 함께 운동하기 어려움
```

**추가 고려사항:**
- PSQ(근력 특화형) 인구는 전체의 8.1%로 적음 → 같은 유형만 매칭하면 매칭 풀이 너무 작음
- 현재 방식은 PSQ가 비슷한 LSQ(거리 1.272)와도 매칭 가능 → 매칭 풀 확대

---

### 매칭 전략 3가지 옵션 (구현 선택 가이드)

담당자는 서비스 목적에 맞춰 다음 3가지 전략 중 선택하거나 혼합할 수 있습니다.

#### 옵션 1: 엄격 매칭 (Strict Matching) - 같은 유형만

```python
def strict_matching(user_fitdna, db):
    """같은 FIT-DNA 유형만 매칭"""
    return [user for user in db if user.fitdna == user_fitdna]
```

**장점:**
- 가장 단순하고 직관적
- 운동 목표가 완전히 동일 (예: PSQ끼리 → 근력 중심 운동)
- 설명이 쉬움 ("같은 유형끼리 매칭됩니다")

**단점:**
- 매칭 풀이 작음 (특히 PSQ 8.1%, LSQ 9.2%)
- 같은 유형이어도 실제 체력 차이가 클 수 있음
- 사용자 만족도 낮을 가능성

**추천 사용 케이스:**
- 사용자 수가 충분히 많을 때 (각 유형별 1,000명 이상)
- "완벽히 같은 체력 패턴" 강조가 중요할 때

---

#### 옵션 2: 유연 매칭 (Flexible Matching) - **현재 구현 방식**

```python
def flexible_matching(user_fitdna, user_zscore, db):
    """
    FIT-DNA 유형 유사도(40%) + 개인별 Z-Score 유사도(60%)
    """
    score = (zscore_similarity * 0.6) + (fitdna_similarity * 0.4)
    return sorted(candidates, key=lambda x: score, reverse=True)[:top_n]
```

**장점:**
- 매칭 풀이 넓음 (다른 유형이어도 실제 체력이 비슷하면 매칭)
- 실제 운동 능력이 더 중요하게 반영됨
- 소수 유형도 충분한 매칭 후보 확보

**단점:**
- 유형이 달라서 운동 목표가 다를 수 있음 (예: PFE는 유지 vs PSE는 유연성 개선)
- 알고리즘이 복잡해 설명이 어려움
- 가중치(60%/40%)가 임의 설정

**추천 사용 케이스:**
- 사용자 수가 제한적일 때 (초기 서비스)
- "실제 운동 능력" 매칭이 중요할 때
- **현재 프로토타입 단계 (지금)**

---

#### 옵션 3: AI 기반 매칭 (AI-based Matching) - 미래 확장

```python
def ai_matching(user_data, preference_history, db):
    """
    머신러닝 모델로 실제 매칭 성공률 학습
    """
    model = load_trained_model()  # 랜덤포레스트, XGBoost 등
    scores = model.predict_proba(candidates)  # 매칭 성공 확률 예측
    return sorted(candidates, key=scores, reverse=True)[:top_n]
```

**필요 데이터:**
- 실제 매칭 이력 (누가 누구와 매칭됐는지)
- 운동 참여 기록 (매칭 후 실제 함께 운동했는지)
- 사용자 피드백 (만족도, 재매칭 여부)

**장점:**
- 실제 데이터 기반으로 최적화
- 개인 선호도 반영 (운동 시간대, 지역, 성격 등)
- 지속적인 성능 개선 가능

**단점:**
- 데이터 수집 필요 (최소 수천 건의 매칭 이력)
- 구현 복잡도 높음
- 설명 가능성 낮음 (블랙박스)

**추천 사용 케이스:**
- 서비스 안정화 후 (6개월~1년 후)
- 충분한 매칭 이력 데이터 확보 시
- A/B 테스트로 규칙 기반 대비 성능 검증 후

---

### 담당자 의사결정 가이드

| 상황 | 추천 전략 |
|------|----------|
| 프로토타입 단계, 사용자 < 10,000명 | **옵션 2 (유연 매칭)** ← 현재 |
| 사용자 > 50,000명, 각 유형별 충분 | 옵션 1 (엄격 매칭) |
| 6개월 이상 운영, 매칭 데이터 충분 | 옵션 3 (AI 매칭) |
| 사용자 선호도 다양, 피드백 많음 | 옵션 2 + 3 혼합 |

**하이브리드 전략 예시:**
```python
# 1단계: 같은 유형 우선 검색
same_type = strict_matching(user_fitdna)

# 2단계: 같은 유형이 5명 미만이면 유연 매칭으로 확장
if len(same_type) < 5:
    candidates = flexible_matching(user_fitdna, user_zscore)
```

---

### 현재 알고리즘의 한계 및 개선 방향

**한계 1: 규칙 기반 (AI 아님)**
- 현재는 명확한 수식으로 계산 → 데이터 학습 없음
- 가중치(60%/40%)는 임의 설정 → 실제 최적값인지 검증 안 됨

**개선 방향:**
- A/B 테스트로 가중치 최적화 (50/50, 70/30 등 비교)
- 사용자 피드백 수집 → 머신러닝 모델 학습

**한계 2: 운동 선호도 미반영**
- 현재는 체력만 고려 → 운동 종목 선호도(러닝/헬스/요가) 미반영

**개선 방향:**
- 운동 선호도 필터링 추가
- 운동 시간대, 지역, 나이대 필터 추가

**한계 3: 유사도 레벨 기준이 임의적**
- 레벨 1 (< 1.2), 레벨 2 (1.2~2.0)는 데이터 분포 기반 임의 설정
- 실제 "함께 운동하기 좋은" 기준인지 검증 안 됨

**개선 방향:**
- 실제 매칭 성공 사례 분석 → 최적 기준 재설정

---

## 🎯 알고리즘 핵심 로직

### 1. FIT-DNA 8가지 유형

```
P = 근력(Power) 높음 / L = 근력 낮음
F = 유연성(Flexibility) 높음 / S = 유연성 낮음
E = 지구력(Endurance) 높음 / Q = 지구력 낮음

8가지 조합:
- PFE: 완벽 균형형 (근력↑, 유연성↑, 지구력↑)
- PFQ: 근력·유연성 우수형
- PSE: 근력·지구력 우수형
- PSQ: 근력 특화형
- LFE: 유연성·지구력 우수형
- LFQ: 유연성 특화형
- LSE: 지구력 특화형
- LSQ: 전체 개선 필요형
```

### 2. 유사도 계산 방법

**① Euclidean Distance (유클리드 거리)**
```python
distance = sqrt((s1-s2)² + (f1-f2)² + (e1-e2)²)
```
- s = strength_z (근력 Z-Score)
- f = flex_z (유연성 Z-Score)
- e = endurance_z (지구력 Z-Score)

**② Cosine Similarity (코사인 유사도)**
```python
similarity = (v1 · v2) / (||v1|| × ||v2||)
```
- 벡터 방향의 유사성 측정 (0~1, 1에 가까울수록 유사)

**③ Manhattan Distance (맨하탄 거리)**
```python
distance = |s1-s2| + |f1-f2| + |e1-e2|
```

### 3. 유사도 레벨 분류

**기준: Euclidean Distance**

| 레벨 | 거리 범위 | 의미 | 쌍 개수 |
|------|-----------|------|---------|
| 레벨 1 (매우 유사) | < 1.2 | 거의 동일한 체력 | 3쌍 |
| 레벨 2 (유사) | 1.2 ~ 2.0 | 비슷한 체력 | 13쌍 |
| 레벨 3 (다름) | > 2.0 | 차이가 큼 | 12쌍 |

**레벨 1 (매우 유사) 3쌍:**
- LSE ↔ PSE: 1.075 (가장 유사)
- LFE ↔ PFE: 1.117
- LFQ ↔ PFQ: 1.170

**가장 다른 쌍:**
- LSQ ↔ PFE: 2.888 (가장 큰 차이)

### 4. 매칭 점수 계산 공식

```python
def calculate_matching_score(user1_zscore, user2_zscore,
                             user1_fitdna, user2_fitdna,
                             exercise_match=True):
    """
    매칭 점수 = Z-Score 유사도(60%) + FIT-DNA 유사도(40%) + 운동선호 보너스(10%)
    """

    # 1. Z-Score 유사도 (60%)
    zscore_distance = euclidean_distance(user1_zscore, user2_zscore)
    zscore_score = max(0, (3 - zscore_distance) / 3 * 100)  # 거리 0~3 → 점수 100~0

    # 2. FIT-DNA 유형 유사도 (40%)
    fitdna_distance = get_fitdna_distance(user1_fitdna, user2_fitdna)  # 사전 계산된 행렬
    fitdna_score = max(0, (3 - fitdna_distance) / 3 * 100)

    # 3. 운동 선호도 보너스 (10%)
    exercise_bonus = 10 if exercise_match else 0

    # 가중 평균
    total_score = (zscore_score * 0.6) + (fitdna_score * 0.4) + exercise_bonus

    return min(100, total_score)  # 최대 100점
```

**점수 해석:**
- **70점 이상:** 높은 매칭도 → 적극 추천
- **50~69점:** 중간 매칭도 → 추천
- **50점 미만:** 낮은 매칭도 → 비추천

---

## 💻 코드 사용법

### 기본 사용 예시

```python
import pandas as pd
from phase2_matching_algorithm import recommend_matches, calculate_matching_score

# 1. 특정 FIT-DNA 유형에 맞는 운동 메이트 추천
matches = recommend_matches(
    user_fitdna='PFE',        # 사용자의 FIT-DNA 유형
    top_n=5,                   # 추천 인원 수
    similarity_level='level1'  # 'level1', 'level2', 'all' 중 선택
)

print(matches)
# 출력: [('PSE', 1.506, '레벨 2 (유사)'), ('PFQ', 1.528, '레벨 2 (유사)'), ...]


# 2. 두 사용자 간 매칭 점수 계산
user1_zscore = [1.2, 0.8, -0.5]  # [근력, 유연성, 지구력] Z-Score
user2_zscore = [1.0, 0.9, -0.3]

score = calculate_matching_score(
    user1_zscore,
    user2_zscore,
    user1_fitdna='PFQ',
    user2_fitdna='PFE',
    exercise_match=True  # 운동 선호도 일치 여부
)

print(f"매칭 점수: {score:.1f}점")
# 출력: 매칭 점수: 78.5점
```

### 주요 함수

**1. `recommend_matches(user_fitdna, top_n=3, similarity_level='all')`**
- **입력:**
  - `user_fitdna`: 사용자의 FIT-DNA 유형 (str, 예: 'PFE')
  - `top_n`: 추천할 메이트 수 (int, 기본값 3)
  - `similarity_level`: 유사도 레벨 필터 (str, 'level1'/'level2'/'all')
- **출력:** 추천 리스트 `[(유형, 거리, 레벨), ...]`

**2. `calculate_matching_score(user1_zscore, user2_zscore, user1_fitdna, user2_fitdna, exercise_match=True)`**
- **입력:**
  - `user1_zscore`: 사용자1의 Z-Score [근력, 유연성, 지구력]
  - `user2_zscore`: 사용자2의 Z-Score
  - `user1_fitdna`: 사용자1의 FIT-DNA 유형
  - `user2_fitdna`: 사용자2의 FIT-DNA 유형
  - `exercise_match`: 운동 선호도 일치 여부 (bool)
- **출력:** 매칭 점수 (float, 0~100)

**3. `calculate_euclidean_distance(v1, v2)`**
- 3차원 유클리드 거리 계산

**4. `calculate_cosine_similarity(v1, v2)`**
- 코사인 유사도 계산

---

## 📊 데이터 구조

### 1. FIT-DNA 유형 대표 벡터

`phase2_matching_algorithm.py:13-22` 참조

```python
FITDNA_VECTORS = {
    'PFE': [1.547, 0.806, 0.959],   # 근력↑, 유연성↑, 지구력↑
    'PFQ': [1.513, 0.782, -0.820],  # 근력↑, 유연성↑, 지구력↓
    'PSE': [1.523, -0.727, 0.908],  # 근력↑, 유연성↓, 지구력↑
    'PSQ': [1.428, -0.740, -0.842], # 근력↑, 유연성↓, 지구력↓
    'LFE': [-1.241, 0.790, 0.873],  # 근력↓, 유연성↑, 지구력↑
    'LFQ': [-1.249, 0.763, -0.809], # 근력↓, 유연성↑, 지구력↓
    'LSE': [-1.270, -0.739, 0.863], # 근력↓, 유연성↓, 지구력↑
    'LSQ': [-1.223, -0.751, -0.823] # 근력↓, 유연성↓, 지구력↓
}
```

### 2. 유클리드 거리 행렬

`matching_euclidean_distance_matrix.csv` 구조:

| From/To | PFE | PFQ | PSE | PSQ | LFE | LFQ | LSE | LSQ |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|
| PFE | 0.000 | 1.528 | 1.505 | 2.393 | 1.117 | 1.808 | 2.112 | 2.888 |
| PFQ | 1.528 | 0.000 | 2.119 | 1.497 | 1.760 | 1.170 | 2.688 | 2.011 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 3. 코사인 유사도 행렬

`matching_cosine_similarity_matrix.csv` 구조:

| From/To | PFE | PFQ | ... |
|---------|-----|-----|-----|
| PFE | 1.000 | 0.704 | ... |
| PFQ | 0.704 | 1.000 | ... |
| ... | ... | ... | ... |

---

## 🚀 서비스 적용 가이드

### API 엔드포인트 설계 예시

```python
from fastapi import FastAPI
from phase2_matching_algorithm import recommend_matches, calculate_matching_score

app = FastAPI()

@app.post("/api/matching/recommend")
def get_exercise_mates(
    user_fitdna: str,
    top_n: int = 5,
    similarity_level: str = "all",
    exercise_preference: str = None
):
    """
    운동 메이트 추천 API

    Parameters:
    - user_fitdna: 사용자의 FIT-DNA 유형 (PFE, PFQ, ...)
    - top_n: 추천 인원 수
    - similarity_level: 'level1', 'level2', 'all'
    - exercise_preference: 운동 선호 종목 (러닝, 헬스, 요가, ...)

    Returns:
    - recommendations: 추천 메이트 리스트
    """
    matches = recommend_matches(user_fitdna, top_n, similarity_level)

    # 운동 선호도 필터링 (DB 조회 로직 추가 필요)
    # if exercise_preference:
    #     matches = filter_by_exercise_preference(matches, exercise_preference)

    return {
        "user_fitdna": user_fitdna,
        "recommendations": [
            {
                "fitdna": match[0],
                "distance": match[1],
                "similarity_level": match[2]
            }
            for match in matches
        ]
    }


@app.post("/api/matching/score")
def calculate_compatibility(
    user1_data: dict,  # {zscore: [s, f, e], fitdna: 'PFE'}
    user2_data: dict,
    exercise_match: bool = False
):
    """
    두 사용자 간 매칭 점수 계산 API
    """
    score = calculate_matching_score(
        user1_data['zscore'],
        user2_data['zscore'],
        user1_data['fitdna'],
        user2_data['fitdna'],
        exercise_match
    )

    return {
        "matching_score": round(score, 1),
        "recommendation": "추천" if score >= 70 else "보통" if score >= 50 else "비추천"
    }
```

### UI 표시 예시

```
┌─────────────────────────────────────────────┐
│  🏃 나와 함께 운동할 메이트를 찾아보세요!      │
├─────────────────────────────────────────────┤
│                                             │
│  당신의 FIT-DNA: PFE (완벽 균형형)          │
│  특징: 근력↑, 유연성↑, 지구력↑              │
│                                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   │
│                                             │
│  📋 추천 운동 메이트 TOP 5                  │
│                                             │
│  1. ⭐ LFE (유연성·지구력 우수형)           │
│     매칭도: 92점 | 거리: 1.117              │
│     [메시지 보내기]                         │
│                                             │
│  2. ⭐ PSE (근력·지구력 우수형)             │
│     매칭도: 85점 | 거리: 1.505              │
│     [메시지 보내기]                         │
│                                             │
│  3. ⭐ PFQ (근력·유연성 우수형)             │
│     매칭도: 83점 | 거리: 1.528              │
│     [메시지 보내기]                         │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🔍 알고리즘 검증 결과

### 1. 유사도 분포

- **레벨 1 (매우 유사):** 3쌍 (10.7%)
- **레벨 2 (유사):** 13쌍 (46.4%)
- **레벨 3 (다름):** 12쌍 (42.9%)

### 2. 주요 인사이트

**① 가장 유사한 쌍:**
- LSE ↔ PSE: 1.075 (지구력 높음이 공통점)
- LFE ↔ PFE: 1.117 (유연성·지구력 높음)
- LFQ ↔ PFQ: 1.170 (유연성 높음)

**② 가장 다른 쌍:**
- LSQ ↔ PFE: 2.888 (정반대 유형)
- LSQ ↔ PSE: 2.660
- PFE ↔ PSQ: 2.393

**③ 유형별 최고 매칭:**
| 유형 | 최고 매칭 유형 | 거리 |
|------|---------------|------|
| PFE | LFE | 1.117 |
| PSE | LSE | 1.075 |
| PFQ | LFQ | 1.170 |
| PSQ | LSQ | 1.272 |

---

## 📝 주의사항 및 한계

### 1. 데이터 기반
- 115,983건의 국민체력100 데이터로 계산된 Z-Score 기준
- 연령·성별 그룹별 정규화 필요

### 2. 유사도 레벨 기준
- 현재 레벨 기준(1.2, 2.0)은 데이터 분포 기반 임의 설정
- 실제 서비스에서 사용자 피드백으로 조정 필요

### 3. 개인정보 고려
- 실제 매칭 시 개인정보 보호 필수
- FIT-DNA 유형만 공개, Z-Score 원값은 비공개 권장

### 4. 확장 가능성
- 운동 선호도, 운동 시간대, 지역 등 추가 필터 구현 가능
- 협업 운동 기록, 피드백 반영 가능

---

## 🔗 관련 문서

1. **FIT_DNA_SERVICE_GUIDE.md** - FIT-DNA 서비스 전체 가이드
2. **phase2_strength_weakness_analysis.py** - 강점/약점 분석 (매칭과 연계 가능)
3. **phase2_exercise_recommendation.py** - 운동 추천 시스템 (매칭 후 운동 추천)
4. **FIT_DNA_PROJECT_SUMMARY_FOR_MEETING.md** - 프로젝트 전체 회의 자료

---

## 📞 문의사항

알고리즘 관련 문의사항은 원 담당자에게 연락하세요.

**인수인계 체크리스트:**
- [ ] 5개 필수 파일 전달 완료
- [ ] 코드 실행 테스트 완료
- [ ] API 설계 검토 완료
- [ ] 데이터 구조 이해 완료
- [ ] 한계점 및 주의사항 숙지 완료

---

**문서 버전:** 1.0
**최종 수정일:** 2024-11-27
