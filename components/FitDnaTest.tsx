import { ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState, useEffect } from 'react';
import { fitDnaTypes } from './FitDnaTypes';
import { Dumbbell, Zap, Activity, Shield, Target, Music, Wind, Timer, TrendingUp } from 'lucide-react';

interface FitDnaTestProps {
  onBack: () => void;
}

interface UserInfo {
  name: string;
  birthdate: string;
  gender: string;
  province: string;
  city: string;
  weight: string;
  height: string;
}

interface FitnessData {
  gripLeft: string;
  gripRight: string;
  sitUp: string;
  repeatJump: string;
  sitReach: string;
  crossSitUp: string;
  shuttle: string;
  standingJump: string;
  chairStand: string;
  absoluteGrip: string;
}

interface Preference {
  sports: string[];
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

export function FitDnaTest({ onBack }: FitDnaTestProps) {
  const [step, setStep] = useState(0);
  const [userInfo, setUserInfo] = useState<UserInfo>({
    name: '',
    birthdate: '',
    gender: '',
    province: '',
    city: '',
    weight: '',
    height: ''
  });
  const [fitnessData, setFitnessData] = useState<FitnessData>({
    gripLeft: '',
    gripRight: '',
    sitUp: '',
    repeatJump: '',
    sitReach: '',
    crossSitUp: '',
    shuttle: '',
    standingJump: '',
    chairStand: '',
    absoluteGrip: ''
  });
  const [preference, setPreference] = useState<Preference>({
    sports: []
  });

  // 회원가입 정보에서 생년월일과 성별 불러오기
  useEffect(() => {
    const savedUserData = localStorage.getItem('userData');
    if (savedUserData) {
      const userData = JSON.parse(savedUserData);
      if (userData.birthdate && userData.gender) {
        setUserInfo(prev => ({
          ...prev,
          birthdate: userData.birthdate,
          gender: userData.gender === '남자' ? '남성' : userData.gender === '여자' ? '여성' : userData.gender
        }));
      }
    }
  }, []);

  const handleProvinceChange = (province: string) => {
    setUserInfo({
      ...userInfo,
      province,
      city: '' // 도/시가 변경되면 행정도시 초기화
    });
  };

  const handleSportToggle = (sport: string) => {
    if (preference.sports.includes(sport)) {
      setPreference({
        ...preference,
        sports: preference.sports.filter(s => s !== sport)
      });
    } else {
      setPreference({
        ...preference,
        sports: [...preference.sports, sport]
      });
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

  const canProceed = () => {
    if (step === 0) {
      return userInfo.name && userInfo.birthdate && userInfo.gender && 
             userInfo.province && userInfo.city && userInfo.weight && userInfo.height;
    }
    if (step === 1) {
      return fitnessData.gripLeft && fitnessData.gripRight && fitnessData.sitUp && 
             fitnessData.repeatJump && fitnessData.sitReach && fitnessData.crossSitUp &&
             fitnessData.shuttle && fitnessData.standingJump && fitnessData.chairStand &&
             fitnessData.absoluteGrip;
    }
    if (step === 2) {
      return preference.sports.length > 0;
    }
    return false;
  };

  const handleSubmit = () => {
    // 나중에 모델 파일을 통해 FIT-DNA 분류
    const testData = {
      userInfo,
      fitnessData,
      preference,
      completedAt: new Date().toISOString()
    };
    localStorage.setItem('fitDnaTestData', JSON.stringify(testData));
    
    // TODO: 모델링을 통해 실제 FIT-DNA 유형 결정
    // 지금은 임시로 PFE로 설정
    localStorage.setItem('fitDnaResult', 'PFE');
    
    // 결과 화면으로 이동
    setStep(3);
  };

  if (step === 0) {
    return (
      <div className="min-h-screen bg-neutral-50">
        <header className="bg-white border-b border-neutral-200">
          <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
            <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
              <ArrowLeft className="w-5 h-5 text-neutral-700" />
            </button>
            <h2 className="text-neutral-900">FIT-DNA 테스트</h2>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-8 py-12">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">1</div>
              <div className="flex-1 h-1 bg-neutral-200"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-200 text-neutral-400 flex items-center justify-center text-sm">2</div>
              <div className="flex-1 h-1 bg-neutral-200"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-200 text-neutral-400 flex items-center justify-center text-sm">3</div>
            </div>
            <h1 className="text-neutral-900 mb-2">기본 정보 입력</h1>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="space-y-6">
              {/* 이름 */}
              <div>
                <label className="block text-neutral-900 mb-3">이름</label>
                <input
                  type="text"
                  value={userInfo.name}
                  onChange={(e) => setUserInfo({ ...userInfo, name: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  placeholder="이름을 입력하세요"
                />
              </div>

              {/* 생년월일 */}
              <div>
                <label className="block text-neutral-900 mb-3">생년월일</label>
                <input
                  type="date"
                  value={userInfo.birthdate}
                  onChange={(e) => setUserInfo({ ...userInfo, birthdate: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                />
              </div>

              {/* 성별 */}
              <div>
                <label className="block text-neutral-900 mb-3">성별</label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => setUserInfo({ ...userInfo, gender: '남성' })}
                    className={`p-4 rounded-lg border-2 transition-colors ${
                      userInfo.gender === '남성'
                        ? 'border-neutral-900 bg-neutral-50'
                        : 'border-neutral-200 hover:border-neutral-300'
                    }`}
                  >
                    <span className="text-neutral-900">남성</span>
                  </button>
                  <button
                    onClick={() => setUserInfo({ ...userInfo, gender: '여성' })}
                    className={`p-4 rounded-lg border-2 transition-colors ${
                      userInfo.gender === '여성'
                        ? 'border-neutral-900 bg-neutral-50'
                        : 'border-neutral-200 hover:border-neutral-300'
                    }`}
                  >
                    <span className="text-neutral-900">여성</span>
                  </button>
                </div>
              </div>

              {/* 지역 */}
              <div>
                <label className="block text-neutral-900 mb-3">지역</label>
                <select 
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg mb-2 focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  value={userInfo.province}
                  onChange={(e) => handleProvinceChange(e.target.value)}
                >
                  <option value="">도/시 선택</option>
                  {Object.keys(regionData).map((province) => (
                    <option key={province} value={province}>{province}</option>
                  ))}
                </select>
                
                {userInfo.province && (
                  <select 
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                    value={userInfo.city}
                    onChange={(e) => setUserInfo({ ...userInfo, city: e.target.value })}
                  >
                    <option value="">시/군/구 선택</option>
                    {regionData[userInfo.province].map((city) => (
                      <option key={city} value={city}>{city}</option>
                    ))}
                  </select>
                )}
              </div>

              {/* 체중 */}
              <div>
                <label className="block text-neutral-900 mb-3">체중 (kg)</label>
                <input
                  type="number"
                  value={userInfo.weight}
                  onChange={(e) => setUserInfo({ ...userInfo, weight: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  placeholder="체중을 입력하세요"
                />
              </div>

              {/* 신장 */}
              <div>
                <label className="block text-neutral-900 mb-3">신장 (cm)</label>
                <input
                  type="number"
                  value={userInfo.height}
                  onChange={(e) => setUserInfo({ ...userInfo, height: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                  placeholder="신장을 입력하세요"
                />
              </div>
            </div>
          </Card>

          <Button 
            className="w-full bg-neutral-900 hover:bg-neutral-800"
            onClick={() => setStep(1)}
            disabled={!canProceed()}
          >
            다음
          </Button>
        </main>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="min-h-screen bg-neutral-50">
        <header className="bg-white border-b border-neutral-200">
          <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
            <button onClick={() => setStep(0)} className="p-2 hover:bg-neutral-100 rounded-lg">
              <ArrowLeft className="w-5 h-5 text-neutral-700" />
            </button>
            <h2 className="text-neutral-900">FIT-DNA 테스트</h2>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-8 py-12">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">✓</div>
              <div className="flex-1 h-1 bg-neutral-900"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">2</div>
              <div className="flex-1 h-1 bg-neutral-200"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-200 text-neutral-400 flex items-center justify-center text-sm">3</div>
            </div>
            <h1 className="text-neutral-900 mb-2">체력 측정 데이터</h1>
            <p className="text-neutral-500">국민체력100 검사 결과 입력</p>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="space-y-6">
              {/* 악력 (왼손) */}
              <div>
                <label className="block text-neutral-900 mb-3">악력 (왼손) (kg)</label>
                <input
                  type="number"
                  value={fitnessData.gripLeft}
                  onChange={(e) => setFitnessData({ ...fitnessData, gripLeft: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 악력 (오른손) */}
              <div>
                <label className="block text-neutral-900 mb-3">악력 (오른손) (kg)</label>
                <input
                  type="number"
                  value={fitnessData.gripRight}
                  onChange={(e) => setFitnessData({ ...fitnessData, gripRight: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 윗몸말아올리기 */}
              <div>
                <label className="block text-neutral-900 mb-3">윗몸말아올리기 (회)</label>
                <input
                  type="number"
                  value={fitnessData.sitUp}
                  onChange={(e) => setFitnessData({ ...fitnessData, sitUp: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 반복점프 */}
              <div>
                <label className="block text-neutral-900 mb-3">반복점프 (회)</label>
                <input
                  type="number"
                  value={fitnessData.repeatJump}
                  onChange={(e) => setFitnessData({ ...fitnessData, repeatJump: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 앉아윗몸앞굽히기 */}
              <div>
                <label className="block text-neutral-900 mb-3">앉아윗몸앞굽히기 (cm)</label>
                <input
                  type="number"
                  value={fitnessData.sitReach}
                  onChange={(e) => setFitnessData({ ...fitnessData, sitReach: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 교차윗몸일으키기 */}
              <div>
                <label className="block text-neutral-900 mb-3">교차윗몸일으키기 (회)</label>
                <input
                  type="number"
                  value={fitnessData.crossSitUp}
                  onChange={(e) => setFitnessData({ ...fitnessData, crossSitUp: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 왕복오래달리기 */}
              <div>
                <label className="block text-neutral-900 mb-3">왕복오래달리기 (회)</label>
                <input
                  type="number"
                  value={fitnessData.shuttle}
                  onChange={(e) => setFitnessData({ ...fitnessData, shuttle: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 제자리 멀리뛰기 */}
              <div>
                <label className="block text-neutral-900 mb-3">제자리 멀리뛰기 (cm)</label>
                <input
                  type="number"
                  value={fitnessData.standingJump}
                  onChange={(e) => setFitnessData({ ...fitnessData, standingJump: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 의자 일어서기 */}
              <div>
                <label className="block text-neutral-900 mb-3">의자 일어서기 (회)</label>
                <input
                  type="number"
                  value={fitnessData.chairStand}
                  onChange={(e) => setFitnessData({ ...fitnessData, chairStand: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 절대 악력 (양손 악력의 평균) */}
              <div>
                <label className="block text-neutral-900 mb-3">절대 악력 (양손 악력의 평균) (kg)</label>
                {/* TODO: 나중에 수정할 예정 - 왼손/오른손 악력 평균 자동 계산 */}
                <input
                  type="number"
                  value={fitnessData.absoluteGrip}
                  onChange={(e) => setFitnessData({ ...fitnessData, absoluteGrip: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>
            </div>
          </Card>

          <Button 
            className="w-full bg-neutral-900 hover:bg-neutral-800"
            onClick={() => setStep(2)}
            disabled={!canProceed()}
          >
            다음
          </Button>
        </main>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="min-h-screen bg-neutral-50">
        <header className="bg-white border-b border-neutral-200">
          <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
            <button onClick={() => setStep(1)} className="p-2 hover:bg-neutral-100 rounded-lg">
              <ArrowLeft className="w-5 h-5 text-neutral-700" />
            </button>
            <h2 className="text-neutral-900">FIT-DNA 테스트</h2>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-8 py-12">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">✓</div>
              <div className="flex-1 h-1 bg-neutral-900"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">✓</div>
              <div className="flex-1 h-1 bg-neutral-900"></div>
              <div className="w-8 h-8 rounded-full bg-neutral-900 text-white flex items-center justify-center text-sm">3</div>
            </div>
            <h1 className="text-neutral-900 mb-2">선호 운동</h1>
            <p className="text-neutral-500">선호하는 운동을 여러 개 선택해주세요.</p>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="grid grid-cols-4 gap-3">
              {sportsList.map((sport) => {
                const { main, sub } = parseSportName(sport);
                return (
                  <button
                    key={sport}
                    onClick={() => handleSportToggle(sport)}
                    className={`p-3 rounded-lg border-2 transition-colors text-center flex flex-col items-center justify-center min-h-[60px] ${
                      preference.sports.includes(sport)
                        ? 'border-neutral-900 bg-neutral-50'
                        : 'border-neutral-200 hover:border-neutral-300'
                    }`}
                  >
                    <span className="text-neutral-900 text-sm">{main}</span>
                    {sub && <span className="text-neutral-600 text-xs mt-0.5">{sub}</span>}
                  </button>
                );
              })}
            </div>
          </Card>

          <Button 
            className="w-full bg-neutral-900 hover:bg-neutral-800"
            onClick={handleSubmit}
            disabled={!canProceed()}
          >
            결과 보기
          </Button>
        </main>
      </div>
    );
  }

  // Step 3: 결과 화면
  if (step === 3) {
    const resultCode = localStorage.getItem('fitDnaResult') || 'PFE';
    const myType = fitDnaTypes.find(type => type.code === resultCode);

    if (!myType) return null;

    const IconComponent = myType.icon === 'Dumbbell' ? Dumbbell : 
                         myType.icon === 'Zap' ? Zap : 
                         myType.icon === 'Activity' ? Activity : 
                         myType.icon === 'Shield' ? Shield : 
                         myType.icon === 'Target' ? Target : 
                         myType.icon === 'Music' ? Music : 
                         myType.icon === 'Wind' ? Wind : 
                         myType.icon === 'Timer' ? Timer : TrendingUp;

    return (
      <div className="min-h-screen bg-neutral-50">
        <header className="bg-white border-b border-neutral-200">
          <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
            <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
              <ArrowLeft className="w-5 h-5 text-neutral-700" />
            </button>
            <h2 className="text-neutral-900">FIT-DNA 테스트 결과</h2>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-8 py-12">
          {/* 결과 안내 */}
          <div className="text-center mb-8">
            <div className="inline-block px-4 py-1.5 bg-neutral-900 text-white rounded-full text-sm mb-4">
              나의 FIT-DNA 유형
            </div>
            <h1 className="text-neutral-900 mb-3">테스트 결과가 나왔습니다!</h1>
            <p className="text-neutral-500">
              당신의 체력 유형을 확인해보세요
            </p>
          </div>

          {/* FIT-DNA 유형 카드 */}
          <Card className="p-10 border-2 border-neutral-900 bg-white mb-8">
            <div className="flex items-start gap-8 mb-8">
              <div className="flex-1">
                <div className="flex items-center gap-4 mb-4">
                  <h2 className="text-neutral-900">{myType.code}</h2>
                  <span className="px-4 py-1.5 bg-neutral-100 rounded-full text-neutral-700">
                    {myType.nickname}
                  </span>
                </div>
                <p className="text-neutral-600 mb-3">{myType.description}</p>
                <p className="text-neutral-500">{myType.description2}</p>
              </div>
              <div className="w-20 h-20 flex-shrink-0 rounded-full bg-neutral-900 flex items-center justify-center">
                <IconComponent className="w-8 h-8 text-white" />
              </div>
            </div>

            {/* 특성 조합 */}
            <div className="mb-8 pb-8 border-b border-neutral-100">
              <p className="text-neutral-500 text-sm mb-4">특성 조합</p>
              <div className="flex flex-wrap gap-3">
                {myType.characteristics.map((char, index) => (
                  <span 
                    key={index}
                    className={`px-4 py-2 rounded ${
                      char === 'Power' || char === 'Flexibility' || char === 'Endurance'
                        ? 'bg-neutral-900 text-white'
                        : 'bg-neutral-200 text-neutral-700'
                    }`}
                  >
                    {char}
                  </span>
                ))}
              </div>
            </div>

            {/* 대표 인물/스포츠 */}
            <div>
              <p className="text-neutral-500 text-sm mb-3">대표 인물/스포츠</p>
              <p className="text-neutral-700 text-lg">{myType.representatives}</p>
            </div>
          </Card>

          {/* 액션 버튼 */}
          <div className="flex gap-4">
            <Button 
              variant="outline"
              className="flex-1 border-neutral-200"
              onClick={() => setStep(0)}
            >
              다시 테스트하기
            </Button>
            <Button 
              className="flex-1 bg-neutral-900 hover:bg-neutral-800"
              onClick={onBack}
            >
              홈으로 돌아가기
            </Button>
          </div>
        </main>
      </div>
    );
  }

  // Overview screen
  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">FIT-DNA 테스트</h2>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-8 py-12">
        <div className="text-center mb-12">
          <div className="inline-block px-4 py-1.5 bg-neutral-900 text-white rounded-full text-sm mb-6">
            체력 MBTI
          </div>
          <h1 className="text-neutral-900 mb-4">나의 FIT-DNA를 찾아보세요</h1>
          <p className="text-neutral-500">
            국민체력100 데이터 기반으로 당신의 체력 유형을 분석합니다
          </p>
        </div>

        <div className="space-y-4 mb-12">
          <Card 
            className="p-6 border border-neutral-200 bg-white cursor-pointer hover:border-neutral-300 transition-colors"
            onClick={() => setStep(0)}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neutral-900 text-white flex items-center justify-center">
                  1
                </div>
                <div>
                  <h3 className="text-neutral-900 mb-1">기본 정보 입력</h3>
                  <p className="text-neutral-500 text-sm">이름, 생년월일, 성별, 지역, 체중, 신장</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-neutral-200 bg-white opacity-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 flex items-center justify-center">
                  2
                </div>
                <div>
                  <h3 className="text-neutral-500 mb-1">체력 측정 데이터</h3>
                  <p className="text-neutral-400 text-sm">국민체력100 검사 결과</p>
                </div>
              </div>
            </div>
          </Card>

          <Card className="p-6 border border-neutral-200 bg-white opacity-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-neutral-100 text-neutral-400 flex items-center justify-center">
                  3
                </div>
                <div>
                  <h3 className="text-neutral-500 mb-1">선호 운동</h3>
                  <p className="text-neutral-400 text-sm">선호하는 운동 종목</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <Button 
          className="w-full bg-neutral-900 hover:bg-neutral-800"
          onClick={() => setStep(0)}
        >
          테스트 시작하기
        </Button>
      </main>
    </div>
  );
}