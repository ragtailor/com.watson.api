from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from tailor.apps.titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    
    def __init__(self, repository: AndrewsArchitectRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        '''앤드류 아키텍트의 자기소개 인터렉트'''
        query = AndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        )
        return self.repository.introduce_myself(query)
