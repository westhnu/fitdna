"""
사용자 측정값 입력 → FIT-DNA 계산 모델
원본 측정값(kg, cm) → Z-Score → FIT-DNA
"""

import pickle
from fitdna_calculator import calculate_fitdna, get_fitdna_description, classify_axis_levels


def load_reference_table(pkl_path='FITDNA_ref_new.pkl'):
    """참조 테이블 로드"""
    with open(pkl_path, 'rb') as f:
        return pickle.load(f)


def calculate_measurement_zscore(value, age, gender, measurement_type, ref_table):
    """
    개인 측정값 → Z-Score 변환

    Parameters:
    -----------
    value : float
        실제 측정값 (예: 악력 35kg, 유연성 15cm)
    age : int
        나이
    gender : str
        성별 ('M' 또는 'F')
    measurement_type : str
        측정 항목 ('grip_right', 'sit_and_reach', 'vo2max' 등)
    ref_table : dict
        참조 테이블

    Returns:
    --------
    float
        Z-Score 값
    """
    key = (age, gender, measurement_type)

    if key not in ref_table:
        raise ValueError(f"참조 데이터에 ({age}세, {gender}, {measurement_type}) 정보가 없습니다.")

    ref = ref_table[key]
    mean = ref['mean']
    std = ref['std']

    if std == 0:
        raise ValueError(f"표준편차가 0입니다. ({age}세, {gender}, {measurement_type})")

    zscore = (value - mean) / std
    return zscore


def calculate_fitdna_from_measurements(
    age,
    gender,
    measurements,
    ref_table,
    threshold=0.25,
    debug=False
):
    """
    사용자 측정값에서 FIT-DNA 계산

    Parameters:
    -----------
    age : int
        나이
    gender : str
        성별 ('M' 또는 'F')
    measurements : dict
        측정값 딕셔너리
        {
            'grip_right': 35.0,    # 악력(오른손) kg
            'grip_left': 33.0,     # 악력(왼손) kg (선택)
            'sit_and_reach': 15.0, # 앉아윗몸앞으로굽히기 cm
            'vo2max': 45.0,        # VO2max mL/kg/min
            'standing_long_jump': 200.0,  # 제자리멀리뛰기 cm (선택)
            'sit_up': 30.0,        # 윗몸일으키기 회/분 (선택)
            'shuttle_run': 50.0,   # 왕복오래달리기 회 (선택)
        }
    ref_table : dict
        참조 테이블
    threshold : float
        High/Low 기준값 (기본: 0.0 → Z-Score 0 기준)
    debug : bool
        디버깅 로그 출력 여부

    Returns:
    --------
    dict
        {
            'fitdna_type': 'PFE',
            'type_name': '완벽 균형형',
            'description': '...',
            'strength_z': 1.2,
            'flexibility_z': 0.6,
            'endurance_z': -0.3,
            'measurements_used': {...}
        }
    """
    # 1. 3축별 Z-Score 계산

    # 근력 축 (여러 측정값의 평균)
    strength_items = ['grip_right', 'grip_left', 'standing_long_jump', 'sit_up']
    strength_zscores = []

    for item in strength_items:
        if item in measurements:
            try:
                z = calculate_measurement_zscore(
                    measurements[item], age, gender, item, ref_table
                )
                strength_zscores.append(z)
            except ValueError as e:
                if debug:
                    print(f"[FITDNA DEBUG] 근력 항목 '{item}' 참조값 없음 → 스킵 ({e})")
                # 참조 데이터 없으면 스킵
                pass

    if not strength_zscores:
        raise ValueError("근력 측정값이 필요합니다 (grip_right, grip_left, standing_long_jump, sit_up 중 1개 이상)")

    strength_z = sum(strength_zscores) / len(strength_zscores)

    # 유연성 축 (sit_and_reach가 없으면 0으로 처리)
    if 'sit_and_reach' in measurements:
        try:
            flex_z = calculate_measurement_zscore(
                measurements['sit_and_reach'], age, gender, 'sit_and_reach', ref_table
            )
        except ValueError as e:
            # 참조 데이터 없으면 중립값(0) 사용
            flex_z = 0.0
            if debug:
                print(f"[FITDNA DEBUG] sit_and_reach 참조값 없음 → flex_z=0.0 사용 ({e})")
    else:
        # 유연성 데이터 없으면 중립값(0) 사용
        flex_z = 0.0
        if debug:
            print("[FITDNA DEBUG] sit_and_reach 측정값 없음 → flex_z=0.0 사용")

    # 지구력 축
    endurance_items = ['vo2max', 'shuttle_run']
    endurance_zscores = []

    for item in endurance_items:
        if item in measurements:
            try:
                z = calculate_measurement_zscore(
                    measurements[item], age, gender, item, ref_table
                )
                endurance_zscores.append(z)
            except ValueError as e:
                if debug:
                    print(f"[FITDNA DEBUG] 지구력 항목 '{item}' 참조값 없음 → 스킵 ({e})")
                pass

    if not endurance_zscores:
        raise ValueError("지구력 측정값이 필요합니다 (vo2max 또는 shuttle_run 중 1개 이상)")

    endurance_z = sum(endurance_zscores) / len(endurance_zscores)

    # 2. FIT-DNA 계산
    fitdna_type = calculate_fitdna(strength_z, flex_z, endurance_z, threshold)
    info = get_fitdna_description(fitdna_type)

    # 실제 Z-Score 기준으로 각 축 High/Low 재계산
    strength_level, flexibility_level, endurance_level = classify_axis_levels(
        strength_z, flex_z, endurance_z, threshold
    )

    if debug:
        print("\n[FITDNA DEBUG] ===============================")
        print(f"age={age}, gender={gender}")
        print(f"measurements={measurements}")
        print(f"Z-scores → strength={strength_z:.2f}, flex={flex_z:.2f}, endurance={endurance_z:.2f}")
        print(f"levels   → strength={strength_level}, flex={flexibility_level}, endurance={endurance_level}")
        print(f"threshold={threshold}")
        print(f"FIT-DNA  → {fitdna_type} ({info['name']})")
        print("[FITDNA DEBUG] ===============================\n")

    # 3. 결과 반환
    return {
        'fitdna_type': fitdna_type,
        'type_name': info['name'],
        'description': info['description'],
        'strength_level': strength_level,
        'flexibility_level': flexibility_level,
        'endurance_level': endurance_level,
        'strength_z': round(strength_z, 2),
        'flexibility_z': round(flex_z, 2),
        'endurance_z': round(endurance_z, 2),
        'measurements_used': {
            'strength_items': [k for k in strength_items if k in measurements],
            'flexibility_items': ['sit_and_reach'] if 'sit_and_reach' in measurements else [],
            'endurance_items': [k for k in endurance_items if k in measurements]
        },
        'age': age,
        'gender': gender
    }


# ============================================================
# 사용 예시
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("사용자 측정값 → FIT-DNA 계산 예시")
    print("=" * 70)

    # 1. 참조 테이블 로드
    print("\n[1단계] 참조 테이블 로드")
    ref_table = load_reference_table()
    print(f">> 로드 완료: {len(ref_table)} 항목")

    # 2. 사용자 A (25세 남성)
    print("\n" + "=" * 70)
    print("\n[예시 1] 25세 남성 - 측정값 입력")

    user_a = {
        'age': 25,
        'gender': 'M',
        'measurements': {
            'grip_right': 35.0,        # 악력(오른손) 35kg
            'grip_left': 33.0,         # 악력(왼손) 33kg
            'sit_and_reach': 15.0,     # 앉아윗몸앞으로굽히기 15cm
            'vo2max': 45.0,            # VO2max 45
            'standing_long_jump': 220.0,  # 제자리멀리뛰기 220cm
        }
    }

    print(f"\n나이: {user_a['age']}세")
    print(f"성별: {'남성' if user_a['gender'] == 'M' else '여성'}")
    print(f"측정값:")
    for key, value in user_a['measurements'].items():
        print(f"  - {key}: {value}")

    try:
        result = calculate_fitdna_from_measurements(
            user_a['age'],
            user_a['gender'],
            user_a['measurements'],
            ref_table,
            debug=True  # 예시에서는 디버깅 켜서 확인
        )

        print(f"\n결과:")
        print(f"  FIT-DNA: {result['fitdna_type']} ({result['type_name']})")
        print(f"  근력: {result['strength_level']} (Z-Score: {result['strength_z']})")
        print(f"  유연성: {result['flexibility_level']} (Z-Score: {result['flexibility_z']})")
        print(f"  지구력: {result['endurance_level']} (Z-Score: {result['endurance_z']})")
        print(f"  설명: {result['description']}")

    except ValueError as e:
        print(f"\n오류: {e}")

    # 3. 사용자 B (30세 여성)
    print("\n" + "=" * 70)
    print("\n[예시 2] 30세 여성 - 최소 측정값만")

    user_b = {
        'age': 30,
        'gender': 'F',
        'measurements': {
            'grip_right': 22.0,        # 악력(오른손) 22kg
            'sit_and_reach': 20.0,     # 앉아윗몸앞으로굽히기 20cm
            'vo2max': 38.0,            # VO2max 38
        }
    }

    print(f"\n나이: {user_b['age']}세")
    print(f"성별: {'남성' if user_b['gender'] == 'M' else '여성'}")
    print(f"측정값:")
    for key, value in user_b['measurements'].items():
        print(f"  - {key}: {value}")

    try:
        result = calculate_fitdna_from_measurements(
            user_b['age'],
            user_b['gender'],
            user_b['measurements'],
            ref_table,
            debug=True  # 여기도 디버깅 켜서 패턴 확인
        )

        print(f"\n결과:")
        print(f"  FIT-DNA: {result['fitdna_type']} ({result['type_name']})")
        print(f"  근력: {result['strength_level']} (Z-Score: {result['strength_z']})")
        print(f"  유연성: {result['flexibility_level']} (Z-Score: {result['flexibility_z']})")
        print(f"  지구력: {result['endurance_level']} (Z-Score: {result['endurance_z']})")
        print(f"  설명: {result['description']}")

    except ValueError as e:
        print(f"\n오류: {e}")

    print("\n" + "=" * 70)
    print("완료!")
    print("=" * 70)
