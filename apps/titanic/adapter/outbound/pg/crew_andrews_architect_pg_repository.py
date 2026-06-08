from __future__ import annotations
from multiprocessing.util import get_logger

from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from tailor.apps.titanic.app.ports.output.crew_andrews_architect_repository import AndrewsArchitectRepository

logger = get_logger(__name__)

class AndrewsArchitectPgRepository(AndrewsArchitectRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, request_data: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        '''월터의 자기 소개 레포지토리 구현 메소드'''
        logger.info(f"[AndrewsArchitectPgRepository] introduce_myself 진입 | request_data={request_data}")
        
        return request_data
