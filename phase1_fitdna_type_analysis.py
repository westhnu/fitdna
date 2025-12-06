import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("FIT-DNA Phase 1-2: 8가지 유형별 분포 및 특성 분석")
print("="*80)

# 데이터 로드
print("\n[1] 데이터 로드...")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')
print(f">> 총 {len(df):,}건 로드 완료")

# FIT-DNA 유형 분포 확인
print("\n[2] FIT-DNA 8가지 유형 분포")
print("-" * 80)
fitdna_dist = df['FIT_DNA'].value_counts().sort_index()
print(fitdna_dist)
print(f"\n총 유형 개수: {len(fitdna_dist)}개")

# 비율 계산
fitdna_pct = (fitdna_dist / len(df) * 100).round(2)
print("\n유형별 비율:")
for type_name, pct in fitdna_pct.items():
    print(f"  {type_name}: {pct}%")

# 유형별 평균 z-score 계산
print("\n[3] FIT-DNA 유형별 평균 체력 지표 (Z-Score)")
print("-" * 80)
type_stats = df.groupby('FIT_DNA')[['strength_z', 'flex_z', 'endurance_z']].mean().round(3)
print(type_stats)

# 유형별 표준편차
print("\n[4] FIT-DNA 유형별 체력 지표 표준편차")
print("-" * 80)
type_std = df.groupby('FIT_DNA')[['strength_z', 'flex_z', 'endurance_z']].std().round(3)
print(type_std)

# 유형별 인구 통계
print("\n[5] FIT-DNA 유형별 기본 정보")
print("-" * 80)
type_demo = df.groupby('FIT_DNA').agg({
    'MESURE_AGE_CO': ['mean', 'median', 'std'],
    'SEXDSTN_FLAG_CD': lambda x: (x == 'M').sum() / len(x) * 100  # 남성 비율
}).round(2)
type_demo.columns = ['평균연령', '중앙연령', '연령표준편차', '남성비율(%)']
print(type_demo)

# 유형 간 유사도 행렬 생성 (z-score 평균 기준)
print("\n[6] FIT-DNA 유형 간 유사도 분석 (유클리드 거리)")
print("-" * 80)

# 각 유형의 대표 벡터 (평균 z-score)
type_vectors = type_stats.values
type_names = type_stats.index.tolist()

# 유클리드 거리 계산
distance_matrix = squareform(pdist(type_vectors, metric='euclidean'))
distance_df = pd.DataFrame(distance_matrix, index=type_names, columns=type_names).round(3)
print(distance_df)

# 가장 유사한 유형 쌍 찾기
print("\n[7] 가장 유사한 FIT-DNA 유형 Top 5")
print("-" * 80)
# 대각선 제외하고 거리 추출
similar_pairs = []
for i in range(len(type_names)):
    for j in range(i+1, len(type_names)):
        similar_pairs.append((type_names[i], type_names[j], distance_matrix[i, j]))

similar_pairs.sort(key=lambda x: x[2])
for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
    print(f"{rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}")

# 가장 다른 유형 쌍
print("\n[8] 가장 다른 FIT-DNA 유형 Top 5")
print("-" * 80)
similar_pairs.sort(key=lambda x: x[2], reverse=True)
for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
    print(f"{rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}")

# 시각화 시작
print("\n[9] 시각화 생성 중...")
print("-" * 80)

fig = plt.figure(figsize=(20, 12))

# 1. FIT-DNA 유형 분포 (파이차트)
ax1 = plt.subplot(2, 3, 1)
colors = sns.color_palette("Set3", len(fitdna_dist))
wedges, texts, autotexts = ax1.pie(fitdna_dist.values, labels=fitdna_dist.index,
                                     autopct='%1.1f%%', startangle=90, colors=colors)
ax1.set_title('1. FIT-DNA 유형 분포', fontsize=14, fontweight='bold', pad=15)
for text in texts:
    text.set_fontsize(10)
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')

# 2. 유형별 평균 Z-Score 히트맵
ax2 = plt.subplot(2, 3, 2)
sns.heatmap(type_stats, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Z-Score'}, ax=ax2, linewidths=0.5)
ax2.set_title('2. 유형별 평균 체력 지표 (Z-Score)', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('')
ax2.set_ylabel('FIT-DNA 유형', fontsize=11)

# 3. 유형 간 유사도 히트맵
ax3 = plt.subplot(2, 3, 3)
sns.heatmap(distance_df, annot=True, fmt='.2f', cmap='YlOrRd',
            cbar_kws={'label': '유클리드 거리'}, ax=ax3, linewidths=0.5)
ax3.set_title('3. FIT-DNA 유형 간 거리 (낮을수록 유사)', fontsize=14, fontweight='bold', pad=15)
ax3.set_xlabel('')
ax3.set_ylabel('')

# 4. 유형별 근력 분포 (바이올린 플롯)
ax4 = plt.subplot(2, 3, 4)
order = sorted(df['FIT_DNA'].unique())
sns.violinplot(data=df, x='FIT_DNA', y='strength_z', order=order, palette='Set2', ax=ax4)
ax4.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax4.set_title('4. 유형별 근력 Z-Score 분포', fontsize=14, fontweight='bold', pad=15)
ax4.set_xlabel('FIT-DNA 유형', fontsize=11)
ax4.set_ylabel('근력 Z-Score', fontsize=11)
ax4.tick_params(axis='x', rotation=45)

# 5. 유형별 유연성 분포
ax5 = plt.subplot(2, 3, 5)
sns.violinplot(data=df, x='FIT_DNA', y='flex_z', order=order, palette='Set2', ax=ax5)
ax5.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax5.set_title('5. 유형별 유연성 Z-Score 분포', fontsize=14, fontweight='bold', pad=15)
ax5.set_xlabel('FIT-DNA 유형', fontsize=11)
ax5.set_ylabel('유연성 Z-Score', fontsize=11)
ax5.tick_params(axis='x', rotation=45)

# 6. 유형별 지구력 분포
ax6 = plt.subplot(2, 3, 6)
sns.violinplot(data=df, x='FIT_DNA', y='endurance_z', order=order, palette='Set2', ax=ax6)
ax6.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax6.set_title('6. 유형별 지구력 Z-Score 분포', fontsize=14, fontweight='bold', pad=15)
ax6.set_xlabel('FIT-DNA 유형', fontsize=11)
ax6.set_ylabel('지구력 Z-Score', fontsize=11)
ax6.tick_params(axis='x', rotation=45)

plt.tight_layout(pad=3.0)
plt.savefig('phase1_fitdna_type_distribution.png', dpi=300, bbox_inches='tight')
print(">> 시각화 저장 완료: phase1_fitdna_type_distribution.png")
plt.close()

# 레이더 차트 생성 (각 유형별 특성)
print("\n[10] 유형별 레이더 차트 생성 중...")
print("-" * 80)

fig, axes = plt.subplots(2, 4, figsize=(20, 10), subplot_kw=dict(projection='polar'))
axes = axes.flatten()

categories = ['근력', '유연성', '지구력']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]

for idx, (type_name, ax) in enumerate(zip(order, axes)):
    if type_name in type_stats.index:
        values = type_stats.loc[type_name].values.tolist()
        values += values[:1]

        ax.plot(angles, values, 'o-', linewidth=2, label=type_name)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(f'{type_name} 유형\n(n={fitdna_dist[type_name]:,})',
                     fontsize=12, fontweight='bold', pad=15)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.grid(True)

plt.tight_layout(pad=3.0)
plt.savefig('phase1_fitdna_radar_charts.png', dpi=300, bbox_inches='tight')
print(">> 레이더 차트 저장 완료: phase1_fitdna_radar_charts.png")
plt.close()

# 분석 결과 저장
print("\n[11] 분석 결과 리포트 저장 중...")
print("-" * 80)

with open('phase1_fitdna_type_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("FIT-DNA 유형별 특성 분석 보고서\n")
    f.write("="*80 + "\n\n")

    f.write(f"분석 대상: {len(df):,}건\n")
    f.write(f"FIT-DNA 유형 수: {len(fitdna_dist)}개\n\n")

    f.write("■ 유형별 분포\n")
    f.write("-" * 80 + "\n")
    for type_name, count in fitdna_dist.items():
        pct = count / len(df) * 100
        f.write(f"{type_name}: {count:,}건 ({pct:.2f}%)\n")

    f.write("\n■ 유형별 평균 체력 지표 (Z-Score)\n")
    f.write("-" * 80 + "\n")
    f.write(type_stats.to_string())

    f.write("\n\n■ 유형별 인구통계 정보\n")
    f.write("-" * 80 + "\n")
    f.write(type_demo.to_string())

    f.write("\n\n■ 가장 유사한 유형 Top 5\n")
    f.write("-" * 80 + "\n")
    similar_pairs.sort(key=lambda x: x[2])
    for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
        f.write(f"{rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}\n")

    f.write("\n■ 가장 다른 유형 Top 5\n")
    f.write("-" * 80 + "\n")
    similar_pairs.sort(key=lambda x: x[2], reverse=True)
    for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
        f.write(f"{rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}\n")

    f.write("\n■ 주요 인사이트\n")
    f.write("-" * 80 + "\n")

    # 가장 많은 유형
    most_common = fitdna_dist.idxmax()
    most_common_pct = (fitdna_dist.max() / len(df) * 100)
    f.write(f"1. 가장 많은 유형: {most_common} ({most_common_pct:.2f}%)\n")

    # 가장 적은 유형
    least_common = fitdna_dist.idxmin()
    least_common_pct = (fitdna_dist.min() / len(df) * 100)
    f.write(f"2. 가장 적은 유형: {least_common} ({least_common_pct:.2f}%)\n")

    # 남성 비율이 가장 높은 유형
    max_male_type = type_demo['남성비율(%)'].idxmax()
    max_male_pct = type_demo.loc[max_male_type, '남성비율(%)']
    f.write(f"3. 남성 비율 최고 유형: {max_male_type} ({max_male_pct:.1f}%)\n")

    # 평균 연령이 가장 높은 유형
    max_age_type = type_demo['평균연령'].idxmax()
    max_age = type_demo.loc[max_age_type, '평균연령']
    f.write(f"4. 평균 연령 최고 유형: {max_age_type} ({max_age:.1f}세)\n")

print(">> 리포트 저장 완료: phase1_fitdna_type_analysis_report.txt")

print("\n" + "="*80)
print("Phase 1-2 완료: FIT-DNA 유형별 분석 완료")
print("="*80)
print("\n생성된 파일:")
print("  1. phase1_fitdna_type_distribution.png (유형 분포 및 특성)")
print("  2. phase1_fitdna_radar_charts.png (유형별 레이더 차트)")
print("  3. phase1_fitdna_type_analysis_report.txt (상세 분석 리포트)")
