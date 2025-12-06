import { ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { Label } from './ui/label';
import { useState } from 'react';

interface SignUpProps {
  onSignUp: (userData: any) => void;
  onBack: () => void;
}

export function SignUp({ onSignUp, onBack }: SignUpProps) {
  const [formData, setFormData] = useState({
    name: '',
    birthdate: '',
    gender: '',
    email: '',
    password: '',
    confirmPassword: '',
    city: '',
    district: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      alert('비밀번호가 일치하지 않습니다.');
      return;
    }

    // 로컬 스토리지에 사용자 정보 저장
    const userData = {
      name: formData.name,
      birthdate: formData.birthdate,
      gender: formData.gender,
      email: formData.email,
      city: formData.city,
      district: formData.district,
      createdAt: new Date().toISOString()
    };
    
    localStorage.setItem('userData', JSON.stringify(userData));
    onSignUp(userData);
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-2xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">회원가입</h2>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-2">FIT-DNA 시작하기</h1>
          <p className="text-neutral-500">나만의 체력 데이터로 건강한 삶을 시작하세요</p>
        </div>

        <Card className="p-8 border border-neutral-200 bg-white">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* 이름 */}
            <div>
              <Label htmlFor="name" className="text-neutral-900 mb-2 block">이름</Label>
              <Input
                id="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="border-neutral-200"
                required
              />
            </div>

            {/* 생년월일 */}
            <div>
              <Label htmlFor="birthdate" className="text-neutral-900 mb-2 block">생년월일</Label>
              <Input
                id="birthdate"
                type="date"
                value={formData.birthdate}
                onChange={(e) => setFormData({ ...formData, birthdate: e.target.value })}
                className="border-neutral-200"
                required
              />
            </div>

            {/* 성별 */}
            <div>
              <Label htmlFor="gender" className="text-neutral-900 mb-2 block">성별</Label>
              <select
                id="gender"
                value={formData.gender}
                onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                className="px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 bg-white"
                required
              >
                <option value="">성별 선택</option>
                <option value="남자">남자</option>
                <option value="여자">여자</option>
              </select>
            </div>

            {/* 이메일 */}
            <div>
              <Label htmlFor="email" className="text-neutral-900 mb-2 block">이메일</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="border-neutral-200"
                required
              />
            </div>

            {/* 거주지 */}
            <div>
              <Label className="text-neutral-900 mb-2 block">거주지</Label>
              <div className="grid grid-cols-2 gap-3">
                <select
                  value={formData.city}
                  onChange={(e) => setFormData({ ...formData, city: e.target.value })}
                  className="px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900 bg-white"
                  required
                >
                  <option value="">시/도 선택</option>
                  <option value="서울특별시">서울특별시</option>
                  <option value="부산광역시">부산광역시</option>
                  <option value="대구광역시">대구광역시</option>
                  <option value="인천광역시">인천광역시</option>
                  <option value="광주광역시">광주광역시</option>
                  <option value="대전광역시">대전광역시</option>
                  <option value="울산광역시">울산광역시</option>
                  <option value="세종특별자치시">세종특별자치시</option>
                  <option value="경기도">경기도</option>
                  <option value="강원도">강원도</option>
                  <option value="충청북도">충청북도</option>
                  <option value="충청남도">충청남도</option>
                  <option value="전라북도">전라북도</option>
                  <option value="전라남도">전라남도</option>
                  <option value="경상북도">경상북도</option>
                  <option value="경상남도">경상남도</option>
                  <option value="제주특별자치도">제주특별자치도</option>
                </select>
                <Input
                  type="text"
                  placeholder="시/군/구"
                  value={formData.district}
                  onChange={(e) => setFormData({ ...formData, district: e.target.value })}
                  className="border-neutral-200"
                  required
                />
              </div>
            </div>

            {/* 비밀번호 */}
            <div>
              <Label htmlFor="password" className="text-neutral-900 mb-2 block">비밀번호</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="border-neutral-200"
                required
                minLength={8}
              />
              <p className="text-neutral-500 text-sm mt-1">8자 이상 입력해주세요</p>
            </div>

            {/* 비밀번호 확인 */}
            <div>
              <Label htmlFor="confirmPassword" className="text-neutral-900 mb-2 block">비밀번호 확인</Label>
              <Input
                id="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                className="border-neutral-200"
                required
                minLength={8}
              />
            </div>

            {/* 약관 동의 */}
            <div className="space-y-3 pt-4 border-t border-neutral-200">
              <label className="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" className="mt-1 rounded border-neutral-300" required />
                <span className="text-neutral-900 text-sm">
                  [필수] 서비스 이용약관에 동의합니다
                </span>
              </label>
              <label className="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" className="mt-1 rounded border-neutral-300" required />
                <span className="text-neutral-900 text-sm">
                  [필수] 개인정보 처리방침에 동의합니다
                </span>
              </label>
              <label className="flex items-start gap-3 cursor-pointer">
                <input type="checkbox" className="mt-1 rounded border-neutral-300" />
                <span className="text-neutral-600 text-sm">
                  [선택] 마케팅 정보 수신에 동의합니다
                </span>
              </label>
            </div>

            <Button type="submit" className="w-full bg-neutral-900 hover:bg-neutral-800">
              가입하기
            </Button>
          </form>
        </Card>
      </main>
    </div>
  );
}