from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.james_director_repository import JamesRepository


class JamesDirectorPgRepository(JamesRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def receive_uploaded_records(self,
                                       person_commands: list[PersonCommand],
                                       booking_commands: list[BookingCommand]) -> int:
        print("[제임스 레포지터리] PersonCommand 상위 5개 레코드:", flush=True)
        for person in person_commands[:5]:
            print(person, flush=True)

        print("[제임스 레포지터리] BookingCommand 상위 5개 레코드:", flush=True)
        for booking in booking_commands[:5]:
            print(booking, flush=True)

        pass

    