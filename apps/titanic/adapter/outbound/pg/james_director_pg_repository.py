from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.james_director_repository import JamesRepository


class JamesDirectorPgRepository(JamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        person_orms = [
            PersonOrm(
                passenger_id=cmd.passenger_id,
                name=cmd.name,
                gender=cmd.gender,
                age=cmd.age,
                sib_sp=cmd.sib_sp,
                parch=cmd.parch,
                survived=cmd.survived,
            )
            for cmd in person_commands
        ]
        self.session.add_all(person_orms)
        await self.session.flush()

        booking_orms = [
            BookingOrm(
                person_id=person_orm.id,
                pclass=cmd.pclass,
                ticket=cmd.ticket,
                fare=cmd.fare,
                cabin=cmd.cabin,
                embarked=cmd.embarked,
            )
            for person_orm, cmd in zip(person_orms, booking_commands)
        ]
        self.session.add_all(booking_orms)
        await self.session.commit()

        return len(person_orms)
