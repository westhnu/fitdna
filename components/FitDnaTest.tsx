import { ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState, useEffect } from 'react';

interface FitDnaTestProps {
  onBack: () => void;
}

interface UserInfo {
  birthdate: string;
  gender: string;
  weight: string;
  height: string;
}

interface FitnessData {
  grip: string;
  sitUp: string;
  sitReach: string;
  standing: string;
  shuttle: string;
}

interface Preference {
  workoutType: string[];
  goal: string[];
  frequency: string;
  customWorkoutType?: string;
}

export function FitDnaTest({ onBack }: FitDnaTestProps) {
  const [step, setStep] = useState(0);
  const [userInfo, setUserInfo] = useState<UserInfo>({
    birthdate: '',
    gender: '',
    weight: '',
    height: ''
  });
  const [fitnessData, setFitnessData] = useState<FitnessData>({
    grip: '',
    sitUp: '',
    sitReach: '',
    standing: '',
    shuttle: ''
  });
  const [preference, setPreference] = useState<Preference>({
    workoutType: [],
    goal: [],
    frequency: ''
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

  const handleWorkoutTypeToggle = (type: string) => {
    if (preference.workoutType.includes(type)) {
      setPreference({
        ...preference,
        workoutType: preference.workoutType.filter(t => t !== type)
      });
    } else {
      setPreference({
        ...preference,
        workoutType: [...preference.workoutType, type]
      });
    }
  };

  const handleGoalToggle = (goal: string) => {
    if (preference.goal.includes(goal)) {
      setPreference({
        ...preference,
        goal: preference.goal.filter(t => t !== goal)
      });
    } else {
      setPreference({
        ...preference,
        goal: [...preference.goal, goal]
      });
    }
  };

  const canProceed = () => {
    if (step === 0) {
      return userInfo.birthdate && userInfo.gender && userInfo.weight && userInfo.height;
    }
    if (step === 1) {
      return fitnessData.grip && fitnessData.sitUp && fitnessData.sitReach && 
             fitnessData.standing && fitnessData.shuttle;
    }
    if (step === 2) {
      return preference.workoutType.length > 0 && preference.goal.length > 0 && preference.frequency;
    }
    return false;
  };

  const handleSubmit = () => {
    // 나중에 모델 파일을 통해 FIT-DNA 분류
    // 지금은 로컬 스토리지에 저장
    const testData = {
      userInfo,
      fitnessData,
      preference,
      completedAt: new Date().toISOString()
    };
    localStorage.setItem('fitDnaTestData', JSON.stringify(testData));
    alert('FIT-DNA 테스트가 완료되었습니다!\n(모델 분석 기능은 추후 추가 예정)');
    onBack();
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
            <p className="text-neutral-500">당신에 대해 알려주세요</p>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="space-y-6">
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

              {/* 체중 */}
              <div>
                <label className="block text-neutral-900 mb-3">체중 (kg)</label>
                <input
                  type="number"
                  value={userInfo.weight}
                  onChange={(e) => setUserInfo({ ...userInfo, weight: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
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
            <p className="text-neutral-500">국민체력100 기준 측정값을 입력해주세요</p>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="space-y-6">
              {/* 악력 */}
              <div>
                <label className="block text-neutral-900 mb-2">악력 (kg)</label>
                <p className="text-neutral-500 text-sm mb-3">근력 측정 - 양손 악력의 평균</p>
                <input
                  type="number"
                  value={fitnessData.grip}
                  onChange={(e) => setFitnessData({ ...fitnessData, grip: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 윗몸일으키기 */}
              <div>
                <label className="block text-neutral-900 mb-2">윗몸일으키기 (회/분)</label>
                <p className="text-neutral-500 text-sm mb-3">근지구력 측정 - 1분간 횟수</p>
                <input
                  type="number"
                  value={fitnessData.sitUp}
                  onChange={(e) => setFitnessData({ ...fitnessData, sitUp: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 앉아 윗몸 앞으로 굽히기 */}
              <div>
                <label className="block text-neutral-900 mb-2">앉아 윗몸 앞으로 굽히기 (cm)</label>
                <p className="text-neutral-500 text-sm mb-3">유연성 측정</p>
                <input
                  type="number"
                  value={fitnessData.sitReach}
                  onChange={(e) => setFitnessData({ ...fitnessData, sitReach: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 제자리멀리뛰기 */}
              <div>
                <label className="block text-neutral-900 mb-2">제자리멀리뛰기 (cm)</label>
                <p className="text-neutral-500 text-sm mb-3">순발력 측정</p>
                <input
                  type="number"
                  value={fitnessData.standing}
                  onChange={(e) => setFitnessData({ ...fitnessData, standing: e.target.value })}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 왕복오래달리기 */}
              <div>
                <label className="block text-neutral-900 mb-2">왕복오래달리기 (회)</label>
                <p className="text-neutral-500 text-sm mb-3">심폐지구력 측정 - 20m 왕복 횟수</p>
                <input
                  type="number"
                  value={fitnessData.shuttle}
                  onChange={(e) => setFitnessData({ ...fitnessData, shuttle: e.target.value })}
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
            <h1 className="text-neutral-900 mb-2">운동 선호도</h1>
            <p className="text-neutral-500">선호하는 운동 스타일과 목표를 선택해주세요</p>
          </div>

          <Card className="p-8 border border-neutral-200 bg-white mb-6">
            <div className="space-y-12">
              {/* 선호하는 운동 유형 (복수 선택) */}
              <div>
                <label className="block text-neutral-900 mb-4">선호하는 운동 유형 (복수 선택 가능)</label>
                <div className="grid grid-cols-3 gap-3 mb-4">
                  {['근력 운동', '유산소 운동', '요가/필라테스', '크로스핏', '수영', '구기 종목', '등산/트레킹', '사이클링', '기타'].map((type) => (
                    <button
                      key={type}
                      onClick={() => handleWorkoutTypeToggle(type)}
                      className={`p-3 rounded-lg border-2 transition-colors text-center ${
                        preference.workoutType.includes(type)
                          ? 'border-neutral-900 bg-neutral-50'
                          : 'border-neutral-200 hover:border-neutral-300'
                      }`}
                    >
                      <span className="text-neutral-900">{type}</span>
                    </button>
                  ))}
                </div>
                {/* 기타 입력 필드 */}
                {preference.workoutType.includes('기타') && (
                  <input
                    type="text"
                    value={preference.customWorkoutType || ''}
                    onChange={(e) => setPreference({ ...preference, customWorkoutType: e.target.value })}
                    placeholder="기타 운동 유형을 입력해주세요"
                    className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
                  />
                )}
              </div>

              {/* 운동 목표 */}
              <div>
                <label className="block text-neutral-900 mb-4">운동 목표 (복수 선택 가능)</label>
                <div className="grid grid-cols-3 gap-3">
                  {['체중 감량', '근육 증가', '체력 향상', '유연성 개선', '건강 유지', '스트레스 해소'].map((goal) => (
                    <button
                      key={goal}
                      onClick={() => handleGoalToggle(goal)}
                      className={`p-3 rounded-lg border-2 transition-colors text-center ${
                        preference.goal.includes(goal)
                          ? 'border-neutral-900 bg-neutral-50'
                          : 'border-neutral-200 hover:border-neutral-300'
                      }`}
                    >
                      <span className="text-neutral-900">{goal}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* 운동 빈도 */}
              <div>
                <label className="block text-neutral-900 mb-4">주당 운동 빈도</label>
                <div className="grid grid-cols-4 gap-3">
                  {['주 1-2회', '주 3-4회', '주 5-6회', '매일'].map((freq) => (
                    <button
                      key={freq}
                      onClick={() => setPreference({ ...preference, frequency: freq })}
                      className={`p-3 rounded-lg border-2 transition-colors text-center ${
                        preference.frequency === freq
                          ? 'border-neutral-900 bg-neutral-50'
                          : 'border-neutral-200 hover:border-neutral-300'
                      }`}
                    >
                      <span className="text-neutral-900">{freq}</span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          <Button 
            className="w-full bg-neutral-900 hover:bg-neutral-800"
            onClick={handleSubmit}
            disabled={!canProceed()}
          >
            테스트 완료
          </Button>
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
                  <p className="text-neutral-500 text-sm">나이, 성별, 체중, 신장</p>
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
                  <p className="text-neutral-400 text-sm">근력, 유연성, 지구력, 순발력</p>
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
                  <h3 className="text-neutral-500 mb-1">운동 선호도</h3>
                  <p className="text-neutral-400 text-sm">선호하는 운동 유형과 목표</p>
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