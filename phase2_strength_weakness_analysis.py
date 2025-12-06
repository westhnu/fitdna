import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("FIT-DNA Phase 2-2: 강점/약점 분석 로직 구현")
print("="*80)

# 데이터 로드
print("\n[1] 데이터 로드...")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')
print(f">> 총 {len(df):,}건 로드 완료")

# ============================================================================
# 강점/약점 판단 기준
# ============================================================================

def classify_fitness_level(z_score):
    """
    Z-Score 기준으로 체력 수준 분류

    Parameters:
    -----------
    z_score : float
        체력 지표의 Z-Score

    Returns:
    --------
    str : 수준 분류
    """
    if z_score >= 1.0:
        return "매우 우수"
    elif z_score >= 0.5:
        return "우수"
    elif z_score >= 0.0:
        return "평균 이상"
    elif z_score >= -0.5:
        return "평균 이하"
    elif z_score >= -1.0:
        return "개선 필요"
    else:
        return "적극 개선 필요"

def get_strength_weakness(strength_z, flex_z, endurance_z):
    """
    3개 축의 Z-Score를 비교하여 강점/약점 판단

    Returns:
    --------
    dict : {
        'strengths': [(축명, z-score, 수준), ...],
        'weaknesses': [(축명, z-score, 수준), ...],
        'balanced': bool
    }
    """
    axes = [
        ('근력', strength_z),
        ('유연성', flex_z),
        ('지구력', endurance_z)
    ]

    # Z-Score 기준 정렬
    sorted_axes = sorted(axes, key=lambda x: x[1], reverse=True)

    strengths = []
    weaknesses = []

    # 강점: 상위 축 중 Z-Score > 0인 것
    for axis_name, z_val in sorted_axes:
        if z_val > 0:
            level = classify_fitness_level(z_val)
            strengths.append((axis_name, z_val, level))

    # 약점: 하위 축 중 Z-Score < 0인 것
    for axis_name, z_val in reversed(sorted_axes):
        if z_val < 0:
            level = classify_fitness_level(z_val)
            weaknesses.append((axis_name, z_val, level))

    # 균형 잡힌 체력 여부 (표준편차가 작으면 균형잡힘)
    std = np.std([strength_z, flex_z, endurance_z])
    balanced = std < 0.3

    return {
        'strengths': strengths,
        'weaknesses': weaknesses,
        'balanced': balanced,
        'std': std
    }

def get_percentile_within_type(fitdna_type, strength_z, flex_z, endurance_z, df):
    """
    같은 FIT-DNA 유형 내에서의 백분위 계산

    Returns:
    --------
    dict : 각 축별 백분위 (0~100)
    """
    same_type_df = df[df['FIT_DNA'] == fitdna_type]

    strength_percentile = stats.percentileofscore(same_type_df['strength_z'].dropna(), strength_z)
    flex_percentile = stats.percentileofscore(same_type_df['flex_z'].dropna(), flex_z)
    endurance_percentile = stats.percentileofscore(same_type_df['endurance_z'].dropna(), endurance_z)

    return {
        '근력': round(strength_percentile, 1),
        '유연성': round(flex_percentile, 1),
        '지구력': round(endurance_percentile, 1)
    }

def generate_feedback_text(fitdna_type, strength_z, flex_z, endurance_z, df):
    """
    개인 맞춤 피드백 텍스트 생성

    Returns:
    --------
    str : 피드백 텍스트
    """
    analysis = get_strength_weakness(strength_z, flex_z, endurance_z)
    percentiles = get_percentile_within_type(fitdna_type, strength_z, flex_z, endurance_z, df)

    feedback = []
    feedback.append(f"[{fitdna_type} 유형 분석 결과]\n")

    # 유형 내 위치
    avg_percentile = np.mean(list(percentiles.values()))
    if avg_percentile >= 75:
        feedback.append(f"당신은 {fitdna_type} 유형 중 상위 {100-avg_percentile:.0f}%에 속합니다.")
    elif avg_percentile >= 50:
        feedback.append(f"당신은 {fitdna_type} 유형 중 평균 수준입니다.")
    else:
        feedback.append(f"당신은 {fitdna_type} 유형 중 하위 {avg_percentile:.0f}%에 속합니다.")

    # 강점
    if analysis['strengths']:
        feedback.append("\n[강점]")
        for axis_name, z_val, level in analysis['strengths']:
            percentile = percentiles[axis_name]
            feedback.append(f"  • {axis_name}: {level} (상위 {100-percentile:.0f}%, Z-Score: {z_val:+.2f})")
    else:
        feedback.append("\n[강점]")
        feedback.append("  • 현재 평균 이상인 축이 없습니다. 전반적인 체력 향상이 필요합니다.")

    # 약점
    if analysis['weaknesses']:
        feedback.append("\n[약점 및 개선 방향]")
        for i, (axis_name, z_val, level) in enumerate(analysis['weaknesses'], 1):
            percentile = percentiles[axis_name]
            feedback.append(f"  {i}. {axis_name}: {level} (하위 {percentile:.0f}%, Z-Score: {z_val:+.2f})")

            # 개선 제안
            if axis_name == '근력':
                feedback.append(f"     → 웨이트 트레이닝, 맨몸 운동 추천")
            elif axis_name == '유연성':
                feedback.append(f"     → 요가, 스트레칭, 필라테스 추천")
            elif axis_name == '지구력':
                feedback.append(f"     → 유산소 운동, 조깅, 수영 추천")
    else:
        feedback.append("\n[약점]")
        feedback.append("  • 모든 축이 평균 이상입니다. 우수한 체력을 유지하세요!")

    # 균형
    if analysis['balanced']:
        feedback.append("\n[종합 평가]")
        feedback.append("  균형 잡힌 체력을 보유하고 있습니다.")
    else:
        feedback.append("\n[종합 평가]")
        feedback.append("  특정 축에 편중된 체력입니다. 약점 보완 운동을 추천합니다.")

    return "\n".join(feedback)

# ============================================================================
# 유형별 강점/약점 통계
# ============================================================================

print("\n[2] FIT-DNA 유형별 강점/약점 통계 분석...")

type_strength_weakness = {}

for fitdna_type in df['FIT_DNA'].unique():
    type_df = df[df['FIT_DNA'] == fitdna_type]

    # 각 축의 평균 Z-Score
    avg_strength = type_df['strength_z'].mean()
    avg_flex = type_df['flex_z'].mean()
    avg_endurance = type_df['endurance_z'].mean()

    # 강점/약점 분석
    analysis = get_strength_weakness(avg_strength, avg_flex, avg_endurance)

    type_strength_weakness[fitdna_type] = {
        'avg_z': {
            '근력': avg_strength,
            '유연성': avg_flex,
            '지구력': avg_endurance
        },
        'analysis': analysis
    }

print("\n유형별 강점/약점 요약:")
for fitdna_type, data in sorted(type_strength_weakness.items()):
    print(f"\n  [{fitdna_type}]")
    print(f"    강점: {[s[0] for s in data['analysis']['strengths']]}")
    print(f"    약점: {[w[0] for w in data['analysis']['weaknesses']]}")

# ============================================================================
# 개인 예시 분석
# ============================================================================

print("\n[3] 개인별 강점/약점 분석 예시...")

# 각 유형에서 무작위 샘플 1명씩
example_users = []
for fitdna_type in df['FIT_DNA'].unique():
    type_df = df[df['FIT_DNA'] == fitdna_type]
    if len(type_df) > 0:
        sample = type_df.sample(1).iloc[0]
        example_users.append(sample)

print(f"\n>> {len(example_users)}개 유형에서 샘플 추출 완료")

# 첫 3명 피드백 생성 (파일로만 저장, 콘솔 출력 제외)
feedbacks_for_report = []
for i, user in enumerate(example_users[:3], 1):
    feedback = generate_feedback_text(
        user['FIT_DNA'],
        user['strength_z'],
        user['flex_z'],
        user['endurance_z'],
        df
    )
    feedbacks_for_report.append((i, feedback))

print(">> 개인 피드백 3건 생성 완료 (리포트에 포함)")

# ============================================================================
# 시각화
# ============================================================================

print("\n[4] 시각화 생성 중...")

fig = plt.figure(figsize=(20, 16))

# 1. 유형별 강점/약점 히트맵
ax1 = plt.subplot(3, 3, 1)
heatmap_data = []
for fitdna_type in sorted(type_strength_weakness.keys()):
    row = [
        type_strength_weakness[fitdna_type]['avg_z']['근력'],
        type_strength_weakness[fitdna_type]['avg_z']['유연성'],
        type_strength_weakness[fitdna_type]['avg_z']['지구력']
    ]
    heatmap_data.append(row)

heatmap_df = pd.DataFrame(heatmap_data,
                          index=sorted(type_strength_weakness.keys()),
                          columns=['근력', '유연성', '지구력'])

sns.heatmap(heatmap_df, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            cbar_kws={'label': 'Z-Score'}, ax=ax1, linewidths=0.5)
ax1.set_title('1. 유형별 평균 체력 지표 (강점=녹색, 약점=빨강)', fontsize=13, fontweight='bold', pad=15)
ax1.set_xlabel('')
ax1.set_ylabel('FIT-DNA 유형', fontsize=11)

# 2. Z-Score 분포 (히스토그램)
ax2 = plt.subplot(3, 3, 2)
ax2.hist([df['strength_z'].dropna(), df['flex_z'].dropna(), df['endurance_z'].dropna()],
         bins=50, label=['근력', '유연성', '지구력'], alpha=0.6, color=['#FF6B6B', '#4ECDC4', '#FFE66D'])
ax2.axvline(x=0, color='black', linestyle='--', linewidth=1, label='평균')
ax2.axvline(x=0.5, color='green', linestyle='--', linewidth=1, alpha=0.5, label='우수')
ax2.axvline(x=-0.5, color='red', linestyle='--', linewidth=1, alpha=0.5, label='개선 필요')
ax2.set_title('2. 전체 Z-Score 분포', fontsize=13, fontweight='bold', pad=15)
ax2.set_xlabel('Z-Score', fontsize=11)
ax2.set_ylabel('인원 수', fontsize=11)
ax2.legend(fontsize=9)
ax2.grid(axis='y', alpha=0.3)

# 3. 강점 개수 분포
ax3 = plt.subplot(3, 3, 3)
strength_counts = {'0개': 0, '1개': 0, '2개': 0, '3개': 0}
for fitdna_type, data in type_strength_weakness.items():
    n_strengths = len(data['analysis']['strengths'])
    strength_counts[f'{n_strengths}개'] += 1

bars = ax3.bar(strength_counts.keys(), strength_counts.values(),
               color=['#FF6B6B', '#FFA94D', '#FFE66D', '#51CF66'], alpha=0.8)
ax3.set_title('3. 유형별 강점 개수 분포', fontsize=13, fontweight='bold', pad=15)
ax3.set_xlabel('강점 축 개수', fontsize=11)
ax3.set_ylabel('유형 수', fontsize=11)
ax3.grid(axis='y', alpha=0.3)

for bar, count in zip(bars, strength_counts.values()):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'{count}개',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# 4-6. 개인 예시 레이더 차트 (3명)
for i, user_idx in enumerate([0, 1, 2]):
    ax = plt.subplot(3, 3, 4+i, projection='polar')

    if user_idx < len(example_users):
        user = example_users[user_idx]

        categories = ['근력', '유연성', '지구력']
        values = [user['strength_z'], user['flex_z'], user['endurance_z']]

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        ax.plot(angles, values, 'o-', linewidth=2, label=user['FIT_DNA'])
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(-2, 2)
        ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
        ax.axhline(y=0.5, color='green', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.axhline(y=-0.5, color='red', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_title(f'{4+i}. {user["FIT_DNA"]} 유형 예시',
                     fontsize=12, fontweight='bold', pad=15)
        ax.grid(True)

# 7. 수준별 분포 (매우 우수 ~ 적극 개선 필요)
ax7 = plt.subplot(3, 3, 7)
all_zscores = pd.concat([
    df['strength_z'].dropna(),
    df['flex_z'].dropna(),
    df['endurance_z'].dropna()
])

level_counts = {
    '매우 우수': (all_zscores >= 1.0).sum(),
    '우수': ((all_zscores >= 0.5) & (all_zscores < 1.0)).sum(),
    '평균 이상': ((all_zscores >= 0.0) & (all_zscores < 0.5)).sum(),
    '평균 이하': ((all_zscores >= -0.5) & (all_zscores < 0.0)).sum(),
    '개선 필요': ((all_zscores >= -1.0) & (all_zscores < -0.5)).sum(),
    '적극\n개선 필요': (all_zscores < -1.0).sum()
}

colors_level = ['#51CF66', '#A8E6CF', '#FFE66D', '#FFA94D', '#FF8B94', '#FF6B6B']
bars = ax7.barh(range(len(level_counts)), list(level_counts.values()),
                color=colors_level, alpha=0.8)
ax7.set_yticks(range(len(level_counts)))
ax7.set_yticklabels(level_counts.keys(), fontsize=10)
ax7.set_xlabel('건수', fontsize=11)
ax7.set_title('7. 체력 수준별 분포 (전체 축 통합)', fontsize=13, fontweight='bold', pad=15)
ax7.invert_yaxis()
ax7.grid(axis='x', alpha=0.3)

for i, (bar, count) in enumerate(zip(bars, level_counts.values())):
    width = bar.get_width()
    pct = count / len(all_zscores) * 100
    ax7.text(width + 1000, i, f'{count:,} ({pct:.1f}%)',
            va='center', fontsize=9, fontweight='bold')

# 8. 유형별 균형도 (표준편차)
ax8 = plt.subplot(3, 3, 8)
balance_data = []
for fitdna_type in sorted(type_strength_weakness.keys()):
    std = type_strength_weakness[fitdna_type]['analysis']['std']
    balance_data.append((fitdna_type, std))

balance_data.sort(key=lambda x: x[1])
types, stds = zip(*balance_data)

colors_balance = ['#51CF66' if s < 0.3 else '#FFA94D' if s < 0.5 else '#FF6B6B' for s in stds]
bars = ax8.barh(range(len(types)), stds, color=colors_balance, alpha=0.8)
ax8.set_yticks(range(len(types)))
ax8.set_yticklabels(types, fontsize=10)
ax8.set_xlabel('표준편차 (낮을수록 균형잡힘)', fontsize=11)
ax8.set_title('8. 유형별 체력 균형도', fontsize=13, fontweight='bold', pad=15)
ax8.axvline(x=0.3, color='green', linestyle='--', linewidth=1, alpha=0.5, label='균형')
ax8.axvline(x=0.5, color='red', linestyle='--', linewidth=1, alpha=0.5, label='불균형')
ax8.invert_yaxis()
ax8.legend(fontsize=9)
ax8.grid(axis='x', alpha=0.3)

# 9. 강점-약점 조합 패턴
ax9 = plt.subplot(3, 3, 9)
pattern_counts = {}
for fitdna_type, data in type_strength_weakness.items():
    n_strengths = len(data['analysis']['strengths'])
    n_weaknesses = len(data['analysis']['weaknesses'])
    pattern = f'강점{n_strengths}-약점{n_weaknesses}'
    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

patterns = list(pattern_counts.keys())
counts = list(pattern_counts.values())
bars = ax9.bar(range(len(patterns)), counts,
               color=sns.color_palette("Set2", len(patterns)), alpha=0.8)
ax9.set_xticks(range(len(patterns)))
ax9.set_xticklabels(patterns, fontsize=9, rotation=45)
ax9.set_ylabel('유형 수', fontsize=11)
ax9.set_title('9. 강점-약점 조합 패턴', fontsize=13, fontweight='bold', pad=15)
ax9.grid(axis='y', alpha=0.3)

for bar, count in zip(bars, counts):
    height = bar.get_height()
    ax9.text(bar.get_x() + bar.get_width()/2., height,
            f'{count}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout(pad=3.0)
plt.savefig('phase2_strength_weakness_analysis.png', dpi=300, bbox_inches='tight')
print(">> 시각화 저장 완료: phase2_strength_weakness_analysis.png")
plt.close()

# ============================================================================
# 리포트 저장
# ============================================================================

print("\n[5] 강점/약점 분석 리포트 저장...")

with open('phase2_strength_weakness_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write(" "*30 + "FIT-DNA 강점/약점 분석 리포트\n")
    f.write("="*100 + "\n\n")

    f.write("■ 분석 기준\n")
    f.write("-" * 100 + "\n")
    f.write("  Z-Score 기준 체력 수준 분류:\n\n")
    f.write("    Z-Score >= 1.0    : 매우 우수\n")
    f.write("    Z-Score >= 0.5    : 우수\n")
    f.write("    Z-Score >= 0.0    : 평균 이상\n")
    f.write("    Z-Score >= -0.5   : 평균 이하\n")
    f.write("    Z-Score >= -1.0   : 개선 필요\n")
    f.write("    Z-Score < -1.0    : 적극 개선 필요\n\n")

    f.write("  강점 판단: Z-Score > 0인 축\n")
    f.write("  약점 판단: Z-Score < 0인 축\n")
    f.write("  균형 판단: 3개 축의 표준편차 < 0.3\n")

    f.write("\n\n■ 유형별 강점/약점 분석\n")
    f.write("-" * 100 + "\n")

    for fitdna_type in sorted(type_strength_weakness.keys()):
        data = type_strength_weakness[fitdna_type]
        f.write(f"\n  [{fitdna_type}]\n")

        # 평균 Z-Score
        f.write(f"    평균 Z-Score:\n")
        f.write(f"      근력: {data['avg_z']['근력']:+.3f}\n")
        f.write(f"      유연성: {data['avg_z']['유연성']:+.3f}\n")
        f.write(f"      지구력: {data['avg_z']['지구력']:+.3f}\n")

        # 강점
        f.write(f"    강점: ")
        if data['analysis']['strengths']:
            strengths_str = ', '.join([f"{s[0]}({s[2]})" for s in data['analysis']['strengths']])
            f.write(strengths_str + "\n")
        else:
            f.write("없음\n")

        # 약점
        f.write(f"    약점: ")
        if data['analysis']['weaknesses']:
            weaknesses_str = ', '.join([f"{w[0]}({w[2]})" for w in data['analysis']['weaknesses']])
            f.write(weaknesses_str + "\n")
        else:
            f.write("없음\n")

        # 균형도
        f.write(f"    균형도: ")
        if data['analysis']['balanced']:
            f.write(f"균형잡힘 (표준편차 {data['analysis']['std']:.3f})\n")
        else:
            f.write(f"불균형 (표준편차 {data['analysis']['std']:.3f})\n")

    f.write("\n\n■ 개인 피드백 예시\n")
    f.write("-" * 100 + "\n")

    for i, feedback in feedbacks_for_report:
        f.write(f"\n예시 {i}:\n")
        f.write("-" * 100 + "\n")
        f.write(feedback + "\n")

    f.write("\n\n■ 서비스 활용 가이드\n")
    f.write("-" * 100 + "\n")
    f.write("  1. 사용자 FIT-DNA 및 Z-Score 입력\n")
    f.write("  2. 강점/약점 자동 분석\n")
    f.write("  3. 같은 유형 내 백분위 계산\n")
    f.write("  4. 맞춤 피드백 텍스트 생성\n")
    f.write("  5. 레이더 차트 시각화\n")
    f.write("  6. 약점 보완 운동 추천\n\n")

    f.write("  [API 함수]\n")
    f.write("    get_strength_weakness(strength_z, flex_z, endurance_z)\n")
    f.write("    get_percentile_within_type(fitdna_type, strength_z, flex_z, endurance_z, df)\n")
    f.write("    generate_feedback_text(fitdna_type, strength_z, flex_z, endurance_z, df)\n")

    f.write("\n" + "="*100 + "\n")

print(">> 리포트 저장 완료: phase2_strength_weakness_report.txt")

print("\n" + "="*80)
print("Phase 2-2 완료: 강점/약점 분석 로직")
print("="*80)
print("\n생성된 파일:")
print("  1. phase2_strength_weakness_analysis.png - 분석 시각화")
print("  2. phase2_strength_weakness_report.txt - 상세 리포트")
