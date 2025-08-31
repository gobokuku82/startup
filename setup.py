#!/usr/bin/env python
"""
Startup Manager - 초기 설정 스크립트
"""
import os
import sys
import subprocess
import json
from pathlib import Path
import secrets
import string

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def generate_secret_key(length=32):
    """보안 키 생성"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def setup_environment():
    """환경 설정"""
    print(f"\n{Colors.BLUE}=== 환경 설정 ==={Colors.ENDC}")
    
    env_path = Path(".env")
    if env_path.exists():
        response = input(f"{Colors.YELLOW}.env 파일이 이미 존재합니다. 덮어쓰시겠습니까? (y/n): {Colors.ENDC}")
        if response.lower() != 'y':
            return
    
    # 설정 수집
    print(f"\n{Colors.GREEN}필수 설정을 입력하세요:{Colors.ENDC}")
    
    openai_key = input("OpenAI API Key (없으면 Enter): ").strip()
    if not openai_key:
        print(f"{Colors.YELLOW}⚠️  OpenAI API Key가 없으면 AI 기능을 사용할 수 없습니다.{Colors.ENDC}")
    
    # 보안 키 생성
    jwt_secret = generate_secret_key(64)
    app_secret = generate_secret_key(32)
    
    # .env 파일 작성
    env_content = f"""# Application
APP_NAME=StartupManager
APP_ENV=development
DEBUG=True

# Security
SECRET_KEY={app_secret}
JWT_SECRET_KEY={jwt_secret}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite:///./data/sqlite/startup.db
DATABASE_ECHO=False

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# OpenAI
OPENAI_API_KEY={openai_key}
OPENAI_MODEL=gpt-4-turbo-preview

# LangSmith (Optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=startup-manager

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./data/chroma
CHROMA_COLLECTION_NAME=policies

# Storage
STORAGE_PATH=./data/storage
MAX_FILE_SIZE_MB=10

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print(f"{Colors.GREEN}✅ .env 파일 생성 완료{Colors.ENDC}")

def setup_directories():
    """디렉터리 생성"""
    print(f"\n{Colors.BLUE}=== 디렉터리 생성 ==={Colors.ENDC}")
    
    directories = [
        "data/sqlite",
        "data/chroma",
        "data/checkpoints",
        "data/storage",
        "logs",
        "backend/app/__pycache__",
        "frontend/src"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}")

def install_dependencies():
    """의존성 설치"""
    print(f"\n{Colors.BLUE}=== 패키지 설치 ==={Colors.ENDC}")
    
    # 가상환경 확인
    if not Path("venv").exists():
        print(f"{Colors.YELLOW}가상환경 생성 중...{Colors.ENDC}")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # 가상환경 활성화 안내
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print(f"\n{Colors.YELLOW}⚠️  가상환경을 먼저 활성화하세요:{Colors.ENDC}")
        print(f"  Windows: {Colors.BOLD}venv\\Scripts\\activate{Colors.ENDC}")
        print(f"  Unix/Mac: {Colors.BOLD}source venv/bin/activate{Colors.ENDC}")
        print(f"\n그 다음 다시 실행: {Colors.BOLD}python setup.py{Colors.ENDC}")
        return False
    
    # 패키지 설치
    response = input(f"{Colors.YELLOW}패키지를 설치하시겠습니까? (y/n): {Colors.ENDC}")
    if response.lower() == 'y':
        print(f"{Colors.GREEN}패키지 설치 중... (5-10분 소요){Colors.ENDC}")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print(f"{Colors.GREEN}✅ 패키지 설치 완료{Colors.ENDC}")
    
    return True

def initialize_database():
    """데이터베이스 초기화"""
    print(f"\n{Colors.BLUE}=== 데이터베이스 초기화 ==={Colors.ENDC}")
    
    response = input(f"{Colors.YELLOW}데이터베이스를 초기화하시겠습니까? (y/n): {Colors.ENDC}")
    if response.lower() == 'y':
        print(f"{Colors.GREEN}데이터베이스 초기화 중...{Colors.ENDC}")
        subprocess.run([sys.executable, "backend/app/db/init_db.py"])
        print(f"{Colors.GREEN}✅ 데이터베이스 초기화 완료{Colors.ENDC}")

def create_sample_data():
    """샘플 데이터 생성"""
    print(f"\n{Colors.BLUE}=== 샘플 데이터 ==={Colors.ENDC}")
    
    response = input(f"{Colors.YELLOW}샘플 템플릿을 생성하시겠습니까? (y/n): {Colors.ENDC}")
    if response.lower() != 'y':
        return
    
    # 샘플 템플릿 디렉터리
    template_dir = Path("shared/templates")
    template_dir.mkdir(parents=True, exist_ok=True)
    
    # 방문보고서 템플릿
    visit_report = """# 방문 보고서

**고객명:** {{ client_name }}
**방문일:** {{ visit_date }}
**담당자:** {{ rep_name }}

## 방문 목적
{{ purpose }}

## 주요 논의 사항
{% for point in key_points %}
- {{ point }}
{% endfor %}

## 다음 조치 사항
{% for action in next_actions %}
- {{ action }}
{% endfor %}

## 비고
{{ notes }}
"""
    
    with open(template_dir / "visit_report.jinja2", "w", encoding="utf-8") as f:
        f.write(visit_report)
    
    print(f"{Colors.GREEN}✅ 샘플 템플릿 생성 완료{Colors.ENDC}")

def print_next_steps():
    """다음 단계 안내"""
    print(f"\n{Colors.GREEN}{'='*50}{Colors.ENDC}")
    print(f"{Colors.BOLD}🎉 초기 설정 완료!{Colors.ENDC}")
    print(f"{Colors.GREEN}{'='*50}{Colors.ENDC}")
    
    print(f"\n{Colors.BLUE}다음 단계:{Colors.ENDC}")
    print(f"1. 서버 실행: {Colors.BOLD}python run.py{Colors.ENDC}")
    print(f"   또는 Windows: {Colors.BOLD}run.bat{Colors.ENDC}")
    print(f"   또는 Unix/Mac: {Colors.BOLD}./run.sh{Colors.ENDC}")
    print(f"\n2. 브라우저에서 접속:")
    print(f"   - API 문서: {Colors.BOLD}http://localhost:8000/api/docs{Colors.ENDC}")
    print(f"   - 헬스체크: {Colors.BOLD}http://localhost:8000/health{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}테스트 계정:{Colors.ENDC}")
    print(f"  Admin: admin@startup.com / admin123")
    print(f"  Rep: rep@startup.com / rep123")

def main():
    """메인 설정 함수"""
    print(f"""
{Colors.BLUE}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Colors.BOLD}⚙️  Startup Manager - 초기 설정 마법사{Colors.ENDC}{Colors.BLUE}                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.ENDC}
    """)
    
    try:
        # 1. 디렉터리 생성
        setup_directories()
        
        # 2. 환경 설정
        setup_environment()
        
        # 3. 의존성 설치
        if not install_dependencies():
            return
        
        # 4. 데이터베이스 초기화
        initialize_database()
        
        # 5. 샘플 데이터
        create_sample_data()
        
        # 6. 완료 안내
        print_next_steps()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}설정이 취소되었습니다.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}오류 발생: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()