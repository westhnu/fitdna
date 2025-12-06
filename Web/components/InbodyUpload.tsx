import { ArrowLeft } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { Label } from './ui/label';
import { useState } from 'react';

interface InbodyUploadProps {
  onBack: () => void;
  onSave: () => void;
}

export function InbodyUpload({ onBack, onSave }: InbodyUploadProps) {
  const [formData, setFormData] = useState({
    weight: '',
    skeletalMuscle: '',
    bodyFat: '',
    bmi: '',
    bodyFatPercentage: '',
    rightArmMuscle: '',
    rightArmPercent: '',
    leftArmMuscle: '',
    leftArmPercent: '',
    trunkMuscle: '',
    trunkPercent: '',
    rightLegMuscle: '',
    rightLegPercent: '',
    leftLegMuscle: '',
    leftLegPercent: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const inbodyData = {
      weight: parseFloat(formData.weight),
      skeletalMuscle: parseFloat(formData.skeletalMuscle),
      bodyFat: parseFloat(formData.bodyFat),
      bmi: parseFloat(formData.bmi),
      bodyFatPercentage: parseFloat(formData.bodyFatPercentage),
      rightArm: {
        muscle: parseFloat(formData.rightArmMuscle),
        percent: parseFloat(formData.rightArmPercent)
      },
      leftArm: {
        muscle: parseFloat(formData.leftArmMuscle),
        percent: parseFloat(formData.leftArmPercent)
      },
      trunk: {
        muscle: parseFloat(formData.trunkMuscle),
        percent: parseFloat(formData.trunkPercent)
      },
      rightLeg: {
        muscle: parseFloat(formData.rightLegMuscle),
        percent: parseFloat(formData.rightLegPercent)
      },
      leftLeg: {
        muscle: parseFloat(formData.leftLegMuscle),
        percent: parseFloat(formData.leftLegPercent)
      },
      uploadedAt: new Date().toISOString()
    };

    localStorage.setItem('inbodyData', JSON.stringify(inbodyData));
    alert('인바디 검사 결과가 저장되었습니다.');
    onSave();
  };

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <h2 className="text-neutral-900">인바디 결과 입력</h2>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-8 py-12">
        <div className="mb-8">
          <h1 className="text-neutral-900 mb-2">인바디 검사 결과 입력</h1>
          <p className="text-neutral-500">
            인바디 검사지의 수치를 입력해주세요
          </p>
        </div>

        <Card className="p-8 border border-neutral-200 bg-white">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* 체성분 분석 */}
            <div>
              <h3 className="text-neutral-900 mb-4">체성분 분석</h3>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="weight" className="text-neutral-900 mb-2 block">체중 (kg)</Label>
                  <Input
                    id="weight"
                    type="number"
                    step="0.1"
                    value={formData.weight}
                    onChange={(e) => setFormData({ ...formData, weight: e.target.value })}
                    className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="skeletalMuscle" className="text-neutral-900 mb-2 block">골격근량 (kg)</Label>
                  <Input
                    id="skeletalMuscle"
                    type="number"
                    step="0.1"
                    value={formData.skeletalMuscle}
                    onChange={(e) => setFormData({ ...formData, skeletalMuscle: e.target.value })}
                    className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="bodyFat" className="text-neutral-900 mb-2 block">체지방량 (kg)</Label>
                  <Input
                    id="bodyFat"
                    type="number"
                    step="0.1"
                    value={formData.bodyFat}
                    onChange={(e) => setFormData({ ...formData, bodyFat: e.target.value })}
                    className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    required
                  />
                </div>
              </div>
            </div>

            {/* 비만 분석 */}
            <div>
              <h3 className="text-neutral-900 mb-4">비만 분석</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="bmi" className="text-neutral-900 mb-2 block">BMI</Label>
                  <Input
                    id="bmi"
                    type="number"
                    step="0.1"
                    value={formData.bmi}
                    onChange={(e) => setFormData({ ...formData, bmi: e.target.value })}
                    className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="bodyFatPercentage" className="text-neutral-900 mb-2 block">체지방률 (%)</Label>
                  <Input
                    id="bodyFatPercentage"
                    type="number"
                    step="0.1"
                    value={formData.bodyFatPercentage}
                    onChange={(e) => setFormData({ ...formData, bodyFatPercentage: e.target.value })}
                    className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                    required
                  />
                </div>
              </div>
            </div>

            {/* 부위별 근육 분석 */}
            <div>
              <h3 className="text-neutral-900 mb-4">부위별 근육 분석</h3>
              <div className="space-y-4">
                {/* 오른팔 */}
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 mb-3">오른팔</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">근육량 (kg)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.rightArmMuscle}
                        onChange={(e) => setFormData({ ...formData, rightArmMuscle: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">발달도 (%)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.rightArmPercent}
                        onChange={(e) => setFormData({ ...formData, rightArmPercent: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                  </div>
                </div>

                {/* 왼팔 */}
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 mb-3">왼팔</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">근육량 (kg)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.leftArmMuscle}
                        onChange={(e) => setFormData({ ...formData, leftArmMuscle: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">발달도 (%)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.leftArmPercent}
                        onChange={(e) => setFormData({ ...formData, leftArmPercent: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                  </div>
                </div>

                {/* 몸통 */}
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 mb-3">몸통</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">근육량 (kg)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.trunkMuscle}
                        onChange={(e) => setFormData({ ...formData, trunkMuscle: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">발달도 (%)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.trunkPercent}
                        onChange={(e) => setFormData({ ...formData, trunkPercent: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                  </div>
                </div>

                {/* 오른다리 */}
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 mb-3">오른다리</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">근육량 (kg)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.rightLegMuscle}
                        onChange={(e) => setFormData({ ...formData, rightLegMuscle: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">발달도 (%)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.rightLegPercent}
                        onChange={(e) => setFormData({ ...formData, rightLegPercent: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                  </div>
                </div>

                {/* 왼다리 */}
                <div className="p-4 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 mb-3">왼다리</p>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">근육량 (kg)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.leftLegMuscle}
                        onChange={(e) => setFormData({ ...formData, leftLegMuscle: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                    <div>
                      <Label className="text-neutral-600 text-sm mb-2 block">발달도 (%)</Label>
                      <Input
                        type="number"
                        step="0.1"
                        value={formData.leftLegPercent}
                        onChange={(e) => setFormData({ ...formData, leftLegPercent: e.target.value })}
                        className="border-neutral-200 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                        required
                      />
                    </div>
                  </div>
                </div>
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
