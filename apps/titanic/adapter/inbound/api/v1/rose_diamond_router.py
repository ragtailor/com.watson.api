from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterPgRepository
from titanic.app.use_cases.caledon_query import CaledonValidation
from titanic.app.use_cases.walter_roaster_interactor import WalterQuery

'''
로즈 드윗 부카터 (Rose DeWitt Bukater)
상류층의 답답함에서 벗어나고자 하는 의지, 그리고
영화의 핵심 매개체인 '다이아몬드'와 관련된 키워드입니다.
'''

rose_diamond_router = APIRouter(prefix="/titanic/rose", tags=["rose"])


@rose_diamond_router.get("/diamond")
async def analyze_rose_survival():
    """로즈 드윗 부카터의 생존 분석"""
    pass


@rose_diamond_router.post("/predict")
async def predict_survival(passenger: CaledonValidation):
    """승객 정보를 입력받아 생존 여부 예측"""
    pass


@rose_diamond_router.get("/passengers")
async def list_passengers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    repository = WalterPgRepository(db)
    use_case = WalterQuery(repository)
    return await use_case.list_paginated(page, page_size)

