from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from tailor.apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from tailor.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse
from tailor.apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from tailor.apps.titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case
from titanic.adapter.outbound.orm.passenger_orm import TitanicRecord

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''

smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith"])


@smith_captain_router.get("/myself")
async def introduce_myself(
    james: SmithCaptainUseCase = Depends(get_smith_captain_use_case)
) -> SmithCaptainResponse :
    return await james.introduce_myself(
        SmithCaptainSchema(
            id=7,
            name="스미스 선장 (Captain Edward John Smith)"
        )
    )

