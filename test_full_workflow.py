"""
전체 워크플로우 테스트
사용자 측정값 입력 → Z-Score 변환 → FIT-DNA 계산
"""

import pickle
from fitdna_calculator import calculate_zscore, calculate_fitdna, get_fitdna_description

print("=" * 70)
print("FIT-DNA 전체 워크플로우 테스트")
print("=" * 70)

# 1. 참조 테이블 로드
print("\n[1단계] 참조 테이블 로드")
with open('fitdna_reference_table.pkl', 'rb') as f:
    ref_table = pickle.load(f)
print(f">> 로드 완료: {len(ref_table)} 항목")

# 2. 사용자 입력 (예시)
print("\n[2단계] 사용자 측정값 입력")
print("\n사용자 A (25세 남성)")
print("  악력(오른손): 42kg")
print("  앉아윗몸앞으로굽히기: 20cm")
print("  VO2max: 38")

age = 25
gender = 'M'
grip_value = 42.0
flex_value = 20.0
vo2_value = 38.0

# 3. Z-Score 변환
print("\n[3단계] Z-Score 변환")

try:
    strength_z = calculate_zscore(grip_value, age, gender, 'strength', ref_table)
    flex_z = calculate_zscore(flex_value, age, gender, 'flexibility', ref_table)
    endurance_z = calculate_zscore(vo2_value, age, gender, 'endurance', ref_table)

    print(f"  근력 Z-Score: {strength_z:.2f}")
    print(f"  유연성 Z-Score: {flex_z:.2f}")
    print(f"  지구력 Z-Score: {endurance_z:.2f}")

    # 4. FIT-DNA 계산
    print("\n[4단계] FIT-DNA 계산")
    fitdna = calculate_fitdna(strength_z, flex_z, endurance_z)
    info = get_fitdna_description(fitdna)

    print(f"\n>> FIT-DNA 결과: {fitdna}")
    print(f">> 유형명: {info['name']}")
    print(f">> 근력: {info['strength']}, 유연성: {info['flexibility']}, 지구력: {info['endurance']}")
    print(f">> 설명: {info['description']}")

except ValueError as e:
    print(f"\n오류: {e}")
    print("\n참조 테이블 확인:")
    print(f"  (25, 'M', 'strength') 존재: {(25, 'M', 'strength') in ref_table}")
    print(f"  (25, 'M', 'flexibility') 존재: {(25, 'M', 'flexibility') in ref_table}")
    print(f"  (25, 'M', 'endurance') 존재: {(25, 'M', 'endurance') in ref_table}")

# 5. 다른 사용자 테스트
print("\n" + "=" * 70)
print("\n사용자 B (30세 여성)")

age2 = 30
gender2 = 'F'
grip_value2 = 28.0
flex_value2 = 25.0
vo2_value2 = 42.0

print(f"  악력(오른손): {grip_value2}kg")
print(f"  앉아윗몸앞으로굽히기: {flex_value2}cm")
print(f"  VO2max: {vo2_value2}")

try:
    strength_z2 = calculate_zscore(grip_value2, age2, gender2, 'strength', ref_table)
    flex_z2 = calculate_zscore(flex_value2, age2, gender2, 'flexibility', ref_table)
    endurance_z2 = calculate_zscore(vo2_value2, age2, gender2, 'endurance', ref_table)

    print(f"\nZ-Score: 근력={strength_z2:.2f}, 유연성={flex_z2:.2f}, 지구력={endurance_z2:.2f}")

    fitdna2 = calculate_fitdna(strength_z2, flex_z2, endurance_z2)
    info2 = get_fitdna_description(fitdna2)

    print(f"\nFIT-DNA: {fitdna2} ({info2['name']})")
    print(f"설명: {info2['description']}")

except ValueError as e:
    print(f"\n오류: {e}")

# 6. 참조 테이블 커버리지 확인
print("\n" + "=" * 70)
print("\n[참조 테이블 커버리지]")

ages = set()
genders = set()
metrics = set()

for key in ref_table.keys():
    age, gender, metric = key
    ages.add(age)
    genders.add(gender)
    metrics.add(metric)

print(f"연령 범위: {min(ages)}세 ~ {max(ages)}세")
print(f"성별: {sorted(genders)}")
print(f"측정 항목: {sorted(metrics)}")
print(f"총 연령×성별 그룹: {len(ages) * len(genders)}")
print(f"총 참조 항목: {len(ref_table)}")

# 7. 8가지 유형 전체 출력
print("\n" + "=" * 70)
print("\n[FIT-DNA 8가지 유형]")

types = ['PFE', 'PFQ', 'PSE', 'PSQ', 'LFE', 'LFQ', 'LSE', 'LSQ']
for fitdna_type in types:
    info = get_fitdna_description(fitdna_type)
    print(f"\n{fitdna_type}: {info['name']}")
    print(f"  근력={info['strength']}, 유연성={info['flexibility']}, 지구력={info['endurance']}")
    print(f"  {info['description']}")

print("\n" + "=" * 70)
print("테스트 완료!")
print("=" * 70)
