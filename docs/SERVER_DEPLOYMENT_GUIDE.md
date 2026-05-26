# FIT-DNA 서버 배포 가이드

**작성일:** 2025-11-23
**목적:** 프로토타입 서버 배포 방안 검토

---

## 📋 목차
1. [서버 요구사항 분석](#1-서버-요구사항-분석)
2. [배포 옵션 비교](#2-배포-옵션-비교)
3. [프로토타입 추천 방안](#3-프로토타입-추천-방안)
4. [단계별 배포 전략](#4-단계별-배포-전략)
5. [기술 스택 추천](#5-기술-스택-추천)

---

## 1. 서버 요구사항 분석

### 1.1 FIT-DNA 서비스 특성

**데이터 처리 특성:**
```
✓ 실시간 계산 필요: FIT-DNA 유형 분석 (Z-Score 계산)
✓ 배치 처리 가능: 매칭 추천, 예측 모델
✓ 데이터 크기: 약 10MB (전처리 완료된 데이터)
✓ 동시 접속: 프로토타입 단계에서는 10~50명 예상
```

**필요한 리소스:**
```
CPU: 중간 (Python 계산 위주)
메모리: 2~4GB (pandas 데이터프레임 로드)
저장소: 1~5GB (데이터 + 모델 + 이미지)
네트워크: 낮음 (API 요청/응답만)
```

**서비스 구성:**
```
1. REST API 서버 (FastAPI 또는 Flask)
2. 데이터베이스 (SQLite → PostgreSQL)
3. 파일 스토리지 (사진 업로드 시)
```

---

## 2. 배포 옵션 비교

### 옵션 1: 학교 원격 서버 (SSH) ⭐ 추천 (프로토타입)

**장점:**
```
✅ 무료 (학교 제공)
✅ 빠른 시작 (바로 사용 가능)
✅ SSH 접속으로 직접 제어 가능
✅ 배포/디버깅 편리
✅ 추가 비용 없음
```

**단점:**
```
❌ 외부 접속 제한 가능 (방화벽)
❌ 성능/용량 제한
❌ 서버 재시작 시 수동 복구 필요
❌ HTTPS 설정 어려울 수 있음
❌ 학기 종료 후 사용 불가능할 수 있음
```

**적합한 경우:**
- ✅ 프로토타입/MVP 단계
- ✅ 팀 내부 테스트
- ✅ 소규모 사용자 (10~50명)
- ✅ 빠른 개발/배포 반복

---

### 옵션 2: AWS 클라우드

#### 2-1. AWS EC2 (가상 서버)

**장점:**
```
✅ 확장성 우수
✅ 외부 접속 자유로움
✅ HTTPS 설정 쉬움
✅ 안정적인 운영
✅ 다양한 서비스 연동 (S3, RDS 등)
```

**단점:**
```
❌ 비용 발생
   - t2.micro (프리티어): 월 $0 (12개월)
   - t3.small: 월 $15~20
   - t3.medium: 월 $30~40
❌ 설정 복잡도 높음
❌ 관리 부담
❌ 프리티어 종료 후 과금
```

**예상 비용 (프로토타입):**
```
EC2 t2.micro (프리티어): $0/월
또는 t3.small: $15~20/월
RDS PostgreSQL (선택): $15~20/월
S3 스토리지: $1~5/월
총합: $0~45/월
```

#### 2-2. AWS Lightsail (간편 서버)

**장점:**
```
✅ 고정 요금제 (예측 가능)
✅ 설정 간단 (EC2보다)
✅ 외부 접속 자유
✅ HTTPS 자동 설정 지원
```

**비용:**
```
$3.50/월: 512MB RAM, 1 vCPU, 20GB SSD
$5/월: 1GB RAM, 1 vCPU, 40GB SSD ⭐ 추천
$10/월: 2GB RAM, 1 vCPU, 60GB SSD
```

#### 2-3. AWS Lambda + API Gateway (서버리스)

**장점:**
```
✅ 사용한 만큼만 과금
✅ 서버 관리 불필요
✅ 자동 확장
✅ 초기 비용 거의 없음
```

**단점:**
```
❌ 콜드 스타트 (첫 요청 느림)
❌ pandas/numpy 라이브러리 크기 제한
❌ 실행 시간 제한 (최대 15분)
❌ 복잡한 구조
```

**비용:**
```
Lambda: 월 100만 요청 무료
API Gateway: 월 100만 요청 무료
→ 프로토타입에서는 거의 무료
```

---

### 옵션 3: 무료 클라우드 서비스

#### 3-1. Heroku (간편 배포)

**장점:**
```
✅ 무료 티어 제공
✅ Git push로 자동 배포
✅ 설정 매우 간단
✅ HTTPS 자동
```

**단점:**
```
❌ 무료 티어: 512MB RAM, sleep 모드 (30분 미사용 시)
❌ 성능 제한
❌ 2022년부터 유료화 ($7/월~)
```

#### 3-2. Google Cloud Platform (GCP)

**장점:**
```
✅ $300 크레딧 (3개월)
✅ Always Free 티어
✅ 다양한 서비스
```

**단점:**
```
❌ AWS보다 설정 복잡
❌ 크레딧 종료 후 과금
```

#### 3-3. Vercel / Netlify (정적 호스팅 + API)

**장점:**
```
✅ 무료
✅ 자동 배포
✅ HTTPS 자동
```

**단점:**
```
❌ Serverless Functions만 지원 (긴 계산 어려움)
❌ pandas 등 무거운 라이브러리 제한
```

---

## 3. 프로토타입 추천 방안

### 🎯 최종 추천: 단계별 접근

### Phase 1: 개발 초기 (1~2주)
```
👉 학교 원격 서버 (SSH)

이유:
- 무료
- 빠른 시작
- 팀 내부 테스트 충분
- 배포/디버깅 편리

구성:
- FastAPI 서버
- SQLite 데이터베이스
- 포트 포워딩 (ngrok 또는 학교 방화벽 설정)
```

### Phase 2: 외부 테스트 (2~4주)
```
👉 AWS Lightsail $5/월

이유:
- 저렴한 고정 요금
- 외부 접속 자유
- HTTPS 설정 가능
- 안정적 운영

구성:
- FastAPI 서버
- PostgreSQL (또는 SQLite)
- Nginx + SSL 인증서
```

### Phase 3: 정식 출시 (검토 필요 시)
```
👉 AWS EC2 + RDS + S3

이유:
- 확장성
- 성능
- 안정성
- 다양한 기능

예상 비용: $30~50/월
```

---

## 4. 단계별 배포 전략

### 4.1 학교 서버 배포 (프로토타입)

**1단계: 환경 설정**
```bash
# SSH 접속
ssh username@school-server.ac.kr

# Python 가상환경 생성
python3 -m venv fitdna_env
source fitdna_env/bin/activate

# 패키지 설치
pip install fastapi uvicorn pandas numpy scipy scikit-learn
```

**2단계: 서버 코드 배포**
```bash
# Git으로 코드 가져오기
git clone https://github.com/your-repo/fitdna-server.git
cd fitdna-server

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000
```

**3단계: 외부 접속 설정**
```bash
# 옵션 1: ngrok (간편, 임시)
ngrok http 8000
→ https://xxxx-xx-xx-xx-xx.ngrok.io 주소 생성

# 옵션 2: 학교 방화벽 포트 개방 요청
→ IT 관리자에게 포트 8000 개방 요청
```

**4단계: 백그라운드 실행**
```bash
# screen 또는 tmux 사용
screen -S fitdna
uvicorn main:app --host 0.0.0.0 --port 8000
# Ctrl+A, D로 분리

# 또는 nohup
nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
```

---

### 4.2 AWS Lightsail 배포 (외부 테스트)

**1단계: Lightsail 인스턴스 생성**
```
1. AWS 콘솔 → Lightsail
2. Create instance
3. OS: Ubuntu 22.04
4. Plan: $5/월 (1GB RAM)
5. SSH 키 다운로드
```

**2단계: 서버 설정**
```bash
# SSH 접속
ssh -i LightsailKey.pem ubuntu@your-lightsail-ip

# 업데이트
sudo apt update && sudo apt upgrade -y

# Python 설치
sudo apt install python3 python3-pip python3-venv -y

# 프로젝트 배포
git clone https://github.com/your-repo/fitdna-server.git
cd fitdna-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3단계: Nginx + SSL 설정**
```bash
# Nginx 설치
sudo apt install nginx certbot python3-certbot-nginx -y

# Nginx 설정
sudo nano /etc/nginx/sites-available/fitdna

# 내용:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 활성화
sudo ln -s /etc/nginx/sites-available/fitdna /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# SSL 인증서 (무료)
sudo certbot --nginx -d your-domain.com
```

**4단계: Systemd 서비스 등록**
```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/fitdna.service

# 내용:
[Unit]
Description=FIT-DNA API Server
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/fitdna-server
Environment="PATH=/home/ubuntu/fitdna-server/venv/bin"
ExecStart=/home/ubuntu/fitdna-server/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target

# 서비스 시작
sudo systemctl daemon-reload
sudo systemctl start fitdna
sudo systemctl enable fitdna
```

---

## 5. 기술 스택 추천

### 5.1 백엔드 프레임워크

**추천: FastAPI** ⭐
```python
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

class FitnessInput(BaseModel):
    age: int
    gender: str
    strength_left: float
    strength_right: float
    jump: float
    flexibility: float
    vo2max: float

@app.post("/calculate-fitdna")
async def calculate_fitdna(data: FitnessInput):
    # Z-Score 계산 로직
    # FIT-DNA 유형 판정
    return {"fitdna": "PFE", "strengths": [...], "weaknesses": [...]}
```

**장점:**
- 빠른 성능
- 자동 문서화 (Swagger)
- 타입 검증 (Pydantic)
- 비동기 지원

**대안: Flask**
- 더 간단
- 레퍼런스 많음
- 프로토타입에 충분

---

### 5.2 데이터베이스

**프로토타입: SQLite** ⭐
```python
import sqlite3

# 간단하고 빠름
# 파일 기반 (별도 서버 불필요)
# 소규모 데이터에 적합
```

**확장 시: PostgreSQL**
```python
# 동시 접속 처리 우수
# 확장성
# AWS RDS 연동 쉬움
```

---

### 5.3 파일 스토리지 (사진 업로드)

**프로토타입: 로컬 파일 시스템**
```python
from fastapi import UploadFile

@app.post("/upload-result")
async def upload_result(file: UploadFile):
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
```

**확장 시: AWS S3**
```python
import boto3

s3 = boto3.client('s3')
s3.upload_file('local_file', 'bucket', 'key')
```

---

## 6. 비용 비교표

| 옵션 | 초기 비용 | 월 비용 | 외부 접속 | HTTPS | 난이도 | 프로토타입 적합도 |
|------|-----------|---------|-----------|-------|--------|------------------|
| 학교 서버 | $0 | $0 | △ (제한적) | △ | 쉬움 | ⭐⭐⭐⭐⭐ |
| AWS Lightsail | $0 | $5 | ✅ | ✅ | 보통 | ⭐⭐⭐⭐ |
| AWS EC2 | $0 | $15~40 | ✅ | ✅ | 어려움 | ⭐⭐⭐ |
| AWS Lambda | $0 | $0~5 | ✅ | ✅ | 어려움 | ⭐⭐ |
| Heroku | $0 | $7 | ✅ | ✅ | 쉬움 | ⭐⭐⭐ |

---

## 7. 최종 권장사항

### 🎯 프로토타입 단계 (현재)

**1순위: 학교 원격 서버**
```
✅ 장점: 무료, 빠른 시작, 팀 내부 테스트 충분
✅ 기간: 1~2주
✅ 구성: FastAPI + SQLite + ngrok
```

**2순위: AWS Lightsail $5/월**
```
✅ 장점: 외부 접속 자유, HTTPS, 안정적
✅ 시기: 외부 테스트 필요 시
✅ 구성: FastAPI + PostgreSQL + Nginx + SSL
```

### 🚀 정식 출시 시 (추후 검토)

**AWS EC2 + RDS + S3**
```
예상 비용: $30~50/월
확장성, 성능, 안정성 확보
```

---

## 8. Q&A

**Q1: 프로토타입에 AWS가 꼭 필요한가?**
```
A: 아니요. 학교 서버로 충분합니다.
   - 팀 내부 테스트: 학교 서버 OK
   - 외부 데모: ngrok 또는 AWS Lightsail $5
```

**Q2: 데이터베이스가 필요한가?**
```
A: 프로토타입에서는 선택사항
   - CSV 파일만으로도 가능
   - SQLite 추천 (간단, 빠름)
   - 사용자 로그인 구현 시 필수
```

**Q3: 사진 업로드 OCR은?**
```
A: 프로토타입에서는 간소화 추천
   - 직접 입력만 구현
   - OCR은 추후 추가 (AWS Textract 또는 Google Vision API)
```

**Q4: 앱과 서버 연동은?**
```
A: REST API 사용
   앱 (Flutter/React Native) → HTTP 요청 → FastAPI 서버
   예: POST /calculate-fitdna
```

**Q5: 학교 서버 외부 접속이 안 되면?**
```
A: ngrok 사용 (무료)
   - 로컬 서버를 임시 도메인으로 노출
   - https://xxxx.ngrok.io
   - 프로토타입/데모용으로 충분
```

---

## 9. 체크리스트

프로토타입 배포 전 확인사항:

### 서버 선택
- [ ] 학교 서버 사용 가능 여부 확인
- [ ] 외부 접속 필요 여부 결정
- [ ] 예산 확인 ($0 / $5 / $30+)

### 기능 범위
- [ ] 직접 입력 vs 사진 업로드
- [ ] 사용자 로그인 필요 여부
- [ ] 매칭 기능 포함 여부

### 기술 스택
- [ ] FastAPI 또는 Flask
- [ ] SQLite 또는 PostgreSQL
- [ ] 로컬 파일 또는 S3

---

**작성일:** 2025-11-23
**다음 업데이트:** 서버 선택 후 상세 배포 가이드 작성
