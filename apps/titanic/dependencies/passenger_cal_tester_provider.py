from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_cal_tester_pg_repository import CalTestPgRepository
from titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTestUseCase
from titanic.app.use_cases.passenger_cal_tester_interactor import CalTestInteractor

def get_cal_test_use_case(
        db: AsyncSession = Depends(get_db)
) -> CalTestUseCase:
    repository: CalTestRepository = CalTestPgRepository(session=db)
    return CalTestInteractor(repository=repository)
