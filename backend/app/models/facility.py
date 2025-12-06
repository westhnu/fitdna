"""
운동 시설 관련 모델
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, Text
from .base import Base, TimestampMixin


class Facility(Base, TimestampMixin):
    """운동 시설"""
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)

    # 기본 정보
    name = Column(String(200), nullable=False, index=True)
    facility_type = Column(String(50), nullable=False, index=True)  # 'gym', 'pool', 'park', 'running'

    # 위치 정보
    address = Column(String(500), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)

    # 연락처
    phone = Column(String(50), nullable=True)
    website = Column(String(500), nullable=True)

    # 편의시설
    has_parking = Column(Boolean, default=False)
    has_shower = Column(Boolean, default=False)
    has_locker = Column(Boolean, default=False)

    # 운영 시간 (JSON)
    operating_hours = Column(JSON, nullable=True)  # {"weekday": "06:00-22:00", ...}

    # 가격 정보 (JSON)
    pricing = Column(JSON, nullable=True)  # {"day_pass": 10000, "month_pass": 60000, ...}

    # 프로그램 정보 (JSON)
    programs = Column(JSON, nullable=True)  # [{"name": "요가", "time": "월수금 10:00-11:00", ...}]

    # 평점 및 리뷰
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    review_scores = Column(JSON, nullable=True)  # {"cleanliness": 4.5, "equipment": 4.3, ...}

    # 썸네일
    thumbnail = Column(String(500), nullable=True)

    # 활성 상태
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Facility(id={self.id}, name={self.name}, type={self.facility_type})>"


class FacilityReview(Base, TimestampMixin):
    """시설 리뷰"""
    __tablename__ = "facility_reviews"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, nullable=False, index=True)  # FK는 나중에 추가
    user_id = Column(Integer, nullable=False, index=True)

    # 평점
    overall_rating = Column(Float, nullable=False)  # 1.0 - 5.0
    cleanliness_rating = Column(Float, nullable=True)
    equipment_rating = Column(Float, nullable=True)
    staff_rating = Column(Float, nullable=True)
    value_rating = Column(Float, nullable=True)

    # 리뷰 내용
    comment = Column(Text, nullable=True)

    # 도움됨 카운트
    helpful_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<FacilityReview(id={self.id}, facility_id={self.facility_id}, rating={self.overall_rating})>"


class FacilityCongestion(Base, TimestampMixin):
    """시설 혼잡도 (시간대별)"""
    __tablename__ = "facility_congestion"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, nullable=False, index=True)

    # 요일 및 시간대
    day_of_week = Column(Integer, nullable=False)  # 0=월요일, 6=일요일
    hour = Column(Integer, nullable=False)  # 0-23

    # 혼잡도
    congestion_level = Column(String(20), nullable=False)  # '낮음', '보통', '높음', '매우높음'
    congestion_score = Column(Float, nullable=False)  # 0-10

    # 통계 데이터 (방문자 수 기반)
    average_visitors = Column(Integer, default=0)

    def __repr__(self):
        return f"<FacilityCongestion(facility_id={self.facility_id}, day={self.day_of_week}, hour={self.hour})>"
