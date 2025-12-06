import { ArrowLeft, Cloud, Sun, CloudRain } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface WeatherWorkoutProps {
  onBack: () => void;
}

export function WeatherWorkout({ onBack }: WeatherWorkoutProps) {
  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-6xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">날씨 맞춤 운동</h2>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-3">오늘의 날씨와 운동</h1>
          <p className="text-neutral-500">현재 날씨에 최적화된 운동을 추천해드립니다</p>
        </div>

        {/* Current Weather */}
        <Card className="p-8 border border-neutral-200 bg-white mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <Sun className="w-16 h-16 text-yellow-500" />
              <div>
                <h2 className="text-neutral-900 mb-2">맑음</h2>
                <p className="text-neutral-500 mb-1">서울특별시 · 오후 2:30</p>
                <p className="text-neutral-900">기온 22°C · 습도 45%</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-neutral-500 text-sm mb-2">운동하기</p>
              <p className="text-neutral-900">최적</p>
            </div>
          </div>
        </Card>

        <h3 className="text-neutral-900 mb-4">추천 야외 운동</h3>
        <div className="grid grid-cols-3 gap-6 mb-8">
          <Card className="p-6 border border-neutral-200 bg-white hover:shadow-lg transition-shadow">
            <div className="w-full h-40 bg-neutral-100 rounded-lg mb-4"></div>
            <h4 className="text-neutral-900 mb-2">공원 러닝</h4>
            <p className="text-neutral-500 text-sm mb-4">맑은 날씨, 완벽한 러닝 조건</p>
            <div className="flex gap-2 mb-4">
              <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">추천</span>
              <span className="text-xs px-2 py-1 bg-neutral-100 rounded">30분</span>
            </div>
            <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
              시작하기
            </Button>
          </Card>

          <Card className="p-6 border border-neutral-200 bg-white hover:shadow-lg transition-shadow">
            <div className="w-full h-40 bg-neutral-100 rounded-lg mb-4"></div>
            <h4 className="text-neutral-900 mb-2">자전거 라이딩</h4>
            <p className="text-neutral-500 text-sm mb-4">완벽한 사이클링 날씨</p>
            <div className="flex gap-2 mb-4">
              <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">추천</span>
              <span className="text-xs px-2 py-1 bg-neutral-100 rounded">1시간</span>
            </div>
            <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
              시작하기
            </Button>
          </Card>

          <Card className="p-6 border border-neutral-200 bg-white hover:shadow-lg transition-shadow">
            <div className="w-full h-40 bg-neutral-100 rounded-lg mb-4"></div>
            <h4 className="text-neutral-900 mb-2">등산</h4>
            <p className="text-neutral-500 text-sm mb-4">날씨가 좋은 등산 최적기</p>
            <div className="flex gap-2 mb-4">
              <span className="text-xs px-2 py-1 bg-green-100 text-green-700 rounded">추천</span>
              <span className="text-xs px-2 py-1 bg-neutral-100 rounded">2시간</span>
            </div>
            <Button className="w-full bg-neutral-900 hover:bg-neutral-800">
              시작하기
            </Button>
          </Card>
        </div>

        {/* Other Weather Conditions */}
        <h3 className="text-neutral-900 mb-4">다른 날씨별 운동</h3>
        <div className="grid grid-cols-2 gap-4">
          <Card className="p-5 border border-neutral-200 bg-white">
            <div className="flex items-center gap-4">
              <Cloud className="w-10 h-10 text-neutral-400" />
              <div className="flex-1">
                <h4 className="text-neutral-900 mb-1">흐린 날</h4>
                <p className="text-neutral-500 text-sm">실내 운동 추천</p>
              </div>
              <Button size="sm" variant="outline">보기</Button>
            </div>
          </Card>

          <Card className="p-5 border border-neutral-200 bg-white">
            <div className="flex items-center gap-4">
              <CloudRain className="w-10 h-10 text-blue-400" />
              <div className="flex-1">
                <h4 className="text-neutral-900 mb-1">비 오는 날</h4>
                <p className="text-neutral-500 text-sm">실내 홈트 추천</p>
              </div>
              <Button size="sm" variant="outline">보기</Button>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
