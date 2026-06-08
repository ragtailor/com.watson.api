from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectResponse


class AndrewsArchitectUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self) -> AndrewsArchitectResponse:
        '''앤드류 아키텍트의 자기소개 메소드'''
        pass
