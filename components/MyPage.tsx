import { ArrowLeft, User, Settings, Bell, HelpCircle, Shield, LogOut, ChevronRight } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Switch } from './ui/switch';
import { useEffect, useState } from 'react';
import { InbodyResult } from './InbodyResult';

interface MyPageProps {
  onBack: () => void;
  onLogout: () => void;
  onProfileEdit: () => void;
  onInbodyUpload: () => void;
  onFitDnaTest: () => void;
}

export function MyPage({ onBack, onLogout, onProfileEdit, onInbodyUpload, onFitDnaTest }: MyPageProps) {
  const [testData, setTestData] = useState<any>(null);
  const [userData, setUserData] = useState<any>(null);
  const [inbodyData, setInbodyData] = useState<any>(null);

  // 나이 계산 함수
  const calculateAge = (birthdate: string) => {
    const today = new Date();
    const birth = new Date(birthdate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };

  useEffect(() => {
    // 로컬 스토리지에서 테스트 데이터 불러오기
    const savedTestData = localStorage.getItem('fitDnaTestData');
    if (savedTestData) {
      setTestData(JSON.parse(savedTestData));
    }

    // 사용자 정보 불러오기
    const savedUserData = localStorage.getItem('userData');
    if (savedUserData) {
      setUserData(JSON.parse(savedUserData));
    }

    // 인바디 데이터 불러오기
    const savedInbodyData = localStorage.getItem('inbodyData');
    if (savedInbodyData) {
      setInbodyData(JSON.parse(savedInbodyData));
    }
  }, []);

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <h1 className="text-neutral-900">마이</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        <div className="grid grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="col-span-2 space-y-6">
            {/* Profile Card */}
            <Card className="p-8 border border-neutral-200 bg-white">
              <div className="flex items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-neutral-100 flex items-center justify-center">
                  <User className="w-12 h-12 text-neutral-400" />
                </div>
                <div className="flex-1">
                  <h2 className="text-neutral-900 mb-1">{userData?.name || '사용자 이름'}</h2>
                  <p className="text-neutral-500 mb-4">{userData?.email || 'user@example.com'}</p>
                  <Button variant="outline" size="sm" className="border-neutral-200" onClick={onProfileEdit}>
                    프로필 수정
                  </Button>
                </div>
              </div>
            </Card>

            {/* 기본 정보 (저장된 데이터 표시) */}
            {testData && testData.userInfo && (
              <Card className="p-6 border border-neutral-200 bg-white">
                <h3 className="text-neutral-900 mb-4">기본 정보</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-neutral-50 rounded-lg">
                    <p className="text-neutral-600 text-sm mb-1">나이</p>
                    <p className="text-neutral-900">
                      {testData.userInfo.birthdate 
                        ? `${calculateAge(testData.userInfo.birthdate)}세`
                        : `${testData.userInfo.age}세`}
                    </p>
                  </div>
                  <div className="p-4 bg-neutral-50 rounded-lg">
                    <p className="text-neutral-600 text-sm mb-1">성별</p>
                    <p className="text-neutral-900">{testData.userInfo.gender}</p>
                  </div>
                  <div className="p-4 bg-neutral-50 rounded-lg">
                    <p className="text-neutral-600 text-sm mb-1">체중</p>
                    <p className="text-neutral-900">{testData.userInfo.weight}kg</p>
                  </div>
                  <div className="p-4 bg-neutral-50 rounded-lg">
                    <p className="text-neutral-600 text-sm mb-1">신장</p>
                    <p className="text-neutral-900">{testData.userInfo.height}cm</p>
                  </div>
                </div>
              </Card>
            )}

            {/* 인바디 결과 */}
            <InbodyResult data={inbodyData} onUpload={onInbodyUpload} />

            {/* FIT-DNA Result (if available) */}
            <Card className="p-6 border border-neutral-200 bg-white">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-neutral-900">나의 FIT-DNA</h3>
                <Button variant="ghost" size="sm">
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
              <div className="p-4 bg-neutral-50 rounded-lg text-center">
                <p className="text-neutral-500 text-sm">아직 FIT-DNA 테스트를 완료하지 않았습니다</p>
                <Button size="sm" className="mt-3" onClick={onFitDnaTest}>테스트 시작하기</Button>
              </div>
            </Card>

            {/* Settings Sections */}
            <div className="space-y-3">
              <h3 className="text-neutral-900">설정</h3>
              
              {/* Account Settings */}
              <Card className="p-5 border border-neutral-200 bg-white">
                <button className="w-full flex items-center justify-between hover:bg-neutral-50 -m-5 p-5 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Settings className="w-5 h-5 text-neutral-700" />
                    <span className="text-neutral-900">계정 설정</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-neutral-400" />
                </button>
              </Card>

              {/* Notifications */}
              <Card className="p-5 border border-neutral-200 bg-white">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <Bell className="w-5 h-5 text-neutral-700" />
                    <span className="text-neutral-900">알림 설정</span>
                  </div>
                  <Switch />
                </div>
              </Card>

              {/* Privacy */}
              <Card className="p-5 border border-neutral-200 bg-white">
                <button className="w-full flex items-center justify-between hover:bg-neutral-50 -m-5 p-5 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Shield className="w-5 h-5 text-neutral-700" />
                    <span className="text-neutral-900">개인정보 처리방침</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-neutral-400" />
                </button>
              </Card>

              {/* Help */}
              <Card className="p-5 border border-neutral-200 bg-white">
                <button className="w-full flex items-center justify-between hover:bg-neutral-50 -m-5 p-5 rounded-lg">
                  <div className="flex items-center gap-3">
                    <HelpCircle className="w-5 h-5 text-neutral-700" />
                    <span className="text-neutral-900">도움말</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-neutral-400" />
                </button>
              </Card>

              {/* Logout */}
              <Card className="p-5 border border-neutral-200 bg-white">
                <button 
                  className="w-full flex items-center justify-between hover:bg-neutral-50 -m-5 p-5 rounded-lg"
                  onClick={onLogout}
                >
                  <div className="flex items-center gap-3">
                    <LogOut className="w-5 h-5 text-neutral-700" />
                    <span className="text-neutral-900">로그아웃</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-neutral-400" />
                </button>
              </Card>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Activity Summary */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">활동 요약</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-neutral-600 text-sm mb-1">가입일</p>
                  <p className="text-neutral-900">2025.01.15</p>
                </div>
                <div>
                  <p className="text-neutral-600 text-sm mb-1">총 운동 일수</p>
                  <p className="text-neutral-900">48일</p>
                </div>
                <div>
                  <p className="text-neutral-600 text-sm mb-1">총 운동 시간</p>
                  <p className="text-neutral-900">32시간</p>
                </div>
              </div>
            </Card>

            {/* App Info */}
            <Card className="p-5 border border-neutral-200 bg-white">
              <h3 className="text-neutral-900 mb-4">앱 정보</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-neutral-600">버전</span>
                  <span className="text-neutral-900">1.0.0</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-neutral-600">최신 업데이트</span>
                  <span className="text-neutral-900">2025.11.28</span>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}