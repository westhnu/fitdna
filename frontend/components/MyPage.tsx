import React, { useState } from 'react';
import { MonthlyReport } from './MonthlyReport';
import { mockMonthlyReport, mockMonthlyReports } from '../data/mockMonthlyReport';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Button } from './ui/button';

// 임시 사용자 데이터
const mockUser = {
  name: '김체력',
  email: 'fitness@example.com',
  age: 28,
  gender: 'M' as const,
  fitDnaType: 'PFE',
  fitDnaName: '파워 애슬리트',
  joinDate: '2025-09-01',
  profileImage: '',
};

export function MyPage() {
  const [selectedMonth, setSelectedMonth] = useState(11); // 11월

  // 선택된 월의 리포트 가져오기
  const currentReport = mockMonthlyReports.find((r) => r.month === selectedMonth) || mockMonthlyReport;

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* 사용자 프로필 섹션 */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="flex items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={mockUser.profileImage} alt={mockUser.name} />
              <AvatarFallback className="text-2xl bg-blue-600 text-white">
                {mockUser.name.charAt(0)}
              </AvatarFallback>
            </Avatar>
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{mockUser.name}님의 마이페이지</h1>
              <div className="flex items-center gap-3 mb-3">
                <Badge className="bg-purple-600 text-white px-3 py-1">
                  FIT-DNA: {mockUser.fitDnaType}
                </Badge>
                <span className="text-gray-600">{mockUser.fitDnaName}</span>
              </div>
              <div className="flex gap-4 text-sm text-gray-600">
                <span>나이: {mockUser.age}세</span>
                <span>성별: {mockUser.gender === 'M' ? '남성' : '여성'}</span>
                <span>가입일: {mockUser.joinDate}</span>
              </div>
            </div>
            <Button variant="outline">프로필 수정</Button>
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
          {/* 월 선택 */}
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">월간 운동 리포트</h2>
            <div className="flex gap-2">
              {mockMonthlyReports.map((report) => (
                <Button
                  key={report.month}
                  variant={selectedMonth === report.month ? 'default' : 'outline'}
                  onClick={() => setSelectedMonth(report.month)}
                  size="sm"
                >
                  {report.month}월
                </Button>
              ))}
            </div>
          </div>

          {/* 월간 리포트 컴포넌트 */}
          <MonthlyReport data={currentReport} />
        </TabsContent>

        {/* 운동 기록 탭 */}
        <TabsContent value="workout-history">
          <Card>
            <CardHeader>
              <CardTitle>운동 기록</CardTitle>
              <CardDescription>모든 운동 세션 기록을 확인할 수 있습니다</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {currentReport.sessions.slice(0, 10).map((session, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">{session.date}</p>
                      <p className="text-sm text-gray-600">{session.exercises.join(', ')}</p>
                    </div>
                    <div className="text-right">
                      <Badge
                        className={
                          session.exerciseType === 'strength'
                            ? 'bg-blue-100 text-blue-700'
                            : session.exerciseType === 'flexibility'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-orange-100 text-orange-700'
                        }
                      >
                        {session.exerciseType === 'strength'
                          ? '근력'
                          : session.exerciseType === 'flexibility'
                            ? '유연성'
                            : '지구력'}
                      </Badge>
                      <p className="text-xs text-gray-500 mt-1">{session.duration}분</p>
                    </div>
                  </div>
                ))}
              </div>
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
                      {mockUser.fitDnaType} - {mockUser.fitDnaName}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">검사일: 2025-11-15</p>
                </div>

                <div className="p-4 bg-gray-50 rounded">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium text-gray-700">이전 유형</span>
                    <Badge className="bg-gray-400 text-white">PSE - 파워 러너</Badge>
                  </div>
                  <p className="text-sm text-gray-600">검사일: 2025-10-01</p>
                </div>

                <div className="p-4 bg-gray-50 rounded">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium text-gray-700">최초 유형</span>
                    <Badge className="bg-gray-400 text-white">LSQ - 유연성 초보</Badge>
                  </div>
                  <p className="text-sm text-gray-600">검사일: 2025-09-01</p>
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
              <CardDescription>개인정보 및 알림 설정</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">운동 알림</p>
                    <p className="text-sm text-gray-600">정기적인 운동 리마인더를 받습니다</p>
                  </div>
                  <Button variant="outline" size="sm">
                    설정
                  </Button>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">목표 설정</p>
                    <p className="text-sm text-gray-600">주간 운동 목표를 설정합니다</p>
                  </div>
                  <Button variant="outline" size="sm">
                    설정
                  </Button>
                </div>
                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">개인정보 관리</p>
                    <p className="text-sm text-gray-600">이메일, 비밀번호 변경</p>
                  </div>
                  <Button variant="outline" size="sm">
                    변경
                  </Button>
                </div>
                <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                  <div>
                    <p className="font-medium text-red-700">계정 삭제</p>
                    <p className="text-sm text-red-600">계정과 모든 데이터가 삭제됩니다</p>
                  </div>
                  <Button variant="destructive" size="sm">
                    삭제
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
