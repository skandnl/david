# GitHub 보너스 과제

---

## 1️⃣ 인기 있는 오픈소스 Fork 및 토큰 관리 보안

### 🔹 Fork한 저장소
- 예시: [psf/requests](https://github.com/psf/requests) (Star 50k 이상)  
- 본인 GitHub 계정으로 Fork 완료  

### 🔹 Personal Access Token 보안
- **토큰이란?**  
  - GitHub에 HTTPS로 인증할 때 사용하는 **비밀번호 대체 키**  
- **텍스트 파일로 저장 후 삭제해야 하는 이유**  
  - 토큰은 Private repository 접근, 코드 수정, 삭제 권한까지 포함  
  - 평문 상태로 보관 시 해킹·유출 위험  
  - 안전한 사용 절차:
    ```bash
    echo "ghp_XXXXXX" > ~/token.txt
    # 인증 시 사용 후
    rm ~/token.txt
    ```
- **보안 원칙:**  
  - 장기 보관 금지  
  - 환경 변수(`export GITHUB_TOKEN=...`)나 Git credential helper 사용 권장  

---

## 2️⃣ 저장소 복제

- 다른 PC나 다른 디렉토리에서 복제:
```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
git branch -a  # 원격 브랜치 확인
# GitHub 보너스 과제

---

## 1️⃣ 인기 있는 오픈소스 Fork 및 토큰 관리 보안

### 🔹 Fork한 저장소
- 예시: [psf/requests](https://github.com/psf/requests) (Star 50k 이상)  
- 본인 GitHub 계정으로 Fork 완료  

### 🔹 Personal Access Token 보안
- **토큰이란?**  
  - GitHub에 HTTPS로 인증할 때 사용하는 **비밀번호 대체 키**  
- **텍스트 파일로 저장 후 삭제해야 하는 이유**  
  - 토큰은 Private repository 접근, 코드 수정, 삭제 권한까지 포함  
  - 평문 상태로 보관 시 해킹·유출 위험  
  - 안전한 사용 절차:
    ```bash
    echo "ghp_XXXXXX" > ~/token.txt
    # 인증 시 사용 후
    rm ~/token.txt
    ```
- **보안 원칙:**  
  - 장기 보관 금지  
  - 환경 변수(`export GITHUB_TOKEN=...`)나 Git credential helper 사용 권장  

---

## 2️⃣ 저장소 복제

- 다른 PC나 다른 디렉토리에서 복제:
```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
git branch -a  # 원격 브랜치 확인
결과:

모든 브랜치(main, add-image 등)와 커밋 기록 정상 복제됨

3️⃣ Python 프로젝트에서 .gitignore 사용 이유
🔹 __pycache__ 디렉토리
Python이 .py 파일을 실행할 때 **바이트코드(.pyc)**를 저장하는 캐시 폴더

OS와 Python 버전에 따라 달라지므로 공유할 필요 없음

🔹 .venv 디렉토리
프로젝트별 가상환경 디렉토리

각 개발자 PC의 Python 경로가 달라서 공유 시 충돌 발생

🔹 GitHub Python .gitignore 템플릿 주요 항목
plaintext
__pycache__/
*.py[cod]
.venv/
env/
build/
dist/
*.egg-info/
🔹 Flask 기반 프로젝트에서 추가할 항목
plaintext
instance/
*.db
*.log