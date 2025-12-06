"""
위치 기반 시설 API
- GPS 기반 주변 운동시설 조회
- 시설 상세 정보 (혼잡도, 가격, 운영시간)
- 날씨 기반 운동 추천
"""

from fastapi import APIRouter, Query, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import math

from app.core.database import get_db
from app.models import Facility

router = APIRouter()


# ===== 요청/응답 스키마 =====

class LocationInput(BaseModel):
    """위치 입력"""
    latitude: float
    longitude: float
    radius_km: float = 2.0  # 기본 2km


# ===== API 엔드포인트 =====

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """두 지점 사이의 거리 계산 (Haversine formula, km 단위)"""
    R = 6371  # 지구 반지름 (km)

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


@router.get("/nearby")
async def get_nearby_facilities(
    lat: float = Query(..., description="위도"),
    lon: float = Query(..., description="경도"),
    radius: float = Query(2.0, description="반경 (km)"),
    limit: int = Query(10, description="최대 결과 수"),
    sports: Optional[str] = Query(None, description="운동 종목 필터 (예: 농구, 축구)"),
    db: Session = Depends(get_db)
):
    """
    GPS 기반 주변 운동시설 조회
    - 헬스장/수영장/공원/러닝코스 등
    - 거리순 정렬
    """

    # 모든 시설 조회
    query = db.query(Facility)

    # 운동 종목 필터링
    if sports:
        query = query.filter(Facility.sports.contains(sports))

    facilities = query.limit(1000).all()  # 일단 1000개만 가져옴

    # 거리 계산 및 필터링
    facilities_with_distance = []
    for facility in facilities:
        distance = calculate_distance(lat, lon, facility.latitude, facility.longitude)

        if distance <= radius:
            facilities_with_distance.append({
                "id": facility.id,
                "name": facility.name,
                "type": facility.category,
                "distance_km": round(distance, 2),
                "address": facility.address,
                "sports": facility.sports,
                "latitude": facility.latitude,
                "longitude": facility.longitude
            })

    # 거리순 정렬
    facilities_with_distance.sort(key=lambda x: x['distance_km'])

    # 제한
    facilities_with_distance = facilities_with_distance[:limit]

    return {
        "location": {"latitude": lat, "longitude": lon},
        "radius_km": radius,
        "facilities": facilities_with_distance,
        "total_count": len(facilities_with_distance)
    }


@router.get("/{facility_id}")
async def get_facility_detail(facility_id: int, db: Session = Depends(get_db)):
    """
    시설 상세 정보
    - 혼잡도, 가격, 운영시간, 프로그램 정보
    - 사용자 리뷰 기반 점수
    - 접근성 점수 (거리·날씨·혼잡도 기반)
    """

    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    return {
        "id": facility.id,
        "name": facility.name,
        "type": facility.category,
        "basic_info": {
            "address": facility.address,
            "sports": facility.sports,
            "latitude": facility.latitude,
            "longitude": facility.longitude
        },
        "operating_hours": facility.operating_hours if facility.operating_hours else {
            "weekday": "미정",
            "weekend": "미정"
        },
        "pricing": facility.pricing if facility.pricing else {
            "info": "가격 정보 없음"
        },
        "reviews": {
            "average_rating": facility.average_rating if facility.average_rating else 0.0,
            "total_reviews": 0
        }
    }


@router.get("/weather-recommendation")
async def get_weather_based_recommendation(
    lat: float = Query(..., description="위도"),
    lon: float = Query(..., description="경도")
):
    """
    날씨 기반 운동 추천
    - 현재 날씨 기준 실내·실외 운동 추천
    - 미세먼지 수치 고려
    """
    # TODO: 날씨 API 연동
    return {
        "location": {"latitude": lat, "longitude": lon},
        "weather": {
            "temperature": 15,
            "condition": "맑음",
            "humidity": 60,
            "wind_speed": 3.5,
            "pm10": 30,  # 미세먼지
            "pm25": 15   # 초미세먼지
        },
        "air_quality": {
            "level": "좋음",
            "outdoor_safe": True
        },
        "recommendations": {
            "outdoor": [
                {
                    "exercise": "러닝",
                    "reason": "날씨가 맑고 미세먼지가 적어 야외 활동에 적합합니다",
                    "suitable": True
                },
                {
                    "exercise": "자전거",
                    "reason": "쾌적한 기온과 낮은 습도로 사이클링하기 좋습니다",
                    "suitable": True
                },
                {
                    "exercise": "등산",
                    "reason": "맑은 날씨로 산행에 최적입니다",
                    "suitable": True
                }
            ],
            "indoor": [
                {
                    "exercise": "웨이트 트레이닝",
                    "reason": "실내 활동 대안",
                    "suitable": True
                },
                {
                    "exercise": "수영",
                    "reason": "온도가 낮아 실내 수영이 좋습니다",
                    "suitable": True
                }
            ]
        },
        "overall_suggestion": "오늘은 야외 운동하기 좋은 날씨입니다! 러닝이나 사이클링을 추천합니다."
    }
