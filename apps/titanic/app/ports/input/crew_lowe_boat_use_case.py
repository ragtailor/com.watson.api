from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from tailor.apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse

class LoweBoatUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''로우 보우트의 자기소개 메소드'''
        pass