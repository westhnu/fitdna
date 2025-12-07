import React, { useState, useEffect } from 'react';
import { MonthlyReport } from './MonthlyReport';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { getFitDNAResult, getMonthlyReport, type MonthlyReportAPI } from '../services/api';
import { MonthlyReport as MonthlyReportType } from '../data/mockMonthlyReport';

// API 응답을 프론트엔드 타입으로 변환
function convertAPIReportToFrontend(apiReport: MonthlyReportAPI): MonthlyReportType {
  return {
    year: apiReport.year,
    month: apiReport.month,
    summary: {
      totalWorkoutDays: apiReport.summary.total_workout_days,
      weeklyAverage: apiReport.summary.weekly_average,
      totalDuration: apiReport.summary.total_duration,
    },
    workoutFrequency: {
      strength: apiReport.workout_frequency.strength,
      flexibility: apiReport.workout_frequency.flexibility,
      endurance: apiReport.workout_frequency.endurance,
    },
    sessions: [], // 세션은 별도 API에서 가져옴
    metricChanges: apiReport.metric_changes.map((m) => ({
      name: m.name,
      unit: m.unit,
      previousMonth: m.previous_month,
      currentMonth: m.current_month,
      change: m.change,
      changePercentage: m.change_percentage,
    })),
    consistencyScore: {
      totalScore: apiReport.consistency_score.total_score,
      breakdown: {
        achievementRate: apiReport.consistency_score.breakdown.achievement_rate,
        regularity: apiReport.consistency_score.breakdown.regularity,
        intensityMaintenance: apiReport.consistency_score.breakdown.intensity_maintenance,
      },
      feedback: apiReport.consistency_score.feedback,
    },
  };
}

export function MyPageIntegrated() {
  const [selectedMonth, setSelectedMonth] = useState(11);
  const [selectedYear] = useState(2024);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 사용자 정보 (FIT-DNA 결과에서 가져옴)
  const [user, setUser] = useState({
    name: '김체력',
    email: 'demo@fitdna.com',
    age: 28,
    gender: 'M' as const,
    fitDnaType: 'PFE',
    fitDnaName: '파워 애슬리트',
    joinDate: '2024-09-01',
    profileImage: '',
  });

  // 월간 리포트 데이터
  const [currentReport, setCurrentReport] = useState<MonthlyReportType | null>(null);

  // 데이터 로드
  useEffect(() => {
    loadData();
  }, [selectedMonth, selectedYear]);

  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      // 1. FIT-DNA 결과 조회
      const fitDnaResult = await getFitDNAResult(1); // 데모 사용자 ID = 1

      setUser((prev) => ({
        ...prev,
        fitDnaType: fitDnaResult.fitdna_card.type,
        fitDnaName: fitDnaResult.fitdna_card.name,
      }));

      // 2. 월간 리포트 조회
      const monthlyReport = await getMonthlyReport(1, selectedYear, selectedMonth);
      const convertedReport = convertAPIReportToFrontend(monthlyReport);

      setCurrentReport(convertedReport);
    } catch (err) {
      console.error('데이터 로드 실패:', err);
      setError('데이터를 불러오는데 실패했습니다. 서버를 확인해주세요.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6 max-w-7xl">
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">데이터를 불러오는 중...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6 max-w-7xl">
        <Card className="bg-red-50 border-red-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <p className="text-red-700 font-medium mb-2">⚠️ 오류 발생</p>
              <p className="text-red-600">{error}</p>
              <Button onClick={loadData} className="mt-4" variant="outline">
                다시 시도
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentReport) {
    return null;
  }

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* 사용자 프로필 섹션 */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="flex items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user.profileImage} alt={user.name} />
              <AvatarFallback className="text-2xl bg-blue-600 text-white">
                {user.name.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{user.name}님의 마이페이지</h1>
              <div className="flex items-center gap-3 mb-3">
                <Badge className="bg-purple-600 text-white px-3 py-1">
                  FIT-DNA: {user.fitDnaType}
                </Badge>
                <span className="text-gray-600">{user.fitDnaName}</span>
              </div>
              <div className="flex gap-4 text-sm text-gray-600">
                <span>나이: {user.age}세</span>
                <span>성별: {user.gender === 'M' ? '남성' : '여성'}</span>
                <span>가입일: {user.joinDate}</span>
              </div>
            </div>
            <div className="flex flex-col gap-2">
              <Button variant="outline" onClick={loadData}>
                🔄 새로고침
              </Button>
              <Badge className="bg-green-600 text-white px-3 py-1 text-center">
                ✅ API 연결됨
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 탭 메뉴 */}
      <Tabs defaultValue="monthly-report" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="monthly-report">월간 리포트</TabsTrigger>
          <TabsTrigger value="workout-history">운동 기록</TabsTrigger>
          <TabsTrigger value="fitdna-history">FIT-DNA 이력</TabsTrigger>
          <TabsTrigger value="settings">설정</TabsTrigger>
        </TabsList>

        {/* 월간 리포트 탭 */}
        <TabsContent value="monthly-report" className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">월간 운동 리포트</h2>
            <div className="flex gap-2">
              {[9, 10, 11].map((month) => (
                <Button
                  key={month}
                  variant={selectedMonth === month ? 'default' : 'outline'}
                  onClick={() => setSelectedMonth(month)}
                  size="sm"
                >
                  {month}월
                </Button>
              ))}
            </div>
          </div>

          <MonthlyReport data={currentReport} />
        </TabsContent>

        {/* 운동 기록 탭 */}
        <TabsContent value="workout-history">
          <Card>
            <CardHeader>
              <CardTitle>운동 기록</CardTitle>
              <CardDescription>
                {selectedYear}년 {selectedMonth}월 운동 세션
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center py-8">
                운동 세션 데이터는 월간 리포트의 summary에 포함되어 있습니다.
                <br />총 {currentReport.summary.totalWorkoutDays}일 운동하셨습니다!
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        {/* FIT-DNA 이력 탭 */}
        <TabsContent value="fitdna-history">
          <Card>
            <CardHeader>
              <CardTitle>FIT-DNA 검사 이력</CardTitle>
              <CardDescription>체력 측정 및 FIT-DNA 유형 변화 기록</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-purple-50 border-l-4 border-purple-500 rounded">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-bold">현재 유형</span>
                    <Badge className="bg-purple-600 text-white">
                      {user.fitDnaType} - {user.fitDnaName}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">검사일: 2024-11-15</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* 설정 탭 */}
        <TabsContent value="settings">
          <Card>
            <CardHeader>
              <CardTitle>설정</CardTitle>
              <CardDescription>API 연결 상태 및 정보</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                  <div>
                    <p className="font-medium">백엔드 서버</p>
                    <p className="text-sm text-gray-600">http://localhost:8000</p>
                  </div>
                  <Badge className="bg-green-600 text-white">연결됨</Badge>
                </div>
                <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
                  <div>
                    <p className="font-medium">API 문서</p>
                    <p className="text-sm text-gray-600">Swagger UI</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => window.open('http://localhost:8000/api/docs', '_blank')}
                  >
                    열기
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
