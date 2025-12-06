import { ArrowLeft, Clock, Flame } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface WorkoutRecommendationProps {
  onBack: () => void;
}

export function WorkoutRecommendation({ onBack }: WorkoutRecommendationProps) {
  const workouts = [
    {
      title: '상체 근력 강화 루틴',
      duration: '30분',
      calories: '250kcal',
      level: '초급',
      exercises: ['푸시업', '덤벨 컬', '숄더 프레스']
    },
    {
      title: '하체 집중 운동',
      duration: '40분',
      calories: '300kcal',
      level: '중급',
      exercises: ['스쿼트', '런지', '레그 프레스']
    },
    {
      title: '전신 유산소 운동',
      duration: '45분',
      calories: '400kcal',
      level: '초급',
      exercises: ['버피', '마운틴 클라이머', '점핑잭']
    },
    {
      title: '코어 강화 프로그램',
      duration: '25분',
      calories: '180kcal',
      level: '중급',
      exercises: ['플랭크', '크런치', '레그 레이즈']
    }
  ];

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-6xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">운동 추천</h2>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-3">맞춤 운동 프로그램</h1>
          <p className="text-neutral-500">당신의 체력 수준과 목표에 맞는 운동을 추천해드립니다</p>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2 mb-8">
          <Button variant="default" className="bg-neutral-900">전체</Button>
          <Button variant="outline" className="border-neutral-200">근력</Button>
          <Button variant="outline" className="border-neutral-200">유산소</Button>
          <Button variant="outline" className="border-neutral-200">유연성</Button>
          <Button variant="outline" className="border-neutral-200">다이어트</Button>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {workouts.map((workout, index) => (
            <Card key={index} className="p-6 border border-neutral-200 bg-white hover:shadow-lg transition-shadow">
              <div className="mb-4">
                <div className="w-full h-40 bg-neutral-100 rounded-lg mb-4"></div>
                <h3 className="text-neutral-900 mb-2">{workout.title}</h3>
                <div className="flex items-center gap-4 text-sm text-neutral-500 mb-3">
                  <span className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {workout.duration}
                  </span>
                  <span className="flex items-center gap-1">
                    <Flame className="w-4 h-4" />
                    {workout.calories}
                  </span>
                  <span className="px-2 py-0.5 bg-neutral-100 rounded text-xs">
                    {workout.level}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 mb-4">
                  {workout.exercises.map((exercise, i) => (
                    <span key={i} className="text-xs text-neutral-600 bg-neutral-50 px-2 py-1 rounded">
                      {exercise}
                    </span>
                  ))}
                </div>
              </div>
              <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
                운동 시작하기
              </Button>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}
