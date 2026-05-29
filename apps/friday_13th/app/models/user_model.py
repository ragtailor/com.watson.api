from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"

    # 1. 시스템 내부용 자동 증감 고유 번호 (기본 키)
    id: Optional[int] = Field(
        default=None, 
        primary_key=True,
        sa_column_kwargs={"name": "id"}  # DB 컬럼명: id
    )

    # 2. 사용자 지정 문자열 고유 ID (예: 로그인 아이디)
    user_id: str = Field(
        index=True,
        unique=True,
        alias="userId",                  # API JSON 통신 시 필드명
        sa_column_kwargs={"name": "user_id"}  # DB 컬럼명: user_id
    )

    # 3. 추가 및 변경된 비즈니스 필드 (모두 str 타입)
    nickname: str = Field(sa_column_kwargs={"name": "nickname"})
    email: str = Field(sa_column_kwargs={"name": "email"})
    address: str = Field(sa_column_kwargs={"name": "address"})
    role: str = Field(sa_column_kwargs={"name": "role"})
    phone: str = Field(sa_column_kwargs={"name": "phone"})

    class Config:
        # FastAPI가 입출력(JSON) 시 'userId'와 'user_id'를 유연하게 매핑하도록 허용
        populate_by_name = True