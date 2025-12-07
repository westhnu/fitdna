import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { MonthlyReport as MonthlyReportType } from '../data/mockMonthlyReport';

interface MonthlyReportProps {
  data: MonthlyReportType;
}

export function MonthlyReport({ data }: MonthlyReportProps) {
  const { year, month, summary, workoutFrequency, metricChanges, consistencyScore } = data;

  // 월 이름
  const monthName = `${year}년 ${month}월`;

  // 운동 종류별 색상
  const exerciseColors = {
    strength: 'bg-blue-500',
    flexibility: 'bg-green-500',
    endurance: 'bg-orange-500',
  };

  // 점수에 따른 등급
  const getScoreGrade = (score: number) => {
    if (score >= 90) return { label: '최고', color: 'bg-green-600' };
    if (score >= 80) return { label: '우수', color: 'bg-blue-600' };
    if (score >= 70) return { label: '양호', color: 'bg-yellow-600' };
    if (score >= 60) return { label: '보통', color: 'bg-orange-600' };
    return { label: '노력 필요', color: 'bg-red-600' };
  };

  const scoreGrade = getScoreGrade(consistencyScore.totalScore);

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">{monthName} 운동 리포트</h2>
        <Badge className={`${scoreGrade.color} text-white px-4 py-2 text-lg`}>
          {scoreGrade.label} {consistencyScore.totalScore}점
        </Badge>
      </div>

      {/* 월간 요약 */}
      <Card>
        <CardHeader>
          <CardTitle>이번 달 운동 요약</CardTitle>
          <CardDescription>전반적인 운동 활동 현황</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-600">총 운동 일수</p>
              <p className="text-3xl font-bold text-blue-600">{summary.totalWorkoutDays}일</p>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-gray-600">주당 평균</p>
              <p className="text-3xl font-bold text-green-600">{summary.weeklyAverage}회</p>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <p className="text-sm text-gray-600">총 운동 시간</p>
              <p className="text-3xl font-bold text-purple-600">
                {Math.floor(summary.totalDuration / 60)}시간
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 운동 종류별 빈도 */}
      <Card>
        <CardHeader>
          <CardTitle>운동 종류별 빈도</CardTitle>
          <CardDescription>근력 · 유연성 · 지구력 운동 분포</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium">💪 근력 운동</span>
                <span className="text-gray-600">{workoutFrequency.strength}회</span>
              </div>
              <Progress value={(workoutFrequency.strength / summary.totalWorkoutDays) * 100} className="h-3" />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium">🧘 유연성 운동</span>
                <span className="text-gray-600">{workoutFrequency.flexibility}회</span>
              </div>
              <Progress value={(workoutFrequency.flexibility / summary.totalWorkoutDays) * 100} className="h-3" />
            </div>
            <div>
              <div className="flex justify-between mb-2">
                <span className="font-medium">🏃 지구력 운동</span>
                <span className="text-gray-600">{workoutFrequency.endurance}회</span>
              </div>
              <Progress value={(workoutFrequency.endurance / summary.totalWorkoutDays) * 100} className="h-3" />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 체력 지표 변화 */}
      <Card>
        <CardHeader>
          <CardTitle>체력 지표 변화</CardTitle>
          <CardDescription>지난 달 대비 이번 달 측정 결과</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {metricChanges.map((metric, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex-1">
                  <p className="font-medium">{metric.name}</p>
                  <p className="text-sm text-gray-600">
                    {metric.previousMonth} → {metric.currentMonth} {metric.unit}
                  </p>
                </div>
                <div className="text-right">
                  <Badge
                    className={metric.change >= 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}
                  >
                    {metric.change >= 0 ? '↑' : '↓'} {Math.abs(metric.changePercentage).toFixed(1)}%
                  </Badge>
                  <p className="text-xs text-gray-500 mt-1">
                    {metric.change >= 0 ? '+' : ''}
                    {metric.change} {metric.unit}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 꾸준함 점수 */}
      <Card>
        <CardHeader>
          <CardTitle>꾸준함 점수 (Consistency Score)</CardTitle>
          <CardDescription>운동 규칙성 및 목표 달성도 평가</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* 총점 */}
            <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
              <p className="text-sm text-gray-600 mb-2">총 꾸준함 점수</p>
              <p className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                {consistencyScore.totalScore}점
              </p>
              <p className="text-sm text-gray-600 mt-2">100점 만점</p>
            </div>

            {/* 세부 점수 */}
            <div className="space-y-3">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">목표 달성률</span>
                  <span className="text-sm text-gray-600">
                    {consistencyScore.breakdown.achievementRate}/40점
                  </span>
                </div>
                <Progress value={(consistencyScore.breakdown.achievementRate / 40) * 100} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">운동 규칙성</span>
                  <span className="text-sm text-gray-600">{consistencyScore.breakdown.regularity}/40점</span>
                </div>
                <Progress value={(consistencyScore.breakdown.regularity / 40) * 100} className="h-2" />
              </div>
              <div>
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-medium">강도 유지도</span>
                  <span className="text-sm text-gray-600">
                    {consistencyScore.breakdown.intensityMaintenance}/20점
                  </span>
                </div>
                <Progress value={(consistencyScore.breakdown.intensityMaintenance / 20) * 100} className="h-2" />
              </div>
            </div>

            {/* 피드백 */}
            <div className="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
              <p className="text-sm font-medium text-blue-900 mb-1">AI 코치 피드백</p>
              <p className="text-sm text-blue-800">{consistencyScore.feedback}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
