from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import RuthValidationSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import RuthValidationQuery, RuthValidationResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import RuthValidationUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import RuthValidationRepository


class RuthValidationInteractor(RuthValidationUseCase):
    
    def __init__(self, repository: RuthValidationRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        '''루스 밸리데이션의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(RuthValidationQuery(
            id = schema.id,
            name = schema.name
        ))
