import { ArrowLeft, TrendingUp, Calendar, Clock, Zap } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface MonthlyReportProps {
  onBack: () => void;
}

export function MonthlyReport({ onBack }: MonthlyReportProps) {
  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={onBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="text-neutral-900">2025년 11월 운동 상세 리포트</h1>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-8 py-12">
        <div className="space-y-6">
          {/* Summary Header */}
          <Card className="p-8 bg-neutral-900 text-white border-0">
            <div className="text-center mb-8">
              <h2 className="text-white mb-2">2025년 11월</h2>
              <p className="text-white/70 text-sm">11월 1일 - 11월 28일 (28일간)</p>
            </div>
            
            <div className="grid grid-cols-4 gap-6">
              <div className="text-center">
                <p className="text-white/70 text-sm mb-1">총 운동 시간</p>
                <p className="text-white text-3xl mb-1">480분</p>
                <p className="text-white/50 text-xs">8시간</p>
              </div>
              <div className="text-center">
                <p className="text-white/70 text-sm mb-1">운동 일수</p>
                <p className="text-white text-3xl mb-1">12일</p>
                <p className="text-white/50 text-xs">주 3회 평균</p>
              </div>
              <div className="text-center">
                <p className="text-white/70 text-sm mb-1">평균 운동 시간</p>
                <p className="text-white text-3xl mb-1">40분</p>
                <p className="text-white/50 text-xs">1회당</p>
              </div>
              <div className="text-center">
                <p className="text-white/70 text-sm mb-1">총 소모 칼로리</p>
                <p className="text-white text-3xl mb-1">3,200</p>
                <p className="text-white/50 text-xs">kcal</p>
              </div>
            </div>
          </Card>

          {/* Monthly Comparison */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="w-5 h-5 text-neutral-700" />
              <h3 className="text-neutral-900">전월 대비 성과</h3>
            </div>
            <div className="grid grid-cols-3 gap-6">
              <div className="p-4 bg-neutral-50 rounded-lg">
                <p className="text-neutral-600 text-sm mb-2">운동 시간</p>
                <p className="text-neutral-900 text-xl mb-1">+20%</p>
                <p className="text-neutral-500 text-xs">80분 증가</p>
              </div>
              <div className="p-4 bg-neutral-50 rounded-lg">
                <p className="text-neutral-600 text-sm mb-2">운동 일수</p>
                <p className="text-neutral-900 text-xl mb-1">+3일</p>
                <p className="text-neutral-500 text-xs">10월 9일 → 11월 12일</p>
              </div>
              <div className="p-4 bg-neutral-50 rounded-lg">
                <p className="text-neutral-600 text-sm mb-2">평균 운동 시간</p>
                <p className="text-neutral-900 text-xl mb-1">+5분</p>
                <p className="text-neutral-500 text-xs">35분 → 40분</p>
              </div>
            </div>
          </Card>

          {/* Exercise Type Breakdown */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-4">운동 유형별 분석</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-neutral-600">근력 운동</span>
                  <span className="text-neutral-900">240분 (50%)</span>
                </div>
                <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                  <div className="h-full bg-neutral-900 w-1/2"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-neutral-600">유산소 운동</span>
                  <span className="text-neutral-900">144분 (30%)</span>
                </div>
                <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                  <div className="h-full bg-neutral-700 w-3/10"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-neutral-600">요가/스트레칭</span>
                  <span className="text-neutral-900">96분 (20%)</span>
                </div>
                <div className="h-2 bg-neutral-100 rounded-full overflow-hidden">
                  <div className="h-full bg-neutral-500 w-1/5"></div>
                </div>
              </div>
            </div>
          </Card>

          {/* Weekly Activity Calendar */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-4">주간 활동 현황</h3>
            <div className="grid grid-cols-7 gap-2">
              {['월', '화', '수', '목', '금', '토', '일'].map((day) => (
                <div key={day} className="text-center text-neutral-500 text-xs mb-2">
                  {day}
                </div>
              ))}
              {/* Week 1 */}
              {[false, false, false, false, true, true, false].map((active, i) => (
                <div
                  key={`w1-${i}`}
                  className={`aspect-square rounded-lg flex items-center justify-center ${
                    active ? 'bg-neutral-900 text-white' : 'bg-neutral-100 text-neutral-400'
                  }`}
                >
                  <span className="text-xs">{i + 1}</span>
                </div>
              ))}
              {/* Week 2 */}
              {[false, true, false, true, false, false, true].map((active, i) => (
                <div
                  key={`w2-${i}`}
                  className={`aspect-square rounded-lg flex items-center justify-center ${
                    active ? 'bg-neutral-900 text-white' : 'bg-neutral-100 text-neutral-400'
                  }`}
                >
                  <span className="text-xs">{i + 8}</span>
                </div>
              ))}
              {/* Week 3 */}
              {[true, false, true, false, false, true, false].map((active, i) => (
                <div
                  key={`w3-${i}`}
                  className={`aspect-square rounded-lg flex items-center justify-center ${
                    active ? 'bg-neutral-900 text-white' : 'bg-neutral-100 text-neutral-400'
                  }`}
                >
                  <span className="text-xs">{i + 15}</span>
                </div>
              ))}
              {/* Week 4 */}
              {[false, true, false, true, false, true, false].map((active, i) => (
                <div
                  key={`w4-${i}`}
                  className={`aspect-square rounded-lg flex items-center justify-center ${
                    active ? 'bg-neutral-900 text-white' : 'bg-neutral-100 text-neutral-400'
                  }`}
                >
                  <span className="text-xs">{i + 22}</span>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-4 mt-4 text-xs text-neutral-500">
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded bg-neutral-900"></div>
                <span>운동 완료</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-3 h-3 rounded bg-neutral-100"></div>
                <span>운동 없음</span>
              </div>
            </div>
          </Card>

          {/* Best Record */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-4">이달의 베스트 기록</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-neutral-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-4 h-4 text-neutral-700" />
                  <p className="text-neutral-600 text-sm">최장 운동 시간</p>
                </div>
                <p className="text-neutral-900 text-xl mb-1">75분</p>
                <p className="text-neutral-500 text-xs">2025.11.15 전신 근력 운동</p>
              </div>
              <div className="p-4 bg-neutral-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="w-4 h-4 text-neutral-700" />
                  <p className="text-neutral-600 text-sm">최다 연속 운동</p>
                </div>
                <p className="text-neutral-900 text-xl mb-1">3일</p>
                <p className="text-neutral-500 text-xs">2025.11.22 - 11.24</p>
              </div>
            </div>
          </Card>

          {/* Most Frequent Exercise */}
          <Card className="p-6 border border-neutral-200 bg-white">
            <h3 className="text-neutral-900 mb-4">자주 한 운동</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-neutral-900 text-white flex items-center justify-center">
                    1
                  </div>
                  <div>
                    <p className="text-neutral-900">스쿼트</p>
                    <p className="text-neutral-500 text-sm">하체 근력</p>
                  </div>
                </div>
                <p className="text-neutral-600">8회</p>
              </div>
              <div className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-neutral-700 text-white flex items-center justify-center">
                    2
                  </div>
                  <div>
                    <p className="text-neutral-900">플랭크</p>
                    <p className="text-neutral-500 text-sm">코어 강화</p>
                  </div>
                </div>
                <p className="text-neutral-600">6회</p>
              </div>
              <div className="flex items-center justify-between p-4 bg-neutral-50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-neutral-500 text-white flex items-center justify-center">
                    3
                  </div>
                  <div>
                    <p className="text-neutral-900">런닝</p>
                    <p className="text-neutral-500 text-sm">유산소</p>
                  </div>
                </div>
                <p className="text-neutral-600">5회</p>
              </div>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
