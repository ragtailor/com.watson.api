from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import MollyScalerSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import MollyScalerQuery, MollyScalerResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import MollyScalerUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import MollyScalerRepository


class MollyScalerInteractor(MollyScalerUseCase):
    
    def __init__(self, repository: MollyScalerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리 스케일러의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(MollyScalerQuery(
            id = schema.id,
            name = schema.name
        ))

