"""
하루 건강 체크 API
- 오늘의 컨디션 체크
- 부상 위험도 분석
- 예방 루틴 추천
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()


# ===== 요청/응답 스키마 =====

class DailyConditionInput(BaseModel):
    """오늘의 컨디션 입력"""
    pain_areas: List[str] = []  # 통증 부위 ['허리', '무릎', '어깨']
    fatigue_level: int  # 피로도 1-10
    tension_level: int  # 긴장도 1-10
    sleep_quality: int  # 수면 질 1-10


# ===== API 엔드포인트 =====

@router.post("/condition")
async def submit_daily_condition(data: DailyConditionInput):
    """
    오늘의 컨디션 체크
    - 통증, 피로도, 긴장도 입력
    """
    return {
        "message": "컨디션 저장 완료",
        "data": data.dict(),
        "risk_analysis_available": True
    }


@router.get("/injury-risk")
async def get_injury_risk_analysis(user_id: int):
    """
    부상 위험도 분석
    - 허리/무릎/어깨 등 부위별 위험도 제공
    - 위험 수준: 낮음/보통/높음
    - "오늘은 ○○ 운동 피하기" 자동 경고
    """
    return {
        "user_id": user_id,
        "overall_risk": "보통",
        "body_parts": {
            "lower_back": {
                "risk_level": "높음",
                "score": 7.5,
                "warning": "오늘은 데드리프트, 스쿼트 같은 허리 부담이 큰 운동을 피하세요",
                "recommended_rest": True
            },
            "knee": {
                "risk_level": "낮음",
                "score": 2.3,
                "warning": None,
                "recommended_rest": False
            },
            "shoulder": {
                "risk_level": "보통",
                "score": 5.1,
                "warning": "숄더프레스, 오버헤드 동작 시 주의하세요",
                "recommended_rest": False
            }
        },
        "exercises_to_avoid": ["데드리프트", "스쿼트", "굿모닝"],
        "safe_exercises": ["워킹", "가벼운 사이클", "상체 스트레칭"]
    }


@router.get("/prevention-routine")
async def get_prevention_routine(user_id: int):
    """
    예방 루틴 추천
    - 오늘 필요한 스트레칭·워밍업 루틴 제공
    - GIF 또는 이미지 URL 포함
    """
    return {
        "user_id": user_id,
        "date": "2025-12-01",
        "routines": [
            {
                "name": "허리 스트레칭",
                "duration": 300,  # 초
                "difficulty": "쉬움",
                "target_area": "허리",
                "image_url": "/static/stretches/lower_back_stretch.gif",
                "steps": [
                    "바닥에 누워 무릎을 가슴으로 당깁니다",
                    "20초간 유지합니다",
                    "3회 반복합니다"
                ]
            },
            {
                "name": "어깨 회전 운동",
                "duration": 180,
                "difficulty": "쉬움",
                "target_area": "어깨",
                "image_url": "/static/stretches/shoulder_rotation.gif",
                "steps": [
                    "팔을 옆으로 펼칩니다",
                    "천천히 원을 그리며 회전합니다",
                    "앞뒤로 각 10회씩 반복합니다"
                ]
            },
            {
                "name": "전신 워밍업",
                "duration": 600,
                "difficulty": "쉬움",
                "target_area": "전신",
                "image_url": "/static/stretches/full_body_warmup.gif",
                "steps": [
                    "가벼운 제자리 걷기 2분",
                    "팔 돌리기 1분",
                    "무릎 회전 1분",
                    "고관절 스트레칭 1분"
                ]
            }
        ],
        "total_duration": 1080,  # 총 18분
        "recommendation": "오늘은 허리 부담이 큰 운동을 피하고, 스트레칭 위주로 진행하세요."
    }


@router.get("/risk-history")
async def get_risk_history(user_id: int, days: int = 7):
    """
    최근 부상 위험도 이력 조회
    - 지난 N일간의 위험도 추이
    """
    return {
        "user_id": user_id,
        "period": f"최근 {days}일",
        "history": [
            {"date": "2025-11-25", "overall_risk": "낮음", "score": 2.5},
            {"date": "2025-11-26", "overall_risk": "낮음", "score": 3.1},
            {"date": "2025-11-27", "overall_risk": "보통", "score": 5.2},
            {"date": "2025-11-28", "overall_risk": "보통", "score": 5.8},
            {"date": "2025-11-29", "overall_risk": "높음", "score": 7.5},
            {"date": "2025-11-30", "overall_risk": "보통", "score": 6.2},
            {"date": "2025-12-01", "overall_risk": "보통", "score": 5.5}
        ]
    }
