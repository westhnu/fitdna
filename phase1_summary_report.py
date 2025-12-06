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
print("FIT-DNA Phase 1 종합 리포트 생성")
print("="*80)

# 데이터 로드
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')

# 종합 리포트 작성
with open('PHASE1_FINAL_SUMMARY_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write(" "*35 + "FIT-DNA PHASE 1\n")
    f.write(" "*25 + "데이터 분석 및 인사이트 도출 종합 보고서\n")
    f.write("="*100 + "\n\n")

    # 개요
    f.write("█ 분석 개요\n")
    f.write("-" * 100 + "\n")
    f.write(f"  • 분석 대상: FIT-DNA 전처리 데이터 (국민체력100 기반)\n")
    f.write(f"  • 총 데이터 건수: {len(df):,}건\n")
    f.write(f"  • FIT-DNA 유형: 8가지 (Power/Light × Flexibility/Stiff × Endurance/Quick)\n")
    f.write(f"  • 분석 기간: 체력 측정 데이터 기준\n")
    f.write(f"  • 주요 지표: 근력(strength_z), 유연성(flex_z), 지구력(endurance_z)\n\n")

    # 1. 데이터 구조
    f.write("█ 1. 데이터 구조 분석 결과\n")
    f.write("-" * 100 + "\n")
    f.write(f"  [1-1] 컬럼 구성 ({len(df.columns)}개)\n")
    for i, col in enumerate(df.columns, 1):
        f.write(f"    {i:2d}. {col:25s} ({str(df[col].dtype):10s})\n")

    f.write(f"\n  [1-2] 결측치 현황\n")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    for col in df.columns:
        if missing[col] > 0:
            f.write(f"    • {col}: {missing[col]:,}건 ({missing_pct[col]:.2f}%)\n")
    if missing.sum() == 0:
        f.write("    • 결측치 없음 (전처리 완료 상태)\n")

    # 2. FIT-DNA 유형 분포
    f.write("\n\n█ 2. FIT-DNA 8가지 유형 분포 및 특성\n")
    f.write("-" * 100 + "\n")

    fitdna_dist = df['FIT_DNA'].value_counts().sort_index()
    type_stats = df.groupby('FIT_DNA')[['strength_z', 'flex_z', 'endurance_z']].mean()

    f.write("  [2-1] 유형별 분포\n")
    for type_name, count in fitdna_dist.items():
        pct = count / len(df) * 100
        f.write(f"    • {type_name:5s}: {count:6,}건 ({pct:5.2f}%)\n")

    f.write("\n  [2-2] 유형별 평균 체력 지표 (Z-Score)\n")
    f.write("    " + "-" * 80 + "\n")
    f.write(f"    {'유형':8s}  {'근력':>10s}  {'유연성':>10s}  {'지구력':>10s}  {'특징':20s}\n")
    f.write("    " + "-" * 80 + "\n")
    for type_name in fitdna_dist.index:
        s = type_stats.loc[type_name, 'strength_z']
        flex_val = type_stats.loc[type_name, 'flex_z']
        e = type_stats.loc[type_name, 'endurance_z']

        # 유형 특징 요약
        traits = []
        if s > 0.5:
            traits.append("높은근력")
        elif s < -0.5:
            traits.append("낮은근력")
        if flex_val > 0.5:
            traits.append("유연함")
        elif flex_val < -0.5:
            traits.append("경직됨")
        if e > 0.5:
            traits.append("높은지구력")
        elif e < -0.5:
            traits.append("낮은지구력")

        trait_str = ", ".join(traits) if traits else "중간"

        f.write(f"    {type_name:8s}  {s:10.3f}  {flex_val:10.3f}  {e:10.3f}  {trait_str}\n")

    # 3. 유형 간 유사도
    f.write("\n  [2-3] 가장 유사한 유형 (유클리드 거리 기준)\n")
    from scipy.spatial.distance import pdist, squareform
    type_vectors = type_stats.values
    type_names = type_stats.index.tolist()
    distance_matrix = squareform(pdist(type_vectors, metric='euclidean'))

    similar_pairs = []
    for i in range(len(type_names)):
        for j in range(i+1, len(type_names)):
            similar_pairs.append((type_names[i], type_names[j], distance_matrix[i, j]))

    similar_pairs.sort(key=lambda x: x[2])
    for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
        f.write(f"    {rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}\n")

    f.write("\n  [2-4] 가장 다른 유형\n")
    similar_pairs.sort(key=lambda x: x[2], reverse=True)
    for rank, (type1, type2, dist) in enumerate(similar_pairs[:5], 1):
        f.write(f"    {rank}. {type1} ↔ {type2}: 거리 = {dist:.3f}\n")

    # 4. 연령대/성별 패턴
    f.write("\n\n█ 3. 연령대/성별 패턴 분석\n")
    f.write("-" * 100 + "\n")

    f.write("  [3-1] 연령대별 주요 유형\n")
    age_type_dist = pd.crosstab(df['AGRDE_FLAG_NM'], df['FIT_DNA'], normalize='index') * 100
    for age_group in age_type_dist.index:
        top_type = age_type_dist.loc[age_group].idxmax()
        top_pct = age_type_dist.loc[age_group].max()
        f.write(f"    • {age_group:10s}: {top_type} ({top_pct:.1f}%)\n")

    f.write("\n  [3-2] 성별 주요 유형\n")
    gender_type_dist = pd.crosstab(df['SEXDSTN_FLAG_CD'], df['FIT_DNA'], normalize='index') * 100
    for gender in gender_type_dist.index:
        top_type = gender_type_dist.loc[gender].idxmax()
        top_pct = gender_type_dist.loc[gender].max()
        gender_name = '남성' if gender == 'M' else '여성'
        f.write(f"    • {gender_name:10s}: {top_type} ({top_pct:.1f}%)\n")

    f.write("\n  [3-3] 연령대별 평균 체력 지표\n")
    age_stats = df.groupby('AGRDE_FLAG_NM')[['strength_z', 'flex_z', 'endurance_z']].mean()
    f.write("    " + "-" * 80 + "\n")
    f.write(f"    {'연령대':10s}  {'근력':>10s}  {'유연성':>10s}  {'지구력':>10s}\n")
    f.write("    " + "-" * 80 + "\n")
    for age_group in age_stats.index:
        s = age_stats.loc[age_group, 'strength_z']
        f_val = age_stats.loc[age_group, 'flex_z']
        e = age_stats.loc[age_group, 'endurance_z']
        f.write(f"    {age_group:10s}  {s:10.3f}  {f_val:10.3f}  {e:10.3f}\n")

    # 5. 핵심 인사이트
    f.write("\n\n█ 4. 핵심 인사이트 및 제안\n")
    f.write("-" * 100 + "\n")

    # 가장 많은/적은 유형
    most_common = fitdna_dist.idxmax()
    most_common_pct = (fitdna_dist.max() / len(df) * 100)
    least_common = fitdna_dist.idxmin()
    least_common_pct = (fitdna_dist.min() / len(df) * 100)

    f.write("\n  [4-1] 유형 분포 인사이트\n")
    f.write(f"    • 가장 많은 유형: {most_common} ({most_common_pct:.2f}%)\n")
    f.write(f"      → 서비스 타겟층으로 우선 고려 필요\n")
    f.write(f"    • 가장 적은 유형: {least_common} ({least_common_pct:.2f}%)\n")
    f.write(f"      → 희소 유형, 특화 콘텐츠 제공 검토\n")

    f.write("\n  [4-2] 운동 매칭 알고리즘 제안\n")
    f.write("    • 유사도 레벨 1 (매우 유사): 거리 < 1.2\n")
    f.write("      예) LSE ↔ PSE (거리 1.075)\n")
    f.write("    • 유사도 레벨 2 (유사): 거리 1.2 ~ 2.0\n")
    f.write("    • 유사도 레벨 3 (다름): 거리 > 2.0\n")
    f.write("      예) LSQ ↔ PFE (거리 2.889) - 매칭 비추천\n")

    f.write("\n  [4-3] 유형별 운동 추천 방향\n")
    for type_name in ['PFE', 'LSQ', 'PSE', 'LFQ']:
        if type_name in type_stats.index:
            s = type_stats.loc[type_name, 'strength_z']
            flex = type_stats.loc[type_name, 'flex_z']
            e = type_stats.loc[type_name, 'endurance_z']

            f.write(f"    • {type_name}:\n")
            if s > 0.5 and flex > 0.5 and e > 0.5:
                f.write(f"      강점: 전반적 높은 체력 | 추천: 고강도 운동, 크로스핏, HIIT\n")
            elif s < -0.5 and e < -0.5:
                f.write(f"      약점: 근력·지구력 낮음 | 추천: 저강도 유산소, 가벼운 근력 운동\n")
            elif flex < -0.5:
                f.write(f"      약점: 유연성 낮음 | 추천: 스트레칭, 요가, 필라테스 우선\n")
            elif s > 0.5:
                f.write(f"      강점: 근력 높음 | 추천: 웨이트 트레이닝, 파워 운동\n")

    f.write("\n  [4-4] 연령대별 맞춤 전략\n")
    for age_group in ['청소년', '성인', '노인']:
        if age_group in age_type_dist.index:
            top_type = age_type_dist.loc[age_group].idxmax()
            f.write(f"    • {age_group}: 주요 유형 {top_type}\n")
            if age_group == '청소년':
                f.write(f"      → 성장기 체력 향상 프로그램 강화\n")
            elif age_group == '성인':
                f.write(f"      → 직장인 대상 짧은 시간 고효율 운동\n")
            elif age_group == '노인':
                f.write(f"      → 안전 중심 저강도 운동, 부상 예방 강조\n")

    # 6. 다음 단계
    f.write("\n\n█ 5. Phase 2 준비 사항\n")
    f.write("-" * 100 + "\n")
    f.write("  [5-1] 운동 메이트 매칭 알고리즘 개발\n")
    f.write("    • 유사도 계산 함수 구현 (유클리드 거리, 코사인 유사도)\n")
    f.write("    • 필터링 옵션: 운동 선호도, 시간대, 위치\n")
    f.write("    • 매칭 스코어링 시스템 구축\n")

    f.write("\n  [5-2] 부상 위험도 예측 모델\n")
    f.write("    • 입력: 컨디션(통증/피로/긴장) + FIT-DNA 유형\n")
    f.write("    • 출력: 부위별 위험도 (허리/무릎/어깨)\n")
    f.write("    • 모델: 로지스틱 회귀 또는 랜덤 포레스트\n")

    f.write("\n  [5-3] 운동 추천 규칙 엔진\n")
    f.write("    • 유형별 강점/약점 기반 운동 매핑\n")
    f.write("    • 난이도별 루틴 (초보/중급/고급)\n")
    f.write("    • 실내/실외 옵션 구분\n")

    f.write("\n  [5-4] 체력 변화 예측 모델\n")
    f.write("    • 재측정 데이터 활용 시계열 분석\n")
    f.write("    • 6개월 후 체력 지표 예측\n")
    f.write("    • Consistency Score 산출\n")

    # 생성 파일 목록
    f.write("\n\n█ 6. Phase 1 산출물\n")
    f.write("-" * 100 + "\n")
    f.write("  [분석 스크립트]\n")
    f.write("    • phase1_fitdna_analysis.py - 데이터 구조 분석\n")
    f.write("    • phase1_fitdna_type_analysis.py - 유형별 특성 분석\n")
    f.write("    • phase1_demographic_analysis.py - 연령/성별 패턴 분석\n")

    f.write("\n  [시각화 파일]\n")
    f.write("    • phase1_fitdna_type_distribution.png - 유형 분포 및 특성\n")
    f.write("    • phase1_fitdna_radar_charts.png - 유형별 레이더 차트\n")
    f.write("    • phase1_demographic_analysis.png - 연령/성별 분석\n")
    f.write("    • phase1_gender_age_fitdna_detail.png - 성별×연령 상세\n")

    f.write("\n  [리포트 파일]\n")
    f.write("    • phase1_data_structure_report.txt - 데이터 구조 보고서\n")
    f.write("    • phase1_fitdna_type_analysis_report.txt - 유형 분석 보고서\n")
    f.write("    • phase1_demographic_analysis_report.txt - 인구통계 보고서\n")
    f.write("    • PHASE1_FINAL_SUMMARY_REPORT.txt - 종합 보고서 (본 파일)\n")

    f.write("\n\n" + "="*100 + "\n")
    f.write(" "*30 + "End of Phase 1 Summary Report\n")
    f.write("="*100 + "\n")

print(">> 종합 리포트 생성 완료: PHASE1_FINAL_SUMMARY_REPORT.txt")

# 최종 통계 출력
print("\n" + "="*80)
print("FIT-DNA PHASE 1 완료 요약")
print("="*80)
print(f"\n분석 데이터: {len(df):,}건")
print(f"FIT-DNA 유형: {len(df['FIT_DNA'].unique())}가지")
print(f"연령대: {len(df['AGRDE_FLAG_NM'].unique())}개 그룹")
print(f"성별: {len(df['SEXDSTN_FLAG_CD'].unique())}개 (남/여)")

print("\n주요 유형 Top 3:")
fitdna_dist = df['FIT_DNA'].value_counts()
for i, (type_name, count) in enumerate(fitdna_dist.head(3).items(), 1):
    pct = count / len(df) * 100
    print(f"  {i}. {type_name}: {count:,}건 ({pct:.2f}%)")

print("\n생성된 파일:")
print("  - Python 스크립트: 3개")
print("  - 시각화 PNG: 4개")
print("  - 분석 리포트: 4개")

print("\n" + "="*80)
print("Phase 1 완료! Phase 2 (모델링)를 시작할 준비가 되었습니다.")
print("="*80)
