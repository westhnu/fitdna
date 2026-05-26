"""
FIT-DNA 백엔드 통합 예시 (FastAPI)
실제 사용자가 측정값을 입력하고 FIT-DNA 결과를 받는 전체 프로세스
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
from typing import Optional
from fitdna_calculator import calculate_zscore, calculate_fitdna, get_fitdna_description

# ============================================================
# 1. 앱 초기화 및 참조 테이블 로드
# ============================================================

app = FastAPI(title="FIT-DNA API")

# 서버 시작 시 참조 테이블 한 번만 로드 (성능 최적화)
print("참조 테이블 로드 중...")
with open('fitdna_reference_table.pkl', 'rb') as f:
    REFERENCE_TABLE = pickle.load(f)
print(f"참조 테이블 로드 완료: {len(REFERENCE_TABLE)} 항목")


# ============================================================
# 2. 요청/응답 데이터 모델
# ============================================================

class UserMeasurement(BaseModel):
    """사용자가 입력하는 체력 측정값"""
    age: int  # 나이
    gender: str  # 성별 ('M' 또는 'F')

    # 근력 측정값 (kg 단위, 하나 이상 필요)
    grip_strength_right: Optional[float] = None  # 악력(오른손)
    grip_strength_left: Optional[float] = None   # 악력(왼손)
    standing_long_jump: Optional[float] = None   # 제자리멀리뛰기(cm)

    # 유연성 측정값 (cm 단위, 하나 이상 필요)
    sit_and_reach: Optional[float] = None        # 앉아윗몸앞으로굽히기

    # 지구력 측정값 (하나 이상 필요)
    vo2max: Optional[float] = None               # VO2max
    shuttle_run_time: Optional[float] = None     # 왕복오래달리기(초)

    threshold: float = 0.5  # High/Low 기준값 (기본: 0.5)


class FitDNAResult(BaseModel):
    """FIT-DNA 계산 결과"""
    fitdna_type: str           # 예: "PFE"
    type_name: str             # 예: "완벽 균형형"
    description: str           # 유형 설명

    # 각 축별 상세 정보
    strength_level: str        # "High" 또는 "Low"
    flexibility_level: str
    endurance_level: str

    # Z-Score 값
    strength_zscore: float
    flexibility_zscore: float
    endurance_zscore: float

    # 입력값 정보
    age: int
    gender: str


# ============================================================
# 3. 핵심 로직: 측정값 → 3축 평균 계산
# ============================================================

def calculate_axis_averages(data: UserMeasurement, ref_table: dict) -> tuple:
    """
    여러 측정값을 3축(근력/유연성/지구력)별로 평균 계산

    Returns:
        (strength_z, flexibility_z, endurance_z) 튜플
    """
    age = data.age
    gender = data.gender

    # 근력 축 계산
    strength_values = []
    if data.grip_strength_right is not None:
        try:
            z = calculate_zscore(data.grip_strength_right, age, gender, 'strength', ref_table)
            strength_values.append(z)
        except ValueError:
            pass

    if data.grip_strength_left is not None:
        try:
            z = calculate_zscore(data.grip_strength_left, age, gender, 'strength', ref_table)
            strength_values.append(z)
        except ValueError:
            pass

    if data.standing_long_jump is not None:
        try:
            z = calculate_zscore(data.standing_long_jump, age, gender, 'strength', ref_table)
            strength_values.append(z)
        except ValueError:
            pass

    if not strength_values:
        raise HTTPException(status_code=400, detail="근력 측정값이 최소 1개 필요합니다.")

    strength_z = sum(strength_values) / len(strength_values)

    # 유연성 축 계산
    flex_values = []
    if data.sit_and_reach is not None:
        try:
            z = calculate_zscore(data.sit_and_reach, age, gender, 'flexibility', ref_table)
            flex_values.append(z)
        except ValueError:
            pass

    if not flex_values:
        raise HTTPException(status_code=400, detail="유연성 측정값이 최소 1개 필요합니다.")

    flex_z = sum(flex_values) / len(flex_values)

    # 지구력 축 계산
    endurance_values = []
    if data.vo2max is not None:
        try:
            z = calculate_zscore(data.vo2max, age, gender, 'endurance', ref_table)
            endurance_values.append(z)
        except ValueError:
            pass

    if data.shuttle_run_time is not None:
        try:
            # 시간 기록은 낮을수록 좋으므로 부호 반전
            z = -calculate_zscore(data.shuttle_run_time, age, gender, 'endurance', ref_table)
            endurance_values.append(z)
        except ValueError:
            pass

    if not endurance_values:
        raise HTTPException(status_code=400, detail="지구력 측정값이 최소 1개 필요합니다.")

    endurance_z = sum(endurance_values) / len(endurance_values)

    return strength_z, flex_z, endurance_z


# ============================================================
# 4. API 엔드포인트
# ============================================================

@app.post("/calculate-fitdna", response_model=FitDNAResult)
async def calculate_user_fitdna(data: UserMeasurement):
    """
    사용자의 체력 측정값을 받아 FIT-DNA 유형을 계산합니다.

    사용 예시:
    ```
    POST /calculate-fitdna
    {
      "age": 25,
      "gender": "M",
      "grip_strength_right": 42.0,
      "sit_and_reach": 20.0,
      "vo2max": 38.0,
      "threshold": 0.5
    }
    ```
    """
    try:
        # 1. 연령 검증
        if data.age < 10 or data.age > 100:
            raise HTTPException(status_code=400, detail="나이는 10세~100세 사이여야 합니다.")

        # 2. 성별 검증
        if data.gender not in ['M', 'F']:
            raise HTTPException(status_code=400, detail="성별은 'M' 또는 'F'여야 합니다.")

        # 3. 3축 Z-Score 계산
        strength_z, flex_z, endurance_z = calculate_axis_averages(data, REFERENCE_TABLE)

        # 4. FIT-DNA 계산
        fitdna_type = calculate_fitdna(strength_z, flex_z, endurance_z, threshold=data.threshold)

        # 5. 유형 정보 조회
        info = get_fitdna_description(fitdna_type)

        # 6. 결과 반환
        return FitDNAResult(
            fitdna_type=fitdna_type,
            type_name=info['name'],
            description=info['description'],
            strength_level=info['strength'],
            flexibility_level=info['flexibility'],
            endurance_level=info['endurance'],
            strength_zscore=round(strength_z, 2),
            flexibility_zscore=round(flex_z, 2),
            endurance_zscore=round(endurance_z, 2),
            age=data.age,
            gender=data.gender
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")


@app.get("/fitdna-types")
async def get_all_fitdna_types():
    """
    8가지 FIT-DNA 유형 전체 정보를 반환합니다.
    """
    types = ['PFE', 'PFQ', 'PSE', 'PSQ', 'LFE', 'LFQ', 'LSE', 'LSQ']
    result = {}
    for fitdna_type in types:
        info = get_fitdna_description(fitdna_type)
        result[fitdna_type] = info
    return result


@app.get("/reference-coverage")
async def get_reference_coverage():
    """
    참조 테이블의 연령×성별 커버리지를 반환합니다.
    """
    ages = set()
    genders = set()

    for key in REFERENCE_TABLE.keys():
        age, gender, metric = key
        ages.add(age)
        genders.add(gender)

    return {
        "age_range": f"{min(ages)}세 ~ {max(ages)}세",
        "genders": sorted(list(genders)),
        "total_age_gender_groups": len(ages) * len(genders),
        "total_reference_entries": len(REFERENCE_TABLE),
        "metrics": ["strength", "flexibility", "endurance"]
    }


@app.get("/")
async def root():
    """API 정보"""
    return {
        "service": "FIT-DNA API",
        "version": "1.0",
        "endpoints": {
            "POST /calculate-fitdna": "사용자 측정값으로 FIT-DNA 계산",
            "GET /fitdna-types": "8가지 FIT-DNA 유형 정보",
            "GET /reference-coverage": "참조 테이블 커버리지 정보"
        }
    }


# ============================================================
# 5. 서버 실행 방법
# ============================================================

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("FIT-DNA API 서버 시작")
    print("=" * 60)
    print("\n사용 방법:")
    print("1. 서버 실행: python backend_integration_example.py")
    print("2. API 문서: http://localhost:8000/docs")
    print("3. 테스트:")
    print("""
    curl -X POST http://localhost:8000/calculate-fitdna \\
         -H "Content-Type: application/json" \\
         -d '{
           "age": 25,
           "gender": "M",
           "grip_strength_right": 42.0,
           "sit_and_reach": 20.0,
           "vo2max": 38.0
         }'
    """)
    print("\n" + "=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
