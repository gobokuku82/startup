#!/usr/bin/env python
"""
Startup Manager - 메인 실행 스크립트
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

# 색상 코드 (Windows/Unix 호환)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """배너 출력"""
    print(f"""
{Colors.BLUE}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Colors.BOLD}🚀 Startup Manager - AI Business Automation Platform{Colors.ENDC}{Colors.BLUE}   ║
║                                                          ║
║  {Colors.GREEN}Powered by LangGraph 0.6.6 + FastAPI{Colors.BLUE}                   ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.ENDC}
    """)

def check_python_version():
    """Python 버전 확인"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"{Colors.RED}❌ Python 3.11+ 이상이 필요합니다. 현재: {sys.version}{Colors.ENDC}")
        return False
    print(f"{Colors.GREEN}✅ Python {sys.version}{Colors.ENDC}")
    return True

def check_venv():
    """가상환경 확인"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print(f"{Colors.YELLOW}⚠️  가상환경이 없습니다. 생성 중...{Colors.ENDC}")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print(f"{Colors.GREEN}✅ 가상환경 생성 완료{Colors.ENDC}")
        return False
    return True

def activate_venv():
    """가상환경 활성화 안내"""
    system = platform.system()
    if system == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"\n{Colors.YELLOW}📌 가상환경을 활성화하세요:{Colors.ENDC}")
    print(f"   {Colors.BOLD}{activate_cmd}{Colors.ENDC}")
    print(f"\n{Colors.YELLOW}📌 그 다음 패키지를 설치하세요:{Colors.ENDC}")
    print(f"   {Colors.BOLD}pip install -r requirements.txt{Colors.ENDC}")

def check_env_file():
    """환경 파일 확인"""
    env_path = Path(".env")
    if not env_path.exists():
        print(f"{Colors.YELLOW}⚠️  .env 파일이 없습니다. 생성 중...{Colors.ENDC}")
        
        # .env.example 복사
        example_path = Path(".env.example")
        if example_path.exists():
            import shutil
            shutil.copy(".env.example", ".env")
            print(f"{Colors.GREEN}✅ .env 파일 생성 완료{Colors.ENDC}")
            print(f"{Colors.YELLOW}📌 .env 파일을 열어서 설정을 완료하세요:{Colors.ENDC}")
            print(f"   - OPENAI_API_KEY 설정 필수")
            print(f"   - 기타 설정 확인")
            return False
    return True

def check_database():
    """데이터베이스 확인"""
    db_path = Path("data/sqlite/startup.db")
    if not db_path.exists():
        print(f"{Colors.YELLOW}⚠️  데이터베이스가 없습니다.{Colors.ENDC}")
        print(f"{Colors.YELLOW}📌 다음 명령으로 데이터베이스를 초기화하세요:{Colors.ENDC}")
        print(f"   {Colors.BOLD}python backend/app/db/init_db.py{Colors.ENDC}")
        return False
    print(f"{Colors.GREEN}✅ 데이터베이스 확인 완료{Colors.ENDC}")
    return True

def run_server():
    """FastAPI 서버 실행"""
    print(f"\n{Colors.GREEN}🚀 서버를 시작합니다...{Colors.ENDC}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}")
    print(f"{Colors.BOLD}API 문서: http://localhost:8000/api/docs{Colors.ENDC}")
    print(f"{Colors.BOLD}헬스체크: http://localhost:8000/health{Colors.ENDC}")
    print(f"{Colors.BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}\n")
    
    try:
        subprocess.run([
            "uvicorn",
            "backend.app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 서버를 종료합니다...{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}❌ uvicorn이 설치되지 않았습니다.{Colors.ENDC}")
        print(f"{Colors.YELLOW}📌 다음 명령으로 패키지를 설치하세요:{Colors.ENDC}")
        print(f"   {Colors.BOLD}pip install -r requirements.txt{Colors.ENDC}")

def main():
    """메인 실행 함수"""
    print_banner()
    
    # 1. Python 버전 확인
    if not check_python_version():
        sys.exit(1)
    
    # 2. 가상환경 확인
    venv_exists = check_venv()
    
    # 3. 가상환경이 활성화되었는지 확인
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    if not in_venv:
        print(f"{Colors.RED}❌ 가상환경이 활성화되지 않았습니다.{Colors.ENDC}")
        activate_venv()
        sys.exit(1)
    
    print(f"{Colors.GREEN}✅ 가상환경 활성화됨{Colors.ENDC}")
    
    # 4. 환경 파일 확인
    if not check_env_file():
        sys.exit(1)
    
    # 5. 데이터베이스 확인
    if not check_database():
        response = input(f"\n{Colors.YELLOW}데이터베이스를 초기화하시겠습니까? (y/n): {Colors.ENDC}")
        if response.lower() == 'y':
            print(f"{Colors.GREEN}데이터베이스 초기화 중...{Colors.ENDC}")
            # 디렉터리 생성
            Path("data/sqlite").mkdir(parents=True, exist_ok=True)
            subprocess.run([sys.executable, "backend/app/db/init_db.py"])
    
    # 6. 서버 실행
    print(f"\n{Colors.GREEN}✅ 모든 체크 완료!{Colors.ENDC}")
    response = input(f"{Colors.YELLOW}서버를 시작하시겠습니까? (y/n): {Colors.ENDC}")
    
    if response.lower() == 'y':
        run_server()
    else:
        print(f"{Colors.BLUE}수동으로 서버를 시작하려면:{Colors.ENDC}")
        print(f"   {Colors.BOLD}uvicorn backend.app.main:app --reload{Colors.ENDC}")

if __name__ == "__main__":
    main()