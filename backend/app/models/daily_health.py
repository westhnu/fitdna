"""
일일 건강 체크 관련 모델
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class DailyCondition(Base, TimestampMixin):
    """일일 컨디션 체크"""
    __tablename__ = "daily_conditions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # 컨디션 정보
    pain_areas = Column(JSON, nullable=True)  # ["허리", "무릎", "어깨"]
    fatigue_level = Column(Integer, nullable=False)  # 1-10
    tension_level = Column(Integer, nullable=False)  # 1-10
    sleep_quality = Column(Integer, nullable=False)  # 1-10

    # 계산된 전체 위험도
    overall_risk_score = Column(Float, nullable=True)  # 0-10
    overall_risk_level = Column(String(20), nullable=True)  # '낮음', '보통', '높음'

    # 관계
    user = relationship("User", back_populates="daily_conditions")
    injury_risks = relationship("InjuryRisk", back_populates="condition", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DailyCondition(id={self.id}, user_id={self.user_id}, date={self.date})>"


class InjuryRisk(Base, TimestampMixin):
    """부상 위험도 분석"""
    __tablename__ = "injury_risks"

    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(Integer, ForeignKey("daily_conditions.id", ondelete="CASCADE"), nullable=False, index=True)

    # 부위별 위험도
    body_part = Column(String(50), nullable=False)  # 'lower_back', 'knee', 'shoulder', etc.
    risk_level = Column(String(20), nullable=False)  # '낮음', '보통', '높음'
    risk_score = Column(Float, nullable=False)  # 0-10

    # 경고 메시지
    warning_message = Column(String(500), nullable=True)

    # 피해야 할 운동 (JSON)
    exercises_to_avoid = Column(JSON, nullable=True)  # ["데드리프트", "스쿼트"]

    # 추천 휴식 여부
    recommended_rest = Column(Integer, default=0, nullable=False)  # 0=No, 1=Yes

    # 관계
    condition = relationship("DailyCondition", back_populates="injury_risks")

    def __repr__(self):
        return f"<InjuryRisk(id={self.id}, body_part={self.body_part}, risk={self.risk_level})>"


class PreventionRoutine(Base, TimestampMixin):
    """예방 루틴 템플릿"""
    __tablename__ = "prevention_routines"

    id = Column(Integer, primary_key=True, index=True)

    # 루틴 정보
    name = Column(String(200), nullable=False)
    target_area = Column(String(50), nullable=False)  # '허리', '어깨', '무릎', '전신'
    difficulty = Column(String(20), nullable=False)  # '쉬움', '보통', '어려움'
    duration = Column(Integer, nullable=False)  # 소요 시간 (초)

    # 설명
    description = Column(String(500), nullable=True)
    steps = Column(JSON, nullable=False)  # ["단계1", "단계2", ...]

    # 미디어
    image_url = Column(String(500), nullable=True)
    video_url = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<PreventionRoutine(id={self.id}, name={self.name}, target={self.target_area})>"
