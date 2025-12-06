import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { Label } from './ui/label';

interface LoginProps {
  onLogin: () => void;
  onSignUp: () => void;
}

export function Login({ onLogin, onSignUp }: LoginProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // 기본적인 로그인 처리 (실제로는 인증 로직 필요)
    onLogin();
  };

  return (
    <div className="min-h-screen bg-neutral-50 flex items-center justify-center px-8">
      <div className="w-full max-w-md">
        {/* Logo/Brand Area */}
        <div className="text-center mb-8">
          <h1 className="text-neutral-900 mb-2">FIT-DNA</h1>
          <p className="text-neutral-500">나만의 체력 데이터로 시작하는 건강한 삶</p>
        </div>

        {/* Login Card */}
        <Card className="p-8 border border-neutral-200 bg-white">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <Label htmlFor="email" className="text-neutral-900 mb-2 block">이메일</Label>
              <Input 
                id="email"
                type="email" 
                placeholder="email@example.com"
                className="border-neutral-200"
                required
              />
            </div>

            <div>
              <Label htmlFor="password" className="text-neutral-900 mb-2 block">비밀번호</Label>
              <Input 
                id="password"
                type="password" 
                placeholder="비밀번호를 입력하세요"
                className="border-neutral-200"
                required
              />
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded border-neutral-300" />
                <span className="text-neutral-600">로그인 상태 유지</span>
              </label>
              <button type="button" className="text-neutral-600 hover:text-neutral-900">
                비밀번호 찾기
              </button>
            </div>

            <Button type="submit" className="w-full">
              로그인
            </Button>
          </form>

          <div className="mt-6 pt-6 border-t border-neutral-200">
            <div className="text-center text-sm text-neutral-600 mb-4">
              또는 다음으로 계속하기
            </div>
            <div className="space-y-3">
              <Button 
                type="button" 
                variant="outline" 
                className="w-full border-neutral-200"
              >
                Google로 계속하기
              </Button>
              <Button 
                type="button" 
                variant="outline" 
                className="w-full border-neutral-200"
              >
                카카오로 계속하기
              </Button>
            </div>
          </div>
        </Card>

        {/* Sign Up Link */}
        <div className="text-center mt-6">
          <p className="text-neutral-600 text-sm">
            아직 계정이 없으신가요?{' '}
            <button className="text-neutral-900 hover:underline" onClick={onSignUp}>
              회원가입
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}