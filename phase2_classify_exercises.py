"""
Phase 2-4: 운동 분류 및 태깅
- 근력(Strength) / 유연성(Flexibility) / 지구력(Endurance) 분류
- 난이도(초급/중급/고급) 태깅
- 장소(실내/실외/양용) 태깅
"""

import pandas as pd
import re

print("=" * 60)
print("Phase 2-4: 운동 분류 및 태깅")
print("=" * 60)

# 데이터 로드
df = pd.read_csv('phase2_extracted_exercise_list.csv', encoding='utf-8-sig')
print(f"\n>> 로드 완료: {len(df)}개 운동")

# 분류 함수
def classify_exercise(exercise_name):
    """
    운동명을 보고 근력/유연성/지구력, 난이도, 장소를 분류

    반환: (근력점수, 유연성점수, 지구력점수, 난이도, 장소)
    - 점수는 0~3 (0=무관, 1=약간, 2=중간, 3=핵심)
    - 난이도: 초급/중급/고급
    - 장소: 실내/실외/양용
    """
    name = exercise_name.lower()

    strength = 0
    flexibility = 0
    endurance = 0
    difficulty = "중급"
    location = "양용"

    # ===== 유연성 운동 =====
    if any(keyword in name for keyword in ['스트레칭', '루틴 스트레칭', '자세', '이완']):
        flexibility = 3
        difficulty = "초급"
        location = "양용"

    # ===== 지구력 운동 =====
    elif any(keyword in name for keyword in ['달리기', '조깅', '걷기', '마라톤', '러닝']):
        endurance = 3
        strength = 1
        difficulty = "초급" if '걷기' in name else "중급"
        location = "실외"

    elif any(keyword in name for keyword in ['자전거', '사이클', '수영', '등산', '트레드밀']):
        endurance = 3
        strength = 1
        difficulty = "중급"
        location = "실내" if any(x in name for x in ['실내', '트레드밀', '고정식']) else "실외"

    elif any(keyword in name for keyword in ['줄넘기', '유산소', '에어로빅', '댄스']):
        endurance = 3
        flexibility = 1
        difficulty = "중급"
        location = "양용"

    # ===== 근력 운동 =====
    elif any(keyword in name for keyword in ['턱걸이', '풀업', '친업']):
        strength = 3
        difficulty = "고급"
        location = "양용"

    elif any(keyword in name for keyword in ['팔굽혀펴기', '푸시업', '푸쉬업', '벤치프레스', '스쿼트', '데드리프트']):
        strength = 3
        endurance = 1
        difficulty = "중급"
        location = "양용"

    elif any(keyword in name for keyword in ['윗몸', '복근', '크런치', '플랭크', '버티기']):
        strength = 3
        endurance = 1
        difficulty = "중급" if '버티기' in name else "초급"
        location = "양용"

    elif any(keyword in name for keyword in ['앉았다 일어서기', '스쿼트', '런지', '레그프레스']):
        strength = 3
        endurance = 1
        difficulty = "초급" if '앉았다' in name else "중급"
        location = "양용"

    elif any(keyword in name for keyword in ['바벨', '덤벨', '웨이트', '머신']):
        strength = 3
        difficulty = "중급"
        location = "실내"

    # ===== 복합 운동 =====
    elif any(keyword in name for keyword in ['버피', '계단', '박스점프', '왕복달리기']):
        strength = 2
        endurance = 2
        difficulty = "고급" if '버피' in name else "중급"
        location = "양용"

    elif any(keyword in name for keyword in ['요가', '필라테스', '밸런스']):
        flexibility = 2
        strength = 1
        difficulty = "중급"
        location = "실내"

    elif any(keyword in name for keyword in ['맨몸운동', '저항밴드', '짐볼', 'trx']):
        strength = 2
        endurance = 1
        difficulty = "중급"
        location = "양용"

    # ===== 기타 운동 (루틴 프로그램, 준비운동 등) =====
    elif '루틴프로그램' in name or '루틴 프로그램' in name:
        if '맨몸' in name or '웨이트' in name:
            strength = 2
            endurance = 1
        elif '유산소' in name:
            endurance = 2
            strength = 1
        else:
            flexibility = 2
        difficulty = "중급"
        location = "양용"

    # 기본값 (분류 안 된 경우)
    else:
        strength = 1
        flexibility = 1
        endurance = 1
        difficulty = "초급"
        location = "양용"

    return strength, flexibility, endurance, difficulty, location


# 분류 적용
print("\n[분류 중...]")
results = []

for idx, row in df.iterrows():
    exercise_name = row['운동명']
    frequency = row['출현빈도']

    s, f, e, diff, loc = classify_exercise(exercise_name)

    # 주 타입 결정 (가장 높은 점수)
    scores = {'근력': s, '유연성': f, '지구력': e}
    primary_type = max(scores, key=scores.get)

    # 부 타입 (두 번째로 높은 점수가 1 이상인 경우)
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    secondary_type = sorted_types[1][0] if sorted_types[1][1] >= 1 else None

    results.append({
        '운동명': exercise_name,
        '출현빈도': frequency,
        '주_타입': primary_type,
        '부_타입': secondary_type if secondary_type else '',
        '근력점수': s,
        '유연성점수': f,
        '지구력점수': e,
        '난이도': diff,
        '장소': loc
    })

# 결과 저장
result_df = pd.DataFrame(results)
result_df.to_csv('phase2_classified_exercise_database.csv', index=False, encoding='utf-8-sig')

print(f">> 분류 완료: {len(result_df)}개 운동")

# 통계
print("\n[통계 정보]")
print(f"\n1. 주 타입별 분포:")
print(result_df['주_타입'].value_counts())

print(f"\n2. 난이도별 분포:")
print(result_df['난이도'].value_counts())

print(f"\n3. 장소별 분포:")
print(result_df['장소'].value_counts())

print(f"\n4. 주 타입별 상위 5개 운동:")
for exercise_type in ['근력', '유연성', '지구력']:
    print(f"\n   [{exercise_type}]")
    top_exercises = result_df[result_df['주_타입'] == exercise_type].nlargest(5, '출현빈도')
    for i, (idx, row) in enumerate(top_exercises.iterrows(), 1):
        print(f"   {i}. {row['운동명']} ({row['출현빈도']:,}회, {row['난이도']}, {row['장소']})")

print("\n" + "=" * 60)
print("저장 완료: phase2_classified_exercise_database.csv")
print("=" * 60)
