import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# Neon 등 PostgreSQL: postgresql+psycopg://user:pass@host/dbname
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True) if DATABASE_URL else None
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


class Base(DeclarativeBase):
    """ORM 모델 베이스."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends용 비동기 DB 세션."""
    if AsyncSessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 .env 등에 설정되지 않았습니다.",
        )
    async with AsyncSessionLocal() as session:
        yield session


async def dispose_engine() -> None:
    """앱 종료 시 연결 풀 정리."""
    global engine, AsyncSessionLocal
    if engine is not None:
        await engine.dispose()
    engine = None
    AsyncSessionLocal = None
