import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("FIT-DNA Phase 1-3: 연령대/성별별 유형 패턴 분석")
print("="*80)

# 데이터 로드
print("\n[1] 데이터 로드...")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')
print(f">> 총 {len(df):,}건 로드 완료")

# 연령대 구분 (10대, 20대, 30대 등)
print("\n[2] 연령대별 FIT-DNA 유형 분포")
print("-" * 80)
age_type_dist = pd.crosstab(df['AGRDE_FLAG_NM'], df['FIT_DNA'], normalize='index') * 100
print(age_type_dist.round(2))

# 성별 FIT-DNA 분포
print("\n[3] 성별 FIT-DNA 유형 분포")
print("-" * 80)
gender_type_dist = pd.crosstab(df['SEXDSTN_FLAG_CD'], df['FIT_DNA'], normalize='index') * 100
print(gender_type_dist.round(2))

# 연령대 × 성별 교차 분석
print("\n[4] 연령대 × 성별 교차 분석")
print("-" * 80)

# 주요 연령대만 선택 (청소년, 성인, 노인)
age_groups_of_interest = ['청소년', '성인', '노인']
for age_group in age_groups_of_interest:
    if age_group in df['AGRDE_FLAG_NM'].values:
        print(f"\n{age_group} 그룹:")
        age_df = df[df['AGRDE_FLAG_NM'] == age_group]
        age_gender_type = pd.crosstab(age_df['SEXDSTN_FLAG_CD'], age_df['FIT_DNA'])
        print(age_gender_type)

# 연령대별 평균 체력 지표 변화
print("\n[5] 연령대별 평균 체력 지표 변화")
print("-" * 80)
age_stats = df.groupby('AGRDE_FLAG_NM')[['strength_z', 'flex_z', 'endurance_z']].mean().round(3)
print(age_stats)

# 성별 평균 체력 지표
print("\n[6] 성별 평균 체력 지표")
print("-" * 80)
gender_stats = df.groupby('SEXDSTN_FLAG_CD')[['strength_z', 'flex_z', 'endurance_z']].mean().round(3)
print(gender_stats)

# 시각화
print("\n[7] 시각화 생성 중...")
print("-" * 80)

fig = plt.figure(figsize=(20, 14))

# 1. 연령대별 FIT-DNA 분포 (스택 바 차트)
ax1 = plt.subplot(3, 3, 1)
age_type_count = pd.crosstab(df['AGRDE_FLAG_NM'], df['FIT_DNA'])
age_type_count.plot(kind='bar', stacked=True, ax=ax1, colormap='Set3')
ax1.set_title('1. 연령대별 FIT-DNA 유형 분포', fontsize=13, fontweight='bold', pad=15)
ax1.set_xlabel('연령대', fontsize=11)
ax1.set_ylabel('인원 수', fontsize=11)
ax1.legend(title='FIT-DNA', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax1.tick_params(axis='x', rotation=45)

# 2. 성별 FIT-DNA 분포 (스택 바 차트)
ax2 = plt.subplot(3, 3, 2)
gender_type_count = pd.crosstab(df['SEXDSTN_FLAG_CD'], df['FIT_DNA'])
gender_type_count.plot(kind='bar', stacked=True, ax=ax2, colormap='Set3')
ax2.set_title('2. 성별 FIT-DNA 유형 분포', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('성별', fontsize=11)
ax2.set_ylabel('인원 수', fontsize=11)
ax2.legend(title='FIT-DNA', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax2.tick_params(axis='x', rotation=0)

# 3. 연령대별 FIT-DNA 비율 (히트맵)
ax3 = plt.subplot(3, 3, 3)
sns.heatmap(age_type_dist, annot=True, fmt='.1f', cmap='YlOrRd',
            cbar_kws={'label': '비율(%)'}, ax=ax3, linewidths=0.5)
ax3.set_title('3. 연령대별 FIT-DNA 비율(%)', fontsize=13, fontweight='bold', pad=15)
ax3.set_xlabel('FIT-DNA 유형', fontsize=11)
ax3.set_ylabel('연령대', fontsize=11)

# 4. 연령대별 근력 변화
ax4 = plt.subplot(3, 3, 4)
age_order = sorted(df['AGRDE_FLAG_NM'].unique())
sns.boxplot(data=df, x='AGRDE_FLAG_NM', y='strength_z', order=age_order,
            palette='Blues', ax=ax4)
ax4.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax4.set_title('4. 연령대별 근력 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax4.set_xlabel('연령대', fontsize=11)
ax4.set_ylabel('근력 Z-Score', fontsize=11)
ax4.tick_params(axis='x', rotation=45)

# 5. 연령대별 유연성 변화
ax5 = plt.subplot(3, 3, 5)
sns.boxplot(data=df, x='AGRDE_FLAG_NM', y='flex_z', order=age_order,
            palette='Greens', ax=ax5)
ax5.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax5.set_title('5. 연령대별 유연성 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax5.set_xlabel('연령대', fontsize=11)
ax5.set_ylabel('유연성 Z-Score', fontsize=11)
ax5.tick_params(axis='x', rotation=45)

# 6. 연령대별 지구력 변화
ax6 = plt.subplot(3, 3, 6)
sns.boxplot(data=df, x='AGRDE_FLAG_NM', y='endurance_z', order=age_order,
            palette='Oranges', ax=ax6)
ax6.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax6.set_title('6. 연령대별 지구력 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax6.set_xlabel('연령대', fontsize=11)
ax6.set_ylabel('지구력 Z-Score', fontsize=11)
ax6.tick_params(axis='x', rotation=45)

# 7. 성별 근력 비교
ax7 = plt.subplot(3, 3, 7)
sns.violinplot(data=df, x='SEXDSTN_FLAG_CD', y='strength_z', palette='Set2', ax=ax7)
ax7.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax7.set_title('7. 성별 근력 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax7.set_xlabel('성별', fontsize=11)
ax7.set_ylabel('근력 Z-Score', fontsize=11)

# 8. 성별 유연성 비교
ax8 = plt.subplot(3, 3, 8)
sns.violinplot(data=df, x='SEXDSTN_FLAG_CD', y='flex_z', palette='Set2', ax=ax8)
ax8.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax8.set_title('8. 성별 유연성 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax8.set_xlabel('성별', fontsize=11)
ax8.set_ylabel('유연성 Z-Score', fontsize=11)

# 9. 성별 지구력 비교
ax9 = plt.subplot(3, 3, 9)
sns.violinplot(data=df, x='SEXDSTN_FLAG_CD', y='endurance_z', palette='Set2', ax=ax9)
ax9.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax9.set_title('9. 성별 지구력 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax9.set_xlabel('성별', fontsize=11)
ax9.set_ylabel('지구력 Z-Score', fontsize=11)

plt.tight_layout(pad=3.0)
plt.savefig('phase1_demographic_analysis.png', dpi=300, bbox_inches='tight')
print(">> 시각화 저장 완료: phase1_demographic_analysis.png")
plt.close()

# 추가 시각화: 연령대 × 성별 × FIT-DNA
print("\n[8] 상세 연령-성별-유형 분석 시각화...")
print("-" * 80)

fig, axes = plt.subplots(2, 1, figsize=(18, 12))

# 남성 연령대별 FIT-DNA 분포
ax_m = axes[0]
male_df = df[df['SEXDSTN_FLAG_CD'] == 'M']
male_age_type = pd.crosstab(male_df['AGRDE_FLAG_NM'], male_df['FIT_DNA'], normalize='index') * 100
male_age_type.plot(kind='bar', ax=ax_m, colormap='Set3')
ax_m.set_title('남성 연령대별 FIT-DNA 유형 비율', fontsize=14, fontweight='bold', pad=15)
ax_m.set_xlabel('연령대', fontsize=12)
ax_m.set_ylabel('비율(%)', fontsize=12)
ax_m.legend(title='FIT-DNA', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax_m.tick_params(axis='x', rotation=45)
ax_m.grid(axis='y', alpha=0.3)

# 여성 연령대별 FIT-DNA 분포
ax_f = axes[1]
female_df = df[df['SEXDSTN_FLAG_CD'] == 'F']
female_age_type = pd.crosstab(female_df['AGRDE_FLAG_NM'], female_df['FIT_DNA'], normalize='index') * 100
female_age_type.plot(kind='bar', ax=ax_f, colormap='Set3')
ax_f.set_title('여성 연령대별 FIT-DNA 유형 비율', fontsize=14, fontweight='bold', pad=15)
ax_f.set_xlabel('연령대', fontsize=12)
ax_f.set_ylabel('비율(%)', fontsize=12)
ax_f.legend(title='FIT-DNA', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax_f.tick_params(axis='x', rotation=45)
ax_f.grid(axis='y', alpha=0.3)

plt.tight_layout(pad=3.0)
plt.savefig('phase1_gender_age_fitdna_detail.png', dpi=300, bbox_inches='tight')
print(">> 상세 분석 저장 완료: phase1_gender_age_fitdna_detail.png")
plt.close()

# 분석 결과 저장
print("\n[9] 분석 결과 리포트 저장...")
print("-" * 80)

with open('phase1_demographic_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("FIT-DNA 연령대/성별 패턴 분석 보고서\n")
    f.write("="*80 + "\n\n")

    f.write("■ 연령대별 FIT-DNA 유형 비율(%)\n")
    f.write("-" * 80 + "\n")
    f.write(age_type_dist.round(2).to_string())

    f.write("\n\n■ 성별 FIT-DNA 유형 비율(%)\n")
    f.write("-" * 80 + "\n")
    f.write(gender_type_dist.round(2).to_string())

    f.write("\n\n■ 연령대별 평균 체력 지표\n")
    f.write("-" * 80 + "\n")
    f.write(age_stats.to_string())

    f.write("\n\n■ 성별 평균 체력 지표\n")
    f.write("-" * 80 + "\n")
    f.write(gender_stats.to_string())

    f.write("\n\n■ 남성 연령대별 FIT-DNA 비율(%)\n")
    f.write("-" * 80 + "\n")
    f.write(male_age_type.round(2).to_string())

    f.write("\n\n■ 여성 연령대별 FIT-DNA 비율(%)\n")
    f.write("-" * 80 + "\n")
    f.write(female_age_type.round(2).to_string())

    # 주요 인사이트
    f.write("\n\n■ 주요 인사이트\n")
    f.write("-" * 80 + "\n")

    # 연령대별 가장 많은 유형
    f.write("\n[연령대별 주요 유형]\n")
    for age_group in age_type_dist.index:
        top_type = age_type_dist.loc[age_group].idxmax()
        top_pct = age_type_dist.loc[age_group].max()
        f.write(f"{age_group}: {top_type} ({top_pct:.1f}%)\n")

    # 성별 주요 유형
    f.write("\n[성별 주요 유형]\n")
    for gender in gender_type_dist.index:
        top_type = gender_type_dist.loc[gender].idxmax()
        top_pct = gender_type_dist.loc[gender].max()
        gender_name = '남성' if gender == 'M' else '여성'
        f.write(f"{gender_name}: {top_type} ({top_pct:.1f}%)\n")

    # 체력 지표 트렌드
    f.write("\n[연령대별 체력 트렌드]\n")
    f.write(f"근력 최고 연령대: {age_stats['strength_z'].idxmax()} ({age_stats['strength_z'].max():.3f})\n")
    f.write(f"근력 최저 연령대: {age_stats['strength_z'].idxmin()} ({age_stats['strength_z'].min():.3f})\n")
    f.write(f"유연성 최고 연령대: {age_stats['flex_z'].idxmax()} ({age_stats['flex_z'].max():.3f})\n")
    f.write(f"유연성 최저 연령대: {age_stats['flex_z'].idxmin()} ({age_stats['flex_z'].min():.3f})\n")
    f.write(f"지구력 최고 연령대: {age_stats['endurance_z'].idxmax()} ({age_stats['endurance_z'].max():.3f})\n")
    f.write(f"지구력 최저 연령대: {age_stats['endurance_z'].idxmin()} ({age_stats['endurance_z'].min():.3f})\n")

print(">> 리포트 저장 완료: phase1_demographic_analysis_report.txt")

print("\n" + "="*80)
print("Phase 1-3 완료: 연령대/성별 패턴 분석 완료")
print("="*80)
print("\n생성된 파일:")
print("  1. phase1_demographic_analysis.png (연령대/성별 분석)")
print("  2. phase1_gender_age_fitdna_detail.png (성별 × 연령대 상세)")
print("  3. phase1_demographic_analysis_report.txt (상세 리포트)")
