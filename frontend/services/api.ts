/**
 * FIT-DNA API 클라이언트
 * FastAPI 백엔드와 통신
 */

const API_BASE_URL = 'http://localhost:8001/api';

// API 응답 타입
export interface FitDNAResult {
  user_id: number;
  fitdna_card: {
    type: string;
    name: string;
    keywords: string[];
    description: string;
  };
  strengths_weaknesses: {
    strength_score: number;
    flexibility_score: number;
    endurance_score: number;
    strengths: string[];
    weaknesses: string[];
  };
  recommended_exercises: Array<{
    name: string;
    category: string;
    difficulty: string;
  }>;
  recommended_routine: {
    level: string;
    weekly_plan: Record<string, string[]>;
  };
  compatible_types: string[];
}

export interface MonthlyReportAPI {
  user_id: number;
  year: number;
  month: number;
  summary: {
    total_workout_days: number;
    weekly_average: number;
    total_duration: number;
    total_sessions: number;
  };
  workout_frequency: {
    strength: number;
    flexibility: number;
    endurance: number;
  };
  metric_changes: Array<{
    name: string;
    unit: string;
    previous_month: number;
    current_month: number;
    change: number;
    change_percentage: number;
  }>;
  consistency_score: {
    total_score: number;
    breakdown: {
      achievement_rate: number;
      regularity: number;
      intensity_maintenance: number;
    };
    feedback: string;
  };
}

export interface Facility {
  id: number;
  name: string;
  type: string;
  distance_km: number;
  address: string;
  sports: string;
  latitude: number;
  longitude: number;
}

/**
 * FIT-DNA 결과 조회
 */
export async function getFitDNAResult(userId: number): Promise<FitDNAResult> {
  const response = await fetch(`${API_BASE_URL}/fitdna/result/${userId}`);
  if (!response.ok) {
    throw new Error('FIT-DNA 결과를 가져올 수 없습니다');
  }
  return response.json();
}

/**
 * 월간 리포트 조회
 */
export async function getMonthlyReport(
  userId: number,
  year: number,
  month: number
): Promise<MonthlyReportAPI> {
  const response = await fetch(
    `${API_BASE_URL}/reports/monthly/${userId}?year=${year}&month=${month}`
  );
  if (!response.ok) {
    throw new Error('월간 리포트를 가져올 수 없습니다');
  }
  return response.json();
}

/**
 * 주변 시설 검색
 */
export async function getNearbyFacilities(
  lat: number,
  lon: number,
  radius: number = 2.0,
  limit: number = 10
): Promise<{ facilities: Facility[]; total_count: number }> {
  const response = await fetch(
    `${API_BASE_URL}/facilities/nearby?lat=${lat}&lon=${lon}&radius=${radius}&limit=${limit}`
  );
  if (!response.ok) {
    throw new Error('주변 시설을 가져올 수 없습니다');
  }
  return response.json();
}

/**
 * 운동 세션 조회
 */
export async function getWorkoutSessions(
  userId: number,
  startDate?: string,
  endDate?: string
): Promise<any> {
  let url = `${API_BASE_URL}/reports/workout-sessions/${userId}`;
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error('운동 세션을 가져올 수 없습니다');
  }
  return response.json();
}

/**
 * FIT-DNA 이력 조회
 */
export async function getFitDNAHistory(userId: number): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/reports/fitdna-history/${userId}`);
  if (!response.ok) {
    throw new Error('FIT-DNA 이력을 가져올 수 없습니다');
  }
  return response.json();
}
