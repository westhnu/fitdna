"""
원본 측정 데이터에서 참조 테이블 생성
사용자 측정값(kg, cm) → Z-Score 변환용
"""

import pandas as pd
import json
import pickle
import numpy as np

print("=" * 70)
print("원본 측정 데이터 기반 참조 테이블 생성")
print("=" * 70)

# 1. 원본 데이터 로드
print("\n[1단계] 원본 측정 데이터 로드")
df = pd.read_csv('KS_NFA_FTNESS_MESURE_ITEM_MESURE_INFO_202504.csv', encoding='utf-8')
print(f">> 로드 완료: {len(df):,}건")

# 2. 측정 항목 매핑 (MESURE_IEM_XXX → 실제 항목명)
print("\n[2단계] 측정 항목 매핑")

# 주요 측정 항목 컬럼 매핑
MEASUREMENT_MAPPING = {
    # 근력
    'grip_left': 'MESURE_IEM_017_VALUE',      # 악력(좌)
    'grip_right': 'MESURE_IEM_018_VALUE',     # 악력(우)
    'standing_long_jump': 'MESURE_IEM_026_VALUE',  # 제자리멀리뛰기
    'sit_up': 'MESURE_IEM_019_VALUE',         # 윗몸일으키기

    # 유연성
    'sit_and_reach': 'MESURE_IEM_027_VALUE',  # 앉아윗몸앞으로굽히기

    # 지구력
    'vo2max': 'MESURE_IEM_036_VALUE',         # VO2max
    'shuttle_run': 'MESURE_IEM_030_VALUE',    # 왕복오래달리기
}

print(f">> 매핑된 측정 항목: {len(MEASUREMENT_MAPPING)}개")

# 3. 연령×성별 그룹별 통계 계산
print("\n[3단계] 연령×성별 그룹별 통계 계산")

reference_data = {}
ages = sorted(df['MESURE_AGE_CO'].dropna().unique())
genders = sorted(df['SEXDSTN_FLAG_CD'].dropna().unique())

total_groups = len(ages) * len(genders) * len(MEASUREMENT_MAPPING)
processed = 0

for age in ages:
    for gender in genders:
        # 해당 연령×성별 그룹 필터링
        group = df[(df['MESURE_AGE_CO'] == age) & (df['SEXDSTN_FLAG_CD'] == gender)]

        if len(group) >= 10:  # 최소 10명 이상 있는 그룹만
            for item_name, column_name in MEASUREMENT_MAPPING.items():
                # 해당 측정 항목의 값 추출 (결측치 제거)
                values = pd.to_numeric(group[column_name], errors='coerce').dropna()

                if len(values) >= 5:  # 최소 5개 이상 데이터 있어야 함
                    reference_data[(int(age), gender, item_name)] = {
                        'mean': float(values.mean()),
                        'std': float(values.std()) if values.std() > 0 else 1.0,  # 0 방지
                        'count': int(len(values)),
                        'min': float(values.min()),
                        'max': float(values.max())
                    }

        processed += len(MEASUREMENT_MAPPING)
        if processed % 50 == 0:
            print(f"   진행: {processed}/{total_groups} ({processed/total_groups*100:.1f}%)")

print(f">> 계산 완료: {len(reference_data)} 항목")

# 4. 3축(strength/flexibility/endurance) 통합 참조 계산
print("\n[4단계] 3축 통합 참조 테이블 생성")

# 3축별 항목 그룹핑
AXIS_ITEMS = {
    'strength': ['grip_left', 'grip_right', 'standing_long_jump', 'sit_up'],
    'flexibility': ['sit_and_reach'],
    'endurance': ['vo2max', 'shuttle_run']
}

axis_reference = {}

for age in ages:
    for gender in genders:
        for axis, items in AXIS_ITEMS.items():
            # 해당 축의 모든 항목 평균값 수집
            axis_values = []

            for item in items:
                key = (int(age), gender, item)
                if key in reference_data:
                    # 각 항목별로 표준화된 값의 평균
                    axis_values.append({
                        'mean': reference_data[key]['mean'],
                        'std': reference_data[key]['std'],
                        'count': reference_data[key]['count']
                    })

            if axis_values:
                # 가중 평균 (샘플 수 기반)
                total_count = sum(v['count'] for v in axis_values)

                axis_reference[(int(age), gender, axis)] = {
                    'items': len(axis_values),
                    'total_count': total_count,
                    # 참고용 평균 (실제로는 각 항목별 계산 사용)
                    'avg_mean': np.mean([v['mean'] for v in axis_values]),
                    'avg_std': np.mean([v['std'] for v in axis_values])
                }

print(f">> 3축 통합 참조: {len(axis_reference)} 항목")

# 5. 통계 정보
print("\n[5단계] 통계 정보")
unique_ages = set(k[0] for k in reference_data.keys())
unique_genders = set(k[1] for k in reference_data.keys())
unique_items = set(k[2] for k in reference_data.keys())

print(f">> 연령 범위: {min(unique_ages)}세 ~ {max(unique_ages)}세")
print(f">> 성별: {sorted(unique_genders)}")
print(f">> 측정 항목: {sorted(unique_items)}")
print(f">> 총 참조 항목: {len(reference_data)}")

# 6. 샘플 출력
print("\n>> 샘플 데이터 (25세 남성):")
for item in ['grip_right', 'sit_and_reach', 'vo2max']:
    key = (25, 'M', item)
    if key in reference_data:
        data = reference_data[key]
        print(f"   {item:20s}: 평균={data['mean']:7.2f}, 표준편차={data['std']:6.2f}, 샘플={data['count']:4d}, 범위=[{data['min']:.1f}~{data['max']:.1f}]")

# 7. JSON 저장
print("\n[6단계] JSON 형식 저장")
json_data = {}
for key, value in reference_data.items():
    str_key = f"{key[0]}_{key[1]}_{key[2]}"
    json_data[str_key] = value

with open('fitdna_original_reference.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)
print(">> 저장 완료: fitdna_original_reference.json")

# 8. Pickle 저장
print("\n[7단계] Pickle 형식 저장")
with open('fitdna_original_reference.pkl', 'wb') as f:
    pickle.dump(reference_data, f)
print(">> 저장 완료: fitdna_original_reference.pkl")

# 9. CSV 저장
print("\n[8단계] CSV 형식 저장")
csv_rows = []
for key, value in reference_data.items():
    csv_rows.append({
        '나이': key[0],
        '성별': key[1],
        '측정항목': key[2],
        '평균': value['mean'],
        '표준편차': value['std'],
        '최소값': value['min'],
        '최대값': value['max'],
        '샘플수': value['count']
    })

csv_df = pd.DataFrame(csv_rows)
csv_df = csv_df.sort_values(['나이', '성별', '측정항목'])
csv_df.to_csv('fitdna_original_reference.csv', index=False, encoding='utf-8-sig')
print(">> 저장 완료: fitdna_original_reference.csv")

print("\n" + "=" * 70)
print("원본 측정 데이터 기반 참조 테이블 생성 완료!")
print("=" * 70)
print("\n생성된 파일:")
print("1. fitdna_original_reference.json  - JSON 형식 (웹 API용)")
print("2. fitdna_original_reference.pkl   - Pickle 형식 (Python용)")
print("3. fitdna_original_reference.csv   - CSV 형식 (확인용)")
print("\n이제 사용자 측정값(kg, cm) → Z-Score → FIT-DNA 계산 가능!")
