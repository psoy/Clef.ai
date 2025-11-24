# Clef.ai Backend 재시작 가이드

## 문제
환경 변수가 PowerShell 세션에 캐시되어 `.env` 파일 변경사항이 반영되지 않습니다.

## 해결 방법

### 1단계: 모든 백엔드 프로세스 종료
현재 실행 중인 모든 uvicorn 프로세스를 종료하세요:
- 터미널에서 `Ctrl+C` 누르기
- 또는 작업 관리자에서 Python 프로세스 종료

### 2단계: 새 PowerShell 창 열기
**중요:** 기존 터미널을 닫고 완전히 새로운 PowerShell 창을 여세요.

### 3단계: 백엔드 시작
새 터미널에서 다음 명령어 실행:

```powershell
cd c:\Clef.ai\backend
..\.venv\Scripts\python -m uvicorn main:app --reload
```

### 4단계: 확인
서버 로그에서 다음 메시지를 확인하세요:
```
OPENAI_API_KEY found. Using OpenAI embeddings and LLM.
```

API 키가 올바르게 로드되었는지 확인:
```powershell
..\.venv\Scripts\python test_api_key.py
```

예상 출력:
```
API Key loaded: sk-proj-TM7j6OKBqh8N...UJYA
✅ OpenAI API connection successful!
Response: Hello! How can I help you today?
```

## 현재 상태
- ✅ `.env` 파일에 유효한 API 키 저장됨 (끝: ...UJYA)
- ✅ test_api_key.py로 검증 완료
- ❌ 백엔드가 여전히 이전 키 사용 중 (캐시 문제)

## 다음 단계
위 가이드를 따라 새 터미널에서 백엔드를 재시작하세요.
