# 엔티티(Entity) 규칙

백엔드 SQLModel 테이블 정의 시 따르는 공통 규칙이다.

---

## 기본 키: `id` (int, 자동 증감)

**모든 테이블은 반드시 `int` 타입의 기본 키를 갖는다.** 컬럼·필드 이름은 **`id`로 통일**한다.

| 항목 | 규칙 |
|------|------|
| Python 필드명 | `id` |
| DB 컬럼명 | `id` (`sa_column_kwargs={"name": "id"}`) |
| 타입 | `Optional[int]` (INSERT 전에는 `None`, DB가 할당) |
| 역할 | 시스템 내부용 자동 증감 고유 번호 (PK) |
| `primary_key` | `True` |
| `default` | `None` |

비즈니스 식별자(로그인 ID, 외부 키 등)는 **별도 컬럼**으로 두고, `id`와 혼용하지 않는다.

---

## 표준 정의 (복사용 템플릿)

```python
from typing import Optional
from sqlmodel import Field, SQLModel

class Example(SQLModel, table=True):
    __tablename__ = "examples"

    # 1. 시스템 내부용 자동 증감 고유 번호 (기본 키)
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )

    # 2. 이하 비즈니스 필드 ...
```

---

## 참조 구현

현재 프로젝트 기준 예시: `backend/apps/secom/app/models/user_model.py`

```python
id: Optional[int] = Field(
    default=None,
    primary_key=True,
    sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
)
```

`User` 엔티티는 `id`(시스템 PK)와 `user_id`(사용자 지정 문자열 고유 ID)를 분리해 둔다.

---

## 저장 후 `id` 동기화

INSERT 후 DB가 부여한 `id`를 모델에 반영하려면 세션 `refresh`를 호출한다.

```python
self.session.add(entity)
await self.session.commit()
await self.session.refresh(entity)  # entity.id 에 자동 증감 값 반영
```

참조: `backend/apps/secom/app/repositories/user_repository.py` — `save_user`

---

## 체크리스트 (신규 테이블)

- [ ] `SQLModel`, `table=True` 클래스에 `id` 필드가 있는가?
- [ ] `id`가 `Optional[int]` + `primary_key=True` + `default=None` 인가?
- [ ] DB 컬럼명이 `id`인가? (`sa_column_kwargs={"name": "id"}`)
- [ ] 비즈니스용 고유 식별자를 `id` 대신 별도 필드로 정의했는가?
