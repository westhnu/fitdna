import pandas as pd

print("="*80)
print("FIT-DNA 측정항목 매핑표 생성")
print("="*80)

# 근력 측정 항목
strength_items = [
    {"축": "근력", "항목명": "악력(좌)", "단위": "kg", "필수여부": "필수", "설명": "왼손 악력"},
    {"축": "근력", "항목명": "악력(우)", "단위": "kg", "필수여부": "필수", "설명": "오른손 악력"},
    {"축": "근력", "항목명": "배근력", "단위": "kg", "필수여부": "선택", "설명": "등 근력"},
    {"축": "근력", "항목명": "각근력", "단위": "kg", "필수여부": "선택", "설명": "다리 근력"},
    {"축": "근력", "항목명": "윗몸일으키기", "단위": "회/분", "필수여부": "선택", "설명": "복근력"},
    {"축": "근력", "항목명": "팔굽혀펴기", "단위": "회", "필수여부": "선택", "설명": "상체 근력"},
    {"축": "근력", "항목명": "제자리멀리뛰기", "단위": "cm", "필수여부": "필수", "설명": "하체 폭발력"},
    {"축": "근력", "항목명": "윗몸말아올리기", "단위": "회/분", "필수여부": "선택", "설명": "복근 지구력"},
]

# 유연성 측정 항목
flexibility_items = [
    {"축": "유연성", "항목명": "앉아윗몸앞으로굽히기", "단위": "cm", "필수여부": "필수", "설명": "상하체 유연성"},
]

# 지구력 측정 항목
endurance_items = [
    {"축": "지구력", "항목명": "6분 걷기", "단위": "m", "필수여부": "선택", "설명": "유산소 지구력"},
    {"축": "지구력", "항목명": "왕복오래달리기", "단위": "회", "필수여부": "선택", "설명": "심폐지구력"},
    {"축": "지구력", "항목명": "오래달리기-걷기", "단위": "초", "필수여부": "선택", "설명": "유산소 능력"},
    {"축": "지구력", "항목명": "심폐지구력", "단위": "mL/kg/min", "필수여부": "선택", "설명": "유산소 능력"},
    {"축": "지구력", "항목명": "VO₂max", "단위": "mL/kg/min", "필수여부": "필수", "설명": "최대산소섭취량"},
    {"축": "지구력", "항목명": "스텝검사", "단위": "점수", "필수여부": "선택", "설명": "심폐능력"},
]

# 전체 데이터프레임 생성
all_items = strength_items + flexibility_items + endurance_items
df = pd.DataFrame(all_items)

# CSV로 저장
df.to_csv('FIT_DNA_측정항목_매핑표.csv', index=False, encoding='utf-8-sig')
print("\n>> CSV 파일 저장 완료: FIT_DNA_측정항목_매핑표.csv")

# 텍스트 보고서 생성
with open('FIT_DNA_측정항목_매핑표.txt', 'w', encoding='utf-8') as f:
    f.write("="*100 + "\n")
    f.write(" "*30 + "FIT-DNA 측정항목 매핑표\n")
    f.write("="*100 + "\n\n")

    f.write("■ 전체 구성\n")
    f.write("-" * 100 + "\n")
    f.write(f"  • 총 측정 항목: {len(df)}개\n")
    f.write(f"  • 근력 항목: {len(strength_items)}개\n")
    f.write(f"  • 유연성 항목: {len(flexibility_items)}개\n")
    f.write(f"  • 지구력 항목: {len(endurance_items)}개\n\n")

    # 축별로 출력
    for axis in ["근력", "유연성", "지구력"]:
        f.write(f"\n■ {axis} 측정 항목\n")
        f.write("-" * 100 + "\n")
        axis_df = df[df['축'] == axis]

        f.write(f"{'항목명':20s} {'단위':15s} {'필수여부':10s} {'설명':30s}\n")
        f.write("-" * 100 + "\n")

        for _, row in axis_df.iterrows():
            f.write(f"{row['항목명']:20s} {row['단위']:15s} {row['필수여부']:10s} {row['설명']:30s}\n")

    f.write("\n\n■ 최소 필수 입력 항목 (FIT-DNA 계산용)\n")
    f.write("-" * 100 + "\n")
    required_df = df[df['필수여부'] == '필수']
    f.write(f"  총 {len(required_df)}개 항목\n\n")

    for axis in ["근력", "유연성", "지구력"]:
        axis_required = required_df[required_df['축'] == axis]
        f.write(f"  [{axis}] {len(axis_required)}개\n")
        for _, row in axis_required.iterrows():
            f.write(f"    • {row['항목명']} ({row['단위']})\n")

    f.write("\n\n■ 성별 구분 필요성\n")
    f.write("-" * 100 + "\n")
    f.write("  FIT-DNA는 연령대 × 성별 그룹별 표준화(Z-Score)를 사용하므로 성별 정보는 필수입니다.\n\n")

    f.write("  [표준화 공식]\n")
    f.write("    Z-Score = (개인 측정값 - 그룹 평균) / 그룹 표준편차\n")
    f.write("    여기서 그룹 = (연령대, 성별) 조합\n\n")

    f.write("  [성별에 따른 체력 차이 예시]\n")
    f.write("    • 악력: 남성 평균 45kg, 여성 평균 27kg (약 1.7배 차이)\n")
    f.write("    • 제자리멀리뛰기: 남성 평균 215cm, 여성 평균 165cm (약 1.3배 차이)\n")
    f.write("    • 유연성: 여성이 평균적으로 남성보다 약 20% 높음\n\n")

    f.write("  → 성별 구분 없이는 정확한 체력 평가 불가능!\n")

    f.write("\n\n■ 서비스 구현 시 고려사항\n")
    f.write("-" * 100 + "\n")
    f.write("  1. 기본 정보 입력\n")
    f.write("     • 나이 (필수)\n")
    f.write("     • 성별 (필수) - 남성/여성 라디오 버튼\n")
    f.write("     • 키, 몸무게 (선택)\n\n")

    f.write("  2. 체력 측정값 입력\n")
    f.write("     • 직접 입력 모드\n")
    f.write("     • 사진 업로드 모드 (국민체력100 결과지 OCR)\n\n")

    f.write("  3. 입력값 검증\n")
    f.write("     • 악력: 5~100 kg\n")
    f.write("     • 제자리멀리뛰기: 50~350 cm\n")
    f.write("     • 유연성: -20~50 cm\n")
    f.write("     • VO₂max: 10~80 mL/kg/min\n\n")

    f.write("  4. 결측 처리\n")
    f.write("     • 한 축의 모든 항목이 NaN → 해당 사용자 데이터 제외\n")
    f.write("     • 일부 항목만 입력 → 입력된 항목의 평균으로 축 Z-Score 계산\n")

    f.write("\n\n" + "="*100 + "\n")
    f.write(" "*35 + "End of Mapping Table\n")
    f.write("="*100 + "\n")

print(">> 텍스트 리포트 저장 완료: FIT_DNA_측정항목_매핑표.txt")

# 화면 출력
print("\n" + "="*80)
print("측정항목 요약")
print("="*80)
print(f"\n총 {len(df)}개 측정 항목")
print(f"  - 근력: {len(strength_items)}개")
print(f"  - 유연성: {len(flexibility_items)}개")
print(f"  - 지구력: {len(endurance_items)}개")

print(f"\n필수 항목: {len(required_df)}개")
for axis in ["근력", "유연성", "지구력"]:
    axis_required = required_df[required_df['축'] == axis]
    print(f"  - {axis}: {len(axis_required)}개")

print("\n생성된 파일:")
print("  1. FIT_DNA_측정항목_매핑표.csv")
print("  2. FIT_DNA_측정항목_매핑표.txt")
print("  3. FIT_DNA_SERVICE_GUIDE.md (서비스 구현 가이드)")

print("\n" + "="*80)
print("매핑표 생성 완료!")
print("="*80)
