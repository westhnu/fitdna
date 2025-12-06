"""
체력 측정 및 FIT-DNA 관련 모델
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class FitnessMeasurement(Base, TimestampMixin):
    """체력 측정 기록"""
    __tablename__ = "fitness_measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    measurement_date = Column(Date, nullable=False, index=True)

    # 체력 측정 항목
    grip_right = Column(Float, nullable=True)  # 악력 (오른손) - kg
    grip_left = Column(Float, nullable=True)  # 악력 (왼손) - kg
    sit_up = Column(Integer, nullable=True)  # 윗몸일으키기 - 회/분
    sit_and_reach = Column(Float, nullable=True)  # 앉아윗몸앞으로굽히기 - cm
    standing_long_jump = Column(Float, nullable=True)  # 제자리멀리뛰기 - cm
    vo2max = Column(Float, nullable=True)  # 최대산소섭취량 - ml/kg/min
    shuttle_run = Column(Integer, nullable=True)  # 왕복오래달리기 - 회

    # 계산된 Z-Score (저장용)
    strength_zscore = Column(Float, nullable=True)
    flexibility_zscore = Column(Float, nullable=True)
    endurance_zscore = Column(Float, nullable=True)

    # 관계
    user = relationship("User", back_populates="fitness_measurements")

    def __repr__(self):
        return f"<FitnessMeasurement(id={self.id}, user_id={self.user_id}, date={self.measurement_date})>"


class FitDNAResult(Base, TimestampMixin):
    """FIT-DNA 검사 결과"""
    __tablename__ = "fitdna_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    measurement_id = Column(Integer, ForeignKey("fitness_measurements.id", ondelete="SET NULL"), nullable=True)
    test_date = Column(Date, nullable=False, index=True)

    # FIT-DNA 유형
    fitdna_type = Column(String(10), nullable=False)  # PFE, PSE, LFE, etc.
    fitdna_name = Column(String(100), nullable=False)  # 파워 애슬리트, 파워 러너, etc.

    # 세부 점수
    strength_score = Column(Float, nullable=True)  # 0-10
    flexibility_score = Column(Float, nullable=True)  # 0-10
    endurance_score = Column(Float, nullable=True)  # 0-10

    # 강점/약점 (JSON)
    strengths = Column(JSON, nullable=True)  # ["근력", "지구력"]
    weaknesses = Column(JSON, nullable=True)  # ["유연성"]

    # 추천 운동 (JSON)
    recommended_exercises = Column(JSON, nullable=True)  # [{"name": "스쿼트", "category": "근력"}, ...]

    # 현재 활성 여부
    is_current = Column(Integer, default=1, nullable=False)  # 1=현재, 0=과거

    # 관계
    user = relationship("User", back_populates="fitdna_results")
    measurement = relationship("FitnessMeasurement")

    def __repr__(self):
        return f"<FitDNAResult(id={self.id}, user_id={self.user_id}, type={self.fitdna_type})>"


class LifestyleSurvey(Base, TimestampMixin):
    """라이프스타일 설문"""
    __tablename__ = "lifestyle_surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    survey_date = Column(Date, nullable=False)

    # 운동 습관
    exercise_frequency = Column(Integer, nullable=True)  # 주당 운동 횟수
    daily_activity_level = Column(String(20), nullable=True)  # 'low', 'medium', 'high'

    # 생활 패턴
    sleep_hours = Column(Float, nullable=True)  # 평균 수면 시간
    stress_level = Column(String(20), nullable=True)  # 'low', 'medium', 'high'

    # 추가 정보 (JSON)
    additional_data = Column(JSON, nullable=True)

    # 관계
    user = relationship("User", back_populates="lifestyle_surveys")

    def __repr__(self):
        return f"<LifestyleSurvey(id={self.id}, user_id={self.user_id}, date={self.survey_date})>"
