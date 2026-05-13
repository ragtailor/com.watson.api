"""라우트와 SQLAlchemy 세션 사이: DB 연결·시간 점검만 담당."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DbHealthAdapter:
    """Neon/Postgres 등 비동기 세션으로 `SELECT NOW()` 점검. HTTP는 알지 않음."""

    _NOW_SQL = text("SELECT NOW();")

    @classmethod
    async def neon_time_check(cls, session: AsyncSession) -> dict[str, object]:
        try:
            result = await session.execute(cls._NOW_SQL)
            now = result.scalar()
            return {"status": "success", "neon_time": now}
        except Exception as e:
            return {"status": "error", "message": str(e)}
