"""
Phase 2-3: 운동 목록 통합 추출
- 체력 측정별 운동처방 데이터
- 국민연령별추천운동정보
두 데이터셋에서 모든 운동 목록을 추출하고 통합
"""

import pandas as pd
import re
from collections import Counter

# 데이터 로드
print("=" * 60)
print("Phase 2-3: 운동 목록 통합 추출")
print("=" * 60)

# 1. 체력 측정별 운동처방 데이터
print("\n[1단계] 체력 측정별 운동처방 데이터 로드")
prescription_path = "최종/최종/체력 측정별 운동처방 데이터/merged_KS_NFA_FTNESS_MESURE_MVM_PRSCRPTN_INFO_2025_0107.csv"
df_prescription = pd.read_csv(prescription_path, encoding='utf-8-sig')
print(f">> 로드 완료: {len(df_prescription):,}건")

# 2. 국민연령별추천운동정보
print("\n[2단계] 국민연령별추천운동정보 로드")
recommendation_path = "최종/최종/국민연령별추천운동정보/KS_MRFN_AGE_ACCTO_RECOMMEND_SPORTS_INFO_202507.csv"
df_recommendation = pd.read_csv(recommendation_path, encoding='utf-8-sig')
print(f">> 로드 완료: {len(df_recommendation):,}건")

# 3. 운동처방 데이터에서 운동 추출 (텍스트 파싱)
print("\n[3단계] 운동처방 데이터에서 운동 추출")
exercises_from_prescription = []

for idx, row in df_prescription.iterrows():
    text = str(row['MVM_PRSCRPTN_CN'])
    if pd.isna(text) or text == 'nan':
        continue

    # "준비운동:..., 본운동:..., 정리운동:..." 형태 파싱
    # '/' 또는 ',' 로 분리
    parts = re.split(r'[/,]', text)

    for part in parts:
        part = part.strip()
        # "준비운동:", "본운동:", "정리운동:" 제거
        part = re.sub(r'^(준비운동|본운동|정리운동)\s*:\s*', '', part)
        if part and len(part) > 1:
            exercises_from_prescription.append(part)

print(f">> 추출된 운동: {len(exercises_from_prescription):,}개 (중복 포함)")

# 4. 국민연령별추천운동정보에서 운동 추출
print("\n[4단계] 국민연령별추천운동정보에서 운동 추출")
exercises_from_recommendation = df_recommendation['RECOMEND_MVM_NM'].dropna().tolist()
print(f">> 추출된 운동: {len(exercises_from_recommendation):,}개 (중복 포함)")

# 5. 통합 및 중복 제거
print("\n[5단계] 운동 목록 통합")
all_exercises = exercises_from_prescription + exercises_from_recommendation

# 빈도수 계산
exercise_counter = Counter(all_exercises)
print(f">> 전체 운동 건수: {len(all_exercises):,}개")
print(f">> 유니크 운동 수: {len(exercise_counter)}개")

# 6. 빈도수 높은 순으로 정렬
print("\n[6단계] 빈도수 기준 상위 운동")
sorted_exercises = exercise_counter.most_common(100)
for i, (exercise, count) in enumerate(sorted_exercises[:30], 1):
    print(f"{i:2d}. {exercise:40s} ({count:,}회)")

# 7. 전체 운동 목록을 CSV로 저장
print("\n[7단계] 전체 운동 목록 저장")
exercise_df = pd.DataFrame([
    {'운동명': exercise, '출현빈도': count}
    for exercise, count in sorted_exercises
])
exercise_df.to_csv('phase2_extracted_exercise_list.csv', index=False, encoding='utf-8-sig')
print(f">> 저장 완료: phase2_extracted_exercise_list.csv ({len(exercise_df)}개 운동)")

# 8. 통계 정보
print("\n[8단계] 통계 정보")
print(f">> 총 출현 횟수: {sum(exercise_counter.values()):,}회")
print(f">> 평균 출현 횟수: {sum(exercise_counter.values()) / len(exercise_counter):.1f}회")
print(f">> 1회만 나온 운동: {sum(1 for c in exercise_counter.values() if c == 1)}개")
print(f">> 10회 이상 나온 운동: {sum(1 for c in exercise_counter.values() if c >= 10)}개")
print(f">> 100회 이상 나온 운동: {sum(1 for c in exercise_counter.values() if c >= 100)}개")

print("\n" + "=" * 60)
print("운동 목록 추출 완료!")
print("=" * 60)
