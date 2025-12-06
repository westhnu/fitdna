
# ===== 참조 테이블 사용 예시 =====

import json
import pickle

# 방법 1: JSON 파일 로드
with open('fitdna_reference_table.json', 'r', encoding='utf-8') as f:
    ref_json = json.load(f)

# 25세 남성의 근력 참조값 조회
key = "25_M_strength"
if key in ref_json:
    ref = ref_json[key]
    print(f"평균: {ref['mean']}, 표준편차: {ref['std']}")

# 방법 2: Pickle 파일 로드 (더 빠름)
with open('fitdna_reference_table.pkl', 'rb') as f:
    ref_dict = pickle.load(f)

# 튜플 키로 직접 조회
ref = ref_dict.get((25, 'M', 'strength'))
if ref:
    print(f"평균: {ref['mean']}, 표준편차: {ref['std']}")

# 방법 3: 함수로 감싸기
def get_reference(age, gender, metric_type):
    """참조 데이터 조회"""
    key = (age, gender, metric_type)
    return ref_dict.get(key)

# 사용
ref = get_reference(25, 'M', 'strength')
if ref:
    # Z-Score 계산
    grip_value = 42.0  # kg
    z_score = (grip_value - ref['mean']) / ref['std']
    print(f"악력 Z-Score: {z_score:.2f}")
