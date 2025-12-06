import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState } from 'react';

interface InjuryManagementProps {
  onBack: () => void;
}

export function InjuryManagement({ onBack }: InjuryManagementProps) {
  const bodyParts = ['허리', '무릎', '발목', '어깨', '팔꿈치'];
  const [selectedParts, setSelectedParts] = useState<Record<string, number>>({});

  const handleLevelSelect = (part: string, level: number) => {
    setSelectedParts({ ...selectedParts, [part]: level });
  };

  const getLevelColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 border-green-500 text-green-700';
      case 2: return 'bg-yellow-100 border-yellow-500 text-yellow-700';
      case 3: return 'bg-red-100 border-red-500 text-red-700';
      default: return 'border-neutral-200 hover:bg-neutral-50 hover:border-neutral-900';
    }
  };

  const getLevelText = (level: number) => {
    switch (level) {
      case 1: return '경미';
      case 2: return '보통';
      case 3: return '심각';
      default: return '';
    }
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-6xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">부상 관리</h2>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-3">부상 관리 센터</h1>
          <p className="text-neutral-500">부상 부위를 선택하고 맞춤 재활 운동을 받아보세요</p>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Body Part Selection */}
          <div className="col-span-2">
            <Card className="p-8 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-6">부상 부위 선택</h3>
              <div className="space-y-12">
                {bodyParts.map((part) => (
                  <div key={part} className="space-y-3">
                    <div className="text-neutral-900 text-center">{part}</div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-neutral-600">통증 없음</span>
                      <div className="flex gap-3 flex-1 justify-center">
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

            {/* Recommended Exercises */}
            <div className="mt-6">
              <h3 className="text-neutral-900 mb-4">추천 재활 운동</h3>
              <div className="space-y-4">
                <Card className="p-5 border border-neutral-200 bg-white">
                  <div className="flex items-center gap-4">
                    <div className="w-20 h-20 bg-neutral-100 rounded-lg"></div>
                    <div className="flex-1">
                      <h4 className="text-neutral-900 mb-1">목 스트레칭</h4>
                      <p className="text-neutral-500 text-sm mb-2">경추 긴장 완화 · 10분</p>
                      <div className="flex gap-2">
                        <span className="text-xs px-2 py-1 bg-neutral-100 rounded">초급</span>
                        <span className="text-xs px-2 py-1 bg-neutral-100 rounded">스트레칭</span>
                      </div>
                    </div>
                    <Button size="sm">시작</Button>
                  </div>
                </Card>

                <Card className="p-5 border border-neutral-200 bg-white">
                  <div className="flex items-center gap-4">
                    <div className="w-20 h-20 bg-neutral-100 rounded-lg"></div>
                    <div className="flex-1">
                      <h4 className="text-neutral-900 mb-1">어깨 회전 운동</h4>
                      <p className="text-neutral-500 text-sm mb-2">회전근개 강화 · 15분</p>
                      <div className="flex gap-2">
                        <span className="text-xs px-2 py-1 bg-neutral-100 rounded">초급</span>
                        <span className="text-xs px-2 py-1 bg-neutral-100 rounded">재활</span>
                      </div>
                    </div>
                    <Button size="sm">시작</Button>
                  </div>
                </Card>
              </div>
            </div>
          </div>

          {/* Info Sidebar */}
          <div className="space-y-6">
            <Card className="p-5 border border-neutral-200 bg-white">
              <div className="flex items-start gap-3 mb-4">
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

            <Card className="p-5 border border-neutral-200 bg-white">
              <h4 className="text-neutral-900 mb-3">재활 진행도</h4>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">이번 주</span>
                    <span className="text-neutral-900">4/7일</span>
                  </div>
                  <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                    <div className="h-full bg-neutral-900 w-4/7"></div>
                  </div>
                </div>
              </div>
            </Card>

            <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
              AI 상담 받기
            </Button>
          </div>
        </div>
      </main>
    </div>
  );
}