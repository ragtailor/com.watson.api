import asyncio
import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. 환경 변수 로드 (.env 파일에서 DATABASE_URL을 읽어옴)
load_dotenv()

# Neon DB 커넥션 스트링 예시: postgresql+psycopg://user:pass@host/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

# 비동기 전용 PostgreSQL 엔진 생성 (psycopg 드라이버 사용)
engine = create_async_engine(DATABASE_URL, echo=True) if DATABASE_URL else None

# 비동기 세션 생성기 설정
AsyncSessionLocal = (
    async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    if engine is not None
    else None
)


# 2. SQLAlchemy 2.0 선언적 베이스 클래스
class Base(DeclarativeBase):
    """ORM 모델 베이스."""
    pass


# 3. Mapped 타입 힌트를 활용한 User 모델 정의
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


# 4. FastAPI 디펜던시용 DB 세션 제너레이터
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends용 비동기 DB 세션."""
    if AsyncSessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
        )
    async with AsyncSessionLocal() as session:
        yield session


# 5. 엔진 종료 함수 (애플리케이션 수명 주기 관리용)
async def dispose_engine() -> None:
    """앱 종료 시 연결 풀 정리."""
    global engine, AsyncSessionLocal
    if engine is not None:
        await engine.dispose()
    engine = None
    AsyncSessionLocal = None


# --- 검증 및 CLI 실행을 위한 메인 비동기 루틴 ---
async def main():
    if not DATABASE_URL:
        print("에러: .env 파일에 DATABASE_URL이 설정되지 않았습니다.")
        return

    print("1. Neon DB 테이블 생성 중...")
    # 비동기 환경에서 테이블 생성 처리 (Neon DB에 users 테이블이 생성됩니다)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("2. 비동기 세션을 통한 데이터 생성(Insert) 및 조회(Select)...")
    async with AsyncSessionLocal() as session:
        # 데이터 삽입
        new_user = User(name="홍길동", age=30)
        session.add(new_user)
        await session.commit()
        print("샘플 데이터 등록 완료.")

        # 데이터 조회 (SQLAlchemy 2.0 모던 스타일)
        stmt = select(User).where(User.age >= 20)
        result = await session.execute(stmt)
        
        users = result.scalars().all()
        for u in users:
            print(f" -> [조회 성공] 유저: {u.name} ({u.age}세)")

    # 사용이 끝난 엔진 커넥션 풀 정리
    await dispose_engine()

if __name__ == "__main__":
    # 스크립트로 직접 실행 시 비동기 루프 가동
    asyncio.run(main())