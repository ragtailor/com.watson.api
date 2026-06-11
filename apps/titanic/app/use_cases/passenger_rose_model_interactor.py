from __future__ import annotations

from typing import Any

from tailor.apps.titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from tailor.apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from tailor.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from tailor.apps.titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository


class RoseModelInteractor(RoseModelUseCase):
    
    def __init__(self, repository: RoseModelRepository):
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        '''로즈 모델의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(RoseModelQuery(
            id = schema.id,
            name = schema.name
        ))

    async def analyze_rose_survival(self) -> dict[str, Any]:
        return await self.repository.get_all_records()

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
