import { ArrowLeft, Dumbbell, Zap, Activity, Shield, Target, Music, Wind, Timer, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface FitDnaTypesProps {
  onBack: () => void;
  onStartTest?: () => void;
}

export const fitDnaTypes = [
  {
    code: 'PFE',
    nickname: '완성형 올라운더',
    description: '근력·유연성·지구력이 모두 상위에 속하는 유형',
    description2: '다양한 움직임에서 안정적으로 수치를 확보하며, 전반적인 신체 기능이 균형 있게 드러나는 타입',
    characteristics: ['Power', 'Flexibility', 'Endurance'],
    representatives: '손흥민, 크로스핏 선수',
    icon: 'Dumbbell',
  },
  {
    code: 'PFQ',
    nickname: '스피드 앨리트형',
    description: '근력과 유연성이 상위에 있어 힘을 쓰는 동작이나 몸을 크게 사용하는 동작에서 수치가 잘 나타나는 유형',
    description2: '반면 지구력 지표는 상대적으로 낮기 때문에, 짧고 집중된 활동에서 강점이 표현되는 타입',
    characteristics: ['Power', 'Flexibility', 'Quick'],
    representatives: '우사인 볼트, 체조선수',
    icon: 'Zap',
  },
  {
    code: 'PSE',
    nickname: '안정·지구력 탱커형',
    description: '근력과 지구력이 모두 상위로 나타나 지속적인 힘을 요구하는 상황에서 좋은 수치를 보여주는 유형',
    description2: '신체 가동 범위보다는 힘과 유지 능력이 돋보이는 타입',
    characteristics: ['Power', 'Stiff', 'Endurance'],
    representatives: '마라톤 선수, 사이클',
    icon: 'Shield',
  },
  {
    code: 'PSQ',
    nickname: '파워 임팩트형',
    description: '근력 지표가 상위로 나타나 힘을 활용하는 동작에서 좋은 수치를 기록하는 유형',
    description2: '순간적인 힘과 폭발력이 뛰어나, 짧고 강한 동작에 강점이 있는 타입',
    characteristics: ['Power', 'Stiff', 'Quick'],
    representatives: '역도선수, 보디빌더',
    icon: 'Target',
  },
  {
    code: 'LFE',
    nickname: '리듬·동작 미학형',
    description: '유연성과 지구력이 상위에 있어 부드럽고 지속적인 움직임에서 높은 수치가 나타나는 유형',
    description2: '힘을 크게 쓰는 동작보다는 흐름과 유지 능력이 더 두드러지는 타입',
    characteristics: ['Light', 'Flexibility', 'Endurance'],
    representatives: '발레리나, 요가 강사',
    icon: 'Music',
  },
  {
    code: 'LFG',
    nickname: '유연 동작형',
    description: '유연성 지표가 상위로 나타나는 유형',
    description2: '몸의 가동 범위나 움직임의 넓이에서 높은 수치를 보여주는 타입',
    characteristics: ['Light', 'Flexibility', 'Quick'],
    representatives: '피겨선수, 무술인',
    icon: 'Wind',
  },
  {
    code: 'LSE',
    nickname: '안정적 페이스 메이커형',
    description: '지구력 지표가 상위로 나타나 오래 지속되는 움직임에서 수치가 잘 나타나는 유형',
    description2: '근력과 유연성은 하위권으로, 꾸준히 반복하는 활동에서 강점이 드러나는 타입',
    characteristics: ['Light', 'Stiff', 'Endurance'],
    representatives: '장거리 러너, 트레일러',
    icon: 'Timer',
  },
  {
    code: 'LSQ',
    nickname: '성장 잠재력 타입',
    description: '근력 / 유연성 / 지구력 지표를 향상시켜야하는 유형',
    description2: '작은 변화를 겪으며, 실력이 늘어나는, 성장 가능성이 많은 타입',
    characteristics: ['Light', 'Stiff', 'Quick'],
    representatives: '운동 입문자',
    icon: 'TrendingUp',
  },
];

export function FitDnaTypes({ onBack, onStartTest }: FitDnaTypesProps) {
  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      {onBack && (
        <header className="bg-white border-b border-neutral-200">
          <div className="max-w-7xl mx-auto px-8 py-4 flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={onBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="text-neutral-900">FIT-DNA 8가지 유형</h1>
          </div>
        </header>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        {/* Introduction */}
        <div className="mb-12 text-center">
          <h1 className="text-neutral-900 mb-3">8가지 FIT-DNA 유형</h1>
          <p className="text-neutral-500">
            근력지표, 가동범위, 지속성의 조합으로 구성된 당신만의 체력 유형을 확인하세요
          </p>
        </div>

        {/* Type Categories Legend */}
        <div className="mb-8">
          <Card className="p-6 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-4">유형 구성 요소</h3>
            <div className="grid grid-cols-3 gap-6">
              <div>
                <p className="text-neutral-700 mb-2">근력지표</p>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-neutral-900 text-white rounded text-sm">Power</span>
                  <span className="px-3 py-1 bg-neutral-200 text-neutral-700 rounded text-sm">Light</span>
                </div>
              </div>
              <div>
                <p className="text-neutral-700 mb-2">가동범위</p>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-neutral-900 text-white rounded text-sm">Flexibility</span>
                  <span className="px-3 py-1 bg-neutral-200 text-neutral-700 rounded text-sm">Stiff</span>
                </div>
              </div>
              <div>
                <p className="text-neutral-700 mb-2">지속성</p>
                <div className="flex gap-2">
                  <span className="px-3 py-1 bg-neutral-900 text-white rounded text-sm">Endurance</span>
                  <span className="px-3 py-1 bg-neutral-200 text-neutral-700 rounded text-sm">Quick</span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Type Cards Grid */}
        <div className="grid grid-cols-2 gap-6">
          {fitDnaTypes.map((type) => {
            const IconComponent = type.icon === 'Dumbbell' ? Dumbbell : 
                                 type.icon === 'Zap' ? Zap : 
                                 type.icon === 'Activity' ? Activity : 
                                 type.icon === 'Shield' ? Shield : 
                                 type.icon === 'Target' ? Target : 
                                 type.icon === 'Music' ? Music : 
                                 type.icon === 'Wind' ? Wind : 
                                 type.icon === 'Timer' ? Timer : TrendingUp;
            
            return (
              <Card 
                key={type.code} 
                className="p-8 border border-neutral-200 bg-white hover:shadow-lg transition-shadow cursor-pointer"
              >
                <div className="flex items-start gap-6 mb-6">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-3">
                      <h2 className="text-neutral-900">{type.code}</h2>
                      <span className="px-3 py-1 bg-neutral-100 rounded-full text-neutral-700">
                        {type.nickname}
                      </span>
                    </div>
                    <p className="text-neutral-600 text-sm mb-2">{type.description}</p>
                    <p className="text-neutral-500 text-sm">{type.description2}</p>
                  </div>
                  <div className="w-16 h-16 flex-shrink-0 rounded-full bg-neutral-100 flex items-center justify-center">
                    <IconComponent className="w-6 h-6 text-neutral-700" />
                  </div>
                </div>

                {/* Characteristics */}
                <div className="mb-6">
                  <p className="text-neutral-500 text-sm mb-3">특성 조합</p>
                  <div className="flex flex-wrap gap-2">
                    {type.characteristics.map((char, index) => (
                      <span 
                        key={index}
                        className={`px-3 py-1 rounded text-sm ${
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

                {/* Representatives */}
                <div className="pt-6 border-t border-neutral-100">
                  <p className="text-neutral-500 text-sm mb-2">대표 인물/스포츠</p>
                  <p className="text-neutral-700">{type.representatives}</p>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="mt-12 text-center">
          <Card className="p-8 bg-neutral-900 text-white border-0 inline-block">
            <h3 className="text-white mb-3">나의 FIT-DNA 유형이 궁금하다면?</h3>
            <p className="text-white/70 mb-6">
              국민체력100 데이터 기반으로 당신의 체력 유형을 분석해드립니다
            </p>
            <Button className="bg-white text-neutral-900 hover:bg-white/90" onClick={onStartTest}>
              테스트 시작하기
            </Button>
          </Card>
        </div>
      </main>
    </div>
  );
}