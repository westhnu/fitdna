"""
FIT-DNA 체력 유형 검사 API
- 기본 정보 입력
- 체력 측정값 입력
- 라이프스타일 설문
- 결과 조회 (유형, 강점/약점, 추천 운동, 루틴)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User, FitnessMeasurement, FitDNAResult
from app.services.fitdna_service import (
    calculate_user_fitdna,
    get_fitdna_strengths_weaknesses,
    zscore_to_score_0_10
)

router = APIRouter()


# ===== 요청/응답 스키마 =====

class BasicInfoInput(BaseModel):
    """기본 정보 입력"""
    age: int
    gender: str  # 'M' or 'F'
    height: float  # cm
    weight: float  # kg


class FitnessMeasurementsInput(BaseModel):
    """체력 측정값 입력"""
    grip_right: Optional[float] = None  # 악력 (오른손) - kg
    grip_left: Optional[float] = None  # 악력 (왼손) - kg
    sit_up: Optional[int] = None  # 윗몸일으키기 - 회/분
    sit_and_reach: Optional[float] = None  # 앉아윗몸앞으로굽히기 - cm
    standing_long_jump: Optional[float] = None  # 제자리멀리뛰기 - cm
    vo2max: Optional[float] = None  # 최대산소섭취량
    shuttle_run: Optional[int] = None  # 왕복오래달리기 - 회


class LifestyleSurveyInput(BaseModel):
    """라이프스타일 설문"""
    exercise_frequency: int  # 주당 운동 횟수
    daily_activity_level: str  # 'low', 'medium', 'high'
    sleep_hours: float  # 평균 수면 시간
    stress_level: str  # 'low', 'medium', 'high'


# ===== API 엔드포인트 =====

@router.post("/basic-info")
async def submit_basic_info(data: BasicInfoInput):
    """
    1단계: 기본 정보 입력
    - 나이, 성별, 키, 몸무게
    """
    return {
        "message": "기본 정보 저장 완료",
        "data": data.dict(),
        "next_step": "측정값 입력"
    }


@router.post("/measurements")
async def submit_measurements(data: FitnessMeasurementsInput):
    """
    2단계: 체력 측정값 입력
    - 악력, 윗몸일으키기, 앉아윗몸앞으로굽히기 등
    - 사진 업로드 기능은 추후 구현
    """
    return {
        "message": "측정값 저장 완료",
        "data": data.dict(),
        "next_step": "설문 검사"
    }


@router.post("/survey")
async def submit_survey(data: LifestyleSurveyInput):
    """
    3단계: 라이프스타일 설문
    - 운동 습관, 일상 활동량, 수면, 스트레스
    """
    return {
        "message": "설문 저장 완료",
        "data": data.dict(),
        "next_step": "결과 확인"
    }


@router.post("/calculate")
async def calculate_fitdna():
    """
    FIT-DNA 유형 계산
    - 기본 정보 + 측정값 + 설문을 종합하여 유형 계산
    """
    # TODO: fitdna_from_measurements.py 연동
    return {
        "fitdna_type": "PFE",
        "type_name": "파워 애슬리트",
        "description": "근력과 지구력이 뛰어난 유형",
        "message": "계산 로직 구현 예정"
    }


@router.get("/result/{user_id}")
async def get_fitdna_result(user_id: int, db: Session = Depends(get_db)):
    """
    FIT-DNA 검사 결과 조회
    - 체력 DNA 카드
    - 강점/약점 분석
    - 추천 운동
    - 추천 루틴
    - 나와 맞는 운동 친구 유형
    """

    # 사용자 조회
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 최신 FIT-DNA 결과 조회
    fitdna_result = db.query(FitDNAResult).filter(
        FitDNAResult.user_id == user_id
    ).order_by(FitDNAResult.test_date.desc()).first()

    if not fitdna_result:
        raise HTTPException(status_code=404, detail="FIT-DNA result not found")

    # 강점/약점 가져오기 (DB에 이미 저장되어 있음)
    strengths = fitdna_result.strengths if fitdna_result.strengths else []
    weaknesses = fitdna_result.weaknesses if fitdna_result.weaknesses else []

    # 점수 가져오기 (DB에 이미 저장되어 있음)
    strength_score = fitdna_result.strength_score if fitdna_result.strength_score else 5.0
    flexibility_score = fitdna_result.flexibility_score if fitdna_result.flexibility_score else 5.0
    endurance_score = fitdna_result.endurance_score if fitdna_result.endurance_score else 5.0

    # 추천 운동 (JSON에서 가져오거나 기본값)
    recommended_exercises = fitdna_result.recommended_exercises if fitdna_result.recommended_exercises else []

    # 호환 가능한 타입 계산 (같은 카테고리나 보완 관계)
    compatible_types = _get_compatible_types(fitdna_result.fitdna_type)

    return {
        "user_id": user_id,
        "fitdna_card": {
            "type": fitdna_result.fitdna_type,
            "name": fitdna_result.fitdna_name,
            "keywords": strengths,
            "description": f"{fitdna_result.fitdna_name} 유형입니다."
        },
        "strengths_weaknesses": {
            "strength_score": strength_score,
            "flexibility_score": flexibility_score,
            "endurance_score": endurance_score,
            "strengths": strengths,
            "weaknesses": weaknesses
        },
        "recommended_exercises": recommended_exercises if recommended_exercises else [
            {"name": "스쿼트", "category": "근력", "difficulty": "중급"},
            {"name": "요가", "category": "유연성", "difficulty": "초급"},
            {"name": "조깅", "category": "지구력", "difficulty": "초급"}
        ],
        "recommended_routine": {
            "level": _get_fitness_level(strength_score, flexibility_score, endurance_score),
            "weekly_plan": {
                "monday": ["스쿼트", "벤치프레스"] if "근력" in weaknesses else ["조깅"],
                "wednesday": ["요가", "스트레칭"] if "유연성" in weaknesses else ["인터벌 러닝"],
                "friday": ["데드리프트", "풀업"] if "근력" in weaknesses else ["사이클링"],
                "sunday": ["요가", "스트레칭"]
            }
        },
        "compatible_types": compatible_types
    }


def _get_compatible_types(fitdna_type: str) -> List[str]:
    """호환 가능한 FIT-DNA 타입 반환"""
    compatibility_map = {
        "PFE": ["PFE", "PSE", "PFQ"],  # 파워형끼리
        "PFQ": ["PFE", "PFQ", "PSQ"],
        "PSE": ["PFE", "PSE", "PSQ"],
        "PSQ": ["PSE", "PSQ", "PFQ"],
        "LFE": ["LFE", "LSE", "LFQ"],  # 라이트형끼리
        "LFQ": ["LFE", "LFQ", "LSQ"],
        "LSE": ["LFE", "LSE", "LSQ"],
        "LSQ": ["LSE", "LSQ", "LFQ"]
    }
    return compatibility_map.get(fitdna_type, [fitdna_type])


def _get_fitness_level(strength: float, flexibility: float, endurance: float) -> str:
    """전체 체력 레벨 계산"""
    avg_score = (strength + flexibility + endurance) / 3
    if avg_score >= 7.5:
        return "고급"
    elif avg_score >= 5.5:
        return "중급"
    else:
        return "초급"


@router.get("/types")
async def get_all_fitdna_types():
    """
    모든 FIT-DNA 유형 정보 조회
    - 8가지 유형 (PFE, PFQ, PSE, PSQ, LFE, LFQ, LSE, LSQ)
    """
    return {
        "types": [
            {"code": "PFE", "name": "파워 애슬리트", "description": "근력·유연성·지구력 모두 우수"},
            {"code": "PFQ", "name": "파워 스프린터", "description": "근력·유연성 우수, 순발력 중심"},
            {"code": "PSE", "name": "파워 러너", "description": "근력·지구력 우수"},
            {"code": "PSQ", "name": "파워 리프터", "description": "근력 특화형"},
            {"code": "LFE", "name": "밸런스 러너", "description": "유연성·지구력 우수"},
            {"code": "LFQ", "name": "유연성 마스터", "description": "유연성 특화형"},
            {"code": "LSE", "name": "지구력 전문가", "description": "지구력 특화형"},
            {"code": "LSQ", "name": "입문자형", "description": "균형 잡힌 발전 필요"}
        ]
    }
