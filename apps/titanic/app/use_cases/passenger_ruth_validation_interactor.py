from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from tailor.apps.titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from tailor.apps.titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from tailor.apps.titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository


class RuthValidationInteractor(RuthValidationUseCase):
    
    def __init__(self, repository: RuthValidationRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        '''루스 밸리데이션의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(RuthValidationQuery(
            id = schema.id,
            name = schema.name
        ))
