import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import euclidean, cosine, cityblock
from scipy.cluster.hierarchy import dendrogram, linkage
import networkx as nx
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*80)
print("FIT-DNA Phase 2-1: 운동 메이트 매칭 알고리즘 설계")
print("="*80)

# 데이터 로드
print("\n[1] 데이터 로드...")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')
print(f">> 총 {len(df):,}건 로드 완료")

# 유형별 대표 벡터 계산 (평균 Z-Score)
print("\n[2] FIT-DNA 유형별 대표 벡터 계산...")
type_vectors = df.groupby('FIT_DNA')[['strength_z', 'flex_z', 'endurance_z']].mean()
print(type_vectors)

# ============================================================================
# 유사도 계산 함수들
# ============================================================================

def calculate_euclidean_distance(vec1, vec2):
    """유클리드 거리 계산 (낮을수록 유사)"""
    return euclidean(vec1, vec2)

def calculate_cosine_similarity(vec1, vec2):
    """코사인 유사도 계산 (높을수록 유사, 0~1)"""
    # cosine은 거리를 반환하므로 1에서 빼서 유사도로 변환
    return 1 - cosine(vec1, vec2)

def calculate_manhattan_distance(vec1, vec2):
    """맨하탄 거리 계산 (낮을수록 유사)"""
    return cityblock(vec1, vec2)

def get_similarity_level(euclidean_dist):
    """
    유클리드 거리 기준으로 유사도 레벨 분류
    - 레벨 1 (매우 유사): 거리 < 1.2
    - 레벨 2 (유사): 거리 1.2 ~ 2.0
    - 레벨 3 (다름): 거리 > 2.0
    """
    if euclidean_dist < 1.2:
        return "레벨 1 (매우 유사)"
    elif euclidean_dist < 2.0:
        return "레벨 2 (유사)"
    else:
        return "레벨 3 (다름)"

# ============================================================================
# 유형 간 유사도 행렬 생성
# ============================================================================

print("\n[3] 유형 간 유사도 행렬 생성...")

type_names = type_vectors.index.tolist()
n_types = len(type_names)

# 유클리드 거리 행렬
euclidean_matrix = np.zeros((n_types, n_types))
for i, type1 in enumerate(type_names):
    for j, type2 in enumerate(type_names):
        vec1 = type_vectors.loc[type1].values
        vec2 = type_vectors.loc[type2].values
        euclidean_matrix[i, j] = calculate_euclidean_distance(vec1, vec2)

euclidean_df = pd.DataFrame(euclidean_matrix, index=type_names, columns=type_names)
print("\n[유클리드 거리 행렬]")
print(euclidean_df.round(3))

# 코사인 유사도 행렬
cosine_matrix = np.zeros((n_types, n_types))
for i, type1 in enumerate(type_names):
    for j, type2 in enumerate(type_names):
        vec1 = type_vectors.loc[type1].values
        vec2 = type_vectors.loc[type2].values
        cosine_matrix[i, j] = calculate_cosine_similarity(vec1, vec2)

cosine_df = pd.DataFrame(cosine_matrix, index=type_names, columns=type_names)
print("\n[코사인 유사도 행렬]")
print(cosine_df.round(3))

# CSV로 저장
euclidean_df.to_csv('matching_euclidean_distance_matrix.csv', encoding='utf-8-sig')
cosine_df.to_csv('matching_cosine_similarity_matrix.csv', encoding='utf-8-sig')
print("\n>> 유사도 행렬 CSV 저장 완료")

# ============================================================================
# 매칭 추천 함수
# ============================================================================

def recommend_matches(user_fitdna, top_n=3, similarity_level='all'):
    """
    주어진 FIT-DNA 유형에 대해 유사한 유형을 추천

    Parameters:
    -----------
    user_fitdna : str
        사용자의 FIT-DNA 유형 (예: 'PFE')
    top_n : int
        추천할 유형 개수
    similarity_level : str
        'level1' (매우 유사만), 'level2' (유사까지), 'all' (전체)

    Returns:
    --------
    list : 추천 유형 리스트 [(유형, 거리, 레벨), ...]
    """
    if user_fitdna not in type_names:
        return []

    # 해당 유형의 거리 가져오기
    distances = euclidean_df.loc[user_fitdna].copy()

    # 자기 자신 제외
    distances = distances[distances.index != user_fitdna]

    # 정렬
    distances = distances.sort_values()

    # 유사도 레벨 필터링
    if similarity_level == 'level1':
        distances = distances[distances < 1.2]
    elif similarity_level == 'level2':
        distances = distances[distances < 2.0]

    # 상위 N개 추출
    recommendations = []
    for type_name, dist in distances.head(top_n).items():
        level = get_similarity_level(dist)
        recommendations.append((type_name, dist, level))

    return recommendations

# ============================================================================
# 개인 간 매칭 점수 계산 함수
# ============================================================================

def calculate_matching_score(user1_zscore, user2_zscore,
                              user1_fitdna, user2_fitdna,
                              exercise_match=True):
    """
    두 사용자 간 매칭 점수 계산

    Parameters:
    -----------
    user1_zscore : array-like
        사용자1의 [strength_z, flex_z, endurance_z]
    user2_zscore : array-like
        사용자2의 [strength_z, flex_z, endurance_z]
    user1_fitdna : str
        사용자1의 FIT-DNA 유형
    user2_fitdna : str
        사용자2의 FIT-DNA 유형
    exercise_match : bool
        운동 선호도가 일치하는지 (추가 가중치)

    Returns:
    --------
    float : 매칭 점수 (0~100)
    """
    # 1. Z-Score 유사도 (유클리드 거리 → 점수 변환)
    zscore_distance = euclidean(user1_zscore, user2_zscore)
    # 거리 0~3을 점수 100~0으로 변환
    zscore_score = max(0, 100 - (zscore_distance / 3.0 * 100))

    # 2. FIT-DNA 유형 유사도
    fitdna_distance = euclidean_df.loc[user1_fitdna, user2_fitdna]
    fitdna_score = max(0, 100 - (fitdna_distance / 3.0 * 100))

    # 3. 가중 평균 (Z-Score 60%, FIT-DNA 40%)
    base_score = zscore_score * 0.6 + fitdna_score * 0.4

    # 4. 운동 선호도 보너스
    if exercise_match:
        base_score = min(100, base_score * 1.1)  # 10% 보너스

    return round(base_score, 2)

# ============================================================================
# 매칭 예시 생성
# ============================================================================

print("\n[4] 유형별 매칭 추천 예시")
print("-" * 80)

for fitdna_type in type_names:
    print(f"\n[{fitdna_type} 유형 사용자를 위한 추천]")
    recommendations = recommend_matches(fitdna_type, top_n=3, similarity_level='all')

    if recommendations:
        for i, (rec_type, dist, level) in enumerate(recommendations, 1):
            print(f"  {i}. {rec_type} - 거리: {dist:.3f} ({level})")
    else:
        print("  추천 없음")

# ============================================================================
# 시각화
# ============================================================================

print("\n[5] 시각화 생성 중...")

fig = plt.figure(figsize=(20, 12))

# 1. 유클리드 거리 히트맵
ax1 = plt.subplot(2, 3, 1)
sns.heatmap(euclidean_df, annot=True, fmt='.2f', cmap='YlOrRd',
            cbar_kws={'label': '유클리드 거리'}, ax=ax1, linewidths=0.5)
ax1.set_title('1. FIT-DNA 유형 간 유클리드 거리', fontsize=14, fontweight='bold', pad=15)
ax1.set_xlabel('')
ax1.set_ylabel('')

# 2. 코사인 유사도 히트맵
ax2 = plt.subplot(2, 3, 2)
sns.heatmap(cosine_df, annot=True, fmt='.2f', cmap='RdYlGn',
            cbar_kws={'label': '코사인 유사도'}, ax=ax2, linewidths=0.5)
ax2.set_title('2. FIT-DNA 유형 간 코사인 유사도', fontsize=14, fontweight='bold', pad=15)
ax2.set_xlabel('')
ax2.set_ylabel('')

# 3. 네트워크 그래프 (유사도 레벨 1만)
ax3 = plt.subplot(2, 3, 3)
G = nx.Graph()

# 노드 추가
for type_name in type_names:
    G.add_node(type_name)

# 레벨 1 (매우 유사) 엣지만 추가
for i, type1 in enumerate(type_names):
    for j, type2 in enumerate(type_names):
        if i < j:  # 중복 방지
            dist = euclidean_df.loc[type1, type2]
            if dist < 1.2:  # 레벨 1
                G.add_edge(type1, type2, weight=dist)

# 그래프 그리기
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800, ax=ax3)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax3)
nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray', ax=ax3)
ax3.set_title('3. 매칭 네트워크 (레벨 1: 매우 유사)', fontsize=14, fontweight='bold', pad=15)
ax3.axis('off')

# 4. 계층적 클러스터링 덴드로그램
ax4 = plt.subplot(2, 3, 4)
linkage_matrix = linkage(euclidean_matrix, method='ward')
dendrogram(linkage_matrix, labels=type_names, ax=ax4)
ax4.set_title('4. 계층적 클러스터링 (유사 유형 그룹화)', fontsize=14, fontweight='bold', pad=15)
ax4.set_xlabel('FIT-DNA 유형', fontsize=11)
ax4.set_ylabel('거리', fontsize=11)

# 5. 유사도 레벨별 비율
ax5 = plt.subplot(2, 3, 5)
level_counts = {'레벨 1\n(매우 유사)': 0, '레벨 2\n(유사)': 0, '레벨 3\n(다름)': 0}

for i, type1 in enumerate(type_names):
    for j, type2 in enumerate(type_names):
        if i < j:
            dist = euclidean_df.loc[type1, type2]
            level = get_similarity_level(dist)
            if '레벨 1' in level:
                level_counts['레벨 1\n(매우 유사)'] += 1
            elif '레벨 2' in level:
                level_counts['레벨 2\n(유사)'] += 1
            else:
                level_counts['레벨 3\n(다름)'] += 1

colors = ['#51CF66', '#FFA94D', '#FF6B6B']
bars = ax5.bar(level_counts.keys(), level_counts.values(), color=colors, alpha=0.8)
ax5.set_title('5. 유형 쌍의 유사도 레벨 분포', fontsize=14, fontweight='bold', pad=15)
ax5.set_ylabel('쌍의 개수', fontsize=11)
ax5.grid(axis='y', alpha=0.3)

for bar, count in zip(bars, level_counts.values()):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(count)}쌍',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# 6. 매칭 점수 예시 (PFE 유형 기준)
ax6 = plt.subplot(2, 3, 6)
example_user = type_vectors.loc['PFE'].values
matching_scores = []

for type_name in type_names:
    if type_name != 'PFE':
        target_user = type_vectors.loc[type_name].values
        score = calculate_matching_score(example_user, target_user, 'PFE', type_name, exercise_match=True)
        matching_scores.append((type_name, score))

matching_scores.sort(key=lambda x: x[1], reverse=True)
types, scores = zip(*matching_scores)

colors_score = ['#51CF66' if s >= 70 else '#FFA94D' if s >= 50 else '#FF6B6B' for s in scores]
bars = ax6.barh(range(len(types)), scores, color=colors_score, alpha=0.8)
ax6.set_yticks(range(len(types)))
ax6.set_yticklabels(types, fontsize=10)
ax6.set_xlabel('매칭 점수 (0~100)', fontsize=11)
ax6.set_title('6. PFE 유형과의 매칭 점수 (예시)', fontsize=14, fontweight='bold', pad=15)
ax6.invert_yaxis()
ax6.grid(axis='x', alpha=0.3)

for i, (bar, score) in enumerate(zip(bars, scores)):
    width = bar.get_width()
    ax6.text(width + 2, i, f'{score:.1f}',
            va='center', fontsize=9, fontweight='bold')

plt.tight_layout(pad=3.0)
plt.savefig('phase2_matching_algorithm_analysis.png', dpi=300, bbox_inches='tight')
print(">> 시각화 저장 완료: phase2_matching_algorithm_analysis.png")
plt.close()

# ============================================================================
# 리포트 저장
# ============================================================================

print("\n[6] 매칭 알고리즘 리포트 저장...")

with open('phase2_matching_algorithm_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write(" "*30 + "FIT-DNA 매칭 알고리즘 리포트\n")
    f.write("="*100 + "\n\n")

    f.write("■ 알고리즘 개요\n")
    f.write("-" * 100 + "\n")
    f.write("  FIT-DNA 유형 간 유사도를 계산하여 운동 메이트를 추천하는 알고리즘\n\n")

    f.write("  [사용 지표]\n")
    f.write("    1. 유클리드 거리: 3차원 공간(근력/유연성/지구력)에서의 직선 거리\n")
    f.write("    2. 코사인 유사도: 벡터 방향의 유사성\n")
    f.write("    3. 맨하탄 거리: 축별 차이의 합\n\n")

    f.write("  [유사도 레벨 기준] (유클리드 거리)\n")
    f.write("    • 레벨 1 (매우 유사): 거리 < 1.2\n")
    f.write("    • 레벨 2 (유사): 거리 1.2 ~ 2.0\n")
    f.write("    • 레벨 3 (다름): 거리 > 2.0\n\n")

    f.write("\n■ 유형 간 유사도 분석\n")
    f.write("-" * 100 + "\n")

    # 레벨별 통계
    f.write(f"\n  [유사도 레벨 분포]\n")
    f.write(f"    • 레벨 1 (매우 유사): {level_counts['레벨 1\n(매우 유사)']}쌍\n")
    f.write(f"    • 레벨 2 (유사): {level_counts['레벨 2\n(유사)']}쌍\n")
    f.write(f"    • 레벨 3 (다름): {level_counts['레벨 3\n(다름)']}쌍\n")

    f.write("\n  [유형별 최고 매칭 (Top 3)]\n")
    for fitdna_type in type_names:
        f.write(f"\n    [{fitdna_type}]\n")
        recommendations = recommend_matches(fitdna_type, top_n=3)
        for i, (rec_type, dist, level) in enumerate(recommendations, 1):
            f.write(f"      {i}. {rec_type}: 거리 {dist:.3f} ({level})\n")

    f.write("\n\n■ 매칭 점수 계산 로직\n")
    f.write("-" * 100 + "\n")
    f.write("  두 사용자 간 매칭 점수 = 다음 요소의 가중 평균\n\n")
    f.write("    1. Z-Score 유사도 (60%)\n")
    f.write("       - 개인별 체력 Z-Score 간 유클리드 거리\n")
    f.write("       - 거리 0~3을 점수 100~0으로 변환\n\n")
    f.write("    2. FIT-DNA 유형 유사도 (40%)\n")
    f.write("       - 유형 대표 벡터 간 유클리드 거리\n\n")
    f.write("    3. 운동 선호도 보너스 (+10%)\n")
    f.write("       - 선호 운동 종목이 일치할 경우\n\n")
    f.write("    최종 점수: 0~100점\n")
    f.write("      • 70점 이상: 높은 매칭도 (추천)\n")
    f.write("      • 50~69점: 중간 매칭도\n")
    f.write("      • 50점 미만: 낮은 매칭도 (비추천)\n")

    f.write("\n\n■ 서비스 구현 가이드\n")
    f.write("-" * 100 + "\n")
    f.write("  1. 사용자 FIT-DNA 입력\n")
    f.write("  2. 유사도 레벨 선택 (레벨 1만 / 레벨 1+2 / 전체)\n")
    f.write("  3. 운동 종목 선택 (러닝/헬스/요가/수영 등)\n")
    f.write("  4. 추천 목록 반환 (Top N명)\n")
    f.write("  5. 매칭 점수 표시\n\n")

    f.write("  [API 함수 예시]\n")
    f.write("    recommend_matches(user_fitdna='PFE', top_n=5, similarity_level='level1')\n")
    f.write("    → [('PSE', 1.506, '레벨 2'), ...]\n\n")

    f.write("\n" + "="*100 + "\n")

print(">> 리포트 저장 완료: phase2_matching_algorithm_report.txt")

print("\n" + "="*80)
print("Phase 2-1 완료: 운동 메이트 매칭 알고리즘")
print("="*80)
print("\n생성된 파일:")
print("  1. matching_euclidean_distance_matrix.csv - 유클리드 거리 행렬")
print("  2. matching_cosine_similarity_matrix.csv - 코사인 유사도 행렬")
print("  3. phase2_matching_algorithm_analysis.png - 분석 시각화")
print("  4. phase2_matching_algorithm_report.txt - 상세 리포트")
