"""
운동 기록 관련 모델
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class WorkoutSession(Base, TimestampMixin):
    """운동 세션 기록"""
    __tablename__ = "workout_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)

    # 운동 정보
    exercise_type = Column(String(20), nullable=False)  # 'strength', 'flexibility', 'endurance'
    exercises = Column(JSON, nullable=False)  # ["스쿼트", "푸시업", "플랭크"]
    duration = Column(Integer, nullable=False)  # 운동 시간 (분)
    intensity = Column(String(10), nullable=False)  # 'low', 'medium', 'high'

    # 완료 여부
    completed = Column(Boolean, default=True, nullable=False)

    # 메모
    notes = Column(String(500), nullable=True)

    # 관계
    user = relationship("User", back_populates="workout_sessions")

    def __repr__(self):
        return f"<WorkoutSession(id={self.id}, user_id={self.user_id}, date={self.date}, type={self.exercise_type})>"


class UserGoal(Base, TimestampMixin):
    """사용자 목표"""
    __tablename__ = "user_goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # 목표 정보
    goal_type = Column(String(50), nullable=False)  # 'weekly_workouts', 'monthly_workouts', 'custom'
    goal_name = Column(String(200), nullable=False)  # "주 4회 운동", "벤치프레스 100kg"
    target_value = Column(Integer, nullable=False)  # 목표값
    current_value = Column(Integer, default=0, nullable=False)  # 현재값
    unit = Column(String(20), nullable=True)  # 단위: '회', 'kg', '분', etc.

    # 기간
    start_date = Column(Date, nullable=False)
    deadline = Column(Date, nullable=True)

    # 상태
    is_active = Column(Boolean, default=True, nullable=False)
    is_achieved = Column(Boolean, default=False, nullable=False)

    # 관계
    user = relationship("User", back_populates="goals")

    def __repr__(self):
        return f"<UserGoal(id={self.id}, user_id={self.user_id}, goal={self.goal_name})>"
