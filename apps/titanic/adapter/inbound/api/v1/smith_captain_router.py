from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.adapter.outbound.orm.person_orm import TitanicRecord

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''

smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith"])


@smith_captain_router.get("/wheel")
async def get_passenger_stats(db: AsyncSession = Depends(get_db)):
    """전체 승객 생존/사망 통계"""
    total = (
        await db.execute(select(func.count()).select_from(TitanicRecord))
    ).scalar_one()
    survived = (
        await db.execute(
            select(func.count()).where(TitanicRecord.survived == "1")
        )
    ).scalar_one()
    return {
        "total": total,
        "survived": survived,
        "perished": total - survived,
    }
