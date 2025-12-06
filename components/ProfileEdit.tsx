import { ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { Label } from './ui/label';
import { useState, useEffect } from 'react';

interface ProfileEditProps {
  onBack: () => void;
  onSave: () => void;
}

export function ProfileEdit({ onBack, onSave }: ProfileEditProps) {
  const [formData, setFormData] = useState({
    name: '',
    birthdate: '',
    email: '',
    city: '',
    district: '',
    weight: '',
    height: ''
  });

  useEffect(() => {
    // 로컬 스토리지에서 사용자 정보 불러오기
    const userData = localStorage.getItem('userData');
    const testData = localStorage.getItem('fitDnaTestData');
    
    if (userData) {
      const parsed = JSON.parse(userData);
      setFormData(prev => ({
        ...prev,
        name: parsed.name || '',
        birthdate: parsed.birthdate || '',
        email: parsed.email || '',
        city: parsed.city || '',
        district: parsed.district || ''
      }));
    }
    
    if (testData) {
      const parsed = JSON.parse(testData);
      if (parsed.userInfo) {
        setFormData(prev => ({
          ...prev,
          weight: parsed.userInfo.weight || '',
          height: parsed.userInfo.height || ''
        }));
      }
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // 사용자 정보 업데이트
    const userData = {
      name: formData.name,
      birthdate: formData.birthdate,
      email: formData.email,
      city: formData.city,
      district: formData.district
    };
    localStorage.setItem('userData', JSON.stringify(userData));

    // 체중/신장 정보 업데이트
    const testData = localStorage.getItem('fitDnaTestData');
    if (testData) {
      const parsed = JSON.parse(testData);
      parsed.userInfo = {
        ...parsed.userInfo,
        weight: formData.weight,
        height: formData.height
      };
      localStorage.setItem('fitDnaTestData', JSON.stringify(parsed));
    } else {
      // 테스트 데이터가 없으면 기본 정보만 저장
      const newTestData = {
        userInfo: {
          weight: formData.weight,
          height: formData.height,
          age: '',
          gender: ''
        }
      };
      localStorage.setItem('fitDnaTestData', JSON.stringify(newTestData));
    }

    alert('프로필이 저장되었습니다.');
    onSave();
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-2xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">프로필 수정</h2>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-12">
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

            <div className="border-t border-neutral-200 pt-6">
              <h3 className="text-neutral-900 mb-4">신체 정보</h3>
              
              {/* 체중 */}
              <div className="mb-4">
                <Label htmlFor="weight" className="text-neutral-900 mb-2 block">체중 (kg)</Label>
                <Input
                  id="weight"
                  type="number"
                  value={formData.weight}
                  onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                  className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>

              {/* 신장 */}
              <div>
                <Label htmlFor="height" className="text-neutral-900 mb-2 block">신장 (cm)</Label>
                <Input
                  id="height"
                  type="number"
                  value={formData.height}
                  onChange={(e) => setFormData({ ...formData, height: e.target.value })}
                  className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                />
              </div>
            </div>

            <div className="flex gap-3">
              <Button type="button" variant="outline" className="flex-1 border-neutral-200" onClick={onBack}>
                취소
              </Button>
              <Button type="submit" className="flex-1 bg-neutral-900 hover:bg-neutral-800">
                저장
              </Button>
            </div>
          </form>
        </Card>
      </main>
    </div>
  );
}
