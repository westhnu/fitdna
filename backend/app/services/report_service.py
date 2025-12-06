"""
월간 리포트 생성 서비스
모델링 파일(models_monthly_report.py) 연동
"""

import sys
import os
from typing import List, Dict
from datetime import date

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

# 모델링 파일 import (선택적)
_MODELING_AVAILABLE = False
try:
    from models_monthly_report import (
        WorkoutSession as ModelWorkoutSession,
        FitnessMeasurement as ModelFitnessMeasurement,
        generate_monthly_report,
        calculate_monthly_summary,
        calculate_workout_frequency,
        calculate_metric_changes,
        calculate_consistency_score
    )
    _MODELING_AVAILABLE = True
except Exception as e:
    print(f"WARNING: models_monthly_report.py import failed (using simple version): {e}")
    ModelWorkoutSession = None
    ModelFitnessMeasurement = None


def convert_db_session_to_model(db_session) -> ModelWorkoutSession:
    """
    DB WorkoutSession을 모델링 파일의 WorkoutSession으로 변환
    """
    return ModelWorkoutSession(
        user_id=db_session.user_id,
        date=db_session.date.strftime('%Y-%m-%d'),
        exercise_type=db_session.exercise_type,
        exercises=db_session.exercises,
        duration=db_session.duration,
        intensity=db_session.intensity,
        completed=db_session.completed
    )


def convert_db_measurement_to_model(db_measurement) -> ModelFitnessMeasurement:
    """
    DB FitnessMeasurement를 모델링 파일의 FitnessMeasurement로 변환
    """
    measurements = {
        'grip_right': db_measurement.grip_right,
        'grip_left': db_measurement.grip_left,
        'sit_up': db_measurement.sit_up,
        'sit_and_reach': db_measurement.sit_and_reach,
        'standing_long_jump': db_measurement.standing_long_jump,
        'vo2max': db_measurement.vo2max,
        'shuttle_run': db_measurement.shuttle_run
    }

    return ModelFitnessMeasurement(
        user_id=db_measurement.user_id,
        measurement_date=db_measurement.measurement_date.strftime('%Y-%m-%d'),
        age=None,  # DB에서 user 정보 필요
        gender=None,
        measurements=measurements
    )


def generate_user_monthly_report(
    user_id: int,
    year: int,
    month: int,
    db_sessions: List,
    current_measurement=None,
    previous_measurement=None,
    user=None
) -> Dict:
    """
    사용자 월간 리포트 생성

    Args:
        user_id: 사용자 ID
        year: 연도
        month: 월
        db_sessions: DB에서 조회한 WorkoutSession 목록
        current_measurement: 현재 측정 기록
        previous_measurement: 이전 측정 기록
        user: User 객체 (나이/성별 정보 필요)

    Returns:
        월간 리포트 딕셔너리
    """

    # 모델링 파일을 사용할 수 없으면 간단한 버전 사용
    if not _MODELING_AVAILABLE:
        return generate_simple_report(user_id, year, month, db_sessions,
                                     current_measurement, previous_measurement)

    try:
        # DB 세션을 모델 세션으로 변환
        model_sessions = [convert_db_session_to_model(s) for s in db_sessions]

        # 측정 기록 변환
        current_model_measurement = None
        previous_model_measurement = None

        if current_measurement and user:
            current_model_measurement = ModelFitnessMeasurement(
                user_id=user_id,
                measurement_date=current_measurement.measurement_date.strftime('%Y-%m-%d'),
                age=user.age,
                gender=user.gender.value if hasattr(user.gender, 'value') else user.gender,
                measurements={
                    'grip_right': current_measurement.grip_right,
                    'grip_left': current_measurement.grip_left,
                    'sit_up': current_measurement.sit_up,
                    'sit_and_reach': current_measurement.sit_and_reach,
                    'standing_long_jump': current_measurement.standing_long_jump,
                    'vo2max': current_measurement.vo2max,
                    'shuttle_run': current_measurement.shuttle_run
                }
            )

        if previous_measurement and user:
            previous_model_measurement = ModelFitnessMeasurement(
                user_id=user_id,
                measurement_date=previous_measurement.measurement_date.strftime('%Y-%m-%d'),
                age=user.age,
                gender=user.gender.value if hasattr(user.gender, 'value') else user.gender,
                measurements={
                    'grip_right': previous_measurement.grip_right,
                    'grip_left': previous_measurement.grip_left,
                    'sit_up': previous_measurement.sit_up,
                    'sit_and_reach': previous_measurement.sit_and_reach,
                    'standing_long_jump': previous_measurement.standing_long_jump,
                    'vo2max': previous_measurement.vo2max,
                    'shuttle_run': previous_measurement.shuttle_run
                }
            )

        # 월간 리포트 생성
        report = generate_monthly_report(
            user_id=user_id,
            year=year,
            month=month,
            sessions=model_sessions,
            current_measurement=current_model_measurement,
            previous_measurement=previous_model_measurement
        )

        return report

    except Exception as e:
        print(f"❌ 월간 리포트 생성 중 에러: {e}")
        # 에러 발생 시 간단한 버전으로 fallback
        return generate_simple_report(user_id, year, month, db_sessions,
                                     current_measurement, previous_measurement)


def generate_simple_report(
    user_id: int,
    year: int,
    month: int,
    db_sessions: List,
    current_measurement=None,
    previous_measurement=None
) -> Dict:
    """간단한 버전의 월간 리포트 (모델링 파일 없이)"""

    # 운동 요약
    unique_dates = set(s.date for s in db_sessions)
    total_duration = sum(s.duration for s in db_sessions)

    summary = {
        'total_workout_days': len(unique_dates),
        'weekly_average': round(len(unique_dates) / 4, 1),
        'total_duration': total_duration,
        'total_sessions': len(db_sessions)
    }

    # 운동 빈도
    frequency = {
        'strength': sum(1 for s in db_sessions if s.exercise_type == 'strength'),
        'flexibility': sum(1 for s in db_sessions if s.exercise_type == 'flexibility'),
        'endurance': sum(1 for s in db_sessions if s.exercise_type == 'endurance')
    }

    # 체력 지표 변화
    metric_changes = []
    if current_measurement and previous_measurement:
        metrics = [
            ('grip_right', '악력 (오른손)', 'kg'),
            ('sit_up', '윗몸일으키기', '회/분'),
            ('sit_and_reach', '앉아윗몸앞으로굽히기', 'cm')
        ]

        for key, name, unit in metrics:
            curr_val = getattr(current_measurement, key, None)
            prev_val = getattr(previous_measurement, key, None)

            if curr_val and prev_val:
                change = round(curr_val - prev_val, 1)
                change_pct = round((change / prev_val * 100), 1) if prev_val != 0 else 0

                metric_changes.append({
                    'name': name,
                    'unit': unit,
                    'previous_month': prev_val,
                    'current_month': curr_val,
                    'change': change,
                    'change_percentage': change_pct
                })

    # 꾸준함 점수
    consistency_score = calculate_simple_consistency_score(db_sessions)

    return {
        'user_id': user_id,
        'year': year,
        'month': month,
        'summary': summary,
        'workout_frequency': frequency,
        'metric_changes': metric_changes,
        'consistency_score': consistency_score
    }


def calculate_simple_consistency_score(sessions: List) -> Dict:
    """
    간단한 꾸준함 점수 계산 (모델링 파일 없이)

    Args:
        sessions: DB WorkoutSession 목록

    Returns:
        꾸준함 점수 정보
    """

    total_sessions = len(sessions)
    target_monthly = 16  # 주 4회 × 4주

    # 목표 달성률 (40점)
    achievement_rate = min((total_sessions / target_monthly) * 40, 40)

    # 간단한 규칙성 계산 (40점)
    regularity = 30 if total_sessions >= 12 else 20

    # 강도 유지도 (20점)
    high_intensity_count = sum(1 for s in sessions if s.intensity == 'high')
    intensity_maintenance = min((high_intensity_count / total_sessions) * 20, 20) if total_sessions > 0 else 0

    total_score = round(achievement_rate + regularity + intensity_maintenance)

    # 피드백
    if total_score >= 90:
        feedback = f"완벽해요! 이번 달 {total_sessions}회 운동으로 목표를 초과 달성했습니다."
    elif total_score >= 80:
        feedback = f"훌륭해요! 이번 달 {total_sessions}회 꾸준히 운동하셨네요."
    elif total_score >= 70:
        feedback = f"잘하고 있어요! 목표까지 {target_monthly - total_sessions}회 남았어요."
    else:
        feedback = f"좋은 시작이에요. 운동 빈도를 조금 더 늘려보세요."

    return {
        'total_score': total_score,
        'breakdown': {
            'achievement_rate': round(achievement_rate, 1),
            'regularity': round(regularity, 1),
            'intensity_maintenance': round(intensity_maintenance, 1)
        },
        'feedback': feedback
    }
