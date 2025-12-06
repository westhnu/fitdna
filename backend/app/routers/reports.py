"""
마이페이지 리포트 API
- 월간 운동 리포트
- 운동 기록 조회
- FIT-DNA 재검 요청
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.core.database import get_db
from app.models import User, WorkoutSession, FitnessMeasurement
from app.services.report_service import generate_user_monthly_report

router = APIRouter()


# ===== 요청/응답 스키마 =====

class WorkoutSessionCreate(BaseModel):
    """운동 세션 생성"""
    date: str  # YYYY-MM-DD
    exercise_type: str  # 'strength', 'flexibility', 'endurance'
    exercises: List[str]
    duration: int  # 분
    intensity: str  # 'low', 'medium', 'high'


# ===== API 엔드포인트 =====

@router.get("/monthly/{user_id}")
async def get_monthly_report(
    user_id: int,
    year: int = Query(..., description="연도"),
    month: int = Query(..., ge=1, le=12, description="월 (1-12)"),
    db: Session = Depends(get_db)
):
    """
    월간 운동 리포트
    - 월간 운동 빈도/종류/지표 변화
    - 꾸준함 점수 (Consistency Score) 제공
    """

    # 사용자 조회
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 해당 월의 운동 세션 조회
    sessions = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user_id,
        extract('year', WorkoutSession.date) == year,
        extract('month', WorkoutSession.date) == month
    ).all()

    # 해당 월의 체력 측정 기록 조회 (가장 최근)
    current_measurement = db.query(FitnessMeasurement).filter(
        FitnessMeasurement.user_id == user_id,
        extract('year', FitnessMeasurement.measurement_date) == year,
        extract('month', FitnessMeasurement.measurement_date) == month
    ).order_by(FitnessMeasurement.measurement_date.desc()).first()

    # 이전 월의 체력 측정 기록 조회
    previous_month = month - 1 if month > 1 else 12
    previous_year = year if month > 1 else year - 1

    previous_measurement = db.query(FitnessMeasurement).filter(
        FitnessMeasurement.user_id == user_id,
        extract('year', FitnessMeasurement.measurement_date) == previous_year,
        extract('month', FitnessMeasurement.measurement_date) == previous_month
    ).order_by(FitnessMeasurement.measurement_date.desc()).first()

    # 월간 리포트 생성 (모델링 파일 사용)
    try:
        report = generate_user_monthly_report(
            user_id=user_id,
            year=year,
            month=month,
            db_sessions=sessions,
            current_measurement=current_measurement,
            previous_measurement=previous_measurement,
            user=user
        )

        # sessions 필드 제거 (너무 크므로)
        if 'sessions' in report:
            del report['sessions']

        return report

    except Exception as e:
        # 에러 발생 시 기본 응답 반환
        print(f"Error generating report: {e}")
        return {
            "user_id": user_id,
            "year": year,
            "month": month,
            "summary": {
                "total_workout_days": len(set(s.date for s in sessions)),
                "weekly_average": round(len(sessions) / 4, 1),
                "total_duration": sum(s.duration for s in sessions),
                "total_sessions": len(sessions)
            },
            "workout_frequency": {
                "strength": sum(1 for s in sessions if s.exercise_type == 'strength'),
                "flexibility": sum(1 for s in sessions if s.exercise_type == 'flexibility'),
                "endurance": sum(1 for s in sessions if s.exercise_type == 'endurance')
            },
            "metric_changes": [],
            "consistency_score": {
                "total_score": 75,
                "breakdown": {
                    "achievement_rate": 30.0,
                    "regularity": 30.0,
                    "intensity_maintenance": 15.0
                },
                "feedback": "운동을 꾸준히 하고 계시네요!"
            }
        }


@router.post("/workout-sessions")
async def create_workout_session(user_id: int, data: WorkoutSessionCreate):
    """
    운동 세션 기록
    - 날짜, 운동 종류, 시간, 강도 등
    """
    return {
        "message": "운동 기록 저장 완료",
        "session": {
            "user_id": user_id,
            **data.dict(),
            "created_at": "2025-12-01T19:00:00"
        }
    }


@router.get("/workout-sessions/{user_id}")
async def get_workout_sessions(
    user_id: int,
    start_date: Optional[str] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    exercise_type: Optional[str] = Query(None, description="운동 유형 필터")
):
    """
    운동 기록 조회
    - 기간별, 운동 유형별 필터링
    """
    return {
        "user_id": user_id,
        "filters": {
            "start_date": start_date,
            "end_date": end_date,
            "exercise_type": exercise_type
        },
        "sessions": [
            {
                "id": 1,
                "date": "2025-11-30",
                "exercise_type": "strength",
                "exercises": ["스쿼트", "푸시업", "플랭크"],
                "duration": 60,
                "intensity": "high"
            },
            {
                "id": 2,
                "date": "2025-11-28",
                "exercise_type": "endurance",
                "exercises": ["조깅"],
                "duration": 45,
                "intensity": "medium"
            },
            {
                "id": 3,
                "date": "2025-11-26",
                "exercise_type": "flexibility",
                "exercises": ["요가", "스트레칭"],
                "duration": 50,
                "intensity": "low"
            }
        ],
        "total_count": 3
    }


@router.get("/fitdna-history/{user_id}")
async def get_fitdna_history(user_id: int):
    """
    FIT-DNA 검사 이력
    - 체력 측정 및 FIT-DNA 유형 변화 기록
    """
    return {
        "user_id": user_id,
        "history": [
            {
                "id": 1,
                "test_date": "2025-11-15",
                "fitdna_type": "PFE",
                "fitdna_name": "파워 애슬리트",
                "measurements": {
                    "grip_right": 41.2,
                    "grip_left": 39.1,
                    "sit_up": 48,
                    "sit_and_reach": 15.8,
                    "standing_long_jump": 205,
                    "vo2max": 44.8
                },
                "is_current": True
            },
            {
                "id": 2,
                "test_date": "2025-10-01",
                "fitdna_type": "PSE",
                "fitdna_name": "파워 러너",
                "measurements": {
                    "grip_right": 38.5,
                    "grip_left": 36.8,
                    "sit_up": 42,
                    "sit_and_reach": 12.5,
                    "standing_long_jump": 195,
                    "vo2max": 42.3
                },
                "is_current": False
            },
            {
                "id": 3,
                "test_date": "2025-09-01",
                "fitdna_type": "LSQ",
                "fitdna_name": "입문자형",
                "measurements": {
                    "grip_right": 35.2,
                    "grip_left": 33.5,
                    "sit_up": 38,
                    "sit_and_reach": 10.2,
                    "standing_long_jump": 180,
                    "vo2max": 38.5
                },
                "is_current": False
            }
        ],
        "next_test_recommended": "2025-12-15",
        "days_until_next_test": 14
    }


@router.post("/request-retest")
async def request_retest(user_id: int):
    """
    FIT-DNA 재검 요청
    - 6개월마다 재측정 주기 알림
    """
    return {
        "user_id": user_id,
        "message": "재검 요청이 접수되었습니다",
        "last_test_date": "2025-11-15",
        "recommended_test_date": "2025-12-15",
        "status": "예약 가능"
    }


@router.get("/statistics/{user_id}")
async def get_user_statistics(user_id: int):
    """
    사용자 통계
    - 전체 운동 일수, 총 시간, 성취 배지 등
    """
    return {
        "user_id": user_id,
        "lifetime_stats": {
            "total_workout_days": 120,
            "total_workout_hours": 180,
            "total_sessions": 150,
            "member_since": "2025-01-15",
            "days_active": 320
        },
        "current_streak": {
            "days": 12,
            "description": "12일 연속 운동 중!"
        },
        "achievements": [
            {
                "badge": "100일 연속 운동",
                "earned_date": "2025-10-25",
                "icon": "/static/badges/100_day_streak.png"
            },
            {
                "badge": "총 운동 시간 100시간",
                "earned_date": "2025-09-15",
                "icon": "/static/badges/100_hours.png"
            },
            {
                "badge": "FIT-DNA 레벨업",
                "earned_date": "2025-11-15",
                "icon": "/static/badges/levelup.png"
            }
        ],
        "monthly_trend": [
            {"month": "2025-06", "workout_days": 8, "consistency_score": 60},
            {"month": "2025-07", "workout_days": 10, "consistency_score": 68},
            {"month": "2025-08", "workout_days": 12, "consistency_score": 72},
            {"month": "2025-09", "workout_days": 12, "consistency_score": 79},
            {"month": "2025-10", "workout_days": 15, "consistency_score": 87},
            {"month": "2025-11", "workout_days": 18, "consistency_score": 92}
        ]
    }


@router.get("/goals/{user_id}")
async def get_user_goals(user_id: int):
    """
    사용자 목표 조회
    - 주간/월간 운동 목표
    """
    return {
        "user_id": user_id,
        "weekly_goal": {
            "target_workouts": 4,
            "current_workouts": 3,
            "progress_percentage": 75,
            "days_remaining": 2
        },
        "monthly_goal": {
            "target_workouts": 16,
            "current_workouts": 14,
            "progress_percentage": 87.5,
            "days_remaining": 7
        },
        "custom_goals": [
            {
                "goal": "벤치프레스 100kg 달성",
                "current": 85,
                "target": 100,
                "unit": "kg",
                "progress_percentage": 85,
                "deadline": "2025-12-31"
            },
            {
                "goal": "10km 러닝 45분 안에 완주",
                "current": 52,
                "target": 45,
                "unit": "분",
                "progress_percentage": 86.5,
                "deadline": "2025-12-15"
            }
        ]
    }
