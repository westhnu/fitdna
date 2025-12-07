/**
 * FIT-DNA 웹 애플리케이션 - API 통합 버전
 *
 * 사용법:
 * 1. 백엔드 서버 실행: cd backend && python run.py
 * 2. 이 파일을 App.tsx로 복사하거나 import 경로 변경
 * 3. npm run dev 또는 개발 서버 실행
 */

import { MyPageIntegrated } from './components/MyPageIntegrated';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <MyPageIntegrated />
    </div>
  );
}
