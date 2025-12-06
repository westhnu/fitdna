import { ArrowLeft, Search, Filter, Dumbbell, TrendingUp, Clock, Target } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Input } from './ui/input';

interface WorkoutMainProps {
  onBack: () => void;
}

export function WorkoutMain({ onBack }: WorkoutMainProps) {
  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="text-neutral-900">운동</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        {/* Search Bar */}
        <div className="mb-8 flex gap-3">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-neutral-400" />
            <Input 
              placeholder="운동 검색..." 
              className="pl-10 border-neutral-200"
            />
          </div>
          <Button variant="outline" className="border-neutral-200">
            <Filter className="w-4 h-4 mr-2" />
            필터
          </Button>
        </div>

        <div className="grid grid-cols-3 gap-6">
          {/* Left Column - Categories */}
          <div className="col-span-2 space-y-6">
            <div>
              <h2 className="text-neutral-900 mb-4">운동 카테고리</h2>
              <div className="grid grid-cols-2 gap-4">
                <Card className="p-6 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center">
                      <Dumbbell className="w-6 h-6 text-neutral-700" />
                    </div>
                    <div>
                      <h3 className="text-neutral-900 mb-1">근력 운동</h3>
                      <p className="text-neutral-500 text-sm">기구 및 맨몸 운동</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-6 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center">
                      <TrendingUp className="w-6 h-6 text-neutral-700" />
                    </div>
                    <div>
                      <h3 className="text-neutral-900 mb-1">유산소 운동</h3>
                      <p className="text-neutral-500 text-sm">런닝, 사이클 등</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-6 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center">
                      <Target className="w-6 h-6 text-neutral-700" />
                    </div>
                    <div>
                      <h3 className="text-neutral-900 mb-1">스트레칭</h3>
                      <p className="text-neutral-500 text-sm">유연성 향상</p>
                    </div>
                  </div>
                </Card>

                <Card className="p-6 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-full bg-neutral-100 flex items-center justify-center">
                      <Clock className="w-6 h-6 text-neutral-700" />
                    </div>
                    <div>
                      <h3 className="text-neutral-900 mb-1">요가/필라테스</h3>
                      <p className="text-neutral-500 text-sm">심신 안정</p>
                    </div>
                  </div>
                </Card>
              </div>
            </div>

            {/* Recommended Programs */}
            <div>
              <h2 className="text-neutral-900 mb-4">추천 프로그램</h2>
              <div className="space-y-3">
                <Card className="p-5 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-center gap-4">
                    <div className="w-20 h-20 rounded-lg bg-neutral-100"></div>
                    <div className="flex-1">
                      <h3 className="text-neutral-900 mb-1">전신 근력 프로그램</h3>
                      <p className="text-neutral-500 text-sm mb-2">4주 / 주 3회 / 중급</p>
                      <div className="flex gap-2">
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">근력</span>
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">헬스장</span>
                      </div>
                    </div>
                    <Button size="sm">시작하기</Button>
                  </div>
                </Card>

                <Card className="p-5 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                  <div className="flex items-center gap-4">
                    <div className="w-20 h-20 rounded-lg bg-neutral-100"></div>
                    <div className="flex-1">
                      <h3 className="text-neutral-900 mb-1">홈 트레이닝 루틴</h3>
                      <p className="text-neutral-500 text-sm mb-2">6주 / 주 5회 / 초급</p>
                      <div className="flex gap-2">
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">맨몸</span>
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">홈</span>
                      </div>
                    </div>
                    <Button size="sm">시작하기</Button>
                  </div>
                </Card>
              </div>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* My Programs */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">내 운동 프로그램</h3>
              <div className="space-y-3">
                <div className="p-3 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-700 text-sm mb-2">현재 진행중</p>
                  <p className="text-neutral-500 text-xs">프로그램을 시작해보세요</p>
                </div>
              </div>
            </Card>

            {/* Quick Stats */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">이번 달 통계</h3>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">총 운동 시간</span>
                    <span className="text-neutral-900">480분</span>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">운동 일수</span>
                    <span className="text-neutral-900">12일</span>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
