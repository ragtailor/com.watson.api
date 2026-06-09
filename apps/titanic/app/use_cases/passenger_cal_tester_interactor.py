from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import CalTesterSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import CalTesterQuery, CalTesterResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import CalTesterUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import CalTesterRepository


class CalTesterInteractor(CalTesterUseCase):
    
    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(CalTesterQuery(
            id = schema.id,
            name = schema.name
        ))
