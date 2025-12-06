import { ArrowLeft, Calendar, TrendingUp } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { useState } from 'react';
import { MonthlyReport } from './MonthlyReport';

interface RecordProps {
  onBack: () => void;
}

export function Record({ onBack }: RecordProps) {
  const [showMonthlyReport, setShowMonthlyReport] = useState(false);

  if (showMonthlyReport) {
    return <MonthlyReport onBack={() => setShowMonthlyReport(false)} />;
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={onBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="text-neutral-900">기록</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        <div className="grid grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="col-span-2 space-y-6">
            {/* Summary Report Card */}
            <Card className="p-8 bg-neutral-900 text-white border-0">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-white mb-2">2025년 11월 운동 요약 리포트</h2>
                  <p className="text-white/70 text-sm">2025년 11월 1일 - 11월 28일</p>
                </div>
                <Button size="sm" className="bg-white text-neutral-900 hover:bg-white/90" onClick={() => setShowMonthlyReport(true)}>
                  상세보기
                </Button>
              </div>
              
              <div className="grid grid-cols-2 gap-8 max-w-xl mx-auto">
                <div className="text-center">
                  <p className="text-white/70 text-sm mb-1">총 운동 시간</p>
                  <p className="text-white text-2xl">480분</p>
                  <p className="text-white/50 text-xs mt-1">지난달 대비 +20%</p>
                </div>
                <div className="text-center">
                  <p className="text-white/70 text-sm mb-1">운동 일수</p>
                  <p className="text-white text-2xl">12일</p>
                  <p className="text-white/50 text-xs mt-1">목표 달성률 60%</p>
                </div>
              </div>
            </Card>

            {/* Tabs for different views */}
            <Tabs defaultValue="timeline" className="w-full">
              <TabsList className="bg-white border border-neutral-200 mb-6">
                <TabsTrigger value="timeline">타임라인</TabsTrigger>
                <TabsTrigger value="weekly">주간 보기</TabsTrigger>
                <TabsTrigger value="monthly">월간 보기</TabsTrigger>
              </TabsList>

              <TabsContent value="timeline" className="space-y-3">
                {/* Timeline Records */}
                <Card className="p-5 border border-neutral-200 bg-white">
                  <div className="flex items-start gap-4">
                    <div className="w-16 h-16 rounded-lg bg-neutral-100 flex items-center justify-center">
                      <Calendar className="w-6 h-6 text-neutral-700" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <h3 className="text-neutral-900 mb-1">전신 근력 운동</h3>
                          <p className="text-neutral-500 text-sm">2025.11.28 오전 10:00</p>
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
                          <h3 className="text-neutral-900 mb-1">런닝</h3>
                          <p className="text-neutral-500 text-sm">2025.11.27 오후 6:30</p>
                        </div>
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">완료</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <p className="text-neutral-600">운동 시간: 30분</p>
                        <p className="text-neutral-600">소모 칼로리: 250kcal</p>
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
                          <p className="text-neutral-500 text-sm">2025.11.26 오전 7:00</p>
                        </div>
                        <span className="px-2 py-1 bg-neutral-100 rounded text-xs text-neutral-700">완료</span>
                      </div>
                      <div className="space-y-1 text-sm">
                        <p className="text-neutral-600">운동 시간: 60분</p>
                        <p className="text-neutral-600">소모 칼로리: 180kcal</p>
                      </div>
                    </div>
                  </div>
                </Card>
              </TabsContent>

              <TabsContent value="weekly">
                <Card className="p-6 border border-neutral-200 bg-white">
                  <p className="text-neutral-500 text-center">주간 데이터 차트가 여기에 표시됩니다</p>
                </Card>
              </TabsContent>

              <TabsContent value="monthly">
                <Card className="p-6 border border-neutral-200 bg-white">
                  <p className="text-neutral-500 text-center">월간 데이터 차트가 여기에 표시됩니다</p>
                </Card>
              </TabsContent>
            </Tabs>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Performance Trend */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <div className="flex items-center gap-2 mb-4">
                <TrendingUp className="w-5 h-5 text-neutral-700" />
                <h3 className="text-neutral-900">성과 추이</h3>
              </div>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">평균 운동 시간</span>
                    <span className="text-neutral-900">40분</span>
                  </div>
                  <div className="h-1.5 bg-neutral-100 rounded-full overflow-hidden">
                    <div className="h-full bg-neutral-900 w-4/5"></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">운동 빈도</span>
                    <span className="text-neutral-900">주 3회</span>
                  </div>
                  <div className="h-1.5 bg-neutral-100 rounded-full overflow-hidden">
                    <div className="h-full bg-neutral-900 w-3/5"></div>
                  </div>
                </div>
              </div>
            </Card>

            {/* Goals */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">이번 달 목표</h3>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">운동 일수</span>
                    <span className="text-neutral-900">12/20일</span>
                  </div>
                  <div className="h-1.5 bg-neutral-100 rounded-full overflow-hidden">
                    <div className="h-full bg-neutral-900 w-3/5"></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-neutral-600">총 운동 시간</span>
                    <span className="text-neutral-900">480/600분</span>
                  </div>
                  <div className="h-1.5 bg-neutral-100 rounded-full overflow-hidden">
                    <div className="h-full bg-neutral-900 w-4/5"></div>
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