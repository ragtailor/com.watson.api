from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import RoseModelSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import RoseModelQuery, RoseModelResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import RoseModelUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):
    
    def __init__(self, repository: RoseModelRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        '''로즈 모델의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(RoseModelQuery(
            id = schema.id,
            name = schema.name
        ))
