"""
map_2k.html에서 시설 데이터 파싱
"""

import re
import json
from bs4 import BeautifulSoup


def parse_facility_html(html_path='../map_2k.html'):
    """HTML 파일에서 시설 데이터 추출"""

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 마커 패턴 찾기
    marker_pattern = r'var marker_\w+ = L\.marker\(\s*\[([0-9.]+),\s*([0-9.]+)\]'
    popup_pattern = r'<b>\[(.*?)\]</b><br>\s*운동종목:\s*(.*?)<br>\s*주소:\s*(.*?)<br>'

    markers = re.findall(marker_pattern, html_content)
    popups = re.findall(popup_pattern, html_content)

    facilities = []

    for i, (marker, popup) in enumerate(zip(markers, popups)):
        lat, lon = marker
        facility_type_raw, sports, address = popup

        # 시설 유형 매핑
        type_mapping = {
            '학교': 'school',
            '체육관': 'gym',
            '수영장': 'pool',
            '공원': 'park',
            '헬스장': 'fitness_center'
        }

        facility_type = type_mapping.get(facility_type_raw, 'other')

        # 운동 종목 리스트로 변환
        sports_list = [s.strip() for s in sports.split(',')]

        facility = {
            'id': i + 1,
            'name': extract_facility_name(address),
            'facility_type': facility_type,
            'facility_type_kr': facility_type_raw,
            'address': address.strip(),
            'latitude': float(lat),
            'longitude': float(lon),
            'sports': sports_list,
            'phone': None,
            'website': None,
            'has_parking': True if facility_type in ['gym', 'school'] else False,
            'has_shower': True if facility_type in ['gym', 'pool'] else False,
            'has_locker': True if facility_type in ['gym', 'pool'] else False,
            'operating_hours': {
                'weekday': '06:00-22:00' if facility_type == 'gym' else '09:00-18:00',
                'weekend': '08:00-20:00' if facility_type == 'gym' else '09:00-17:00',
                'holiday': '휴무'
            },
            'pricing': {
                'day_pass': 0 if facility_type in ['school', 'park'] else 5000,
                'month_pass': 0 if facility_type in ['school', 'park'] else 30000
            },
            'programs': [
                {'name': sport, 'available': True}
                for sport in sports_list
            ],
            'average_rating': round(4.0 + (i % 10) / 10, 1),
            'total_reviews': (i % 50) + 10,
            'thumbnail': f'/static/facilities/facility_{i+1}.jpg',
            'is_active': True
        }

        facilities.append(facility)

    return facilities


def extract_facility_name(address):
    """주소에서 시설명 추출"""
    # 패턴: "주소, 시설명 (동)"
    match = re.search(r',\s*([^(]+)', address)
    if match:
        return match.group(1).strip()

    # 패턴 실패 시 전체 주소 사용
    return address.split(',')[-1].strip() if ',' in address else address


def save_facilities_json(facilities, output_path='facilities_data.json'):
    """시설 데이터를 JSON 파일로 저장"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(facilities, f, ensure_ascii=False, indent=2)

    print(f"✅ 시설 데이터가 '{output_path}'에 저장되었습니다.")
    print(f"   총 시설 수: {len(facilities)}개")


def insert_facilities_to_db(facilities):
    """시설 데이터를 DB에 삽입"""
    from app.core.database import SessionLocal
    from app.models import Facility

    db = SessionLocal()

    try:
        # 기존 시설 데이터 삭제 (재생성용)
        db.query(Facility).delete()

        for fac_data in facilities:
            facility = Facility(
                name=fac_data['name'],
                facility_type=fac_data['facility_type'],
                address=fac_data['address'],
                latitude=fac_data['latitude'],
                longitude=fac_data['longitude'],
                phone=fac_data['phone'],
                website=fac_data['website'],
                has_parking=fac_data['has_parking'],
                has_shower=fac_data['has_shower'],
                has_locker=fac_data['has_locker'],
                operating_hours=fac_data['operating_hours'],
                pricing=fac_data['pricing'],
                programs=fac_data['programs'],
                average_rating=fac_data['average_rating'],
                total_reviews=fac_data['total_reviews'],
                thumbnail=fac_data['thumbnail'],
                is_active=fac_data['is_active']
            )
            db.add(facility)

        db.commit()
        print(f"✅ {len(facilities)}개 시설이 DB에 저장되었습니다.")

    except Exception as e:
        print(f"❌ DB 저장 중 에러: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🗺️  map_2k.html에서 시설 데이터 파싱 시작...\n")

    # 1. HTML 파싱
    facilities = parse_facility_html()

    print(f"✅ {len(facilities)}개 시설 데이터 파싱 완료\n")

    # 샘플 출력
    print("📋 샘플 데이터 (첫 3개):")
    for fac in facilities[:3]:
        print(f"  - {fac['name']} ({fac['facility_type_kr']})")
        print(f"    위치: {fac['address']}")
        print(f"    좌표: {fac['latitude']}, {fac['longitude']}")
        print(f"    운동: {', '.join(fac['sports'])}\n")

    # 2. JSON 저장
    save_facilities_json(facilities)

    # 3. DB에 저장
    print("\n💾 DB에 저장 중...")
    insert_facilities_to_db(facilities)

    print("\n✅ 완료!")
