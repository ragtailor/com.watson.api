from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesRepository
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(self, schema: list[TitanicRecordSchema]) -> dict[str, Any]:
        # schema 에 상위 5줄 출력 하는 로그
        print("[제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드:", flush=True)
        for record in schema[:5]:
            print(record, flush=True)

        # schema 를 PersonCommand 및 BookingCommand 로 나눠서 옮겨담기
        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in schema:
            person_commands.append(PersonCommand(
                passenger_id=record.passenger_id or "",
                name=record.name or "",
                gender=record.gender or "",
                age=record.age or "",
                sib_sp=record.sib_sp or "",
                parch=record.parch or "",
                survived=record.survived or "",
            ))
            booking_commands.append(BookingCommand(
                pclass=record.pclass or "",
                ticket=record.ticket or "",
                fare=record.fare or "",
                cabin=record.cabin or "",
                embarked=record.embarked or "",
            ))

        await self._repository.receive_uploaded_records(person_commands, booking_commands)

        return {
            "persons": len(person_commands),
            "bookings": len(booking_commands),
        }
