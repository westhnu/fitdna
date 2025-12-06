"""
운동 메이트 매칭 API
- FIT-DNA 기반 매칭
- 운동 종목 선택
- 매칭 결과 조회
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


# ===== 요청/응답 스키마 =====

class MatchingPreferenceInput(BaseModel):
    """매칭 선호도 입력"""
    fitdna_similarity: int  # 0-3: FIT-DNA 유사도 (0=같음, 3=완전 다름)
    exercise_types: List[str]  # ['러닝', '헬스', '요가', '수영', '클라이밍']
    preferred_times: List[str]  # ['아침', '점심', '저녁', '심야']
    location_radius_km: float = 5.0  # 활동 반경
    age_range: Optional[tuple] = None  # (min_age, max_age)
    gender_preference: Optional[str] = None  # 'M', 'F', 'any'


# ===== API 엔드포인트 =====

@router.post("/preferences")
async def set_matching_preferences(data: MatchingPreferenceInput):
    """
    매칭 선호도 설정
    - FIT-DNA 유사도 선택 (0~3개 차이)
    - 운동 종목 선택
    - 시간대 선택
    """
    return {
        "message": "매칭 선호도 저장 완료",
        "preferences": data.dict(),
        "ready_to_match": True
    }


@router.post("/request")
async def request_matching(user_id: int):
    """
    매칭 요청
    - 사용자의 선호도 기반으로 매칭 시작
    """
    # TODO: phase2_matching_algorithm.py 연동
    return {
        "user_id": user_id,
        "status": "매칭 진행 중",
        "estimated_time": "약 5분 소요",
        "matching_id": "match_12345"
    }


@router.get("/results")
async def get_matching_results(user_id: int):
    """
    매칭 결과 조회
    - 매칭된 사용자 목록 제공
    - 운동 스타일·시간대·위치 정보 비교
    """
    return {
        "user_id": user_id,
        "status": "매칭 완료",
        "matches": [
            {
                "match_id": 1,
                "user": {
                    "nickname": "런너123",
                    "age": 28,
                    "gender": "M",
                    "fitdna_type": "PFE",
                    "profile_image": "/static/profiles/user_1.jpg"
                },
                "compatibility": {
                    "total_score": 92,
                    "fitdna_similarity": 100,  # 같은 유형
                    "exercise_overlap": 80,  # 운동 종목 80% 일치
                    "time_overlap": 90,  # 시간대 90% 일치
                    "location_distance_km": 1.2
                },
                "common_exercises": ["러닝", "헬스", "수영"],
                "preferred_times": ["아침", "저녁"],
                "location": "서울 강남구",
                "bio": "주 5회 러닝하는 직장인입니다. 함께 운동하실 분 찾습니다!"
            },
            {
                "match_id": 2,
                "user": {
                    "nickname": "헬스매니아",
                    "age": 26,
                    "gender": "M",
                    "fitdna_type": "PSE",
                    "profile_image": "/static/profiles/user_2.jpg"
                },
                "compatibility": {
                    "total_score": 85,
                    "fitdna_similarity": 87,  # 1개 차이 (F vs S)
                    "exercise_overlap": 66,
                    "time_overlap": 100,
                    "location_distance_km": 2.5
                },
                "common_exercises": ["헬스", "러닝"],
                "preferred_times": ["저녁"],
                "location": "서울 서초구",
                "bio": "벤치프레스 120kg 찍는게 목표입니다. 같이 운동해요!"
            },
            {
                "match_id": 3,
                "user": {
                    "nickname": "요가러버",
                    "age": 30,
                    "gender": "F",
                    "fitdna_type": "LFE",
                    "profile_image": "/static/profiles/user_3.jpg"
                },
                "compatibility": {
                    "total_score": 78,
                    "fitdna_similarity": 75,  # 2개 차이 (P vs L, F vs S)
                    "exercise_overlap": 50,
                    "time_overlap": 80,
                    "location_distance_km": 3.8
                },
                "common_exercises": ["요가"],
                "preferred_times": ["아침", "점심"],
                "location": "서울 강동구",
                "bio": "요가 5년차입니다. 초보자도 환영해요!"
            }
        ],
        "total_matches": 3
    }


@router.get("/candidate/{candidate_id}")
async def get_candidate_detail(candidate_id: int, current_user_id: int):
    """
    매칭 후보자 상세 정보
    - 운동 스타일, 통계, 활동 이력
    """
    return {
        "candidate_id": candidate_id,
        "current_user_id": current_user_id,
        "detailed_profile": {
            "nickname": "런너123",
            "age": 28,
            "gender": "M",
            "fitdna_type": "PFE",
            "fitdna_name": "파워 애슬리트",
            "joined_date": "2025-01-15",
            "profile_image": "/static/profiles/user_1.jpg"
        },
        "workout_style": {
            "intensity_preference": "high",
            "session_duration_avg": 90,  # 분
            "weekly_frequency": 5,
            "favorite_exercises": ["러닝", "헬스", "수영", "클라이밍"],
            "workout_goals": ["체력 증진", "체중 감량"]
        },
        "statistics": {
            "total_workouts": 240,
            "consistency_score": 92,
            "months_active": 10,
            "achievement_badges": ["100일 연속 운동", "마라톤 완주", "체중 10kg 감량"]
        },
        "activity_history": [
            {"date": "2025-11-30", "exercise": "러닝", "duration": 60},
            {"date": "2025-11-28", "exercise": "헬스", "duration": 90},
            {"date": "2025-11-26", "exercise": "수영", "duration": 45}
        ],
        "compatibility_analysis": {
            "strengths": [
                "운동 빈도가 비슷합니다 (주 5회)",
                "선호 시간대가 일치합니다 (아침, 저녁)",
                "FIT-DNA 유형이 같아 체력 수준이 비슷합니다"
            ],
            "considerations": [
                "운동 강도가 높은 편이니 체력을 고려하세요"
            ]
        }
    }


@router.post("/request/{match_id}")
async def send_match_request(match_id: int, user_id: int):
    """
    매칭 신청
    - 후보자에게 매칭 신청 전송
    """
    return {
        "user_id": user_id,
        "match_id": match_id,
        "status": "신청 완료",
        "message": "상대방이 수락하면 알림을 보내드립니다."
    }


@router.post("/accept/{match_id}")
async def accept_match_request(match_id: int, user_id: int):
    """
    매칭 수락
    - 상대방의 매칭 신청 수락
    """
    return {
        "user_id": user_id,
        "match_id": match_id,
        "status": "매칭 성사",
        "chat_room_id": "chat_67890",
        "message": "매칭이 성사되었습니다! 채팅으로 운동 계획을 세워보세요."
    }


@router.get("/my-matches")
async def get_my_matches(user_id: int):
    """
    내 매칭 목록
    - 진행 중인 매칭, 완료된 매칭
    """
    return {
        "user_id": user_id,
        "active_matches": [
            {
                "match_id": 1,
                "partner": "런너123",
                "fitdna_type": "PFE",
                "matched_date": "2025-11-25",
                "total_workouts_together": 5,
                "status": "활동 중"
            }
        ],
        "pending_requests": [
            {
                "match_id": 2,
                "requester": "헬스매니아",
                "fitdna_type": "PSE",
                "request_date": "2025-11-30",
                "status": "대기 중"
            }
        ],
        "past_matches": [
            {
                "match_id": 3,
                "partner": "요가러버",
                "fitdna_type": "LFE",
                "matched_date": "2025-09-10",
                "ended_date": "2025-10-31",
                "total_workouts_together": 12,
                "status": "종료"
            }
        ]
    }
