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
print("FIT-DNA Phase 1: 데이터 구조 분석 및 유형별 특성 파악")
print("="*80)

# 1. FIT-DNA 전처리 파일 로드
print("\n[1] FIT-DNA 전처리 데이터 로드 중...")
df = pd.read_csv('최종/최종/체력측정 항목별 측정 데이터/fit_dna_preprocessed_cp949.csv', encoding='cp949')

print(f">> 총 데이터 건수: {len(df):,}건")
print(f">> 컬럼 수: {len(df.columns)}개")

# 2. 데이터 구조 확인
print("\n[2] 데이터 구조 확인")
print("-" * 80)
print(df.head())
print("\n컬럼 목록:")
print(df.columns.tolist())
print("\n데이터 타입:")
print(df.dtypes)

# 3. 기본 통계
print("\n[3] 기본 통계")
print("-" * 80)
print(df.describe())

# 4. 결측치 확인
print("\n[4] 결측치 현황")
print("-" * 80)
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    '결측 건수': missing,
    '결측 비율(%)': missing_pct
})
print(missing_df[missing_df['결측 건수'] > 0])

# 5. FIT-DNA 유형 분포 확인
print("\n[5] FIT-DNA 유형 분포")
print("-" * 80)

# FIT-DNA 컬럼 찾기
fitdna_col = [col for col in df.columns if 'dna' in col.lower() or 'DNA' in col]
print(f"FIT-DNA 관련 컬럼: {fitdna_col}")

# 각 축 라벨 컬럼 찾기
power_col = [col for col in df.columns if 'power' in col.lower() or 'light' in col.lower()]
flex_col = [col for col in df.columns if 'flex' in col.lower() or 'stiff' in col.lower()]
endurance_col = [col for col in df.columns if 'endurance' in col.lower() or 'quick' in col.lower()]

print(f"근력 관련 컬럼: {power_col}")
print(f"유연성 관련 컬럼: {flex_col}")
print(f"지구력 관련 컬럼: {endurance_col}")

# z-score 컬럼 찾기
zscore_cols = [col for col in df.columns if '_z' in col.lower() or 'zscore' in col.lower()]
print(f"\nZ-score 컬럼: {zscore_cols}")

# 6. 성별/연령대 분포
print("\n[6] 인구통계학적 분포")
print("-" * 80)

# 성별 컬럼 찾기
gender_cols = [col for col in df.columns if '성별' in col or 'SEXDSTN' in col or 'gender' in col.lower()]
age_cols = [col for col in df.columns if '연령' in col or 'AGE' in col or 'age' in col.lower()]

print(f"성별 컬럼: {gender_cols}")
print(f"연령 컬럼: {age_cols}")

if gender_cols:
    print(f"\n성별 분포:")
    print(df[gender_cols[0]].value_counts())

if age_cols:
    print(f"\n연령대 분포:")
    for col in age_cols:
        if '연령대' in col or 'AGRDE' in col:
            print(f"\n{col}:")
            print(df[col].value_counts().sort_index())

# 7. 파일 저장 - 탐색 결과
print("\n[7] 데이터 구조 분석 결과 저장")
print("-" * 80)

# 기본 정보를 텍스트 파일로 저장
with open('phase1_data_structure_report.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("FIT-DNA 데이터 구조 분석 보고서\n")
    f.write("="*80 + "\n\n")

    f.write(f"총 데이터 건수: {len(df):,}건\n")
    f.write(f"컬럼 수: {len(df.columns)}개\n\n")

    f.write("컬럼 목록:\n")
    f.write("-" * 80 + "\n")
    for i, col in enumerate(df.columns, 1):
        f.write(f"{i}. {col} ({df[col].dtype})\n")

    f.write("\n결측치 현황:\n")
    f.write("-" * 80 + "\n")
    f.write(missing_df[missing_df['결측 건수'] > 0].to_string())

    f.write("\n\nFIT-DNA 관련 컬럼:\n")
    f.write("-" * 80 + "\n")
    f.write(f"FIT-DNA 코드: {fitdna_col}\n")
    f.write(f"근력: {power_col}\n")
    f.write(f"유연성: {flex_col}\n")
    f.write(f"지구력: {endurance_col}\n")
    f.write(f"Z-scores: {zscore_cols}\n")

print(">> 보고서 저장 완료: phase1_data_structure_report.txt")

print("\n" + "="*80)
print("Phase 1-1 완료: 데이터 구조 확인 완료")
print("="*80)
