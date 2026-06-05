from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.adapter.outbound.pg.james_director_pg_repository import JamesDirectorPgRepository
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesRepository
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor


def get_james_director_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesDirectorUseCase:
    repository: JamesRepository = JamesDirectorPgRepository(session=db)
    return JamesDirectorInteractor(repository=repository)