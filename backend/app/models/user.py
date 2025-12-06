"""
User 관련 모델
"""

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin
import enum


class GenderEnum(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"


class User(Base, TimestampMixin):
    """사용자 테이블"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # 기본 정보
    nickname = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(SQLEnum(GenderEnum), nullable=True)
    height = Column(Float, nullable=True)  # cm
    weight = Column(Float, nullable=True)  # kg
    birth_date = Column(Date, nullable=True)

    # 프로필
    profile_image = Column(String(500), nullable=True)
    bio = Column(String(500), nullable=True)

    # 계정 상태
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # 가입일
    joined_date = Column(Date, nullable=True)

    # 현재 FIT-DNA (최신 검사 결과에서 참조)
    current_fitdna_type = Column(String(10), nullable=True)  # PFE, PSE, etc.

    # 관계
    fitness_measurements = relationship("FitnessMeasurement", back_populates="user", cascade="all, delete-orphan")
    fitdna_results = relationship("FitDNAResult", back_populates="user", cascade="all, delete-orphan")
    lifestyle_surveys = relationship("LifestyleSurvey", back_populates="user", cascade="all, delete-orphan")
    workout_sessions = relationship("WorkoutSession", back_populates="user", cascade="all, delete-orphan")
    daily_conditions = relationship("DailyCondition", back_populates="user", cascade="all, delete-orphan")
    matching_preferences = relationship("MatchingPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    goals = relationship("UserGoal", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
