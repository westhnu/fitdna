"""
운동 메이트 매칭 관련 모델
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class MatchStatusEnum(str, enum.Enum):
    PENDING = "pending"  # 대기 중
    ACCEPTED = "accepted"  # 수락됨
    REJECTED = "rejected"  # 거절됨
    EXPIRED = "expired"  # 만료됨
    ACTIVE = "active"  # 활성 (진행 중)
    ENDED = "ended"  # 종료됨


class MatchingPreference(Base, TimestampMixin):
    """매칭 선호도 설정"""
    __tablename__ = "matching_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # FIT-DNA 유사도 (0-3)
    fitdna_similarity = Column(Integer, default=1, nullable=False)  # 0=같음, 3=완전 다름

    # 선호 운동 종목 (JSON)
    exercise_types = Column(JSON, nullable=False)  # ["러닝", "헬스", "요가"]

    # 선호 시간대 (JSON)
    preferred_times = Column(JSON, nullable=False)  # ["아침", "저녁"]

    # 활동 반경 (km)
    location_radius_km = Column(Float, default=5.0, nullable=False)

    # 나이 범위 (JSON)
    age_range = Column(JSON, nullable=True)  # {"min": 25, "max": 35}

    # 성별 선호
    gender_preference = Column(String(10), nullable=True)  # 'M', 'F', 'any'

    # 관계
    user = relationship("User", back_populates="matching_preferences")

    def __repr__(self):
        return f"<MatchingPreference(id={self.id}, user_id={self.user_id})>"


class Match(Base, TimestampMixin):
    """매칭 결과"""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)

    # 매칭 사용자들
    user1_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user2_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 매칭 점수
    compatibility_score = Column(Float, nullable=False)  # 0-100
    fitdna_similarity_score = Column(Float, nullable=True)  # 0-100
    exercise_overlap_score = Column(Float, nullable=True)  # 0-100
    time_overlap_score = Column(Float, nullable=True)  # 0-100
    location_distance_km = Column(Float, nullable=True)

    # 공통 운동 종목 (JSON)
    common_exercises = Column(JSON, nullable=True)  # ["러닝", "헬스"]

    # 매칭 상태
    status = Column(SQLEnum(MatchStatusEnum), default=MatchStatusEnum.PENDING, nullable=False, index=True)

    # 신청자
    requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 매칭 날짜
    matched_date = Column(Date, nullable=True)
    ended_date = Column(Date, nullable=True)

    # 함께한 운동 횟수
    total_workouts_together = Column(Integer, default=0)

    # 채팅방 ID (외부 시스템)
    chat_room_id = Column(String(100), nullable=True)

    # 관계
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    requester = relationship("User", foreign_keys=[requester_id])

    def __repr__(self):
        return f"<Match(id={self.id}, user1={self.user1_id}, user2={self.user2_id}, status={self.status})>"


class MatchRequest(Base, TimestampMixin):
    """매칭 요청 (후보자 목록)"""
    __tablename__ = "match_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 요청 시간
    request_date = Column(Date, nullable=False)

    # 매칭 후보자 목록 (JSON) - 계산 결과 캐싱
    candidates = Column(JSON, nullable=True)  # [{"user_id": 2, "score": 92, ...}, ...]

    # 요청 상태
    status = Column(String(20), default="processing", nullable=False)  # 'processing', 'completed', 'failed'

    def __repr__(self):
        return f"<MatchRequest(id={self.id}, user_id={self.user_id}, status={self.status})>"
