from typing import Any

from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import WalterRoasterSchema
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterRoasterPgRepository
import logging

logger = logging.getLogger(__name__)


class WalterQuery:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self.repository.list_paginated(page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self):
        pass

    def introduce_myself(self, schema: WalterRoasterSchema):
        '''월터의 자기소개 메소드'''
        query = WalterRoasterQuery(
            id=schema.id,
            name=schema.name,
            memo=schema.memo,
        )
        logger.info("###############################################")
        logger.info("💊[월터 유스케이스] 라우터에서 가져온 월터 정보")
        logger.info(f"👍🏻ID: {query.id}")
        logger.info(f"🐥이름: {query.name}")
        logger.info(f"🦜메모: {query.memo}")
        logger.info("###############################################")

        walter: WalterRoasterRepository = WalterRoasterPgRepository()
        walter.introduce_myself(query)

        pass
