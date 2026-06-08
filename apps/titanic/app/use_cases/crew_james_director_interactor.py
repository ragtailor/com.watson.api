from __future__ import annotations

from tailor.apps.titanic.adapter.inbound.api.schemas.crew_james_director_schema import TitanicRecordSchema
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository
from titanic.app.dtos.crew_james_director_dto import BookingCommand, PersonCommand


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesDirectorRepository) -> None:
        self.repository = repository

    async def upload_titanic_file(self, schema: list[TitanicRecordSchema]) -> dict:
        person_commands = [
            PersonCommand(
                passenger_id=record.passenger_id or "",
                name=record.name or "",
                gender=record.gender or "",
                age=record.age or "",
                sib_sp=record.sib_sp or "",
                parch=record.parch or "",
                survived=record.survived or "",
            )
            for record in schema
        ]
        booking_commands = [
            BookingCommand(
                pclass=record.pclass or "",
                ticket=record.ticket or "",
                fare=record.fare or "",
                cabin=record.cabin or "",
                embarked=record.embarked or "",
            )
            for record in schema
        ]

        saved = await self.repository.receive_uploaded_records(person_commands, booking_commands)
        return {"saved": saved}
