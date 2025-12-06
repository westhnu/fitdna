import { ArrowLeft, Search, Filter, Dumbbell, TrendingUp, Clock, Target, Calendar, Plus } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Input } from './ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { useState } from 'react';

interface WorkoutRecordProps {
  onBack: () => void;
}

export function WorkoutRecord({ onBack }: WorkoutRecordProps) {
  const [activeTab, setActiveTab] = useState('workout');

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="text-neutral-900">운동 & 기록</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        {/* Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="bg-white border border-neutral-200 mb-8 w-full max-w-md">
            <TabsTrigger value="workout" className="flex-1">운동</TabsTrigger>
            <TabsTrigger value="record" className="flex-1">기록</TabsTrigger>
          </TabsList>

          {/* Workout Tab Content */}
          <TabsContent value="workout" className="space-y-8">
            {/* Search Bar */}
            <div className="flex gap-3">
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
              {/* Left Column - Categories & Programs */}
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
                        <div className="w-16 h-16 rounded-lg bg-neutral-100"></div>
                        <div className="flex-1">
                          <h3 className="text-neutral-900 mb-1">초보자 전신 운동</h3>
                          <p className="text-neutral-500 text-sm mb-2">4주 프로그램 · 주 3회</p>
                          <div className="flex items-center gap-2 text-xs text-neutral-600">
                            <span>30분</span>
                            <span>·</span>
                            <span>난이도: 하</span>
                          </div>
                        </div>
                        <Button size="sm">시작하기</Button>
                      </div>
                    </Card>

                    <Card className="p-5 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-lg bg-neutral-100"></div>
                        <div className="flex-1">
                          <h3 className="text-neutral-900 mb-1">체지방 감량 프로그램</h3>
                          <p className="text-neutral-500 text-sm mb-2">6주 프로그램 · 주 4회</p>
                          <div className="flex items-center gap-2 text-xs text-neutral-600">
                            <span>45분</span>
                            <span>·</span>
                            <span>난이도: 중</span>
                          </div>
                        </div>
                        <Button size="sm">시작하기</Button>
                      </div>
                    </Card>

                    <Card className="p-5 border border-neutral-200 bg-white hover:bg-neutral-50 cursor-pointer">
                      <div className="flex items-center gap-4">
                        <div className="w-16 h-16 rounded-lg bg-neutral-100"></div>
                        <div className="flex-1">
                          <h3 className="text-neutral-900 mb-1">근력 향상 집중</h3>
                          <p className="text-neutral-500 text-sm mb-2">8주 프로그램 · 주 5회</p>
                          <div className="flex items-center gap-2 text-xs text-neutral-600">
                            <span>60분</span>
                            <span>·</span>
                            <span>난이도: 상</span>
                          </div>
                        </div>
                        <Button size="sm">시작하기</Button>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>

              {/* Right Column - Today's Workout */}
              <div className="space-y-6">
                <Card className="p-6 border border-neutral-200 bg-white">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-neutral-900">오늘의 운동</h3>
                    <Button size="sm" variant="ghost">
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                  <div className="space-y-3">
                    <div className="p-4 bg-neutral-50 rounded-lg">
                      <h4 className="text-neutral-900 mb-2">스쿼트</h4>
                      <p className="text-neutral-600 text-sm mb-2">3세트 × 12회</p>
                      <div className="h-1.5 bg-neutral-200 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-1/3"></div>
                      </div>
                    </div>
                    <div className="p-4 bg-neutral-50 rounded-lg">
                      <h4 className="text-neutral-900 mb-2">플랭크</h4>
                      <p className="text-neutral-600 text-sm mb-2">3세트 × 1분</p>
                      <div className="h-1.5 bg-neutral-200 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-0"></div>
                      </div>
                    </div>
                  </div>
                </Card>

                <Card className="p-6 border border-neutral-200 bg-white">
                  <h3 className="text-neutral-900 mb-4">이번 주 활동</h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-neutral-600">운동 일수</span>
                        <span className="text-neutral-900">3/5일</span>
                      </div>
                      <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-3/5"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-neutral-600">운동 시간</span>
                        <span className="text-neutral-900">120분</span>
                      </div>
                      <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-2/3"></div>
                      </div>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Record Tab Content */}
          <TabsContent value="record" className="space-y-6">
            <div className="grid grid-cols-3 gap-6">
              {/* Left Column */}
              <div className="col-span-2 space-y-6">
                {/* Summary Report Card */}
                <Card className="p-8 bg-neutral-900 text-white border-0">
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <h2 className="text-white mb-2">2025년 12월 운동 요약 리포트</h2>
                      <p className="text-white/70 text-sm">2025년 12월 1일 - 12월 5일</p>
                    </div>
                    <Button size="sm" className="bg-white text-neutral-900 hover:bg-white/90">
                      상세보기
                    </Button>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-6">
                    <div className="text-center">
                      <p className="text-white/70 text-sm mb-1">총 운동 시간</p>
                      <p className="text-white text-2xl">120분</p>
                      <p className="text-white/50 text-xs mt-1">지난주 대비 +15%</p>
                    </div>
                    <div className="text-center">
                      <p className="text-white/70 text-sm mb-1">운동 일수</p>
                      <p className="text-white text-2xl">3일</p>
                      <p className="text-white/50 text-xs mt-1">목표 달성률 60%</p>
                    </div>
                    <div className="text-center">
                      <p className="text-white/70 text-sm mb-1">소모 칼로리</p>
                      <p className="text-white text-2xl">960kcal</p>
                      <p className="text-white/50 text-xs mt-1">평균 320kcal/일</p>
                    </div>
                  </div>
                </Card>

                {/* Record Timeline */}
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-neutral-900">운동 기록</h2>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm" className="border-neutral-200">
                        주간
                      </Button>
                      <Button variant="outline" size="sm" className="border-neutral-200">
                        월간
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <Card className="p-5 border border-neutral-200 bg-white">
                      <div className="flex items-start gap-4">
                        <div className="w-16 h-16 rounded-lg bg-neutral-100 flex items-center justify-center">
                          <Calendar className="w-6 h-6 text-neutral-700" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h3 className="text-neutral-900 mb-1">전신 근력 운동</h3>
                              <p className="text-neutral-500 text-sm">2025.12.05 오전 10:00</p>
                            </div>
                            <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">완료</span>
                          </div>
                          <div className="space-y-1 text-sm">
                            <p className="text-neutral-600">운동 시간: 45분</p>
                            <p className="text-neutral-600">소모 칼로리: 320kcal</p>
                          </div>
                        </div>
                      </div>
                    </Card>

                    <Card className="p-5 border border-neutral-200 bg-white">
                      <div className="flex items-start gap-4">
                        <div className="w-16 h-16 rounded-lg bg-neutral-100 flex items-center justify-center">
                          <Calendar className="w-6 h-6 text-neutral-700" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h3 className="text-neutral-900 mb-1">러닝</h3>
                              <p className="text-neutral-500 text-sm">2025.12.03 오후 6:00</p>
                            </div>
                            <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">완료</span>
                          </div>
                          <div className="space-y-1 text-sm">
                            <p className="text-neutral-600">운동 시간: 30분</p>
                            <p className="text-neutral-600">거리: 5.2km</p>
                            <p className="text-neutral-600">소모 칼로리: 280kcal</p>
                          </div>
                        </div>
                      </div>
                    </Card>

                    <Card className="p-5 border border-neutral-200 bg-white">
                      <div className="flex items-start gap-4">
                        <div className="w-16 h-16 rounded-lg bg-neutral-100 flex items-center justify-center">
                          <Calendar className="w-6 h-6 text-neutral-700" />
                        </div>
                        <div className="flex-1">
                          <div className="flex items-start justify-between mb-2">
                            <div>
                              <h3 className="text-neutral-900 mb-1">요가</h3>
                              <p className="text-neutral-500 text-sm">2025.12.01 오전 7:00</p>
                            </div>
                            <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">완료</span>
                          </div>
                          <div className="space-y-1 text-sm">
                            <p className="text-neutral-600">운동 시간: 45분</p>
                            <p className="text-neutral-600">소모 칼로리: 180kcal</p>
                          </div>
                        </div>
                      </div>
                    </Card>
                  </div>
                </div>
              </div>

              {/* Right Column - Calendar & Stats */}
              <div className="space-y-6">
                <Card className="p-6 border border-neutral-200 bg-white">
                  <h3 className="text-neutral-900 mb-4">12월 운동 캘린더</h3>
                  <div className="space-y-2">
                    <div className="grid grid-cols-7 gap-1 text-center text-xs text-neutral-500 mb-2">
                      <div>일</div>
                      <div>월</div>
                      <div>화</div>
                      <div>수</div>
                      <div>목</div>
                      <div>금</div>
                      <div>토</div>
                    </div>
                    <div className="grid grid-cols-7 gap-1">
                      {[1, 2, 3, 4, 5, 6, 7].map((day) => (
                        <div 
                          key={day} 
                          className={`aspect-square flex items-center justify-center text-sm rounded ${
                            day === 1 || day === 3 || day === 5 
                              ? 'bg-neutral-900 text-white' 
                              : 'bg-neutral-50 text-neutral-400'
                          }`}
                        >
                          {day}
                        </div>
                      ))}
                    </div>
                  </div>
                </Card>

                <Card className="p-6 border border-neutral-200 bg-white">
                  <h3 className="text-neutral-900 mb-4">이번 달 목표</h3>
                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-neutral-600">운동 일수</span>
                        <span className="text-neutral-900">3/20일</span>
                      </div>
                      <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-[15%]"></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span className="text-neutral-600">총 운동 시간</span>
                        <span className="text-neutral-900">120/600분</span>
                      </div>
                      <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                        <div className="h-full bg-neutral-900 w-[20%]"></div>
                      </div>
                    </div>
                  </div>
                </Card>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
