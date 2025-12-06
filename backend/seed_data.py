"""
프로토타입용 시드 데이터
단일 사용자 페르소나로 전체 기능 시연
"""

from datetime import date, datetime, timedelta
from app.core.database import SessionLocal, init_db
from app.models import (
    User, GenderEnum,
    FitnessMeasurement, FitDNAResult, LifestyleSurvey,
    WorkoutSession, UserGoal,
    DailyCondition, InjuryRisk,
    MatchingPreference, Match, MatchStatusEnum,
    Facility
)


def create_demo_user(db):
    """데모 사용자 생성 - 김체력"""
    user = User(
        email="demo@fitdna.com",
        username="demo_user",
        hashed_password="$2b$12$demo_hashed_password",  # 실제 해시 아님
        nickname="김체력",
        age=28,
        gender=GenderEnum.MALE,
        height=175.0,
        weight=72.0,
        birth_date=date(1997, 3, 15),
        profile_image="/static/profiles/demo_user.jpg",
        bio="주 4-5회 운동하는 직장인입니다. 건강한 삶을 추구합니다!",
        is_active=True,
        is_verified=True,
        joined_date=date(2025, 9, 1),
        current_fitdna_type="PFE"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ 사용자 생성: {user.nickname} (ID: {user.id})")
    return user


def create_fitness_measurements(db, user_id):
    """체력 측정 기록 - 3개월치"""
    measurements_data = [
        # 9월 측정 (초기)
        {
            "measurement_date": date(2025, 9, 15),
            "grip_right": 38.5, "grip_left": 36.8,
            "sit_up": 42, "sit_and_reach": 12.5,
            "standing_long_jump": 195, "vo2max": 42.3, "shuttle_run": 45,
            "strength_zscore": 0.3, "flexibility_zscore": -0.2, "endurance_zscore": 0.5
        },
        # 10월 측정 (개선)
        {
            "measurement_date": date(2025, 10, 15),
            "grip_right": 39.8, "grip_left": 38.1,
            "sit_up": 45, "sit_and_reach": 14.2,
            "standing_long_jump": 200, "vo2max": 43.5, "shuttle_run": 47,
            "strength_zscore": 0.45, "flexibility_zscore": 0.1, "endurance_zscore": 0.6
        },
        # 11월 측정 (현재)
        {
            "measurement_date": date(2025, 11, 15),
            "grip_right": 41.2, "grip_left": 39.1,
            "sit_up": 48, "sit_and_reach": 15.8,
            "standing_long_jump": 205, "vo2max": 44.8, "shuttle_run": 48,
            "strength_zscore": 0.6, "flexibility_zscore": 0.25, "endurance_zscore": 0.7
        }
    ]

    for data in measurements_data:
        measurement = FitnessMeasurement(user_id=user_id, **data)
        db.add(measurement)

    db.commit()
    print(f"✅ 체력 측정 기록 생성: {len(measurements_data)}개")


def create_fitdna_results(db, user_id):
    """FIT-DNA 검사 결과 - 3회"""
    results_data = [
        # 9월 - LSQ (입문자형)
        {
            "test_date": date(2025, 9, 15),
            "fitdna_type": "LSQ", "fitdna_name": "입문자형",
            "strength_score": 6.5, "flexibility_score": 5.8, "endurance_score": 7.0,
            "strengths": ["기초 체력"], "weaknesses": ["근력", "유연성"],
            "recommended_exercises": [
                {"name": "가벼운 웨이트", "category": "근력", "difficulty": "초급"},
                {"name": "스트레칭", "category": "유연성", "difficulty": "초급"}
            ],
            "is_current": 0
        },
        # 10월 - PSE (파워 러너)
        {
            "test_date": date(2025, 10, 15),
            "fitdna_type": "PSE", "fitdna_name": "파워 러너",
            "strength_score": 7.5, "flexibility_score": 6.5, "endurance_score": 8.0,
            "strengths": ["근력", "지구력"], "weaknesses": ["유연성"],
            "recommended_exercises": [
                {"name": "스쿼트", "category": "근력", "difficulty": "중급"},
                {"name": "조깅", "category": "지구력", "difficulty": "초급"},
                {"name": "요가", "category": "유연성", "difficulty": "초급"}
            ],
            "is_current": 0
        },
        # 11월 - PFE (파워 애슬리트) - 현재
        {
            "test_date": date(2025, 11, 15),
            "fitdna_type": "PFE", "fitdna_name": "파워 애슬리트",
            "strength_score": 8.5, "flexibility_score": 7.2, "endurance_score": 8.8,
            "strengths": ["근력", "지구력", "유연성"], "weaknesses": [],
            "recommended_exercises": [
                {"name": "데드리프트", "category": "근력", "difficulty": "중급"},
                {"name": "벤치프레스", "category": "근력", "difficulty": "중급"},
                {"name": "필라테스", "category": "유연성", "difficulty": "중급"},
                {"name": "인터벌 러닝", "category": "지구력", "difficulty": "중급"}
            ],
            "is_current": 1
        }
    ]

    for data in results_data:
        result = FitDNAResult(user_id=user_id, **data)
        db.add(result)

    db.commit()
    print(f"✅ FIT-DNA 검사 결과 생성: {len(results_data)}개")


def create_workout_sessions(db, user_id):
    """운동 세션 - 최근 3개월 (실제 월간 리포트 데이터 활용)"""
    import json

    # 생성된 mock 데이터 로드
    try:
        with open('monthly_reports_mock_data.json', 'r', encoding='utf-8') as f:
            reports = json.load(f)

        session_count = 0
        for report in reports:
            for session in report['sessions']:
                workout = WorkoutSession(
                    user_id=user_id,
                    date=datetime.strptime(session['date'], '%Y-%m-%d').date(),
                    exercise_type=session['exercise_type'],
                    exercises=session['exercises'],
                    duration=session['duration'],
                    intensity=session['intensity'],
                    completed=session['completed']
                )
                db.add(workout)
                session_count += 1

        db.commit()
        print(f"✅ 운동 세션 생성: {session_count}개")
    except FileNotFoundError:
        print("⚠️  monthly_reports_mock_data.json 파일을 찾을 수 없습니다. 기본 데이터로 생성합니다.")
        create_default_workout_sessions(db, user_id)


def create_default_workout_sessions(db, user_id):
    """기본 운동 세션 (파일이 없을 경우)"""
    today = date.today()
    sessions = []

    for i in range(18):  # 최근 18일
        workout_date = today - timedelta(days=i*2)
        exercise_type = ["strength", "flexibility", "endurance"][i % 3]

        exercises_map = {
            "strength": ["스쿼트", "푸시업", "플랭크"],
            "flexibility": ["요가", "스트레칭"],
            "endurance": ["조깅", "사이클링"]
        }

        session = WorkoutSession(
            user_id=user_id,
            date=workout_date,
            exercise_type=exercise_type,
            exercises=exercises_map[exercise_type],
            duration=60,
            intensity="medium",
            completed=True
        )
        sessions.append(session)

    db.add_all(sessions)
    db.commit()
    print(f"✅ 기본 운동 세션 생성: {len(sessions)}개")


def create_lifestyle_survey(db, user_id):
    """라이프스타일 설문"""
    survey = LifestyleSurvey(
        user_id=user_id,
        survey_date=date(2025, 11, 15),
        exercise_frequency=4,  # 주 4회
        daily_activity_level="medium",
        sleep_hours=7.0,
        stress_level="medium",
        additional_data={"occupation": "직장인", "hobbies": ["운동", "독서"]}
    )
    db.add(survey)
    db.commit()
    print("✅ 라이프스타일 설문 생성")


def create_daily_condition(db, user_id):
    """오늘의 컨디션"""
    condition = DailyCondition(
        user_id=user_id,
        date=date.today(),
        pain_areas=["허리"],
        fatigue_level=6,
        tension_level=5,
        sleep_quality=7,
        overall_risk_score=5.5,
        overall_risk_level="보통"
    )
    db.add(condition)
    db.commit()
    db.refresh(condition)

    # 부상 위험도
    risks = [
        InjuryRisk(
            condition_id=condition.id,
            body_part="lower_back",
            risk_level="높음",
            risk_score=7.5,
            warning_message="오늘은 데드리프트, 스쿼트 같은 허리 부담이 큰 운동을 피하세요",
            exercises_to_avoid=["데드리프트", "스쿼트", "굿모닝"],
            recommended_rest=1
        ),
        InjuryRisk(
            condition_id=condition.id,
            body_part="knee",
            risk_level="낮음",
            risk_score=2.3,
            warning_message=None,
            exercises_to_avoid=[],
            recommended_rest=0
        )
    ]
    db.add_all(risks)
    db.commit()
    print("✅ 일일 컨디션 및 부상 위험도 생성")


def create_user_goals(db, user_id):
    """사용자 목표"""
    goals = [
        UserGoal(
            user_id=user_id,
            goal_type="weekly_workouts",
            goal_name="주 4회 운동",
            target_value=4,
            current_value=3,
            unit="회",
            start_date=date.today() - timedelta(days=7),
            deadline=date.today() + timedelta(days=7),
            is_active=True,
            is_achieved=False
        ),
        UserGoal(
            user_id=user_id,
            goal_type="custom",
            goal_name="벤치프레스 100kg 달성",
            target_value=100,
            current_value=85,
            unit="kg",
            start_date=date(2025, 11, 1),
            deadline=date(2025, 12, 31),
            is_active=True,
            is_achieved=False
        )
    ]
    db.add_all(goals)
    db.commit()
    print(f"✅ 사용자 목표 생성: {len(goals)}개")


def create_facilities(db):
    """주요 운동 시설 - 서울 지역 샘플"""
    facilities = [
        # 강남 지역
        Facility(name="강남 스포츠센터", type="체육관", address="서울 강남구 테헤란로 123",
                 sports="헬스,수영,요가", latitude=37.4979, longitude=127.0276),
        Facility(name="역삼 휘트니스", type="헬스장", address="서울 강남구 역삼동 456",
                 sports="헬스,PT", latitude=37.4999, longitude=127.0364),
        Facility(name="논현 요가원", type="요가", address="서울 강남구 논현동 789",
                 sports="요가,필라테스", latitude=37.5105, longitude=127.0223),

        # 강북 지역
        Facility(name="강북 종합 체육관", type="체육관", address="서울 강북구 수유동 234",
                 sports="농구,배드민턴,탁구", latitude=37.6390, longitude=127.0259),
        Facility(name="수유 수영장", type="수영장", address="서울 강북구 수유동 567",
                 sports="수영,아쿼로빅", latitude=37.6398, longitude=127.0252),

        # 마포 지역
        Facility(name="홍대 클라이밍", type="클라이밍", address="서울 마포구 홍익로 789",
                 sports="클라이밍", latitude=37.5564, longitude=126.9246),
        Facility(name="상수 필라테스", type="필라테스", address="서울 마포구 상수동 101",
                 sports="필라테스", latitude=37.5478, longitude=126.9221),

        # 송파 지역
        Facility(name="잠실 스포츠센터", type="체육관", address="서울 송파구 잠실동 123",
                 sports="헬스,수영,에어로빅", latitude=37.5133, longitude=127.1028),
        Facility(name="석촌 헬스클럽", type="헬스장", address="서울 송파구 석촌동 456",
                 sports="헬스,크로스핏", latitude=37.5054, longitude=127.1062),

        # 용산 지역
        Facility(name="이촌 수영장", type="수영장", address="서울 용산구 이촌동 234",
                 sports="수영", latitude=37.5245, longitude=126.9655),

        # 서초 지역
        Facility(name="서초 종합운동장", type="운동장", address="서울 서초구 서초동 789",
                 sports="축구,농구,배구", latitude=37.4836, longitude=127.0327),
        Facility(name="방배 테니스장", type="테니스장", address="서울 서초구 방배동 123",
                 sports="테니스", latitude=37.4814, longitude=126.9963),
    ]

    db.add_all(facilities)
    db.commit()
    print(f"✅ 운동 시설 생성: {len(facilities)}개")


def create_matching_data(db, user_id):
    """매칭 선호도 및 더미 매칭 파트너"""
    # 매칭 선호도
    preference = MatchingPreference(
        user_id=user_id,
        fitdna_similarity=1,  # 1개 차이까지 허용
        exercise_types=["러닝", "헬스", "수영"],
        preferred_times=["아침", "저녁"],
        location_radius_km=5.0,
        age_range={"min": 25, "max": 35},
        gender_preference="any"
    )
    db.add(preference)
    db.commit()
    print("✅ 매칭 선호도 생성")

    # 더미 매칭 파트너 (프로토타입용)
    dummy_partners = [
        User(
            email=f"partner{i}@fitdna.com",
            username=f"partner_{i}",
            hashed_password="dummy",
            nickname=["런너123", "헬스매니아", "요가러버"][i-1],
            age=[28, 26, 30][i-1],
            gender=GenderEnum.MALE if i <= 2 else GenderEnum.FEMALE,
            current_fitdna_type=["PFE", "PSE", "LFE"][i-1],
            is_active=True,
            joined_date=date(2025, 1, 1)
        )
        for i in range(1, 4)
    ]
    db.add_all(dummy_partners)
    db.commit()

    # 매칭 결과 생성
    match = Match(
        user1_id=user_id,
        user2_id=dummy_partners[0].id,
        compatibility_score=92.0,
        fitdna_similarity_score=100.0,
        exercise_overlap_score=80.0,
        time_overlap_score=90.0,
        location_distance_km=1.2,
        common_exercises=["러닝", "헬스", "수영"],
        status=MatchStatusEnum.ACTIVE,
        requester_id=user_id,
        matched_date=date(2025, 11, 25),
        total_workouts_together=5,
        chat_room_id="chat_12345"
    )
    db.add(match)
    db.commit()
    print(f"✅ 더미 파트너 및 매칭 생성: {len(dummy_partners)}명")


def seed_all():
    """전체 시드 데이터 생성"""
    print("\n🌱 시드 데이터 생성 시작...\n")

    # DB 초기화
    init_db()

    db = SessionLocal()

    try:
        # 1. 사용자 생성
        user = create_demo_user(db)

        # 2. 체력 측정 기록
        create_fitness_measurements(db, user.id)

        # 3. FIT-DNA 검사 결과
        create_fitdna_results(db, user.id)

        # 4. 운동 세션
        create_workout_sessions(db, user.id)

        # 5. 라이프스타일 설문
        create_lifestyle_survey(db, user.id)

        # 6. 일일 컨디션
        create_daily_condition(db, user.id)

        # 7. 사용자 목표
        create_user_goals(db, user.id)

        # 8. 운동 시설
        create_facilities(db)

        # 9. 매칭 데이터
        create_matching_data(db, user.id)

        print("\n✅ 시드 데이터 생성 완료!")
        print(f"\n📊 데모 사용자 정보:")
        print(f"   - 이메일: demo@fitdna.com")
        print(f"   - 닉네임: {user.nickname}")
        print(f"   - FIT-DNA: {user.current_fitdna_type} (파워 애슬리트)")
        print(f"   - User ID: {user.id}")

    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()
