from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from tailor.apps.titanic.adapter.outbound.pg.passenger_ruth_validation_pg_repository import RuthValidationPgRepository
from tailor.apps.titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from tailor.apps.titanic.app.use_cases.passenger_ruth_validation_interactor import RuthValidationInteractor

def get_ruth_validation_use_case(
        db: AsyncSession = Depends(get_db)
) -> RuthValidationUseCase:
    repository: RuthValidationRepository = RuthValidationPgRepository(session=db)
    return RuthValidationInteractor(repository=repository)
