from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic.adapter.outbound.pg.passenger_jack_trainer_pg_repository import JackTrainPgRepository
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainUseCase
from titanic.app.use_cases.passenger_jack_trainer_interactor import JackTrainInteractor

def get_jack_train_use_case(
        db: AsyncSession = Depends(get_db)
) -> JackTrainUseCase:
    repository: JackTrainRepository = JackTrainPgRepository(session=db)
    return JackTrainInteractor(repository=repository)
