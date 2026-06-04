from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.use_cases.walter_roaster_interactor import WalterQuery

'''
루스 드윗 부카터 (Ruth DeWitt Bukater)
딸 로즈의 코르셋 끈을 강하게 조이며 상류층의 체면을 강요하던
통제욕의 상징. 1등석 승객(상류층) 조회를 담당한다.

추천 파일명: ruth_corset_router.py
'''

ruth_corset_router = APIRouter(prefix="/titanic/ruth", tags=["ruth"])


@ruth_corset_router.get("/corset")
async def list_first_class_passengers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    """1등석(상류층) 승객 목록 조회"""
    repository = WalterPgRepository(db)
    use_case = WalterQuery(repository)
    return await use_case.list_paginated(page, page_size)
