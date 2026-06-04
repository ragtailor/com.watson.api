from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema
from titanic.adapter.outbound.pg.james_director_pg_repository import JamesDirectorPgRepository
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def receive_uploaded_records(self, schema: list[TitanicRecordSchema]) -> dict:
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

        repository = JamesDirectorPgRepository(self.session)
        saved = await repository.receive_uploaded_records(person_commands, booking_commands)
        return {"saved": saved}
