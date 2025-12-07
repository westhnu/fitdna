/**
 * 월간 리포트 임시 데이터
 * 마이페이지에서 사용할 Mock Data
 */

export interface WorkoutSession {
  date: string; // YYYY-MM-DD
  exerciseType: 'strength' | 'flexibility' | 'endurance';
  exercises: string[];
  duration: number; // 분
  intensity: 'low' | 'medium' | 'high';
}

export interface MetricChange {
  name: string; // 측정 항목 이름 (예: "악력(오른손)")
  unit: string; // 단위 (kg, cm, 회)
  previousMonth: number;
  currentMonth: number;
  change: number; // 변화량
  changePercentage: number; // 변화율 (%)
}

export interface ConsistencyScore {
  totalScore: number; // 0-100점
  breakdown: {
    achievementRate: number; // 목표 달성률 (0-40점)
    regularity: number; // 운동 규칙성 (0-40점)
    intensityMaintenance: number; // 강도 유지도 (0-20점)
  };
  feedback: string; // 피드백 메시지
}

export interface MonthlyReport {
  year: number;
  month: number; // 1-12
  summary: {
    totalWorkoutDays: number; // 총 운동 일수
    weeklyAverage: number; // 주당 평균 운동 횟수
    totalDuration: number; // 총 운동 시간 (분)
  };
  workoutFrequency: {
    strength: number; // 근력 운동 횟수
    flexibility: number; // 유연성 운동 횟수
    endurance: number; // 지구력 운동 횟수
  };
  sessions: WorkoutSession[];
  metricChanges: MetricChange[];
  consistencyScore: ConsistencyScore;
}

// 임시 데이터
export const mockMonthlyReport: MonthlyReport = {
  year: 2025,
  month: 11, // 11월
  summary: {
    totalWorkoutDays: 18,
    weeklyAverage: 4.5,
    totalDuration: 1080, // 18시간
  },
  workoutFrequency: {
    strength: 12,
    flexibility: 8,
    endurance: 10,
  },
  sessions: [
    {
      date: '2025-11-01',
      exerciseType: 'strength',
      exercises: ['스쿼트', '푸시업', '플랭크'],
      duration: 60,
      intensity: 'high',
    },
    {
      date: '2025-11-03',
      exerciseType: 'endurance',
      exercises: ['조깅', '버피테스트'],
      duration: 45,
      intensity: 'medium',
    },
    {
      date: '2025-11-05',
      exerciseType: 'flexibility',
      exercises: ['요가', '스트레칭'],
      duration: 50,
      intensity: 'low',
    },
    {
      date: '2025-11-07',
      exerciseType: 'strength',
      exercises: ['데드리프트', '벤치프레스', '풀업'],
      duration: 70,
      intensity: 'high',
    },
    {
      date: '2025-11-09',
      exerciseType: 'endurance',
      exercises: ['사이클링'],
      duration: 60,
      intensity: 'medium',
    },
    {
      date: '2025-11-11',
      exerciseType: 'strength',
      exercises: ['레그프레스', '숄더프레스'],
      duration: 55,
      intensity: 'high',
    },
    {
      date: '2025-11-13',
      exerciseType: 'flexibility',
      exercises: ['필라테스'],
      duration: 60,
      intensity: 'medium',
    },
    {
      date: '2025-11-15',
      exerciseType: 'endurance',
      exercises: ['수영'],
      duration: 50,
      intensity: 'high',
    },
    {
      date: '2025-11-17',
      exerciseType: 'strength',
      exercises: ['스쿼트', '런지', '카프레이즈'],
      duration: 65,
      intensity: 'high',
    },
    {
      date: '2025-11-19',
      exerciseType: 'flexibility',
      exercises: ['요가', '폼롤러'],
      duration: 45,
      intensity: 'low',
    },
    {
      date: '2025-11-21',
      exerciseType: 'endurance',
      exercises: ['인터벌 러닝'],
      duration: 40,
      intensity: 'high',
    },
    {
      date: '2025-11-23',
      exerciseType: 'strength',
      exercises: ['풀업', '딥스', '플랭크'],
      duration: 55,
      intensity: 'medium',
    },
    {
      date: '2025-11-25',
      exerciseType: 'endurance',
      exercises: ['조깅', '계단오르기'],
      duration: 50,
      intensity: 'medium',
    },
    {
      date: '2025-11-26',
      exerciseType: 'flexibility',
      exercises: ['스트레칭', '요가'],
      duration: 55,
      intensity: 'low',
    },
    {
      date: '2025-11-27',
      exerciseType: 'strength',
      exercises: ['벤치프레스', '로우'],
      duration: 60,
      intensity: 'high',
    },
    {
      date: '2025-11-28',
      exerciseType: 'endurance',
      exercises: ['수영'],
      duration: 55,
      intensity: 'medium',
    },
    {
      date: '2025-11-29',
      exerciseType: 'strength',
      exercises: ['데드리프트', '스쿼트'],
      duration: 70,
      intensity: 'high',
    },
    {
      date: '2025-11-30',
      exerciseType: 'flexibility',
      exercises: ['필라테스', '폼롤러'],
      duration: 50,
      intensity: 'medium',
    },
  ],
  metricChanges: [
    {
      name: '악력 (오른손)',
      unit: 'kg',
      previousMonth: 38.5,
      currentMonth: 41.2,
      change: 2.7,
      changePercentage: 7.0,
    },
    {
      name: '악력 (왼손)',
      unit: 'kg',
      previousMonth: 36.8,
      currentMonth: 39.1,
      change: 2.3,
      changePercentage: 6.3,
    },
    {
      name: '윗몸일으키기',
      unit: '회/분',
      previousMonth: 42,
      currentMonth: 48,
      change: 6,
      changePercentage: 14.3,
    },
    {
      name: '앉아윗몸앞으로굽히기',
      unit: 'cm',
      previousMonth: 12.5,
      currentMonth: 15.8,
      change: 3.3,
      changePercentage: 26.4,
    },
    {
      name: '제자리멀리뛰기',
      unit: 'cm',
      previousMonth: 195,
      currentMonth: 205,
      change: 10,
      changePercentage: 5.1,
    },
    {
      name: 'VO2max',
      unit: 'ml/kg/min',
      previousMonth: 42.3,
      currentMonth: 44.8,
      change: 2.5,
      changePercentage: 5.9,
    },
  ],
  consistencyScore: {
    totalScore: 87,
    breakdown: {
      achievementRate: 36, // 목표 대비 90% 달성 (40점 만점)
      regularity: 35, // 주 4-5회 규칙적 운동 (40점 만점)
      intensityMaintenance: 16, // 강도 유지 잘함 (20점 만점)
    },
    feedback:
      '훌륭해요! 이번 달 꾸준히 운동하셨네요. 특히 근력 운동에 집중하신 것이 지표 개선으로 나타났습니다. 다음 달에는 유연성 운동을 조금 더 늘려보는 것을 추천드립니다.',
  },
};

// 여러 달 데이터 (차트용)
export const mockMonthlyReports: MonthlyReport[] = [
  // 9월 데이터
  {
    year: 2025,
    month: 9,
    summary: {
      totalWorkoutDays: 12,
      weeklyAverage: 3.0,
      totalDuration: 720,
    },
    workoutFrequency: {
      strength: 7,
      flexibility: 5,
      endurance: 6,
    },
    sessions: [],
    metricChanges: [],
    consistencyScore: {
      totalScore: 68,
      breakdown: {
        achievementRate: 27,
        regularity: 26,
        intensityMaintenance: 15,
      },
      feedback: '운동을 시작하셨네요! 꾸준히 이어가세요.',
    },
  },
  // 10월 데이터
  {
    year: 2025,
    month: 10,
    summary: {
      totalWorkoutDays: 15,
      weeklyAverage: 3.75,
      totalDuration: 900,
    },
    workoutFrequency: {
      strength: 9,
      flexibility: 6,
      endurance: 8,
    },
    sessions: [],
    metricChanges: [],
    consistencyScore: {
      totalScore: 76,
      breakdown: {
        achievementRate: 30,
        regularity: 30,
        intensityMaintenance: 16,
      },
      feedback: '지난 달보다 개선되었어요! 이 페이스를 유지해보세요.',
    },
  },
  // 11월 데이터 (현재)
  mockMonthlyReport,
];
