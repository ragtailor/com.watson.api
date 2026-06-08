from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.crew_Iowe_boat_pg_repository import IoweBoatPgRepository
from tailor.apps.titanic.app.ports.output.crew_lowe_boat_repository import IoweBoatRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.titanic.app.ports.input.crew_lowe_boat_use_case import IoweBoatUseCase
from tailor.apps.titanic.app.use_cases.crew_lowe_boat_interactor import IoweBoatInteractor

def get_lowe_boat_use_case(
        db: AsyncSession = Depends(get_db)
) -> IoweBoatUseCase:
    repository: IoweBoatRepository = IoweBoatPgRepository(session=db)
    return IoweBoatInteractor(repository=repository)
