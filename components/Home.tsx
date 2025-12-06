import { ChevronRight, User, Dumbbell, AlertTriangle, Cloud, Users, Home as HomeIcon } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState } from 'react';
import { FitDnaTest } from './FitDnaTest';
import { AiChat } from './AiChat';
import { WorkoutRecommendation } from './WorkoutRecommendation';
import { InjuryManagement } from './InjuryManagement';
import { WeatherWorkout } from './WeatherWorkout';
import { MateMatching } from './MateMatching';
import { WorkoutRecord } from './WorkoutRecord';
import { MyPage } from './MyPage';
import { Login } from './Login';
import { SignUp } from './SignUp';
import { ProfileEdit } from './ProfileEdit';
import { InbodyUpload } from './InbodyUpload';
import { FitDnaTypes } from './FitDnaTypes';

type Screen = 'home' | 'fitdna' | 'aichat' | 'workout' | 'injury' | 'weather' | 'mate' | 'workout-record' | 'my' | 'login' | 'signup' | 'profile-edit' | 'inbody-upload' | 'fitdna-types';

export function Home() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('home');
  const [isLoggedIn, setIsLoggedIn] = useState(true);

  // Handle login
  const handleLogin = () => {
    setIsLoggedIn(true);
    setCurrentScreen('home');
  };

  // Handle signup
  const handleSignUp = (userData: any) => {
    setIsLoggedIn(true);
    setCurrentScreen('home');
  };

  // Handle logout
  const handleLogout = () => {
    setIsLoggedIn(false);
    setCurrentScreen('login');
  };

  // Show login screen if not logged in
  if (!isLoggedIn && currentScreen === 'login') {
    return <Login onLogin={handleLogin} onSignUp={() => setCurrentScreen('signup')} />;
  }

  if (currentScreen === 'signup') {
    return <SignUp onSignUp={handleSignUp} onBack={() => setCurrentScreen('login')} />;
  }

  if (currentScreen === 'profile-edit') {
    return <ProfileEdit onBack={() => setCurrentScreen('my')} onSave={() => setCurrentScreen('my')} />;
  }

  if (currentScreen === 'inbody-upload') {
    return <InbodyUpload onBack={() => setCurrentScreen('my')} onSave={() => setCurrentScreen('my')} />;
  }

  if (currentScreen === 'fitdna') {
    return <FitDnaTest onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'aichat') {
    return <AiChat onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'workout') {
    return <WorkoutRecommendation onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'injury') {
    return <InjuryManagement onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'weather') {
    return <WeatherWorkout onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'mate') {
    return <MateMatching onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'workout-record') {
    return <WorkoutRecord onBack={() => setCurrentScreen('home')} />;
  }

  if (currentScreen === 'my') {
    return (
      <MyPage 
        onBack={() => setCurrentScreen('home')} 
        onLogout={handleLogout}
        onProfileEdit={() => setCurrentScreen('profile-edit')}
        onInbodyUpload={() => setCurrentScreen('inbody-upload')}
        onFitDnaTest={() => setCurrentScreen('fitdna')}
      />
    );
  }

  if (currentScreen === 'fitdna-types') {
    return <FitDnaTypes onBack={() => setCurrentScreen('home')} onStartTest={() => setCurrentScreen('fitdna')} />;
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-8 py-4 flex items-center justify-between">
          <div className="h-8"></div>
          <nav className="flex items-center gap-4">
            <button 
              className={`p-2 ${currentScreen === 'home' ? 'text-neutral-900' : 'text-neutral-500 hover:text-neutral-900'}`}
              onClick={() => setCurrentScreen('home')}
            >
              <HomeIcon className="w-5 h-5" />
            </button>
            <button className="p-2" onClick={() => setCurrentScreen('my')}>
              <User className={`w-5 h-5 ${currentScreen === 'my' ? 'text-neutral-900' : 'text-neutral-700 hover:text-neutral-900'}`} />
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12">
        {/* Greeting */}
        <div className="mb-12 text-center">
          <h1 className="text-neutral-900 mb-3">
            안녕하세요,<br />
            오늘도 건강한 하루 되세요
          </h1>
          <p className="text-neutral-500">나만의 체력 데이터로 맞춤 운동을 시작해보세요</p>
        </div>

        <div className="max-w-4xl mx-auto space-y-6">
          {/* FIT-DNA Test Card */}
          <Card className="p-8 bg-neutral-900 text-white border-0">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="inline-block px-3 py-1 bg-white/10 rounded-full text-xs mb-4">
                  체력 MBTI
                </div>
                <h2 className="text-white mb-3">나의 FIT-DNA는?</h2>
                <p className="text-white/70 mb-6">
                  국민체력100 데이터로 분석하는 내 체력 유형 검사
                </p>
                <div className="flex gap-3">
                  <Button className="bg-white text-neutral-900 hover:bg-white/90" onClick={() => setCurrentScreen('fitdna')}>
                    테스트 시작하기
                    <ChevronRight className="w-4 h-4 ml-1" />
                  </Button>
                  <Button 
                    className="bg-transparent border border-white text-white hover:bg-white/10"
                    onClick={() => setCurrentScreen('fitdna-types')}
                  >
                    FIT-DNA 8가지 유형 모두 보기
                  </Button>
                </div>
              </div>
              <div className="w-32 h-32 bg-white/5 rounded-lg"></div>
            </div>
          </Card>

          {/* Quick Menu */}
          <div>
            <h3 className="text-neutral-900 mb-4">빠른 메뉴</h3>
            <div className="grid grid-cols-2 gap-4">
              <Button 
                variant="outline" 
                className="h-40 flex-col gap-4 border-neutral-200 bg-white hover:bg-neutral-50"
                onClick={() => setCurrentScreen('workout-record')}
              >
                <div className="w-24 h-24 rounded-full bg-neutral-100 flex items-center justify-center">
                  <Dumbbell className="w-20 h-20 text-neutral-700" />
                </div>
                <span className="text-neutral-900">운동 & 기록</span>
              </Button>
              
              <Button 
                variant="outline" 
                className="h-40 flex-col gap-4 border-neutral-200 bg-white hover:bg-neutral-50"
                onClick={() => setCurrentScreen('injury')}
              >
                <div className="w-24 h-24 rounded-full bg-neutral-100 flex items-center justify-center">
                  <AlertTriangle className="w-20 h-20 text-neutral-700" />
                </div>
                <span className="text-neutral-900">부상 관리</span>
              </Button>

              <Button 
                variant="outline" 
                className="h-40 flex-col gap-4 border-neutral-200 bg-white hover:bg-neutral-50"
                onClick={() => setCurrentScreen('weather')}
              >
                <div className="w-24 h-24 rounded-full bg-neutral-100 flex items-center justify-center">
                  <Cloud className="w-20 h-20 text-neutral-700" />
                </div>
                <span className="text-neutral-900">날씨 운동</span>
              </Button>

              <Button 
                variant="outline" 
                className="h-40 flex-col gap-4 border-neutral-200 bg-white hover:bg-neutral-50"
                onClick={() => setCurrentScreen('mate')}
              >
                <div className="w-24 h-24 rounded-full bg-neutral-100 flex items-center justify-center">
                  <Users className="w-20 h-20 text-neutral-700" />
                </div>
                <span className="text-neutral-900">FIT-MATE</span>
              </Button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}