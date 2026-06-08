from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_orm import PersonOrm


class SmithCaptainPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_stats(self) -> dict[str, Any]:
        """전체 승객 생존/사망 통계 조회"""
        total = (
            await self.session.execute(select(func.count()).select_from(PersonOrm))
        ).scalar_one()
        survived = (
            await self.session.execute(
                select(func.count()).where(PersonOrm.survived == "1")
            )
        ).scalar_one()
        return {"total": total, "survived": survived, "perished": total - survived}
