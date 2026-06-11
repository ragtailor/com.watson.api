from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import DATABASE_URL
from tailor.core.matrix.grid_neo_theone_base import Base


engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None


def init_engine() -> None:
    global engine, async_session_factory
    if not DATABASE_URL:
        return
        
    # 이미 초기화되었다면 중복 생성을 방지 (레이스 컨디션 완화)
    if engine is not None:
        return

    engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
    
    # [변경 2] async_sessionmaker는 class_=AsyncSession을 기본으로 내장하므로 생략 가능
    # [변경 3] 2.0에서 완전히 제거(Deprecated & Removed)된 autocommit=False 옵션 삭제
    async_session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if async_session_factory is None:
        init_engine()
        
    if async_session_factory is None:
        raise RuntimeError("데이터베이스 엔진이 초기화되지 않았습니다.")

    # 원본의 안전한 비동기 컨텍스트 매니저 패턴 유지
    async with async_session_factory() as session:
        yield session


async def create_all_tables() -> None:
    # 테이블 생성 시에도 엔진 초기화 여부 체크 추가
    if engine is None:
        init_engine()
        
    if engine is not None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    global engine, async_session_factory
    if engine is not None:
        await engine.dispose()
    engine = None
    async_session_factory = None