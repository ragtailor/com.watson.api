from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(self, schema: list[TitanicRecordSchema]) -> dict[str, Any]:
        # schema 에 상위 5줄 출력 하는 로그
        print("[제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드:")
        for record in schema[:5]:
            print(record)

        # schema 를 PersonCommand 및 BookingCommand 로 나눠서 옮겨담기
        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(PersonCommand(
                passenger_id=record.get("passenger_id") or "",
                name=record.get("name") or "",
                gender=record.get("gender") or "",
                age=record.get("age") or "",
                sib_sp=record.get("sib_sp") or "",
                parch=record.get("parch") or "",
                survived=record.get("survived") or "",
            ))
            booking_commands.append(BookingCommand(
                pclass=record.get("pclass") or "",
                ticket=record.get("ticket") or "",
                fare=record.get("fare") or "",
                cabin=record.get("cabin") or "",
                embarked=record.get("embarked") or "",
            ))
        # person_commands 와 booking_commands 에 상위 5줄 출력 하는 로그

        pass
