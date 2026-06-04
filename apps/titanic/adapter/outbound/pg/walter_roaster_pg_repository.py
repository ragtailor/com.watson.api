from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.titanic_model import TitanicRecord
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger(__name__)

_ROW_FIELDS = [
    "id", "passenger", "survived", "pclass", "name", "gender",
    "age", "sibsp", "parch", "ticket", "fare", "cabin", "embarked",
]


class WalterPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_paginated(
        self, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        total = (
            await self.session.execute(
                select(func.count()).select_from(TitanicRecord)
            )
        ).scalar_one()
        rows = (
            await self.session.execute(
                select(TitanicRecord)
                .order_by(TitanicRecord.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).scalars().all()
        items = [{f: getattr(r, f) for f in _ROW_FIELDS} for r in rows]
        return total, items


class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 이용한 월터의 승객 명단 관리 저장소'''

    def __init__(self):
        pass

    def introduce_myself(self, query: WalterRoasterQuery):
        '''승객 명단을 가져오는 메소드'''
        logger.info("###############################################")
        logger.info("💊[월터 레포지토리] 유스케이스에서 가져온 월터 정보")
        logger.info(f"👍🏻ID: {query.id}")
        logger.info(f"🐥이름: {query.name}")
        logger.info(f"🦜메모: {query.memo}")
        logger.info("###############################################")

        pass
