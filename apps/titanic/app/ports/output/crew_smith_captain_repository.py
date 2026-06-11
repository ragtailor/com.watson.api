from __future__ import annotations

from abc import ABC, abstractmethod
from tailor.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse

class SmithCaptainRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        '''스미스 선장의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def chat(self, message: str) -> SmithCaptainResponse:
        '''사용자 자연어 메시지를 받아 응답을 반환'''
        pass

