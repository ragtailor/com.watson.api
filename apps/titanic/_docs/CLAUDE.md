# Titanic 앱

타이타닉 승객 CSV 업로드·조회 앱. ML 교육용 데이터셋을 다루는 헥사고날 아키텍처 실습 맥락이다.
백엔드 공통 지침은 [../../CLAUDE.md](../../CLAUDE.md)를 참고한다.

---

## 캐릭터 체계

이 앱은 **타이타닉 영화 캐릭터**를 bounded context 식별자로 사용한다.

| 캐릭터 | 역할 |
|--------|------|
| `jack` (Jack Dawson) | 승객 훈련 데이터 조회·ML 예측 인터페이스 |
| `rose` (Rose DeWitt Bukater) | 예약(booking) ORM 모델 |
| `james` (James Cameron, 감독) | CSV 파일 업로드·저장 |
| `andrews` (Thomas Andrews, 설계자) | 아키텍처 자기소개 |
| `walter` (Walter Lord, 작가) | 데이터 로딩 |
| `ruth` (Ruth DeWitt Bukater) | 유효성 검사 |
| `molly` (Molly Brown) | 스케일러 |
| `cal` (Cal Hockley) | 테스터 |
| `isidor` (Isidor Straus) | 커플(페어) 데이터 |
| `hartley` (Wallace Hartley, 악단장) | 미정 |
| `lowe` (Harold Lowe, 구조 장교) | 구명보트 |
| `smith` (Captain Smith) | 캡틴(관리자) |

새 컴포넌트를 추가할 때 캐릭터 이름을 파일명·클래스명·라우터 prefix에 사용한다.

---

## 헥사고날 레이어

```
apps/titanic/
├── domain/
│   ├── entities/           # PassengerEntity (도메인 행위 포함)
│   └── value_objects/      # PassengerId, PassengerName, Gender, Age, FamilyRelation, SurvivalStatus
├── app/
│   ├── dtos/               # Query / Command / Response 데이터 클래스
│   ├── ports/input/        # UseCase ABC (입력 포트)
│   ├── ports/output/       # Repository ABC (출력 포트)
│   └── use_cases/          # Interactor 구현체
├── adapter/
│   ├── inbound/api/
│   │   ├── schemas/        # Pydantic 요청·응답 모델
│   │   └── v1/             # FastAPI 라우터
│   └── outbound/
│       ├── mappers/        # ORM ↔ Entity 변환
│       ├── orm/            # SQLAlchemy 모델 (passengers, bookings 테이블)
│       └── pg/             # PostgreSQL 레포지터리 구현체
├── dependencies/           # FastAPI DI 프로바이더
└── tests/                  # TDD 단위 테스트 (DB 불필요)
```

**의존성 방향:** `adapter` → `app` → `domain`

어댑터 레이어(API 스키마 등)를 앱 레이어(유스케이스·포트)에서 직접 임포트하면 순환 참조가 발생한다. 타입 힌트 목적이면 `TYPE_CHECKING` 가드를 사용한다.

---

## TDD 구조

켄트 벡의 **Red → Green → Refactor** 사이클을 적용한다. 테스트는 헥사고날 레이어를 미러링한다.

```
tests/
├── conftest.py                         # sys.path 설정, 공통 픽스처
├── domain/
│   ├── value_objects/
│   │   └── test_passenger_jack_trainer_vo.py     # VO 불변식·경계값 (외부 의존 없음)
│   └── entities/
│       └── test_passenger_jack_trainer_entity.py  # 도메인 행위 (is_high_risk 등)
├── app/use_cases/
│   ├── test_passenger_jack_trainer_interactor.py  # mock repository로 유스케이스 검증
│   └── test_crew_james_director_interactor.py     # CSV 업로드 커맨드 변환 검증
└── adapter/outbound/mappers/
    └── test_passenger_jack_trainer_mapper.py       # ORM ↔ Entity 변환 (SimpleNamespace mock)
```

### 테스트 실행

```bash
cd tailor
python -m pytest apps/titanic/tests/ -v        # titanic 전체
python -m pytest apps/titanic/tests/domain/    # 도메인 레이어만
```

### 새 기능 TDD 절차

```text
1. tests/<레이어>/ 에 실패하는 테스트 작성 (Red)
   → 검증: pytest 가 FAILED 를 출력한다
2. 최소한의 구현 코드 작성 (Green)
   → 검증: pytest 가 PASSED 를 출력한다
3. 중복 제거·네이밍 정리 (Refactor)
   → 검증: 전체 테스트가 여전히 PASSED
```

### 알려진 버그 (Red 상태 유지)

- `JackTrainerMapper.to_orm()`: `JackTrainerOrm`에 `id` 컬럼이 없어 `TypeError` 발생.
  `TestToOrm` 는 이 버그를 문서화하는 의도적 Red 테스트다. 수정 시 `JackTrainerOrm`에 `id` 컬럼 추가 또는 mapper 로직 수정이 필요하다.

---

## 도메인 규칙

### PassengerEntity.is_high_risk()

`남성 AND 성인(18세 이상) AND 혼자 탑승` → 생존 가능성 통계적으로 낮은 고위험군.

### SurvivalStatus

CSV 원천 데이터: `"1"` = 생존, `"0"` = 사망, 빈 값 = 미확인.

### FamilyRelation

`sib_sp`(형제자매·배우자) + `parch`(부모·자녀) = `total_family_size`. 둘 다 0이면 `is_alone = True`.
