# Backend — tailor

FastAPI Python 백엔드. 루트 지침은 [../CLAUDE.md](../CLAUDE.md)를 참고한다.

---

## 실행

```powershell
cd tailor
# PYTHONPATH에 tailor/ 와 tailor/apps/ 모두 포함 필요
$env:PYTHONPATH = ".;apps"
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

---

## 환경 변수

`tailor/.env`를 `.env.example` 기반으로 생성한다.

```
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/dbname
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash   # 선택
```

---

## 의존성

```bash
cd tailor
pip install -r requirements.txt

# 테스트 의존성 (최초 1회)
pip install -r requirements-test.txt
```

---

## DB 마이그레이션

테이블은 앱 시작 시 `create_all_tables()`로 자동 생성된다. Alembic 마이그레이션이 필요할 때:

```bash
cd tailor
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## 아키텍처

**헥사고날(Ports & Adapters)** 아키텍처를 사용한다. 각 앱(`apps/<name>/`)은 다음 레이어로 구성된다.

```
apps/<앱명>/
├── domain/             # 엔티티·값 객체 (순수 비즈니스 로직)
├── app/
│   ├── ports/input/    # 유스케이스 인터페이스 (입력 포트)
│   ├── ports/output/   # 레포지터리 인터페이스 (출력 포트)
│   └── use_cases/      # 유스케이스 구현체
├── adapter/
│   ├── inbound/api/    # FastAPI 라우터 및 Pydantic 스키마
│   └── outbound/       # DB 구현체 (ORM 모델, pg 레포지터리)
└── tests/              # 앱별 단위 테스트 (TDD)
    ├── domain/
    ├── app/use_cases/
    └── adapter/
```

**Python import 경로**: `tailor/apps/`가 PYTHONPATH에 있으므로 `from titanic.xxx import ...` 형태로 임포트한다 (`from apps.titanic.xxx`가 아님).

의존성 방향: `adapter` → `app` → `domain`. 역방향 임포트는 순환 참조를 유발한다.

---

## 앱 목록 및 역할

| 앱 | 역할 | CLAUDE.md |
|----|------|-----------|
| `titanic` | 타이타닉 승객 CSV 업로드·조회 (ML 교육용 데이터셋) | [apps/titanic/_docs/CLAUDE.md](apps/titanic/_docs/CLAUDE.md) |
| `kingsman` | 사용자·관리자 관리 | — |
| `matrix` | Gemini API 키·외부 클라이언트 싱글톤 관리 (`Keymaker`) | — |
| `goal` | DB 헬스체크 | — |
| `avengers` | 문서 읽기·분석 | — |
| `lion_king` | 소셜 기능 (스켈레톤) | — |

새 앱이 추가될 때 위 표에 행을 추가하고, `apps/<앱명>/_docs/CLAUDE.md`를 생성한다.

---

## 네이밍 컨벤션

파일명·클래스명·라우터 prefix에 **영화 캐릭터 이름**을 bounded context 식별자로 사용한다.

예: `james_router`, `rose_router`, `walter_repository`, `jason_command_router`

새 컴포넌트를 추가할 때도 해당 앱의 기존 캐릭터 체계를 따른다. 앱별 캐릭터 목록은 각 앱의 CLAUDE.md를 참고한다.

---

## 테스트 (TDD)

```bash
cd tailor
python -m pytest                          # 전체
python -m pytest apps/titanic/tests/ -v   # 앱별
```

`pytest.ini`가 `tailor/` 루트에 있으며 `asyncio_mode = auto`로 설정되어 있다. 각 앱의 테스트 구조와 실행 방법은 해당 앱의 CLAUDE.md를 참고한다.
