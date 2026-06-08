from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_Iowe_boat_pg_repository import IoweBoatPgRepository
from titanic.app.ports.output.crew_Iowe_boat_repository import IoweBoatRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.crew_Iowe_boat_use_case import IoweBoatUseCase
from titanic.app.use_cases.crew_Iowe_boat_interactor import IoweBoatInteractor

def get_iowe_boat_use_case(
        db: AsyncSession = Depends(get_db)
) -> IoweBoatUseCase:
    repository: IoweBoatRepository = IoweBoatPgRepository(session=db)
    return IoweBoatInteractor(repository=repository)
