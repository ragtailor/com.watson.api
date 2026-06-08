from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import SmithCaptainSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import SmithCaptainQuery, SmithCaptainResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import SmithCaptainUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import SmithCaptainRepository


class SmithCaptainInteractor(SmithCaptainUseCase):
    
    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))
