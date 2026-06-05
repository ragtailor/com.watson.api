from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.adapter.outbound.pg.walter_roaster_pg_repository import WalterRoasterPgRepository
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
"""
JamesDirector 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JamesDirectorPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JamesDirectorUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from backend.core.matrix.oracle_database import get_db
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor


def get_walter_roaster_use_case(
                db : AsyncSession = Depends(get_db)
) -> WalterRoasterUseCase:
        repository : WalterRoasterRepository = WalterRoasterPgRepository(session=db)
        return WalterRoasterInteractor(repository=repository)
        



