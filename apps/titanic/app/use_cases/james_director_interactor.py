from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_repository import JamesRepository


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(self, schema: TitanicRecordSchema):
        # schema 에 상위 5줄 출력 하는 로그
        print("[제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드:")
        for record in schema[:5]:
            print(record)
        
        pass
