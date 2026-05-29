from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_model import TitanicRecord
from titanic.app.ports.output.walter_repository import WalterRepository

_ROW_FIELDS = [
    "id", "passenger", "survived", "pclass", "name", "gender",
    "age", "sibsp", "parch", "ticket", "fare", "cabin", "embarked",
]


class WalterPgRepository(WalterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_paginated(self, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        total = (await self.session.execute(select(func.count()).select_from(TitanicRecord))).scalar_one()
        rows = (await self.session.execute(
            select(TitanicRecord).order_by(TitanicRecord.id).offset((page - 1) * page_size).limit(page_size)
        )).scalars().all()
        items = [{f: getattr(r, f) for f in _ROW_FIELDS} for r in rows]
        return total, items
