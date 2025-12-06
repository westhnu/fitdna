"""
FIT-DNA 계산 모듈
사용자의 체력 측정값을 입력받아 FIT-DNA 유형을 계산합니다.
"""


def classify_axis_levels(strength_z, flex_z, endurance_z, threshold=0.0):
    """
    각 축(근력/유연성/지구력)의 High/Low 여부를 반환

    Parameters:
    -----------
    strength_z : float
    flex_z : float
    endurance_z : float
    threshold : float
        High/Low 기준값 (기본값: 0.0)

    Returns:
    --------
    (str, str, str)
        (strength_level, flexibility_level, endurance_level)
        각각 'High' 또는 'Low'
    """
    strength_level = 'High' if strength_z >= threshold else 'Low'
    flex_level = 'High' if flex_z >= threshold else 'Low'
    endurance_level = 'High' if endurance_z >= threshold else 'Low'
    return strength_level, flex_level, endurance_level


def calculate_fitdna(strength_z, flex_z, endurance_z, threshold=0.0):
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
        High/Low 기준값 (기본값: 0.0)
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
    """
    # 근력 코드
    p_code = 'P' if strength_z >= threshold else 'L'

    # 유연성 코드
    f_code = 'F' if flex_z >= threshold else 'S'

    # 지구력 코드
    e_code = 'E' if endurance_z >= threshold else 'Q'

    # FIT-DNA 조합
    fitdna = f"{p_code}{f_code}{e_code}"

    # 디버깅이 필요하면 아래 주석 해제해서 확인 가능
    # print(f"[FITDNA] Z: strength={strength_z:.2f}, flex={flex_z:.2f}, endur={endurance_z:.2f}, th={threshold}")
    # print(f"[FITDNA] code: {fitdna}")

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
    """
    if reference_data is None:
        raise ValueError("reference_data가 필요합니다. 연령×성별 그룹별 평균·표준편차 데이터를 제공하세요.")
