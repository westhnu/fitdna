import { Card } from './ui/card';
import { Button } from './ui/button';
import { Edit } from 'lucide-react';

interface InbodyData {
  weight: number;
  skeletalMuscle: number;
  bodyFat: number;
  bmi: number;
  bodyFatPercentage: number;
  rightArm: { muscle: number; percent: number };
  leftArm: { muscle: number; percent: number };
  trunk: { muscle: number; percent: number };
  rightLeg: { muscle: number; percent: number };
  leftLeg: { muscle: number; percent: number };
  uploadedAt?: string;
}

interface InbodyResultProps {
  data?: InbodyData;
  onUpload?: () => void;
}

export function InbodyResult({ data, onUpload }: InbodyResultProps) {
  if (!data) {
    return (
      <Card className="p-6 border border-neutral-200 bg-white">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-neutral-900">인바디 검사 결과</h3>
        </div>
        <div className="p-8 bg-neutral-50 rounded-lg text-center">
          <Edit className="w-12 h-12 text-neutral-400 mx-auto mb-3" />
          <p className="text-neutral-500 text-sm mb-4">
            인바디 검사 결과를 입력하면<br />
            상세한 신체 분석 정보를 확인할 수 있습니다
          </p>
          <Button size="sm" onClick={onUpload}>결과 입력</Button>
        </div>
      </Card>
    );
  }

  const getBarColor = (percent: number) => {
    if (percent < 90) return 'bg-blue-500';
    if (percent >= 90 && percent <= 110) return 'bg-neutral-900';
    return 'bg-red-500';
  };

  const getStatusText = (percent: number) => {
    if (percent < 90) return '부족';
    if (percent >= 90 && percent <= 110) return '정상';
    return '과다';
  };

  return (
    <Card className="p-6 border border-neutral-200 bg-white">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-neutral-900 mb-1">인바디 검사 결과</h3>
          {data.uploadedAt && (
            <p className="text-neutral-500 text-sm">
              {new Date(data.uploadedAt).toLocaleDateString('ko-KR')} 측정
            </p>
          )}
        </div>
        <Button size="sm" variant="outline" onClick={onUpload}>
          재입력
        </Button>
      </div>

      {/* 체성분 분석 */}
      <div className="mb-8">
        <h4 className="text-neutral-900 mb-4">체성분 분석</h4>
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 bg-neutral-50 rounded-lg">
            <p className="text-neutral-600 text-sm mb-1">체중</p>
            <p className="text-neutral-900">{data.weight} kg</p>
          </div>
          <div className="p-4 bg-neutral-50 rounded-lg">
            <p className="text-neutral-600 text-sm mb-1">골격근량</p>
            <p className="text-neutral-900">{data.skeletalMuscle} kg</p>
          </div>
          <div className="p-4 bg-neutral-50 rounded-lg">
            <p className="text-neutral-600 text-sm mb-1">체지방량</p>
            <p className="text-neutral-900">{data.bodyFat} kg</p>
          </div>
        </div>
      </div>

      {/* 비만 분석 */}
      <div className="mb-8">
        <h4 className="text-neutral-900 mb-4">비만 분석</h4>
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-neutral-50 rounded-lg">
            <p className="text-neutral-600 text-sm mb-1">BMI</p>
            <p className="text-neutral-900">{data.bmi}</p>
          </div>
          <div className="p-4 bg-neutral-50 rounded-lg">
            <p className="text-neutral-600 text-sm mb-1">체지방률</p>
            <p className="text-neutral-900">{data.bodyFatPercentage}%</p>
          </div>
        </div>
      </div>

      {/* 부위별 근육 분석 */}
      <div>
        <h4 className="text-neutral-900 mb-4">부위별 근육 분석</h4>
        
        {/* 신체 시각화 */}
        <div className="relative mb-6">
          <div className="flex items-center justify-center gap-8 py-8">
            {/* 신체 도식 */}
            <div className="relative">
              {/* 머리 */}
              <div className="w-16 h-16 rounded-full bg-neutral-200 mx-auto mb-2"></div>
              
              {/* 몸통과 팔 */}
              <div className="flex items-center justify-center gap-2">
                {/* 왼팔 */}
                <div className="flex flex-col items-center">
                  <div className="w-8 h-24 bg-neutral-200 rounded-full"></div>
                  <p className="text-xs text-neutral-600 mt-2">왼팔</p>
                  <p className="text-xs text-neutral-900">{data.leftArm.muscle}kg</p>
                </div>
                
                {/* 몸통 */}
                <div className="flex flex-col items-center">
                  <div className="w-24 h-32 bg-neutral-200 rounded-lg"></div>
                  <p className="text-xs text-neutral-600 mt-2">몸통</p>
                  <p className="text-xs text-neutral-900">{data.trunk.muscle}kg</p>
                </div>
                
                {/* 오른팔 */}
                <div className="flex flex-col items-center">
                  <div className="w-8 h-24 bg-neutral-200 rounded-full"></div>
                  <p className="text-xs text-neutral-600 mt-2">오른팔</p>
                  <p className="text-xs text-neutral-900">{data.rightArm.muscle}kg</p>
                </div>
              </div>
              
              {/* 다리 */}
              <div className="flex items-start justify-center gap-4 mt-2">
                {/* 왼다리 */}
                <div className="flex flex-col items-center">
                  <div className="w-10 h-32 bg-neutral-200 rounded-full"></div>
                  <p className="text-xs text-neutral-600 mt-2">왼다리</p>
                  <p className="text-xs text-neutral-900">{data.leftLeg.muscle}kg</p>
                </div>
                
                {/* 오른다리 */}
                <div className="flex flex-col items-center">
                  <div className="w-10 h-32 bg-neutral-200 rounded-full"></div>
                  <p className="text-xs text-neutral-600 mt-2">오른다리</p>
                  <p className="text-xs text-neutral-900">{data.rightLeg.muscle}kg</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}