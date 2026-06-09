from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import IsidorCoupleSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import IsidorCoupleQuery, IsidorCoupleResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import IsidorCoupleUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import IsidorCoupleRepository


class IsidorCoupleInteractor(IsidorCoupleUseCase):
    
    def __init__(self, repository: IsidorCoupleRepository):
        self.repository = repository

    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        '''이시도어 커플의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(IsidorCoupleQuery(
            id = schema.id,
            name = schema.name
        ))
