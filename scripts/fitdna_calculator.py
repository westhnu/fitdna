"""
FIT-DNA 계산 모듈
사용자의 체력 측정값을 입력받아 FIT-DNA 유형을 계산합니다.
"""


def calculate_fitdna(strength_z, flex_z, endurance_z, threshold=0.5):
    """
    Z-Score를 입력받아 FIT-DNA 유형 계산

    Parameters:
    -----------
    strength_z : float
        근력 Z-Score (연령×성별 그룹별 정규화된 값)
    flex_z : float
        유연성 Z-Score
    endurance_z : float
        지구력 Z-Score
    threshold : float, optional
        High/Low 기준값 (기본값: 0.5)
        - threshold 이상: High
        - threshold 미만: Low

    Returns:
    --------
    str
        FIT-DNA 유형 코드 (예: 'PFE', 'LSQ', 'PFQ' 등)

    FIT-DNA 코드 체계:
    -----------------
    - 1번째 자리 (근력): P (Power, High) / L (Light, Low)
    - 2번째 자리 (유연성): F (Flexibility, High) / S (Stiff, Low)
    - 3번째 자리 (지구력): E (Endurance, High) / Q (Quick, Low)

    8가지 조합:
    - PFE: 완벽 균형형 (근력↑, 유연성↑, 지구력↑)
    - PFQ: 근력·유연성 우수형 (근력↑, 유연성↑, 지구력↓)
    - PSE: 근력·지구력 우수형 (근력↑, 유연성↓, 지구력↑)
    - PSQ: 근력 특화형 (근력↑, 유연성↓, 지구력↓)
    - LFE: 유연성·지구력 우수형 (근력↓, 유연성↑, 지구력↑)
    - LFQ: 유연성 특화형 (근력↓, 유연성↑, 지구력↓)
    - LSE: 지구력 특화형 (근력↓, 유연성↓, 지구력↑)
    - LSQ: 전체 개선 필요형 (근력↓, 유연성↓, 지구력↓)

    Example:
    --------
    >>> calculate_fitdna(1.2, 0.6, -0.3)
    'PFQ'

    >>> calculate_fitdna(-0.3, 0.8, 1.5)
    'LFE'

    >>> calculate_fitdna(0.4, -0.2, -0.1)
    'LSQ'
    """
    # 근력 코드
    p_code = 'P' if strength_z >= threshold else 'L'

    # 유연성 코드
    f_code = 'F' if flex_z >= threshold else 'S'

    # 지구력 코드
    e_code = 'E' if endurance_z >= threshold else 'Q'

    # FIT-DNA 조합
    fitdna = f"{p_code}{f_code}{e_code}"

    return fitdna


def get_fitdna_description(fitdna_code):
    """
    FIT-DNA 코드에 대한 설명 반환

    Parameters:
    -----------
    fitdna_code : str
        FIT-DNA 유형 코드 (예: 'PFE')

    Returns:
    --------
    dict
        FIT-DNA 유형에 대한 상세 정보
        - name: 유형명 (한글)
        - strength: 근력 수준 (High/Low)
        - flexibility: 유연성 수준 (High/Low)
        - endurance: 지구력 수준 (High/Low)
        - description: 설명

    Example:
    --------
    >>> info = get_fitdna_description('PFE')
    >>> print(info['name'])
    '완벽 균형형'
    """
    fitdna_info = {
        'PFE': {
            'name': '완벽 균형형',
            'strength': 'High',
            'flexibility': 'High',
            'endurance': 'High',
            'description': '근력, 유연성, 지구력 모두 우수한 이상적인 체력 상태입니다.'
        },
        'PFQ': {
            'name': '근력·유연성 우수형',
            'strength': 'High',
            'flexibility': 'High',
            'endurance': 'Low',
            'description': '근력과 유연성은 우수하나 지구력 개선이 필요합니다.'
        },
        'PSE': {
            'name': '근력·지구력 우수형',
            'strength': 'High',
            'flexibility': 'Low',
            'endurance': 'High',
            'description': '근력과 지구력은 우수하나 유연성 개선이 필요합니다.'
        },
        'PSQ': {
            'name': '근력 특화형',
            'strength': 'High',
            'flexibility': 'Low',
            'endurance': 'Low',
            'description': '근력은 우수하나 유연성과 지구력 개선이 필요합니다.'
        },
        'LFE': {
            'name': '유연성·지구력 우수형',
            'strength': 'Low',
            'flexibility': 'High',
            'endurance': 'High',
            'description': '유연성과 지구력은 우수하나 근력 개선이 필요합니다.'
        },
        'LFQ': {
            'name': '유연성 특화형',
            'strength': 'Low',
            'flexibility': 'High',
            'endurance': 'Low',
            'description': '유연성은 우수하나 근력과 지구력 개선이 필요합니다.'
        },
        'LSE': {
            'name': '지구력 특화형',
            'strength': 'Low',
            'flexibility': 'Low',
            'endurance': 'High',
            'description': '지구력은 우수하나 근력과 유연성 개선이 필요합니다.'
        },
        'LSQ': {
            'name': '전체 개선 필요형',
            'strength': 'Low',
            'flexibility': 'Low',
            'endurance': 'Low',
            'description': '근력, 유연성, 지구력 모두 개선이 필요합니다. 균형잡힌 운동을 시작하세요.'
        }
    }

    return fitdna_info.get(fitdna_code.upper(), {
        'name': '알 수 없는 유형',
        'strength': 'Unknown',
        'flexibility': 'Unknown',
        'endurance': 'Unknown',
        'description': '유효하지 않은 FIT-DNA 코드입니다.'
    })


def calculate_zscore(value, age, gender, measurement_type, reference_data=None):
    """
    개인 측정값을 Z-Score로 변환

    Parameters:
    -----------
    value : float
        개인의 측정값 (예: 악력 35kg)
    age : int
        나이
    gender : str
        성별 ('M' 또는 'F')
    measurement_type : str
        측정 항목 ('grip_strength', 'flexibility', 'vo2max' 등)
    reference_data : dict, optional
        연령×성별 그룹별 평균·표준편차 데이터
        형식: {(age, gender, type): {'mean': float, 'std': float}}

    Returns:
    --------
    float
        Z-Score 값

    Note:
    -----
    실제 서비스에서는 reference_data를 국민체력100 데이터베이스에서 조회해야 합니다.
    현재는 간단한 예시 함수로 구현되었습니다.

    Example:
    --------
    >>> # 25세 남성, 악력 40kg (평균 35kg, 표준편차 5kg)
    >>> ref = {(25, 'M', 'grip'): {'mean': 35, 'std': 5}}
    >>> zscore = calculate_zscore(40, 25, 'M', 'grip', ref)
    >>> print(zscore)  # (40-35)/5 = 1.0
    1.0
    """
    if reference_data is None:
        raise ValueError("reference_data가 필요합니다. 연령×성별 그룹별 평균·표준편차 데이터를 제공하세요.")

    # 연령×성별×측정항목 키 생성
    key = (age, gender, measurement_type)

    if key not in reference_data:
        raise ValueError(f"참조 데이터에 ({age}세, {gender}, {measurement_type}) 정보가 없습니다.")

    ref = reference_data[key]
    mean = ref['mean']
    std = ref['std']

    if std == 0:
        raise ValueError("표준편차가 0입니다. Z-Score를 계산할 수 없습니다.")

    # Z-Score 계산
    zscore = (value - mean) / std

    return zscore


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("FIT-DNA 계산기")
    print("=" * 60)

    # 예시 1: Z-Score 직접 입력
    print("\n[예시 1] Z-Score를 이미 알고 있는 경우")
    strength_z = 1.2
    flex_z = 0.6
    endurance_z = -0.3

    fitdna = calculate_fitdna(strength_z, flex_z, endurance_z)
    info = get_fitdna_description(fitdna)

    print(f"\n입력값:")
    print(f"  근력 Z-Score: {strength_z}")
    print(f"  유연성 Z-Score: {flex_z}")
    print(f"  지구력 Z-Score: {endurance_z}")
    print(f"\nFIT-DNA 결과: {fitdna} - {info['name']}")
    print(f"설명: {info['description']}")

    # 예시 2: 다른 유형
    print("\n" + "=" * 60)
    print("\n[예시 2] 다른 체력 패턴")

    examples = [
        (-0.3, 0.8, 1.5, "유연성·지구력 우수형"),
        (0.4, -0.2, -0.1, "전체 개선 필요형"),
        (1.8, 1.2, 1.5, "완벽 균형형"),
    ]

    for s_z, f_z, e_z, expected in examples:
        fitdna = calculate_fitdna(s_z, f_z, e_z)
        info = get_fitdna_description(fitdna)
        print(f"\nZ-Score: [{s_z:5.1f}, {f_z:5.1f}, {e_z:5.1f}] → {fitdna} ({info['name']})")

    # 예시 3: Z-Score 계산 (참조 데이터 필요)
    print("\n" + "=" * 60)
    print("\n[예시 3] 측정값에서 Z-Score 계산")
    print("\n※ 실제 서비스에서는 국민체력100 데이터베이스의 참조값이 필요합니다.")
    print("※ 아래는 가상의 참조 데이터를 사용한 예시입니다.\n")

    # 가상의 참조 데이터 (실제로는 DB에서 조회)
    reference_data = {
        (25, 'M', 'grip'): {'mean': 35.0, 'std': 5.0},
        (25, 'M', 'flexibility'): {'mean': 15.0, 'std': 6.0},
        (25, 'M', 'vo2max'): {'mean': 45.0, 'std': 8.0},
    }

    # 25세 남성의 측정값
    grip_value = 42  # 악력 42kg
    flex_value = 20  # 유연성 20cm
    vo2_value = 38   # VO2max 38

    s_z = calculate_zscore(grip_value, 25, 'M', 'grip', reference_data)
    f_z = calculate_zscore(flex_value, 25, 'M', 'flexibility', reference_data)
    e_z = calculate_zscore(vo2_value, 25, 'M', 'vo2max', reference_data)

    print(f"측정값:")
    print(f"  악력: {grip_value}kg → Z-Score: {s_z:.2f}")
    print(f"  유연성: {flex_value}cm → Z-Score: {f_z:.2f}")
    print(f"  VO2max: {vo2_value} → Z-Score: {e_z:.2f}")

    fitdna = calculate_fitdna(s_z, f_z, e_z)
    info = get_fitdna_description(fitdna)

    print(f"\nFIT-DNA 결과: {fitdna} - {info['name']}")
    print(f"설명: {info['description']}")

    print("\n" + "=" * 60)
