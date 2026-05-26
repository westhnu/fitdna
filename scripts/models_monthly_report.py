"""
월간 리포트 생성을 위한 데이터 모델링
실제 백엔드 DB 구조를 반영한 임시 데이터 생성
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Literal
import random
import json

# ===========================================
# 1. 사용자 운동 기록 데이터 모델
# ===========================================

class WorkoutSession:
    """개별 운동 세션"""
    def __init__(
        self,
        user_id: int,
        date: str,  # YYYY-MM-DD
        exercise_type: Literal['strength', 'flexibility', 'endurance'],
        exercises: List[str],
        duration: int,  # 분
        intensity: Literal['low', 'medium', 'high'],
        completed: bool = True
    ):
        self.user_id = user_id
        self.date = date
        self.exercise_type = exercise_type
        self.exercises = exercises
        self.duration = duration
        self.intensity = intensity
        self.completed = completed

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'date': self.date,
            'exercise_type': self.exercise_type,
            'exercises': self.exercises,
            'duration': self.duration,
            'intensity': self.intensity,
            'completed': self.completed
        }


# ===========================================
# 2. 체력 측정 기록 데이터 모델
# ===========================================

class FitnessMeasurement:
    """체력 측정 기록"""
    def __init__(
        self,
        user_id: int,
        measurement_date: str,  # YYYY-MM-DD
        age: int,
        gender: Literal['M', 'F'],
        measurements: Dict[str, float]
    ):
        self.user_id = user_id
        self.measurement_date = measurement_date
        self.age = age
        self.gender = gender
        self.measurements = measurements  # {'grip_right': 41.2, 'sit_up': 48, ...}

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'measurement_date': self.measurement_date,
            'age': self.age,
            'gender': self.gender,
            **self.measurements
        }


# ===========================================
# 3. 월간 운동 빈도 계산
# ===========================================

def calculate_workout_frequency(sessions: List[WorkoutSession]) -> Dict[str, int]:
    """운동 종류별 빈도 계산"""
    frequency = {
        'strength': 0,
        'flexibility': 0,
        'endurance': 0
    }

    for session in sessions:
        if session.completed:
            frequency[session.exercise_type] += 1

    return frequency


# ===========================================
# 4. 월간 운동 요약 계산
# ===========================================

def calculate_monthly_summary(sessions: List[WorkoutSession]) -> Dict:
    """월간 운동 요약 통계"""
    completed_sessions = [s for s in sessions if s.completed]

    # 고유 운동 날짜 수
    unique_dates = set(s.date for s in completed_sessions)
    total_workout_days = len(unique_dates)

    # 총 운동 시간
    total_duration = sum(s.duration for s in completed_sessions)

    # 주당 평균 (4주 기준)
    weekly_average = round(total_workout_days / 4, 1)

    return {
        'total_workout_days': total_workout_days,
        'weekly_average': weekly_average,
        'total_duration': total_duration,
        'total_sessions': len(completed_sessions)
    }


# ===========================================
# 5. 체력 지표 변화 계산
# ===========================================

def calculate_metric_changes(
    previous_measurement: FitnessMeasurement,
    current_measurement: FitnessMeasurement
) -> List[Dict]:
    """전월 대비 체력 지표 변화 계산"""

    metric_names = {
        'grip_right': ('악력 (오른손)', 'kg'),
        'grip_left': ('악력 (왼손)', 'kg'),
        'sit_up': ('윗몸일으키기', '회/분'),
        'sit_and_reach': ('앉아윗몸앞으로굽히기', 'cm'),
        'standing_long_jump': ('제자리멀리뛰기', 'cm'),
        'vo2max': ('VO2max', 'ml/kg/min'),
        'shuttle_run': ('왕복오래달리기', '회')
    }

    changes = []

    for metric_key, (name, unit) in metric_names.items():
        if metric_key in previous_measurement.measurements and metric_key in current_measurement.measurements:
            prev_value = previous_measurement.measurements[metric_key]
            curr_value = current_measurement.measurements[metric_key]

            change = round(curr_value - prev_value, 2)
            change_percentage = round((change / prev_value * 100), 1) if prev_value != 0 else 0

            changes.append({
                'name': name,
                'unit': unit,
                'previous_month': prev_value,
                'current_month': curr_value,
                'change': change,
                'change_percentage': change_percentage
            })

    return changes


# ===========================================
# 6. 꾸준함 점수 계산 알고리즘
# ===========================================

def calculate_consistency_score(
    sessions: List[WorkoutSession],
    target_weekly_workouts: int = 4,
    target_monthly_workouts: int = 16
) -> Dict:
    """
    꾸준함 점수 계산
    - 총점: 100점 만점
    - 목표 달성률: 40점 (계획 대비 실제 운동 달성)
    - 운동 규칙성: 40점 (운동 간격의 일관성)
    - 강도 유지도: 20점 (운동 강도 유지)
    """

    completed_sessions = [s for s in sessions if s.completed]
    total_sessions = len(completed_sessions)

    # 1. 목표 달성률 (40점 만점)
    achievement_rate = min((total_sessions / target_monthly_workouts) * 40, 40)

    # 2. 운동 규칙성 (40점 만점) - 운동 간격의 표준편차로 계산
    if len(completed_sessions) >= 2:
        dates = sorted([datetime.strptime(s.date, '%Y-%m-%d') for s in completed_sessions])
        intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]

        # 이상적 간격: 2-3일 (주 4회 기준)
        ideal_interval = 2
        interval_variance = sum(abs(interval - ideal_interval) for interval in intervals) / len(intervals)

        # 간격이 균일할수록 높은 점수 (최대 40점)
        regularity = max(40 - interval_variance * 5, 0)
    else:
        regularity = 0

    # 3. 강도 유지도 (20점 만점)
    intensity_scores = {'low': 1, 'medium': 2, 'high': 3}
    intensities = [intensity_scores[s.intensity] for s in completed_sessions]

    if intensities:
        avg_intensity = sum(intensities) / len(intensities)
        # 평균 강도가 높을수록 높은 점수
        intensity_maintenance = min(avg_intensity / 3 * 20, 20)
    else:
        intensity_maintenance = 0

    total_score = round(achievement_rate + regularity + intensity_maintenance)

    # 피드백 생성
    feedback = generate_feedback(total_score, total_sessions, target_monthly_workouts)

    return {
        'total_score': total_score,
        'breakdown': {
            'achievement_rate': round(achievement_rate, 1),
            'regularity': round(regularity, 1),
            'intensity_maintenance': round(intensity_maintenance, 1)
        },
        'feedback': feedback
    }


def generate_feedback(score: int, actual_workouts: int, target_workouts: int) -> str:
    """점수에 따른 피드백 메시지 생성"""

    if score >= 90:
        return f"완벽해요! 이번 달 {actual_workouts}회 운동으로 목표를 초과 달성했습니다. 이 페이스를 유지하세요!"
    elif score >= 80:
        return f"훌륭해요! 이번 달 {actual_workouts}회 꾸준히 운동하셨네요. 다음 달에도 화이팅!"
    elif score >= 70:
        return f"잘하고 있어요! 목표까지 {target_workouts - actual_workouts}회 남았어요. 조금만 더 힘내세요!"
    elif score >= 60:
        return f"좋은 시작이에요. 운동 빈도를 조금 더 늘려보는 건 어떨까요?"
    else:
        return f"운동을 시작하셨네요! 작은 목표부터 차근차근 달성해봐요. 화이팅!"


# ===========================================
# 7. 임시 데이터 생성기
# ===========================================

def generate_mock_workout_sessions(
    user_id: int,
    year: int,
    month: int,
    workout_days: int = 18
) -> List[WorkoutSession]:
    """특정 월의 운동 세션 임시 데이터 생성"""

    # 해당 월의 날짜 범위
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)

    # 랜덤하게 운동 날짜 선택
    total_days = (end_date - start_date).days + 1
    workout_dates = sorted(random.sample(range(total_days), min(workout_days, total_days)))

    sessions = []

    # 운동 목록
    strength_exercises = [
        ['스쿼트', '푸시업', '플랭크'],
        ['데드리프트', '벤치프레스', '풀업'],
        ['레그프레스', '숄더프레스'],
        ['풀업', '딥스', '플랭크'],
        ['벤치프레스', '로우'],
        ['스쿼트', '런지', '카프레이즈']
    ]

    flexibility_exercises = [
        ['요가', '스트레칭'],
        ['필라테스'],
        ['스트레칭', '폼롤러'],
        ['필라테스', '폼롤러']
    ]

    endurance_exercises = [
        ['조깅', '버피테스트'],
        ['사이클링'],
        ['수영'],
        ['인터벌 러닝'],
        ['조깅', '계단오르기'],
        ['왕복오래달리기']
    ]

    for day_offset in workout_dates:
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime('%Y-%m-%d')

        # 랜덤 운동 유형 선택 (근력 운동을 좀 더 많이)
        exercise_type = random.choices(
            ['strength', 'flexibility', 'endurance'],
            weights=[0.4, 0.3, 0.3]
        )[0]

        # 운동 선택
        if exercise_type == 'strength':
            exercises = random.choice(strength_exercises)
            intensity = random.choices(['medium', 'high'], weights=[0.3, 0.7])[0]
            duration = random.randint(50, 75)
        elif exercise_type == 'flexibility':
            exercises = random.choice(flexibility_exercises)
            intensity = random.choices(['low', 'medium'], weights=[0.6, 0.4])[0]
            duration = random.randint(45, 60)
        else:  # endurance
            exercises = random.choice(endurance_exercises)
            intensity = random.choices(['medium', 'high'], weights=[0.5, 0.5])[0]
            duration = random.randint(40, 60)

        session = WorkoutSession(
            user_id=user_id,
            date=date_str,
            exercise_type=exercise_type,
            exercises=exercises,
            duration=duration,
            intensity=intensity,
            completed=True
        )

        sessions.append(session)

    return sessions


def generate_mock_fitness_measurement(
    user_id: int,
    measurement_date: str,
    age: int,
    gender: Literal['M', 'F'],
    base_measurements: Dict[str, float] = None,
    improvement_factor: float = 1.0
) -> FitnessMeasurement:
    """체력 측정 임시 데이터 생성"""

    if base_measurements is None:
        # 기본 측정값 (28세 남성 평균 기준)
        base_measurements = {
            'grip_right': 38.5,
            'grip_left': 36.8,
            'sit_up': 42,
            'sit_and_reach': 12.5,
            'standing_long_jump': 195,
            'vo2max': 42.3,
            'shuttle_run': 45
        }

    # 개선 효과 적용 (improvement_factor > 1.0이면 향상)
    measurements = {}
    for key, value in base_measurements.items():
        # 약간의 랜덤 변동 추가
        variation = random.uniform(-0.02, 0.05)  # -2% ~ +5%
        measurements[key] = round(value * improvement_factor * (1 + variation), 2)

    return FitnessMeasurement(
        user_id=user_id,
        measurement_date=measurement_date,
        age=age,
        gender=gender,
        measurements=measurements
    )


# ===========================================
# 8. 월간 리포트 생성 메인 함수
# ===========================================

def generate_monthly_report(
    user_id: int,
    year: int,
    month: int,
    sessions: List[WorkoutSession],
    current_measurement: FitnessMeasurement,
    previous_measurement: FitnessMeasurement = None
) -> Dict:
    """월간 리포트 전체 데이터 생성"""

    # 1. 운동 요약
    summary = calculate_monthly_summary(sessions)

    # 2. 운동 빈도
    frequency = calculate_workout_frequency(sessions)

    # 3. 체력 지표 변화
    metric_changes = []
    if previous_measurement:
        metric_changes = calculate_metric_changes(previous_measurement, current_measurement)

    # 4. 꾸준함 점수
    consistency_score = calculate_consistency_score(sessions)

    return {
        'user_id': user_id,
        'year': year,
        'month': month,
        'summary': summary,
        'workout_frequency': frequency,
        'sessions': [s.to_dict() for s in sessions],
        'metric_changes': metric_changes,
        'consistency_score': consistency_score
    }


# ===========================================
# 9. 테스트 실행
# ===========================================

if __name__ == '__main__':
    print("=== 월간 리포트 임시 데이터 생성 테스트 ===\n")

    # 사용자 정보
    user_id = 1
    age = 28
    gender = 'M'

    # 3개월치 데이터 생성
    reports = []

    for month_offset, (month, workout_days) in enumerate([(9, 12), (10, 15), (11, 18)]):
        print(f"\n--- {2025}년 {month}월 데이터 생성 ---")

        # 운동 세션 생성
        sessions = generate_mock_workout_sessions(
            user_id=user_id,
            year=2025,
            month=month,
            workout_days=workout_days
        )

        print(f"생성된 운동 세션: {len(sessions)}개")

        # 체력 측정 데이터 생성
        current_measurement = generate_mock_fitness_measurement(
            user_id=user_id,
            measurement_date=f'2025-{month:02d}-15',
            age=age,
            gender=gender,
            improvement_factor=1.0 + (month_offset * 0.05)  # 매달 5%씩 향상
        )

        previous_measurement = None
        if month_offset > 0:
            previous_measurement = generate_mock_fitness_measurement(
                user_id=user_id,
                measurement_date=f'2025-{month-1:02d}-15',
                age=age,
                gender=gender,
                improvement_factor=1.0 + ((month_offset - 1) * 0.05)
            )

        # 월간 리포트 생성
        report = generate_monthly_report(
            user_id=user_id,
            year=2025,
            month=month,
            sessions=sessions,
            current_measurement=current_measurement,
            previous_measurement=previous_measurement
        )

        reports.append(report)

        # 결과 출력
        print(f"총 운동 일수: {report['summary']['total_workout_days']}일")
        print(f"주당 평균: {report['summary']['weekly_average']}회")
        print(f"꾸준함 점수: {report['consistency_score']['total_score']}점")
        print(f"피드백: {report['consistency_score']['feedback']}")

    # JSON 파일로 저장
    output_file = 'monthly_reports_mock_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(reports, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 월간 리포트 데이터가 '{output_file}'에 저장되었습니다.")

    # DataFrame으로 변환하여 CSV로도 저장
    sessions_data = []
    for report in reports:
        for session in report['sessions']:
            sessions_data.append({
                'user_id': report['user_id'],
                'year': report['year'],
                'month': report['month'],
                **session
            })

    df_sessions = pd.DataFrame(sessions_data)
    df_sessions.to_csv('workout_sessions_mock_data.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] 운동 세션 데이터가 'workout_sessions_mock_data.csv'에 저장되었습니다.")
