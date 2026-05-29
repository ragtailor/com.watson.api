from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic.app.use_cases.walter_query import WalterQuery

walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_router.get("/passengers")
async def list_passengers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    repository = WalterPgRepository(db)
    use_case = WalterQuery(repository)
    return await use_case.list_paginated(page, page_size)
