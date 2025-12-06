import { ArrowLeft, Send } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { useState } from 'react';

interface AiChatProps {
  onBack: () => void;
}

export function AiChat({ onBack }: AiChatProps) {
  const [message, setMessage] = useState('');

  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col">
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4 flex items-center gap-4">
          <button onClick={onBack} className="p-2 hover:bg-neutral-100 rounded-lg">
            <ArrowLeft className="w-5 h-5 text-neutral-700" />
          </button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-neutral-100 flex items-center justify-center">
              <span className="text-lg">🤖</span>
            </div>
            <div>
              <h2 className="text-neutral-900">AI 운동 비서 하루</h2>
              <span className="text-neutral-500 text-sm">항상 함께하는 운동 파트너</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-4xl mx-auto w-full px-8 py-8 overflow-auto">
        <div className="space-y-6">
          {/* AI Message */}
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-neutral-100 flex items-center justify-center flex-shrink-0">
              <span>🤖</span>
            </div>
            <Card className="p-4 border border-neutral-200 bg-white max-w-md">
              <p className="text-neutral-700 text-sm">
                안녕하세요! 저는 AI 운동 비서 하루입니다. 😊<br />
                오늘 운동 계획을 함께 세워볼까요?
              </p>
              <span className="text-neutral-400 text-xs mt-2 block">오전 9:30</span>
            </Card>
          </div>

          {/* User Message */}
          <div className="flex gap-3 justify-end">
            <Card className="p-4 bg-neutral-900 text-white max-w-md">
              <p className="text-sm">
                오늘 날씨가 좋은데 추천해줄 운동 있어?
              </p>
              <span className="text-white/60 text-xs mt-2 block">오전 9:32</span>
            </Card>
          </div>

          {/* AI Message */}
          <div className="flex gap-3">
            <div className="w-8 h-8 rounded-full bg-neutral-100 flex items-center justify-center flex-shrink-0">
              <span>🤖</span>
            </div>
            <Card className="p-4 border border-neutral-200 bg-white max-w-md">
              <p className="text-neutral-700 text-sm mb-3">
                날씨가 좋으시다니 야외 운동이 좋을 것 같아요! 🌤️<br />
                이런 운동들은 어떠세요?
              </p>
              <div className="space-y-2">
                <div className="p-3 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 text-sm mb-1">🏃‍♂️ 공원 러닝 30분</p>
                  <p className="text-neutral-500 text-xs">유산소 운동 · 칼로리 200kcal</p>
                </div>
                <div className="p-3 bg-neutral-50 rounded-lg">
                  <p className="text-neutral-900 text-sm mb-1">🚴‍♂️ 자전거 라이딩 1시간</p>
                  <p className="text-neutral-500 text-xs">유산소 운동 · 칼로리 400kcal</p>
                </div>
              </div>
              <span className="text-neutral-400 text-xs mt-2 block">오전 9:33</span>
            </Card>
          </div>
        </div>
      </main>

      {/* Input Area */}
      <div className="bg-white border-t border-neutral-200">
        <div className="max-w-4xl mx-auto px-8 py-4">
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="하루에게 메시지 보내기..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="flex-1 px-4 py-3 border border-neutral-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-neutral-900"
            />
            <Button className="bg-neutral-900 hover:bg-neutral-800 px-6">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
