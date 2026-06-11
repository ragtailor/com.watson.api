from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from tailor.apps.titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from tailor.apps.titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from tailor.apps.titanic.app.ports.output.passenger_molly_scaler_repository import MollyScalerRepository


class MollyScalerInteractor(MollyScalerUseCase):
    
    def __init__(self, repository: MollyScalerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리 스케일러의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(MollyScalerQuery(
            id = schema.id,
            name = schema.name
        ))

