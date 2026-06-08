from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import LoweBoatSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import LoweBoatQuery, LoweBoatResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import LoweBoatUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import LoweBoatRepository


class LoweBoatInteractor(LoweBoatUseCase):
    
    def __init__(self, repository: LoweBoatRepository):
        self.repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''로우 보트의 자기소개 인터렉트'''
        
        return  await self.repository.introduce_myself(LoweBoatQuery(
            id = schema.id,
            name = schema.name
        ))

