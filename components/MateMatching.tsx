import { ArrowLeft, MapPin, Users } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState } from 'react';

interface MateMatchingProps {
  onBack: () => void;
}

// 한국 지역 데이터
const regionData: { [key: string]: string[] } = {
  '서울': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'],
  '경기': ['수원시', '고양시', '용인시', '성남시', '부천시', '화성시', '안산시', '남양주시', '안양시', '평택시', '시흥시', '파주시', '의정부시', '김포시', '광주시', '광명시', '군포시', '하남시', '오산시', '양주시', '이천시', '구리시', '안성시', '포천시', '의왕시', '양평군', '여주시', '동두천시', '과천시', '가평군', '연천군'],
  '인천': ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군'],
  '부산': ['중구', '서구', '동구', '영도구', '부산진구', '동래구', '남구', '북구', '해운대구', '사하구', '금정구', '강서구', '연제구', '수영구', '사상구', '기장군'],
  '대구': ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군'],
  '대전': ['동구', '중구', '서구', '유성구', '대덕구'],
  '광주': ['동구', '서구', '남구', '북구', '광산구'],
  '울산': ['중구', '남구', '동구', '북구', '울주군'],
  '세종': ['세종시'],
  '강원': ['춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시', '홍천군', '횡성군', '영월군', '평창군', '정선군', '철원군', '화천군', '양구군', '인제군', '고성군', '양양군'],
  '충북': ['청주시', '충주시', '제천시', '보은군', '옥천군', '영동군', '증평군', '진천군', '괴산군', '음성군', '단양군'],
  '충남': ['천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시', '금산군', '부여군', '서천군', '청양군', '홍성군', '예산군', '태안군'],
  '전북': ['전주시', '군산시', '익산시', '정읍시', '남원시', '김제시', '완주군', '진안군', '무주군', '장수군', '임실군', '순창군', '고창군', '부안군'],
  '전남': ['목포시', '여수시', '순천시', '나주시', '광양시', '담양군', '곡성군', '구례군', '고흥군', '보성군', '화순군', '장흥군', '강진군', '해남군', '영암군', '무안군', '함평군', '영광군', '장성군', '완도군', '진도군', '신안군'],
  '경북': ['포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시', '군위군', '의성군', '청송군', '영양군', '영덕군', '청도군', '고령군', '성주군', '칠곡군', '예천군', '봉화군', '울진군', '울릉군'],
  '경남': ['창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시', '의령군', '함안군', '창녕군', '고성군', '남해군', '하동군', '산청군', '함양군', '거창군', '합천군'],
  '제주': ['제주시', '서귀포시']
};

const fitDnaTypes = ['PFE', 'PFQ', 'PSE', 'PSQ', 'LFE', 'LFG', 'LSE', 'LSQ'];

// 60개 운동 종목 (사전순 정렬)
const sportsList = [
  '가라테', '검도', '게이트볼', '골프 (스크린골프 포함)', '국학기공', '궁도', '그라운드골프', '근대5종',
  '농구', '당구 (포켓볼 포함)', '댄스스포츠', '럭비', '레슬링', '롤러 (인라인/하키 등)', '루지', '바둑',
  '바이애슬론', '배구', '배드민턴', '보디빌딩 (헬스)', '복싱 (권투)', '볼링', '봅슬레이/스켈레톤', '빙상 (스케이트/피겨 등)',
  '사격', '산악 (등산, 클라이밍 등)', '세팍타크로', '소프트테니스 (정구)', '수상스키/웨이크보드', '수영 (수중발레, 다이빙, 수구 등)', '스쿼시', '스키/스노우보드',
  '승마', '씨름', '아이스하키', '야구/소프트볼', '양궁', '에어로빅', '역도', '요트',
  '우슈', '유도', '육상 (단거리, 중거리, 마라톤 등)', '자전거 (사이클, MTB 등)', '조정', '족구', '주짓수', '줄넘기',
  '철인3종 (트라이애슬론)', '체조 (맨손/생활체조 등)', '축구', '카누', '컬링', '탁구', '태권도', '택견',
  '테니스', '파크골프', '패러글라이딩 (행글라이딩)', '펜싱', '핀수영', '하키 (필드하키)', '합기도', '핸드볼'
];

export function MateMatching({ onBack }: MateMatchingProps) {
  const [selectedProvince, setSelectedProvince] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [selectedFitDna, setSelectedFitDna] = useState<string[]>([]);
  const [selectedSports, setSelectedSports] = useState<string[]>([]);

  const mates = [
    { name: '김운동', level: 'PFE', area: '강남구', interests: ['러닝', '헬스'] },
    { name: '이체력', level: 'PSQ', area: '서초구', interests: ['요가', '필라테스'] },
    { name: '박건강', level: 'LFE', area: '송파구', interests: ['등산', '자전거'] },
    { name: '최근력', level: 'PFQ', area: '강남구', interests: ['크로스핏', '복싱'] },
  ];

  const handleProvinceChange = (province: string) => {
    setSelectedProvince(province);
    setSelectedCity(''); // 도/시가 변경되면 행정도시 초기화
  };

  const handleFitDnaToggle = (type: string) => {
    if (selectedFitDna.includes(type)) {
      setSelectedFitDna(selectedFitDna.filter(t => t !== type));
    } else {
      setSelectedFitDna([...selectedFitDna, type]);
    }
  };

  const handleSportToggle = (sport: string) => {
    if (selectedSports.includes(sport)) {
      setSelectedSports(selectedSports.filter(s => s !== sport));
    } else {
      setSelectedSports([...selectedSports, sport]);
    }
  };

  // 운동 종목에서 메인 이름과 괄호 부분 분리
  const parseSportName = (sport: string) => {
    const match = sport.match(/^(.+?)\s(\(.+\))$/);
    if (match) {
      return {
        main: match[1],
        sub: match[2]
      };
    }
    return { main: sport, sub: null };
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-6xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">FIT-MATE</h2>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-3">FIT-MATE MATCH</h1>
          <p className="text-neutral-500">다양한 유형의 FIT-MATE를 찾아보세요</p>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Filters */}
          <div className="col-span-1">
            <Card className="p-6 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">필터</h3>
              
              {/* 지역 필터 */}
              <div className="mb-6">
                <label className="text-sm text-neutral-600 mb-2 block">지역</label>
                <select 
                  className="w-full px-3 py-2 border border-neutral-200 rounded-lg mb-2"
                  value={selectedProvince}
                  onChange={(e) => handleProvinceChange(e.target.value)}
                >
                  <option value="">도/시 선택</option>
                  {Object.keys(regionData).map((province) => (
                    <option key={province} value={province}>{province}</option>
                  ))}
                </select>
                
                {selectedProvince && (
                  <select 
                    className="w-full px-3 py-2 border border-neutral-200 rounded-lg"
                    value={selectedCity}
                    onChange={(e) => setSelectedCity(e.target.value)}
                  >
                    <option value="">시/군/구 선택</option>
                    {regionData[selectedProvince].map((city) => (
                      <option key={city} value={city}>{city}</option>
                    ))}
                  </select>
                )}
              </div>

              {/* FIT-DNA 유형 */}
              <div className="mb-6">
                <label className="text-sm text-neutral-600 mb-2 block">FIT-DNA 유형</label>
                <div className="grid grid-cols-4 gap-2">
                  {fitDnaTypes.map((type) => (
                    <button
                      key={type}
                      onClick={() => handleFitDnaToggle(type)}
                      className={`px-3 py-2 rounded-lg text-xs transition-colors ${
                        selectedFitDna.includes(type)
                          ? 'bg-neutral-900 text-white'
                          : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* 운동 종류 */}
              <div className="mb-6">
                <label className="text-sm text-neutral-600 mb-2 block">운동 종류</label>
                <div className="max-h-64 overflow-y-auto border border-neutral-200 rounded-lg p-3">
                  <div className="grid grid-cols-2 gap-2">
                    {sportsList.map((sport) => {
                      const { main, sub } = parseSportName(sport);
                      return (
                        <button
                          key={sport}
                          onClick={() => handleSportToggle(sport)}
                          className={`p-2 rounded-lg text-xs transition-colors text-center flex flex-col items-center justify-center ${
                            selectedSports.includes(sport)
                              ? 'bg-neutral-900 text-white'
                              : 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200'
                          }`}
                        >
                          <span>{main}</span>
                          {sub && (
                            <span className={`text-xs mt-0.5 ${
                              selectedSports.includes(sport) ? 'text-neutral-300' : 'text-neutral-500'
                            }`}>
                              {sub}
                            </span>
                          )}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>

              <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
                필터 적용
              </Button>
            </Card>
          </div>

          {/* Mate List */}
          <div className="col-span-2 space-y-4">
            {mates.map((mate, index) => (
              <Card key={index} className="p-6 border border-neutral-200 bg-white hover:shadow-lg transition-shadow">
                <div className="flex items-start gap-4">
                  <div className="w-16 h-16 rounded-full bg-neutral-100"></div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="text-neutral-900 mb-1">{mate.name}</h4>
                        <div className="flex items-center gap-2 text-sm text-neutral-500">
                          <span className="px-2 py-0.5 bg-neutral-900 text-white rounded text-xs">
                            {mate.level}
                          </span>
                          <span className="flex items-center gap-1">
                            <MapPin className="w-3 h-3" />
                            {mate.area}
                          </span>
                        </div>
                      </div>
                      <Button size="sm">매칭 요청</Button>
                    </div>
                    <p className="text-neutral-600 text-sm mb-3">
                      함께 운동할 메이트를 찾고 있어요! 꾸준히 운동하실 분 환영합니다 💪
                    </p>
                    <div className="flex gap-2">
                      {mate.interests.map((interest, i) => (
                        <span key={i} className="text-xs px-2 py-1 bg-neutral-50 text-neutral-600 rounded">
                          #{interest}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            ))}

            <Card className="p-8 border border-neutral-200 bg-neutral-50 text-center">
              <Users className="w-12 h-12 text-neutral-400 mx-auto mb-3" />
              <h4 className="text-neutral-900 mb-2">더 많은 메이트 보기</h4>
              <p className="text-neutral-500 text-sm mb-4">
                지역과 관심사를 설정하면 더 많은 메이트를 찾을 수 있어요
              </p>
              <Button variant="outline" className="border-neutral-200">
                더보기
              </Button>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}