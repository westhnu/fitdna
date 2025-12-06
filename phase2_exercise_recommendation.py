"""
Phase 2-5: FIT-DNA 유형별 운동 추천 시스템
- 8가지 FIT-DNA 유형별 맞춤 운동 추천
- 강점 유지 + 약점 개선 전략
- 난이도 및 장소 필터링 지원
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 한글 폰트 설정
matplotlib.rc('font', family='Malgun Gothic')
matplotlib.rc('axes', unicode_minus=False)

print("=" * 60)
print("Phase 2-5: FIT-DNA 유형별 운동 추천 시스템")
print("=" * 60)

# 데이터 로드
exercise_db = pd.read_csv('phase2_classified_exercise_database.csv', encoding='utf-8-sig')
print(f"\n>> 운동 DB 로드: {len(exercise_db)}개 운동")

# FIT-DNA 8가지 유형 정의
FITDNA_TYPES = {
    'PFE': {'근력': 'high', '유연성': 'high', '지구력': 'high', '설명': '완벽 균형형'},
    'PFQ': {'근력': 'high', '유연성': 'high', '지구력': 'low', '설명': '근력·유연성 우수형'},
    'PSE': {'근력': 'high', '유연성': 'low', '지구력': 'high', '설명': '근력·지구력 우수형'},
    'PSQ': {'근력': 'high', '유연성': 'low', '지구력': 'low', '설명': '근력 특화형'},
    'LFE': {'근력': 'low', '유연성': 'high', '지구력': 'high', '설명': '유연성·지구력 우수형'},
    'LFQ': {'근력': 'low', '유연성': 'high', '지구력': 'low', '설명': '유연성 특화형'},
    'LSE': {'근력': 'low', '유연성': 'low', '지구력': 'high', '설명': '지구력 특화형'},
    'LSQ': {'근력': 'low', '유연성': 'low', '지구력': 'low', '설명': '전체 개선 필요형'}
}


def recommend_exercises_for_fitdna(fitdna_type, exercise_db, top_n=10, difficulty_filter=None, location_filter=None):
    """
    FIT-DNA 유형에 맞는 운동 추천

    전략:
    - 약점(low) 축의 운동을 우선 추천 (60%)
    - 강점(high) 축의 운동도 유지 (40%)
    """

    type_info = FITDNA_TYPES[fitdna_type]

    # 약점과 강점 파악
    weaknesses = [axis for axis, level in type_info.items() if level == 'low' and axis in ['근력', '유연성', '지구력']]
    strengths = [axis for axis, level in type_info.items() if level == 'high' and axis in ['근력', '유연성', '지구력']]

    # 필터링
    filtered_db = exercise_db.copy()
    if difficulty_filter:
        filtered_db = filtered_db[filtered_db['난이도'] == difficulty_filter]
    if location_filter:
        filtered_db = filtered_db[filtered_db['장소'].isin([location_filter, '양용'])]

    recommendations = []

    # 1. 약점 개선 운동 (60%)
    weakness_count = int(top_n * 0.6)
    if weaknesses:
        for weakness in weaknesses:
            weakness_exercises = filtered_db[filtered_db['주_타입'] == weakness].nlargest(
                weakness_count // len(weaknesses), '출현빈도'
            )
            for idx, row in weakness_exercises.iterrows():
                recommendations.append({
                    '운동명': row['운동명'],
                    '타입': row['주_타입'],
                    '목적': '약점 개선',
                    '난이도': row['난이도'],
                    '장소': row['장소'],
                    '출현빈도': row['출현빈도'],
                    '근력점수': row['근력점수'],
                    '유연성점수': row['유연성점수'],
                    '지구력점수': row['지구력점수']
                })

    # 2. 강점 유지 운동 (40%)
    strength_count = top_n - len(recommendations)
    if strengths:
        for strength in strengths:
            strength_exercises = filtered_db[filtered_db['주_타입'] == strength].nlargest(
                strength_count // len(strengths) if len(strengths) > 0 else strength_count, '출현빈도'
            )
            for idx, row in strength_exercises.iterrows():
                recommendations.append({
                    '운동명': row['운동명'],
                    '타입': row['주_타입'],
                    '목적': '강점 유지',
                    '난이도': row['난이도'],
                    '장소': row['장소'],
                    '출현빈도': row['출현빈도'],
                    '근력점수': row['근력점수'],
                    '유연성점수': row['유연성점수'],
                    '지구력점수': row['지구력점수']
                })

    # 3. 추천 없으면 일반 운동 추천
    if len(recommendations) == 0:
        general_exercises = filtered_db.nlargest(top_n, '출현빈도')
        for idx, row in general_exercises.iterrows():
            recommendations.append({
                '운동명': row['운동명'],
                '타입': row['주_타입'],
                '목적': '전반적 개선',
                '난이도': row['난이도'],
                '장소': row['장소'],
                '출현빈도': row['출현빈도'],
                '근력점수': row['근력점수'],
                '유연성점수': row['유연성점수'],
                '지구력점수': row['지구력점수']
            })

    return pd.DataFrame(recommendations).head(top_n)


# 8가지 유형별 추천 생성
print("\n[FIT-DNA 8유형별 운동 추천 생성 중...]")
all_recommendations = {}

for fitdna_type, type_info in FITDNA_TYPES.items():
    print(f"\n>> {fitdna_type} ({type_info['설명']})")
    recommendations = recommend_exercises_for_fitdna(fitdna_type, exercise_db, top_n=10)
    all_recommendations[fitdna_type] = recommendations

    # 약점/강점 표시
    weaknesses = [axis for axis, level in type_info.items() if level == 'low' and axis in ['근력', '유연성', '지구력']]
    strengths = [axis for axis, level in type_info.items() if level == 'high' and axis in ['근력', '유연성', '지구력']]

    print(f"   약점: {', '.join(weaknesses) if weaknesses else '없음'}")
    print(f"   강점: {', '.join(strengths) if strengths else '없음'}")
    print(f"   추천 운동 {len(recommendations)}개:")
    for i, (idx, row) in enumerate(recommendations.iterrows(), 1):
        print(f"   {i:2d}. [{row['목적']}] {row['운동명']} ({row['타입']}, {row['난이도']}, {row['장소']})")

# 추천 결과 저장 (CSV로 변경)
print("\n[추천 결과 저장 중...]")
for fitdna_type, recommendations in all_recommendations.items():
    filename = f'phase2_exercise_recommendations_{fitdna_type}.csv'
    recommendations.to_csv(filename, index=False, encoding='utf-8-sig')
print(">> 저장 완료: phase2_exercise_recommendations_[유형].csv (8개 파일)")

# 시각화 1: 8가지 유형별 추천 운동 타입 분포
print("\n[시각화 1: 유형별 추천 운동 타입 분포]")
fig, axes = plt.subplots(2, 4, figsize=(20, 10))
fig.suptitle('FIT-DNA 8가지 유형별 추천 운동 타입 분포', fontsize=16, fontweight='bold')

for idx, (fitdna_type, recommendations) in enumerate(all_recommendations.items()):
    ax = axes[idx // 4, idx % 4]

    type_counts = recommendations['타입'].value_counts()
    colors = {'근력': '#ff6b6b', '유연성': '#4ecdc4', '지구력': '#95e1d3'}
    ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
           colors=[colors.get(t, '#cccccc') for t in type_counts.index],
           startangle=90)
    ax.set_title(f'{fitdna_type}\n({FITDNA_TYPES[fitdna_type]["설명"]})', fontweight='bold')

plt.tight_layout()
plt.savefig('phase2_exercise_recommendation_distribution.png', dpi=150, bbox_inches='tight')
print(">> 저장 완료: phase2_exercise_recommendation_distribution.png")

# 시각화 2: 8가지 유형별 약점-강점 매핑
print("\n[시각화 2: 유형별 약점-강점 매핑]")
fig, ax = plt.subplots(figsize=(14, 8))

fitdna_list = list(FITDNA_TYPES.keys())
axes_list = ['근력', '유연성', '지구력']

# 히트맵 데이터 생성
heatmap_data = []
for fitdna_type in fitdna_list:
    row = []
    for axis in axes_list:
        level = FITDNA_TYPES[fitdna_type][axis]
        row.append(1 if level == 'high' else -1)
    heatmap_data.append(row)

heatmap_data = np.array(heatmap_data)

# 히트맵 그리기
im = ax.imshow(heatmap_data, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)

# 축 설정
ax.set_xticks(np.arange(len(axes_list)))
ax.set_yticks(np.arange(len(fitdna_list)))
ax.set_xticklabels(axes_list, fontsize=12)
ax.set_yticklabels([f"{ft}\n({FITDNA_TYPES[ft]['설명']})" for ft in fitdna_list], fontsize=10)

# 값 표시
for i in range(len(fitdna_list)):
    for j in range(len(axes_list)):
        text = '강점' if heatmap_data[i, j] == 1 else '약점'
        color = 'white' if abs(heatmap_data[i, j]) > 0.5 else 'black'
        ax.text(j, i, text, ha="center", va="center", color=color, fontsize=10, fontweight='bold')

ax.set_title('FIT-DNA 8가지 유형별 3축 강점/약점 매핑', fontsize=14, fontweight='bold', pad=20)
fig.colorbar(im, ax=ax, label='강점(+1) / 약점(-1)')
plt.tight_layout()
plt.savefig('phase2_fitdna_strength_weakness_heatmap.png', dpi=150, bbox_inches='tight')
print(">> 저장 완료: phase2_fitdna_strength_weakness_heatmap.png")

# 리포트 생성
print("\n[리포트 생성 중...]")
with open('phase2_exercise_recommendation_report.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("Phase 2-5: FIT-DNA 유형별 운동 추천 시스템 리포트\n")
    f.write("=" * 80 + "\n\n")

    f.write("1. 개요\n")
    f.write("-" * 80 + "\n")
    f.write(f"- 운동 데이터베이스: {len(exercise_db)}개 운동\n")
    f.write(f"- FIT-DNA 유형: 8가지\n")
    f.write(f"- 추천 전략: 약점 개선(60%) + 강점 유지(40%)\n\n")

    for fitdna_type, type_info in FITDNA_TYPES.items():
        f.write(f"\n{'=' * 80}\n")
        f.write(f"2-{list(FITDNA_TYPES.keys()).index(fitdna_type) + 1}. {fitdna_type} - {type_info['설명']}\n")
        f.write("=" * 80 + "\n\n")

        # 약점/강점
        weaknesses = [axis for axis, level in type_info.items() if level == 'low' and axis in ['근력', '유연성', '지구력']]
        strengths = [axis for axis, level in type_info.items() if level == 'high' and axis in ['근력', '유연성', '지구력']]

        f.write(f"약점: {', '.join(weaknesses) if weaknesses else '없음'}\n")
        f.write(f"강점: {', '.join(strengths) if strengths else '없음'}\n\n")

        # 추천 운동
        recommendations = all_recommendations[fitdna_type]
        f.write(f"추천 운동 TOP 10:\n")
        f.write("-" * 80 + "\n")
        for i, (idx, row) in enumerate(recommendations.iterrows(), 1):
            f.write(f"{i:2d}. [{row['목적']:8s}] {row['운동명']:30s} "
                   f"({row['타입']:4s}, {row['난이도']:4s}, {row['장소']:4s})\n")
        f.write("\n")

print(">> 저장 완료: phase2_exercise_recommendation_report.txt")

print("\n" + "=" * 60)
print("FIT-DNA 유형별 운동 추천 시스템 완성!")
print("=" * 60)
print("\n생성된 파일:")
print("1. phase2_exercise_recommendations_[유형].csv (8개) - 유형별 추천 운동")
print("2. phase2_exercise_recommendation_distribution.png - 유형별 추천 운동 타입 분포")
print("3. phase2_fitdna_strength_weakness_heatmap.png - 유형별 강점/약점 히트맵")
print("4. phase2_exercise_recommendation_report.txt - 상세 리포트")
