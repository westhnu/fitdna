# HaruAdvice.py
# Haru 부상 위험도 결과를 바탕으로
# 1) 부위별 피해야 할 운동 / 추천 루틴
# 2) 연령 + 부위에 맞는 KSPO 영상 링크
# 를 생성하는 모듈

from typing import Dict, Any, List


# -------------------------
# 0. 연령 그룹 매핑
# -------------------------
def map_age_group(age_flag: str) -> str:
    """
    Haru 엔진에서 넘어온 age_flag(예: '성인', '청소년', '노인', '중장년' 등)를
    크게 3그룹으로 묶어줌.
    """
    if "청소년" in age_flag or "유소년" in age_flag:
        return "청소년"
    if "노인" in age_flag or "고령" in age_flag or "중장년" in age_flag:
        return "중장년/노인"
    return "성인"


# -------------------------
# 1. 연령별 KSPO 영상 링크 (초기 버전)
#    → 나중에 실제 KSPO 플레이리스트 링크로 교체하면 됨
# -------------------------
AGE_VIDEO_LINKS = {
    "청소년": [
        {
            "title": "청소년 체력 향상 홈트 루틴",
            "url": "https://www.youtube.com/@kspo100/search?query=청소년%20운동"
        }
    ],
    "성인": [
        {
            "title": "성인 표준운동 프로그램 (국민체력100)",
            "url": "https://www.youtube.com/playlist?list=PLKjEcOd9dGPMl_Z6JJHXtDxHrjq2itoVW"
        }
    ],
    "중장년/노인": [
        {
            "title": "중장년·노인 건강운동 / 관절 보호 루틴",
            "url": "https://www.youtube.com/@kspo100/search?query=시니어%20운동"
        }
    ]
}


# -------------------------
# 2. 부위 + 위험도별 KSPO 영상 링크 (초기 버전)
# -------------------------
BODY_VIDEO_LINKS = {
    ("허리", "주의"): [
        {
            "title": "허리 통증 예방 스트레칭",
            "url": "https://www.youtube.com/@kspo100/search?query=허리%20스트레칭"
        }
    ],
    ("허리", "위험"): [
        {
            "title": "코어 안정화 & 허리 보호 운동",
            "url": "https://www.youtube.com/@kspo100/search?query=코어%20운동"
        }
    ],
    ("무릎", "주의"): [
        {
            "title": "무릎 통증 예방 운동",
            "url": "https://www.youtube.com/@kspo100/search?query=무릎%20운동"
        }
    ],
    ("무릎", "위험"): [
        {
            "title": "무릎 관절 보호 재활 루틴",
            "url": "https://www.youtube.com/@kspo100/search?query=관절%20강화%20운동"
        }
    ],
    ("발목", "주의"): [
        {
            "title": "발목 강화·균형 잡기 운동",
            "url": "https://www.youtube.com/@kspo100/search?query=발목%20운동"
        }
    ],
    ("어깨", "주의"): [
        {
            "title": "어깨·목 풀어주는 스트레칭",
            "url": "https://www.youtube.com/@kspo100/search?query=어깨%20스트레칭"
        }
    ],
    ("팔꿈치", "주의"): [
        {
            "title": "팔꿈치·전완 스트레칭",
            "url": "https://www.youtube.com/@kspo100/search?query=팔꿈치%20스트레칭"
        }
    ]
}


# -------------------------
# 3. 부위별 텍스트 조언
# -------------------------
def get_part_advice(part: str, level: str):
    """
    부위(part)와 위험 등급(level)에 따라
    피해야 할 운동 / 추천 루틴을 텍스트로 반환
    """
    avoid: List[str] = []
    recommend: List[str] = []

    if part == "허리":
        if level == "주의":
            avoid = ["무거운 스쿼트", "과도한 허리 굴곡/신전 동작"]
            recommend = ["가벼운 플랭크", "고양이-소 스트레칭", "햄스트링 스트레칭"]
        elif level in ["위험", "고위험"]:
            avoid = ["데드리프트 전 종류", "고중량 리프팅", "허리를 비트는 동작"]
            recommend = ["걷기", "버드독", "데드버그", "요추 안정화 운동"]

    if part == "무릎":
        if level == "주의":
            avoid = ["경사도 높은 러닝", "점프 후 깊은 착지"]
            recommend = ["레그 익스텐션(가볍게)", "스텝업", "대퇴사두근 스트레칭"]
        elif level in ["위험", "고위험"]:
            avoid = ["깊은 스쿼트", "점프/플라이오메트릭", "축구·농구 경기"]
            recommend = ["실내 자전거(저강도)", "브릿지", "햄스트링·장요근 스트레칭"]

    if part == "발목":
        if level == "주의":
            avoid = ["불안정한 지면에서의 러닝", "급격한 방향 전환"]
            recommend = ["발목 원 그리기", "밴드 이용 발목 강화", "종아리 스트레칭"]
        elif level in ["위험", "고위험"]:
            avoid = ["축구·농구 경기", "점프 착지 반복"]
            recommend = ["평지 걷기", "발목 안정화 운동", "종아리 마사지 및 스트레칭"]

    if part == "어깨":
        if level == "주의":
            avoid = ["과도한 오버헤드 프레스", "반동 이용 풀업"]
            recommend = ["밴드 로테이터커프 운동", "어깨 원 그리기", "가벼운 로우"]
        elif level in ["위험", "고위험"]:
            avoid = ["벤치프레스 고중량", "오버헤드 프레스", "스내치/클린"]
            recommend = ["월슬라이드", "회전근개 강화운동", "가벼운 밴드 풀어파트"]

    if part == "팔꿈치":
        if level == "주의":
            avoid = ["고반복 팔꿈치 굽힘/펴기", "테니스/골프 스윙 반복"]
            recommend = ["전완근 스트레칭", "가벼운 그립 운동"]
        elif level in ["위험", "고위험"]:
            avoid = ["풀업·친업", "고중량 컬", "반복 타격 동작"]
            recommend = ["손목 플렉서/익스텐서 스트레칭", "등척성 그립 트레이닝"]

    return avoid, recommend


# -------------------------
# 3-1. 부위별 재활 정보 공용 함수 (부상 관리 센터용)
# -------------------------
def get_rehab_for_part(part: str, level: str = "주의") -> Dict[str, Any]:
    """
    부상 관리 센터에서 바로 쓰기 위한 공용 함수.

    - 엔진 없이도, 부위(part)와 레벨(level)을 넣으면
      피해야 할 운동 / 추천 운동 / 영상 링크 세트를 한 번에 반환.
    - level == "정상" 이 들어오면, 조언이 필요하다고 보고 "주의" 수준으로 보정.
    """

    # level이 '정상'이면, 조언이 거의 안 나오므로 '주의'로 올려서 가이드 제공
    level_for_advice = "주의" if level == "정상" else level

    avoid, recommend = get_part_advice(part, level_for_advice)
    videos = BODY_VIDEO_LINKS.get((part, level_for_advice), [])

    return {
        "part": part,
        "level": level_for_advice,
        "avoid": avoid,
        "recommend": recommend,
        "videos": videos
    }


# -------------------------
# 4. 최종 메시지 빌더
# -------------------------
def build_daily_message(engine_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    run_haru_engine 결과(engine_result)를 받아
    - headline (요약 문구)
    - detail (부위별 조언 + 영상 링크)
    - age_group / age_videos (연령별 추천 영상)
    를 반환.
    """

    parts = engine_result["body_parts"]
    age_flag = engine_result.get("age_flag", "성인")
    age_group = map_age_group(age_flag)

    messages: List[Dict[str, Any]] = []

    for part, info in parts.items():
        level = info["level"]
        score = info["score"]

        if level == "정상":
            continue  # 정상은 메시지 생략

        # 공용 함수 재사용
        base_msg = get_rehab_for_part(part, level)
        # 엔진에서 계산된 점수 추가
        base_msg["score"] = score

        messages.append(base_msg)

    # 요약 문구
    if not messages:
        headline = "오늘은 전반적으로 부상 위험이 낮아요. 계획한 운동을 진행해도 좋습니다."
    else:
        risk_parts = [m["part"] for m in messages]
        headline = f"오늘은 {', '.join(risk_parts)} 부위의 부상 위험이 높아요. 해당 부위는 강도를 조절해 주세요."

    return {
        "headline": headline,
        "detail": messages,
        "age_group": age_group,
        "age_videos": AGE_VIDEO_LINKS.get(age_group, [])
    }


# 단독 실행 테스트 (원하면 써도 됨)
if __name__ == "__main__":
    dummy_engine_result = {
        "age_flag": "성인",
        "body_parts": {
            "허리": {"score": 3.2, "level": "위험"},
            "무릎": {"score": 2.2, "level": "주의"},
            "발목": {"score": 1.0, "level": "정상"},
            "어깨": {"score": 1.5, "level": "정상"},
            "팔꿈치": {"score": 1.0, "level": "정상"},
        }
    }
    from pprint import pprint
    pprint(build_daily_message(dummy_engine_result))

    # 부상 관리 센터용 함수 테스트
    pprint(get_rehab_for_part("무릎", "주의"))
