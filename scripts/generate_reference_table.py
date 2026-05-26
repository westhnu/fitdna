"""
참조 테이블 생성 스크립트
전처리 데이터에서 연령×성별 그룹별 Z-Score 통계를 추출하여 참조 테이블 생성
"""

import pandas as pd
import json
import pickle

print("=" * 60)
print("참조 테이블 생성 스크립트")
print("=" * 60)

# 1. 전처리 데이터 로드
print("\n[1단계] 전처리 데이터 로드")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv',
                 encoding='cp949')
print(f">> 로드 완료: {len(df):,}건")

# 2. 연령×성별 그룹별 Z-Score 평균·표준편차 계산
print("\n[2단계] 연령×성별 그룹별 통계 계산")
reference_data = {}

ages = df['MESURE_AGE_CO'].unique()
genders = df['SEXDSTN_FLAG_CD'].unique()

total_groups = len(ages) * len(genders)
processed = 0

for age in sorted(ages):
    for gender in genders:
        # 해당 연령×성별 그룹 필터링
        group = df[(df['MESURE_AGE_CO'] == age) & (df['SEXDSTN_FLAG_CD'] == gender)]

        if len(group) >= 10:  # 최소 10명 이상 있는 그룹만
            # 3축 Z-Score 통계 계산
            reference_data[(int(age), gender, 'strength')] = {
                'mean': float(group['strength_z'].mean()),
                'std': float(group['strength_z'].std()),
                'count': len(group)
            }
            reference_data[(int(age), gender, 'flexibility')] = {
                'mean': float(group['flex_z'].mean()),
                'std': float(group['flex_z'].std()),
                'count': len(group)
            }
            reference_data[(int(age), gender, 'endurance')] = {
                'mean': float(group['endurance_z'].mean()),
                'std': float(group['endurance_z'].std()),
                'count': len(group)
            }

        processed += 1
        if processed % 20 == 0:
            print(f"   진행: {processed}/{total_groups} 그룹 ({processed/total_groups*100:.1f}%)")

print(f">> 계산 완료: {len(reference_data)} 항목")

# 3. 통계 정보
print("\n[3단계] 통계 정보")
unique_ages = set(k[0] for k in reference_data.keys())
unique_genders = set(k[1] for k in reference_data.keys())
print(f">> 연령 범위: {min(unique_ages)}세 ~ {max(unique_ages)}세")
print(f">> 성별: {sorted(unique_genders)}")
print(f">> 총 그룹 수: {len(reference_data) // 3} 그룹 (연령×성별)")

# 샘플 출력
print("\n>> 샘플 데이터 (25세 남성):")
for metric in ['strength', 'flexibility', 'endurance']:
    key = (25, 'M', metric)
    if key in reference_data:
        data = reference_data[key]
        print(f"   {metric:12s}: 평균={data['mean']:6.3f}, 표준편차={data['std']:6.3f}, 샘플수={data['count']:4d}")

# 4. JSON 저장 (키를 문자열로 변환)
print("\n[4단계] JSON 형식 저장")
json_data = {}
for key, value in reference_data.items():
    # 튜플 키를 문자열로 변환: (25, 'M', 'strength') -> "25_M_strength"
    str_key = f"{key[0]}_{key[1]}_{key[2]}"
    json_data[str_key] = value

with open('fitdna_reference_table.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
print(">> 저장 완료: fitdna_reference_table.json")

# 5. Pickle 저장 (원본 튜플 키 유지)
print("\n[5단계] Pickle 형식 저장")
with open('fitdna_reference_table.pkl', 'wb') as f:
    pickle.dump(reference_data, f)
print(">> 저장 완료: fitdna_reference_table.pkl")

# 6. CSV 저장 (사람이 읽기 쉬운 형식)
print("\n[6단계] CSV 형식 저장")
csv_rows = []
for key, value in reference_data.items():
    csv_rows.append({
        '나이': key[0],
        '성별': key[1],
        '측정항목': key[2],
        '평균': value['mean'],
        '표준편차': value['std'],
        '샘플수': value['count']
    })

csv_df = pd.DataFrame(csv_rows)
csv_df = csv_df.sort_values(['나이', '성별', '측정항목'])
csv_df.to_csv('fitdna_reference_table.csv', index=False, encoding='utf-8-sig')
print(">> 저장 완료: fitdna_reference_table.csv")

# 7. 사용 예시 함수
print("\n[7단계] 사용 예시 생성")

example_code = '''
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
'''

with open('reference_table_usage_example.py', 'w', encoding='utf-8') as f:
    f.write(example_code)
print(">> 저장 완료: reference_table_usage_example.py")

print("\n" + "=" * 60)
print("참조 테이블 생성 완료!")
print("=" * 60)
print("\n생성된 파일:")
print("1. fitdna_reference_table.json  - JSON 형식 (웹 API용)")
print("2. fitdna_reference_table.pkl   - Pickle 형식 (Python용, 빠름)")
print("3. fitdna_reference_table.csv   - CSV 형식 (사람이 읽기 쉬움)")
print("4. reference_table_usage_example.py - 사용 예시")
print("\n주의: 이 참조 테이블은 Z-Score의 분포를 기반으로 생성되었습니다.")
print("원본 측정값(kg, cm)의 참조 테이블이 아니므로, 새 사용자의 측정값을")
print("Z-Score로 변환하려면 별도의 원본 데이터가 필요합니다.")
