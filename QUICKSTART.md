# 🚀 Startup Manager - 빠른 시작 가이드

## 📋 사전 요구사항

- **Python 3.11 이상** (3.12 권장)
- **Node.js 20+** (프론트엔드용, 선택사항)
- **Git** (버전 관리)

## 🎯 1분 설치 (Windows)

```cmd
# 1. 초기 설정 실행
python setup.py

# 2. 서버 실행
run.bat
```

## 🎯 1분 설치 (Mac/Linux)

```bash
# 1. 실행 권한 부여
chmod +x run.sh setup.py

# 2. 초기 설정 실행
python setup.py

# 3. 서버 실행
./run.sh
```

## 📝 수동 설치 단계

### 1️⃣ 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

### 3️⃣ 환경 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 OPENAI_API_KEY 설정
```

### 4️⃣ 데이터베이스 초기화

```bash
python backend/app/db/init_db.py
```

### 5️⃣ 서버 실행

```bash
# 개발 서버 실행
uvicorn backend.app.main:app --reload

# 또는 Python 스크립트로
python run.py
```

## 🌐 접속 URL

- **API 문서**: http://localhost:8000/api/docs
- **헬스체크**: http://localhost:8000/health
- **메인**: http://localhost:8000

## 🔑 테스트 계정

| 역할 | 이메일 | 비밀번호 |
|------|--------|----------|
| Admin | admin@startup.com | admin123 |
| Rep | rep@startup.com | rep123 |

## 🧪 API 테스트 (curl)

### 1. 헬스체크
```bash
curl http://localhost:8000/health
```

### 2. 로그인
```bash
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@startup.com&password=admin123"
```

### 3. 워크플로우 실행
```bash
curl -X POST http://localhost:8000/api/workflow/execute \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "이번 달 실적 분석하고 상위 고객 타게팅 전략 수립",
    "product_codes": ["PROD001", "PROD002"],
    "period": {"start": "202501", "end": "202512"}
  }'
```

## 🐳 Docker로 실행 (선택사항)

```bash
# 이미지 빌드
docker-compose build

# 컨테이너 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

## ❓ 문제 해결

### Python 버전 오류
```bash
# Python 3.11+ 설치 필요
# Windows: python.org에서 다운로드
# Mac: brew install python@3.11
# Linux: apt install python3.11
```

### 패키지 설치 오류
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 캐시 삭제 후 재설치
pip cache purge
pip install -r requirements.txt
```

### 포트 충돌 (8000번 사용 중)
```bash
# 다른 포트로 실행
uvicorn backend.app.main:app --port 8001
```

### OpenAI API 키 오류
1. `.env` 파일 열기
2. `OPENAI_API_KEY=` 뒤에 실제 API 키 입력
3. 서버 재시작

## 📚 다음 단계

1. **API 문서 확인**: http://localhost:8000/api/docs
2. **LangGraph 워크플로우 커스터마이징**: `backend/app/graphs/`
3. **새 노드 추가**: `backend/app/graphs/nodes/`
4. **프론트엔드 개발**: `frontend/` 디렉터리

## 💡 유용한 명령어

```bash
# 데이터베이스 리셋
rm data/sqlite/startup.db
python backend/app/db/init_db.py

# 로그 확인
tail -f logs/app.log

# 패키지 업데이트
pip install --upgrade -r requirements.txt

# 테스트 실행
pytest backend/tests/
```

## 🆘 도움말

문제가 있으시면 GitHub Issues에 문의하세요!

---

**Happy Coding! 🚀**