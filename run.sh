#!/bin/bash
# Startup Manager - Unix/Linux/Mac 실행 스크립트

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# 배너 출력
echo -e "${BLUE}========================================"
echo -e "  ${BOLD}Startup Manager - AI Platform${NC}"
echo -e "  ${GREEN}LangGraph 0.6.6 + FastAPI${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Python 버전 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3가 설치되지 않았습니다.${NC}"
    echo "Python 3.11 이상을 설치해주세요."
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}[OK] Python $python_version${NC}"

# 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[INFO] 가상환경 생성 중...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}[OK] 가상환경 생성 완료${NC}"
fi

# 가상환경 활성화
echo -e "${YELLOW}[INFO] 가상환경 활성화 중...${NC}"
source venv/bin/activate

# 패키지 설치 확인
if ! pip show fastapi &> /dev/null; then
    echo -e "${YELLOW}[INFO] 패키지 설치 중... (시간이 걸릴 수 있습니다)${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}[OK] 패키지 설치 완료${NC}"
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[INFO] .env 파일 생성 중...${NC}"
    cp .env.example .env
    echo -e "${RED}[WARNING] .env 파일을 열어서 OPENAI_API_KEY를 설정하세요!${NC}"
    echo ""
    read -p "Enter를 눌러 계속..."
fi

# 데이터베이스 디렉터리 생성
if [ ! -d "data/sqlite" ]; then
    echo -e "${YELLOW}[INFO] 데이터 디렉터리 생성 중...${NC}"
    mkdir -p data/sqlite
fi

# 데이터베이스 확인
if [ ! -f "data/sqlite/startup.db" ]; then
    echo -e "${YELLOW}[INFO] 데이터베이스 초기화 중...${NC}"
    python backend/app/db/init_db.py
    echo -e "${GREEN}[OK] 데이터베이스 초기화 완료${NC}"
fi

echo ""
echo -e "${BLUE}========================================"
echo -e "  ${BOLD}서버 시작${NC}"
echo -e "  URL: ${GREEN}http://localhost:8000${NC}"
echo -e "  API 문서: ${GREEN}http://localhost:8000/api/docs${NC}"
echo -e "  종료: ${YELLOW}Ctrl+C${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 서버 실행
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000