import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Card } from './ui/card';
import { useState } from 'react';

interface InjuryManagementProps {
  onBack: () => void;
}

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

export function InjuryManagement({ onBack }: InjuryManagementProps) {
  const bodyParts = ['허리', '무릎', '발목', '어깨', '팔꿈치'];
  const [selectedParts, setSelectedParts] = useState<Record<string, number>>({});
  const [selectedSports, setSelectedSports] = useState<string[]>([]);
  const [hrvChange, setHrvChange] = useState<number>(0);
  const [sleepHours, setSleepHours] = useState<number>(7);
  const [heartRateChange, setHeartRateChange] = useState<string>('0');
  const [exerciseLevel, setExerciseLevel] = useState<number>(1);
  const [riskResult, setRiskResult] = useState<{
    summary: {
      highest_risk_part: string;
      highest_risk_level: string;
    };
    body_parts: {
      [key: string]: {
        score: number;
        level: string;
      };
    };
    advice: {
      detail: Array<{
        part: string;
        avoid: string[];
        recommend: string[];
        videos: Array<{
          title: string;
          url: string;
        }>;
      }>;
      age_videos: Array<{
        title: string;
        url: string;
      }>;
    };
  } | null>(null);

  const handleLevelSelect = (part: string, level: number) => {
    setSelectedParts({ ...selectedParts, [part]: level });
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

  // 레벨별 색상 반환 (정상/주의/위험/고위험)
  const getLevelColor = (level: string) => {
    switch (level) {
      case '정상':
        return 'bg-green-50 border-green-500';
      case '주의':
        return 'bg-orange-50 border-orange-500';
      case '위험':
      case '고위험':
        return 'bg-red-50 border-red-500';
      default:
        return 'bg-neutral-50 border-neutral-300';
    }
  };

  const getLevelTextColor = (level: string) => {
    switch (level) {
      case '정상':
        return 'text-green-700';
      case '주의':
        return 'text-orange-700';
      case '위험':
      case '고위험':
        return 'text-red-700';
      default:
        return 'text-neutral-700';
    }
  };

  // 부상 위험도 계산 (목업 데이터)
  const calculateRisk = () => {
    // TODO: 실제 API 호출로 대체 예정
    // 현재는 목업 데이터 사용
    
    const mockApiResponse = {
      summary: {
        highest_risk_part: '무릎',
        highest_risk_level: '위험'
      },
      body_parts: {
        '무릎': {
          score: 3.545,
          level: '위험'
        },
        '허리': {
          score: 2.1,
          level: '주의'
        }
      },
      advice: {
        detail: [
          {
            part: '무릎',
            avoid: ['깊은 스쿼트', '점프 착지', '계단 오르기', '런지', '레그익스텐션'],
            recommend: ['브릿지', '대퇴사두근 스트레칭', '햄스트링 강화'],
            videos: [
              {
                title: '무릎 완화 루틴',
                url: 'https://youtu.be/knee-relief-routine'
              }
            ]
          },
          {
            part: '허리',
            avoid: ['데드리프트', '스쿼트', '윗몸일으키기', '레그프레스', '바벨로우'],
            recommend: ['고양이 자세', '무릎 가슴 당기기', '골반 틸트 운동'],
            videos: [
              {
                title: '허리 통증 완화 루틴',
                url: 'https://youtu.be/lower-back-relief'
              }
            ]
          }
        ],
        age_videos: [
          {
            title: '성인 추천 체력 루틴',
            url: 'https://youtu.be/adult-fitness-routine'
          }
        ]
      }
    };

    setRiskResult(mockApiResponse);
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">부상 관리</h2>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-8 py-12">
        <div className="mb-8 text-center">
          <h1 className="text-neutral-900 mb-3">부상 관리 센터</h1>
          <p className="text-neutral-500">오늘의 운동과 부상 상태를 관리하세요</p>
        </div>

        <div className="space-y-6">
          {/* 주의사항 */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-orange-500 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-neutral-900 mb-2">주의사항</h4>
                <ul className="text-sm text-neutral-600 space-y-1">
                  <li>• 통증이 심할 경우 즉시 중단</li>
                  <li>• 전문의 상담 권장</li>
                  <li>• 무리하지 않기</li>
                </ul>
              </div>
            </div>
          </Card>

          {/* 오늘의 운동 */}
          <Card className="p-8 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-6">오늘의 운동</h3>
            <div className="grid grid-cols-4 gap-3">
              {sportsList.map((sport) => {
                const { main, sub } = parseSportName(sport);
                return (
                  <button
                    key={sport}
                    onClick={() => handleSportToggle(sport)}
                    className={`p-3 rounded-lg border-2 transition-colors text-center flex flex-col items-center justify-center min-h-[60px] ${
                      selectedSports.includes(sport)
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

          {/* 부위별 통증 */}
          <Card className="p-8 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-6">부위별 통증</h3>
            <div className="space-y-16">
              {bodyParts.map((part) => (
                <div key={part} className="space-y-4">
                  <div className="text-neutral-900 text-center">{part}</div>
                  <div className="flex items-center gap-4">
                    <span className="text-sm text-neutral-600">통증 없음</span>
                    <div className="flex gap-6 flex-1 justify-center">
                      {[0, 1, 2, 3].map((level) => (
                        <button
                          key={level}
                          onClick={() => handleLevelSelect(part, level)}
                          className={`w-8 h-8 rounded-full border-2 transition-all flex items-center justify-center text-sm ${
                            selectedParts[part] === level
                              ? level === 0
                                ? 'border-neutral-900 bg-neutral-200 text-neutral-900'
                                : level === 1
                                ? 'border-neutral-900 bg-neutral-400 text-white'
                                : level === 2
                                ? 'border-neutral-900 bg-neutral-600 text-white'
                                : 'border-neutral-900 bg-neutral-900 text-white'
                              : level === 0
                              ? 'border-neutral-300 bg-neutral-200 text-neutral-500'
                              : level === 1
                              ? 'border-neutral-300 bg-neutral-400 text-neutral-100'
                              : level === 2
                              ? 'border-neutral-300 bg-neutral-600 text-neutral-200'
                              : 'border-neutral-300 bg-neutral-900 text-neutral-400'
                          }`}
                        >
                          {level}
                        </button>
                      ))}
                    </div>
                    <span className="text-sm text-neutral-600">통증 정도가 높음</span>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* 피로도 */}
          <Card className="p-8 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-6">피로도</h3>
            <div className="space-y-12">
              {/* HRV 변화율 */}
              <div>
                <label className="text-neutral-900 mb-4 block">HRV 변화율</label>
                <div className="space-y-4">
                  <input
                    type="range"
                    min="-50"
                    max="20"
                    value={hrvChange}
                    onChange={(e) => setHrvChange(Number(e.target.value))}
                    className="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-neutral-900 [&::-moz-range-thumb]:w-5 [&::-moz-range-thumb]:h-5 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-neutral-900 [&::-moz-range-thumb]:border-0"
                  />
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-neutral-500">-50</span>
                    <span className="text-sm text-neutral-900 px-3 py-1 bg-neutral-100 rounded">{hrvChange}</span>
                    <span className="text-xs text-neutral-500">20</span>
                  </div>
                </div>
              </div>

              {/* 수면 시간 */}
              <div>
                <label className="text-neutral-900 mb-4 block">수면 시간</label>
                <div className="space-y-4">
                  <input
                    type="range"
                    min="0"
                    max="12"
                    step="1"
                    value={sleepHours}
                    onChange={(e) => setSleepHours(Number(e.target.value))}
                    className="w-full h-2 bg-neutral-200 rounded-lg appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-neutral-900 [&::-moz-range-thumb]:w-5 [&::-moz-range-thumb]:h-5 [&::-moz-range-thumb]:rounded-full [&::-moz-range-thumb]:bg-neutral-900 [&::-moz-range-thumb]:border-0"
                  />
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-neutral-500">0시간</span>
                    <span className="text-sm text-neutral-900 px-3 py-1 bg-neutral-100 rounded">{sleepHours}시간</span>
                    <span className="text-xs text-neutral-500">12시간</span>
                  </div>
                </div>
              </div>

              {/* 안정시 심박 변화 */}
              <div>
                <label className="text-neutral-900 mb-4 block">안정시 심박 변화</label>
                <div className="flex items-center gap-4">
                  <span className="text-xs text-neutral-500">-5</span>
                  <input
                    type="number"
                    min="-5"
                    max="20"
                    value={heartRateChange}
                    onChange={(e) => setHeartRateChange(e.target.value)}
                    className="flex-1 px-4 py-2 border border-neutral-200 rounded-lg text-center"
                    placeholder="0"
                  />
                  <span className="text-xs text-neutral-500">+20</span>
                </div>
              </div>

              {/* 운동량 비율 */}
              <div>
                <label className="text-neutral-900 mb-4 block">운동량 비율</label>
                <div className="flex items-center gap-4">
                  <span className="text-sm text-neutral-600">낮음</span>
                  <div className="flex gap-6 flex-1 justify-center">
                    {[0, 1, 2, 3].map((level) => (
                      <button
                        key={level}
                        onClick={() => setExerciseLevel(level)}
                        className={`w-8 h-8 rounded-full border-2 transition-all flex items-center justify-center text-sm ${
                          exerciseLevel === level
                            ? level === 0
                              ? 'border-neutral-900 bg-neutral-200 text-neutral-900'
                              : level === 1
                              ? 'border-neutral-900 bg-neutral-400 text-white'
                              : level === 2
                              ? 'border-neutral-900 bg-neutral-600 text-white'
                              : 'border-neutral-900 bg-neutral-900 text-white'
                            : level === 0
                            ? 'border-neutral-300 bg-neutral-200 text-neutral-500'
                            : level === 1
                            ? 'border-neutral-300 bg-neutral-400 text-neutral-100'
                            : level === 2
                            ? 'border-neutral-300 bg-neutral-600 text-neutral-200'
                            : 'border-neutral-300 bg-neutral-900 text-neutral-400'
                        }`}
                      >
                        {level}
                      </button>
                    ))}
                  </div>
                  <span className="text-sm text-neutral-600">높음</span>
                </div>
              </div>
            </div>
          </Card>

          {/* 위험도 계산하기 */}
          <Card className="p-8 border border-neutral-200 bg-white">
            {!riskResult ? (
              <button
                onClick={calculateRisk}
                className="w-full px-6 py-3 bg-neutral-900 text-white rounded-lg hover:bg-neutral-800 transition-colors"
              >
                위험도 계산하기
              </button>
            ) : (
              <div className="space-y-6">
                {/* 가장 위험한 부위 헤더 */}
                <div className="p-6 bg-red-50 border-l-4 border-red-500 rounded-lg">
                  <div className="flex items-center gap-3">
                    <AlertCircle className="w-6 h-6 text-red-600" />
                    <div>
                      <p className="text-sm text-neutral-600">가장 위험한 부위</p>
                      <p className="text-neutral-900">
                        <strong>{riskResult.summary.highest_risk_part}</strong> - {riskResult.summary.highest_risk_level}
                      </p>
                    </div>
                  </div>
                </div>

                {/* 부위별 위험도 카드 */}
                {riskResult.advice.detail.map((detail, index) => {
                  const bodyPartData = riskResult.body_parts[detail.part];
                  return (
                    <div
                      key={index}
                      className="border border-neutral-200 rounded-lg p-6 bg-white"
                    >
                      {/* 부위명 및 레벨 */}
                      <div className="flex items-center justify-between mb-6 pb-4 border-b border-neutral-200">
                        <h4 className="text-neutral-900">{detail.part} 부위</h4>
                        <span className={`px-4 py-2 rounded ${
                          bodyPartData.level === '정상'
                            ? 'bg-green-500 text-white'
                            : bodyPartData.level === '주의'
                            ? 'bg-orange-500 text-white'
                            : 'bg-red-500 text-white'
                        }`}>
                          {bodyPartData.level}
                        </span>
                      </div>

                      {/* 피할 운동 */}
                      {detail.avoid.length > 0 && (
                        <div className="mb-4 p-4 bg-neutral-50 rounded-lg">
                          <h5 className="text-sm text-neutral-900 mb-3">⚠️ 피할 운동</h5>
                          <div className="flex flex-wrap gap-2">
                            {detail.avoid.map((exercise, idx) => (
                              <span key={idx} className="px-3 py-1 bg-white border border-neutral-200 text-neutral-700 rounded text-sm">
                                {exercise}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 추천 운동 */}
                      {detail.recommend.length > 0 && (
                        <div className="mb-4 p-4 bg-neutral-50 rounded-lg">
                          <h5 className="text-sm text-neutral-900 mb-3">💪 추천 운동</h5>
                          <div className="flex flex-wrap gap-2">
                            {detail.recommend.map((exercise, idx) => (
                              <span key={idx} className="px-3 py-1 bg-white border border-neutral-200 text-neutral-700 rounded text-sm">
                                {exercise}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 완화 루틴 */}
                      {detail.videos.length > 0 && (
                        <div className="p-4 bg-neutral-50 rounded-lg">
                          <h5 className="text-sm text-neutral-900 mb-3">🎥 완화 루틴</h5>
                          <div className="space-y-2">
                            {detail.videos.map((video, idx) => (
                              <a
                                key={idx}
                                href={video.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-2 px-4 py-2 bg-neutral-900 text-white rounded-lg hover:bg-neutral-800 transition-colors text-sm"
                              >
                                {video.title} →
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}

                {/* 연령별 추천 영상 */}
                {riskResult.advice.age_videos.length > 0 && (
                  <div className="border border-neutral-200 rounded-lg p-6 bg-white">
                    <h4 className="text-neutral-900 mb-4">📺 연령별 추천 영상</h4>
                    <div className="space-y-2">
                      {riskResult.advice.age_videos.map((video, idx) => (
                        <a
                          key={idx}
                          href={video.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center gap-2 px-4 py-2 bg-neutral-900 text-white rounded-lg hover:bg-neutral-800 transition-colors text-sm"
                        >
                          {video.title} →
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {/* 다시 계산하기 */}
                <button
                  onClick={() => setRiskResult(null)}
                  className="w-full px-6 py-3 bg-neutral-100 text-neutral-900 rounded-lg hover:bg-neutral-200 transition-colors"
                >
                  다시 계산하기
                </button>
              </div>
            )}
          </Card>
        </div>
      </main>
    </div>
  );
}