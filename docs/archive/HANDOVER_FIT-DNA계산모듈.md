# FIT-DNA 계산 모듈 인수인계 문서

---

## 📋 인수인계 개요

**담당 기능:** 사용자 체력 측정값을 FIT-DNA 유형으로 변환
**작성일:** 2024-11-27
**데이터 기준:** 국민체력100 데이터 (115,983건)

---

## 📦 인수인계 파일 목록

### 1. 핵심 파일 (필수)

| 파일명 | 용도 | 크기 | 비고 |
|--------|------|------|------|
| **fitdna_calculator.py** | FIT-DNA 계산 함수 모듈 | 8KB | 메인 로직 |
| **backend_integration_example.py** | FastAPI 백엔드 통합 예시 | 9KB | 실제 서비스 구현 예시 |
| **FIT_DNA_SERVICE_GUIDE.md** | FIT-DNA 서비스 가이드 | 15KB | 전체 설명서 |
| **FIT_DNA_측정항목_매핑표.csv** | 측정 항목 → 3축 매핑 | 1KB | 15개 항목 정의 |

### 2. 데이터 파일 (권장)

| 파일명 | 용도 | 크기 | 위치 |
|--------|------|------|------|
| **fit_dna_preprocessed_cp949.csv** | 115,983명의 FIT-DNA 데이터 (Z-Score 포함) | 9.1MB | `최종/최종/체력측정 항목별 측정 데이터/` |
| **fitdna_reference_table.json** | 연령×성별 참조 테이블 (JSON) | ~50KB | 루트 디렉토리 |
| **fitdna_reference_table.pkl** | 연령×성별 참조 테이블 (Pickle) | ~40KB | 루트 디렉토리 |
| **fitdna_reference_table.csv** | 연령×성별 참조 테이블 (CSV) | ~30KB | 루트 디렉토리 |

**✅ 중요: 전처리 데이터를 바로 사용 가능!**

이 파일에는 이미 **Z-Score가 계산되어 있어서** 별도의 참조 데이터(평균·표준편차) 없이도 바로 FIT-DNA를 사용할 수 있습니다.

**사용 방법:**
```python
import pandas as pd

# 전처리 데이터 로드
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv',
                 encoding='cp949')

# 특정 사용자의 Z-Score와 FIT-DNA 조회
user_data = df[df['MESURE_AGE_CO'] == 25].iloc[0]
print(f"근력 Z-Score: {user_data['strength_z']}")
print(f"유연성 Z-Score: {user_data['flex_z']}")
print(f"지구력 Z-Score: {user_data['endurance_z']}")
print(f"FIT-DNA: {user_data['FIT_DNA']}")
```

**⚠️ 새로운 사용자 입력을 받는 경우:**

**사용자는 Z-Score를 모릅니다. 사용자가 입력하는 것은 실제 측정값입니다:**
- 악력: 42kg
- 앉아윗몸앞으로굽히기: 20cm
- VO2max: 38

이런 **원본 측정값을 Z-Score로 변환**하려면 **연령×성별 참조 테이블**이 필요합니다.

**참조 테이블 파일:**
- `fitdna_reference_table.json` - 웹 API용 (JSON 형식)
- `fitdna_reference_table.pkl` - Python 백엔드용 (빠름)
- `fitdna_reference_table.csv` - 사람이 읽기 쉬운 형식

이 파일들은 전처리 데이터에서 `generate_reference_table.py`로 생성되었으며, 11세~92세, 남녀 총 161개 연령×성별 그룹의 평균·표준편차를 포함합니다.

### 3. 참조 테이블 생성 파일

| 파일명 | 용도 |
|--------|------|
| **generate_reference_table.py** | 참조 테이블 생성 스크립트 (전처리 데이터에서 추출) |
| **reference_table_usage_example.py** | 참조 테이블 사용 예시 코드 |

### 4. 기타 참조 파일

| 파일명 | 용도 |
|--------|------|
| **phase1_fitdna_type_analysis_report.txt** | 8가지 유형 분석 리포트 |
| **generate_measurement_mapping_table.py** | 측정 항목 매핑 생성 스크립트 |

---

## 🎯 FIT-DNA 계산 로직

### 1. FIT-DNA란?

**FIT-DNA는 개인의 체력을 3축(근력/유연성/지구력)으로 분석하여 8가지 유형으로 분류하는 시스템입니다.**

```
3개 축 × 2단계(High/Low) = 8가지 조합

- P (Power, 근력 High) / L (Light, 근력 Low)
- F (Flexibility, 유연성 High) / S (Stiff, 유연성 Low)
- E (Endurance, 지구력 High) / Q (Quick, 지구력 Low)
```

**8가지 유형:**
1. **PFE** - 완벽 균형형 (근력↑, 유연성↑, 지구력↑)
2. **PFQ** - 근력·유연성 우수형 (근력↑, 유연성↑, 지구력↓)
3. **PSE** - 근력·지구력 우수형 (근력↑, 유연성↓, 지구력↑)
4. **PSQ** - 근력 특화형 (근력↑, 유연성↓, 지구력↓)
5. **LFE** - 유연성·지구력 우수형 (근력↓, 유연성↑, 지구력↑)
6. **LFQ** - 유연성 특화형 (근력↓, 유연성↑, 지구력↓)
7. **LSE** - 지구력 특화형 (근력↓, 유연성↓, 지구력↑)
8. **LSQ** - 전체 개선 필요형 (근력↓, 유연성↓, 지구력↓)

---

### 2. 계산 프로세스

```
[1단계] 체력 측정
    ↓
    최소 5개 항목 측정 (악력, 제자리멀리뛰기, 유연성, VO2max 등)

[2단계] 3축 집계
    ↓
    15개 측정 항목 → 3개 축으로 매핑
    - 근력: 악력(좌/우), 제자리멀리뛰기, 윗몸일으키기 등
    - 유연성: 앉아윗몸앞으로굽히기, 체전굴 등
    - 지구력: VO2max, 왕복오래달리기, 하버드스텝 등

[3단계] Z-Score 정규화
    ↓
    Z-Score = (개인값 - 연령×성별 그룹평균) / 그룹표준편차

[4단계] High/Low 분류
    ↓
    기준값 0.5 적용
    - Z-Score ≥ 0.5 → High
    - Z-Score < 0.5 → Low

[5단계] FIT-DNA 코드 생성
    ↓
    3개 축의 High/Low 조합 → 8가지 유형 중 하나
```

---

## 💻 코드 사용법

### 기본 함수: `calculate_fitdna()`

**가장 간단한 사용 (Z-Score를 이미 알고 있는 경우):**

```python
from fitdna_calculator import calculate_fitdna, get_fitdna_description

# Z-Score 입력
strength_z = 1.2   # 근력 Z-Score
flex_z = 0.6       # 유연성 Z-Score
endurance_z = -0.3 # 지구력 Z-Score

# FIT-DNA 계산
fitdna = calculate_fitdna(strength_z, flex_z, endurance_z)
print(fitdna)  # 'PFQ'

# 상세 정보 조회
info = get_fitdna_description(fitdna)
print(info['name'])         # '근력·유연성 우수형'
print(info['description'])  # '근력과 유연성은 우수하나 지구력 개선이 필요합니다.'
```

---

### Z-Score 계산 함수: `calculate_zscore()`

**측정값에서 Z-Score 계산 (참조 데이터 필요):**

```python
from fitdna_calculator import calculate_zscore, calculate_fitdna

# 참조 데이터 (실제로는 DB에서 조회)
reference_data = {
    (25, 'M', 'grip'): {'mean': 35.0, 'std': 5.0},
    (25, 'M', 'flexibility'): {'mean': 15.0, 'std': 6.0},
    (25, 'M', 'vo2max'): {'mean': 45.0, 'std': 8.0},
}

# 25세 남성의 측정값
age = 25
gender = 'M'
grip = 42       # 악력 42kg
flexibility = 20 # 유연성 20cm
vo2max = 38     # VO2max 38

# Z-Score 계산
s_z = calculate_zscore(grip, age, gender, 'grip', reference_data)
f_z = calculate_zscore(flexibility, age, gender, 'flexibility', reference_data)
e_z = calculate_zscore(vo2max, age, gender, 'vo2max', reference_data)

print(f"Z-Scores: 근력={s_z:.2f}, 유연성={f_z:.2f}, 지구력={e_z:.2f}")
# Z-Scores: 근력=1.40, 유연성=0.83, 지구력=-0.88

# FIT-DNA 계산
fitdna = calculate_fitdna(s_z, f_z, e_z)
print(fitdna)  # 'PFQ'
```

---

### 주요 함수 설명

**1. `calculate_fitdna(strength_z, flex_z, endurance_z, threshold=0.5)`**

- **입력:**
  - `strength_z`: 근력 Z-Score (float)
  - `flex_z`: 유연성 Z-Score (float)
  - `endurance_z`: 지구력 Z-Score (float)
  - `threshold`: High/Low 기준값 (float, 기본값 0.5)

- **출력:** FIT-DNA 코드 (str, 예: 'PFE')

- **로직:**
```python
p_code = 'P' if strength_z >= threshold else 'L'
f_code = 'F' if flex_z >= threshold else 'S'
e_code = 'E' if endurance_z >= threshold else 'Q'
return f"{p_code}{f_code}{e_code}"
```

---

**2. `get_fitdna_description(fitdna_code)`**

- **입력:** FIT-DNA 코드 (str, 예: 'PFE')

- **출력:** 상세 정보 (dict)
```python
{
    'name': '완벽 균형형',
    'strength': 'High',
    'flexibility': 'High',
    'endurance': 'High',
    'description': '근력, 유연성, 지구력 모두 우수한 이상적인 체력 상태입니다.'
}
```

---

**3. `calculate_zscore(value, age, gender, measurement_type, reference_data)`**

- **입력:**
  - `value`: 개인 측정값 (float, 예: 악력 42kg)
  - `age`: 나이 (int)
  - `gender`: 성별 (str, 'M' 또는 'F')
  - `measurement_type`: 측정 항목 (str, 예: 'grip')
  - `reference_data`: 참조 데이터 (dict)

- **출력:** Z-Score (float)

- **로직:**
```python
mean = reference_data[(age, gender, measurement_type)]['mean']
std = reference_data[(age, gender, measurement_type)]['std']
zscore = (value - mean) / std
```

---

## 🗂️ 데이터 구조

### 1. 전처리된 FIT-DNA 데이터

**파일:** `fit_dna_preprocessed_cp949.csv` (9.1MB)

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| AGRDE_FLAG_NM | 연령대 | 20대 |
| MESURE_AGE_CO | 나이 | 25 |
| SEXDSTN_FLAG_CD | 성별 | M/F |
| **strength_z** | **근력 Z-Score** | 1.23 |
| **flex_z** | **유연성 Z-Score** | 0.56 |
| **endurance_z** | **지구력 Z-Score** | -0.34 |
| **FIT_DNA** | **FIT-DNA 유형** | PFQ |

**115,983명의 FIT-DNA가 이미 계산되어 있음**

---

### 2. 측정 항목 매핑

**파일:** `FIT_DNA_측정항목_매핑표.csv`

**근력 측정 항목 (8개):**
- 악력(좌), 악력(우)
- 제자리멀리뛰기
- 윗몸일으키기
- 팔굽혀펴기
- 등 근력
- 각 근력
- 배근력

**유연성 측정 항목 (4개):**
- 앉아윗몸앞으로굽히기 (필수)
- 체전굴
- 체후굴
- 종합유연성

**지구력 측정 항목 (3개):**
- VO₂max (필수)
- 왕복오래달리기
- 하버드스텝테스트

**최소 필수 5개:**
1. 악력(좌)
2. 악력(우)
3. 제자리멀리뛰기
4. 앉아윗몸앞으로굽히기
5. VO₂max

---

### 3. 참조 데이터 생성 방법 (새 사용자 Z-Score 계산용)

**✅ 전처리 데이터에서 참조 테이블 생성 가능!**

새로운 사용자의 측정값을 Z-Score로 변환하려면 연령×성별 그룹별 평균·표준편차가 필요합니다.
이 참조 테이블은 전처리 데이터에서 직접 계산할 수 있습니다.

**참조 테이블 생성 스크립트:**

```python
import pandas as pd

# 1. 전처리 데이터 로드
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv',
                 encoding='cp949')

# 2. 연령×성별 그룹별 평균·표준편차 계산
reference_data = {}

for age in range(10, 100):  # 10세 ~ 99세
    for gender in ['M', 'F']:
        # 해당 연령×성별 그룹 필터링
        group = df[(df['MESURE_AGE_CO'] == age) & (df['SEXDSTN_FLAG_CD'] == gender)]

        if len(group) > 0:  # 데이터가 있는 경우만
            # 근력 Z-Score 역계산으로 원래 값의 평균·표준편차 추정
            # (실제로는 원본 측정값이 필요하지만, 여기서는 Z-Score 분포 사용)
            reference_data[(age, gender, 'strength')] = {
                'mean': group['strength_z'].mean(),
                'std': group['strength_z'].std()
            }
            reference_data[(age, gender, 'flexibility')] = {
                'mean': group['flex_z'].mean(),
                'std': group['flex_z'].std()
            }
            reference_data[(age, gender, 'endurance')] = {
                'mean': group['endurance_z'].mean(),
                'std': group['endurance_z'].std()
            }

# 3. 참조 데이터 저장 (pickle 또는 JSON)
import pickle
with open('fitdna_reference_data.pkl', 'wb') as f:
    pickle.dump(reference_data, f)

print(f"참조 데이터 생성 완료: {len(reference_data)} 항목")
```

**주의:**
- 위 코드는 Z-Score의 분포를 사용한 간접 계산입니다
- 정확한 계산을 위해서는 **원본 측정값**(악력 kg, 유연성 cm 등)이 필요합니다
- 원본 측정값이 없다면, 전처리 데이터의 Z-Score를 직접 사용하는 것을 권장합니다

---

## 🚀 서비스 적용 가이드

### API 엔드포인트 설계 예시

```python
from fastapi import FastAPI, HTTPException
from fitdna_calculator import calculate_fitdna, get_fitdna_description

app = FastAPI()

@app.post("/api/calculate-fitdna")
def calculate_user_fitdna(
    age: int,
    gender: str,
    measurements: dict  # {'grip_left': 42, 'grip_right': 44, ...}
):
    """
    사용자 측정값으로 FIT-DNA 계산

    Parameters:
    - age: 나이
    - gender: 성별 ('M' 또는 'F')
    - measurements: 측정값 딕셔너리

    Returns:
    - fitdna: FIT-DNA 코드
    - info: 상세 정보
    - z_scores: 3축 Z-Score
    """

    try:
        # 1. 참조 데이터 로드 (DB에서 조회)
        reference_data = load_reference_from_db()

        # 2. 측정값 → 3축 집계
        strength_values = [
            measurements.get('grip_left', 0),
            measurements.get('grip_right', 0),
            measurements.get('standing_long_jump', 0),
        ]
        strength_avg = sum(strength_values) / len(strength_values)

        # 3. Z-Score 계산
        strength_z = calculate_zscore(
            strength_avg, age, gender, 'strength', reference_data
        )
        flex_z = calculate_zscore(
            measurements['sit_and_reach'], age, gender, 'flexibility', reference_data
        )
        endurance_z = calculate_zscore(
            measurements['vo2max'], age, gender, 'endurance', reference_data
        )

        # 4. FIT-DNA 계산
        fitdna = calculate_fitdna(strength_z, flex_z, endurance_z)
        info = get_fitdna_description(fitdna)

        return {
            "fitdna": fitdna,
            "name": info['name'],
            "description": info['description'],
            "z_scores": {
                "strength": round(strength_z, 2),
                "flexibility": round(flex_z, 2),
                "endurance": round(endurance_z, 2)
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## 📊 통계 정보 (115,983명 기준)

### FIT-DNA 유형별 분포

| 유형 | 인구 비율 | 설명 |
|------|----------|------|
| **PFE** | 21.3% (24,704명) | 완벽 균형형 (가장 많음) |
| PFQ | 10.9% (12,642명) | 근력·유연성 우수형 |
| PSE | 14.1% (16,354명) | 근력·지구력 우수형 |
| PSQ | 8.1% (9,395명) | 근력 특화형 (적음) |
| LFE | 11.8% (13,686명) | 유연성·지구력 우수형 |
| LFQ | 10.2% (11,830명) | 유연성 특화형 |
| LSE | 14.4% (16,701명) | 지구력 특화형 |
| **LSQ** | 9.2% (10,671명) | 전체 개선 필요형 (적음) |

### 유형별 평균 Z-Score

| 유형 | 근력 | 유연성 | 지구력 |
|------|------|--------|--------|
| PFE | 1.547 | 0.806 | 0.959 |
| PFQ | 1.513 | 0.782 | -0.820 |
| PSE | 1.523 | -0.727 | 0.908 |
| PSQ | 1.428 | -0.740 | -0.842 |
| LFE | -1.241 | 0.790 | 0.873 |
| LFQ | -1.249 | 0.763 | -0.809 |
| LSE | -1.270 | -0.739 | 0.863 |
| LSQ | -1.223 | -0.751 | -0.823 |

---

## ⚠️ 주의사항 및 한계

### 1. 전처리 데이터 활용 (권장)

**✅ 가장 간단한 방법: 전처리 데이터를 직접 사용**

115,983명의 전처리 데이터(`fit_dna_preprocessed_cp949.csv`)에는 이미 Z-Score와 FIT-DNA가 계산되어 있습니다.

**사용 시나리오:**
1. **프로토타입/초기 서비스:** 전처리 데이터를 DB에 넣고 그대로 사용
2. **새 사용자 추가:** 유사한 연령×성별 사용자의 Z-Score 참조
3. **참조 테이블 생성:** 전처리 데이터에서 그룹별 통계 계산

**장점:**
- 별도 계산 불필요
- 115,983명의 검증된 데이터
- 바로 서비스 적용 가능

### 2. 새 사용자 Z-Score 계산 (실제 서비스 시나리오)

**⚠️ 실제 서비스에서는 사용자가 원본 측정값을 입력합니다:**

사용자 입력 예시:
```
나이: 25세
성별: 남성
악력(오른손): 42kg
앉아윗몸앞으로굽히기: 20cm
VO2max: 38
```

**이런 측정값을 Z-Score로 변환하려면 참조 테이블이 필요합니다.**

#### 참조 테이블 사용법

**1단계: 참조 테이블 로드**

```python
import pickle
import json
from fitdna_calculator import calculate_zscore, calculate_fitdna, get_fitdna_description

# 방법 1: Pickle (더 빠름, Python 백엔드용)
with open('fitdna_reference_table.pkl', 'rb') as f:
    ref_table = pickle.load(f)

# 방법 2: JSON (웹 API용)
with open('fitdna_reference_table.json', 'r', encoding='utf-8') as f:
    ref_json = json.load(f)
    # JSON 키는 문자열이므로 변환 필요
    ref_table = {}
    for key_str, value in ref_json.items():
        age, gender, metric = key_str.split('_')
        ref_table[(int(age), gender, metric)] = value
```

**2단계: 사용자 측정값을 Z-Score로 변환**

```python
# 사용자 입력값
age = 25
gender = 'M'
grip_value = 42.0      # kg
flex_value = 20.0      # cm
vo2_value = 38.0

# Z-Score 계산
strength_z = calculate_zscore(grip_value, age, gender, 'strength', ref_table)
flex_z = calculate_zscore(flex_value, age, gender, 'flexibility', ref_table)
endurance_z = calculate_zscore(vo2_value, age, gender, 'endurance', ref_table)

print(f"근력 Z-Score: {strength_z:.2f}")
print(f"유연성 Z-Score: {flex_z:.2f}")
print(f"지구력 Z-Score: {endurance_z:.2f}")
```

**3단계: FIT-DNA 계산**

```python
# FIT-DNA 유형 계산
fitdna_type = calculate_fitdna(strength_z, flex_z, endurance_z)

# 유형 정보 조회
info = get_fitdna_description(fitdna_type)

print(f"\nFIT-DNA: {fitdna_type}")
print(f"유형명: {info['name']}")
print(f"설명: {info['description']}")
```

#### 참조 테이블 생성

참조 테이블은 전처리 데이터에서 `generate_reference_table.py`로 생성됩니다:

```bash
python generate_reference_table.py
```

**생성되는 파일:**
- `fitdna_reference_table.json` - 웹 API용
- `fitdna_reference_table.pkl` - Python 백엔드용 (더 빠름)
- `fitdna_reference_table.csv` - 사람이 읽기 쉬운 형식
- `reference_table_usage_example.py` - 사용 예시 코드

**참조 테이블 구조:**
```python
{
  (25, 'M', 'strength'): {
    'mean': 0.047,      # 25세 남성 근력 Z-Score 평균
    'std': 0.702,       # 표준편차
    'count': 920        # 샘플 수
  },
  (25, 'M', 'flexibility'): {...},
  (25, 'M', 'endurance'): {...},
  # ... 11세~92세, 남녀, 3축 = 총 483개 항목
}
```

**⚠️ 중요한 주의사항:**

**현재 생성된 참조 테이블은 실제 서비스에 사용할 수 없습니다!**

**문제점:**
- 전처리 데이터에는 **이미 Z-Score로 변환된 값**만 있고 원본 측정값(kg, cm)은 없음
- 참조 테이블의 mean/std는 **Z-Score의 분포** (예: mean=0.047, std=0.702)
- 사용자 측정값(42kg)을 이 값으로 나누면 **이중 정규화 발생** → 의미 없는 값

**예시:**
```python
# 잘못된 계산 (현재 참조 테이블 사용 시)
악력 42kg → (42 - 0.047) / 0.702 = 59.74  ❌ 잘못됨!

# 올바른 계산 (원본 통계 필요)
악력 42kg → (42 - 42.5) / 6.2 = -0.08  ✅ 정상!
```

**해결 방법:**

**1. 프로토타입/초기 서비스:**
   - 전처리 데이터를 DB에 넣고 **Z-Score 직접 사용** (calculate_zscore 불필요)
   - 115,983명의 검증된 데이터 활용
   - 신규 사용자는 유사 연령×성별 사용자와 비교

**2. 실제 서비스:**
   - **원본 데이터(619MB CSV) 확보 필수**
   - 15개 측정 항목별 원본 통계 계산 (평균 악력 42.5kg, 표준편차 6.2kg 등)
   - 정확한 참조 테이블 생성
   - `generate_reference_table.py`를 원본 데이터용으로 수정

**현재 상태 요약:**
- ✅ 코드 구조: 정상 (`calculate_zscore`, `calculate_fitdna` 함수 로직 올바름)
- ✅ FIT-DNA 계산: 정상 (Z-Score → FIT-DNA 변환)
- ❌ 참조 테이블: 부정확 (Z-Score 통계이며, 원본 측정값 통계 아님)
- ✅ 전처리 데이터 사용: 정상 (프로토타입에 권장)

### 3. Z-Score 계산 전제조건

**반드시 연령×성별 그룹별 정규화가 필요합니다.**

```
✗ 잘못된 방법: 전체 평균으로 정규화
  20세 남성의 악력 40kg를 전체 평균(30kg)으로 계산
  → 여성과 노인이 포함되어 부정확

✓ 올바른 방법: 그룹별 정규화
  20세 남성의 악력 40kg를 20대 남성 평균(38kg)으로 계산
  → 동일 조건 비교로 정확
```

### 4. 기준값(threshold) 설정

**현재 기준값 0.5는 데이터 분포 기반 설정입니다.**

- Z-Score 0.5 = 상위 약 31% 수준
- 실제 서비스에서는 도메인 전문가와 협의하여 조정 가능
- 예: 0.3 (완화) / 0.7 (강화)

---

## 🔗 관련 문서

1. **FIT_DNA_SERVICE_GUIDE.md** - FIT-DNA 서비스 전체 가이드
2. **phase1_fitdna_type_analysis_report.txt** - 8가지 유형 통계 분석
3. **FIT_DNA_PROJECT_SUMMARY_FOR_MEETING.md** - 프로젝트 전체 요약
4. **HANDOVER_운동매칭알고리즘.md** - 운동 매칭 알고리즘 (FIT-DNA 활용)

---

## 📞 인수인계 체크리스트

### 핵심 파일
- [ ] `fitdna_calculator.py` 파일 전달 완료
- [ ] `generate_reference_table.py` 파일 전달 완료
- [ ] 참조 테이블 파일 3종 전달 완료 (JSON/Pickle/CSV)
- [ ] 코드 실행 테스트 완료 (`python fitdna_calculator.py`)

### 기능 이해
- [ ] 3가지 주요 함수 이해 완료
  - [ ] `calculate_fitdna()` - Z-Score → FIT-DNA
  - [ ] `get_fitdna_description()` - FIT-DNA 정보 조회
  - [ ] `calculate_zscore()` - 측정값 → Z-Score (참조 테이블 필요)
- [ ] FIT-DNA 8가지 유형 숙지 완료
- [ ] Z-Score 계산 프로세스 이해 완료

### 데이터 이해
- [ ] 전처리 데이터 활용 방법 이해 완료
- [ ] 참조 테이블 구조 이해 완료
- [ ] 참조 테이블 생성 방법 숙지 완료 (`python generate_reference_table.py`)

### 서비스 통합
- [ ] **실제 사용자 입력 시나리오** 이해 완료 (측정값 입력 → Z-Score 변환 → FIT-DNA)
- [ ] 참조 테이블 로드 방법 이해 완료 (Pickle/JSON)
- [ ] API 설계 방향 검토 완료

---

**문서 버전:** 1.0
**최종 수정일:** 2024-11-27
