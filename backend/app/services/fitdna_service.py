"""
FIT-DNA 계산 서비스
모델링 파일(fitdna_from_measurements.py) 연동
"""

import sys
import os
import pickle
from typing import Dict, Tuple

# 프로젝트 루트를 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

# 모델링 파일 import
try:
    from fitdna_from_measurements import (
        calculate_fitdna_from_measurements,
        load_reference_table,
        calculate_measurement_zscore
    )
    from fitdna_calculator import get_fitdna_description
except ImportError as e:
    print(f"⚠️  모델링 파일 import 실패: {e}")
    print(f"   프로젝트 루트: {project_root}")


# 참조 테이블 로드 (전역 변수로 캐싱)
_reference_table = None


def get_reference_table():
    """참조 테이블 로드 (캐싱)"""
    global _reference_table
    if _reference_table is None:
        try:
            _reference_table = load_reference_table()
            print("✅ FIT-DNA 참조 테이블 로드 완료")
        except Exception as e:
            print(f"❌ 참조 테이블 로드 실패: {e}")
            raise
    return _reference_table


def calculate_user_fitdna(
    age: int,
    gender: str,
    measurements: Dict[str, float],
    threshold: float = 0.5
) -> Dict:
    """
    사용자 측정값으로 FIT-DNA 계산

    Args:
        age: 나이
        gender: 성별 ('M' or 'F')
        measurements: 측정값 딕셔너리
            {
                'grip_right': 41.2,
                'grip_left': 39.1,
                'sit_up': 48,
                'sit_and_reach': 15.8,
                'standing_long_jump': 205,
                'vo2max': 44.8,
                'shuttle_run': 48
            }
        threshold: FIT-DNA 분류 임계값 (기본 0.5)

    Returns:
        FIT-DNA 계산 결과
        {
            'fitdna_type': 'PFE',
            'type_name': '파워 애슬리트',
            'description': '...',
            'strength_z': 0.6,
            'flexibility_z': 0.25,
            'endurance_z': 0.7,
            'strength_score': 8.5,
            'flexibility_score': 7.2,
            'endurance_score': 8.8
        }
    """

    try:
        ref_table = get_reference_table()

        # FIT-DNA 계산
        result = calculate_fitdna_from_measurements(
            age=age,
            gender=gender,
            measurements=measurements,
            ref_table=ref_table,
            threshold=threshold
        )

        # 타입 정보 추가
        type_info = get_fitdna_description(result['fitdna_type'])
        result.update(type_info)

        return result

    except Exception as e:
        print(f"❌ FIT-DNA 계산 중 에러: {e}")
        raise


def get_fitdna_strengths_weaknesses(
    strength_z: float,
    flexibility_z: float,
    endurance_z: float,
    threshold: float = 0.5
) -> Tuple[list, list]:
    """
    Z-Score로 강점/약점 판단

    Returns:
        (strengths, weaknesses) 튜플
    """

    strengths = []
    weaknesses = []

    # 근력
    if strength_z >= threshold:
        strengths.append('근력')
    else:
        weaknesses.append('근력')

    # 유연성
    if flexibility_z >= threshold:
        strengths.append('유연성')
    else:
        weaknesses.append('유연성')

    # 지구력
    if endurance_z >= threshold:
        strengths.append('지구력')
    else:
        weaknesses.append('지구력')

    return strengths, weaknesses


def zscore_to_score_0_10(zscore: float) -> float:
    """
    Z-Score를 0-10 점수로 변환

    Z-Score 범위: -3 ~ +3
    점수 범위: 0 ~ 10
    """

    # Z-Score를 0-10 스케일로 변환
    # -3 이하 -> 0점, +3 이상 -> 10점
    score = ((zscore + 3) / 6) * 10
    score = max(0.0, min(10.0, score))  # 0-10 범위로 클리핑

    return round(score, 1)
