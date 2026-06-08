from __future__ import annotations

from fastapi import logger
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_orm import PersonOrm
from titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorQuery, JamesDirectorResponse, PersonCommand
from titanic.app.ports.output.crew_james_director_repository import JamesDirectorRepository


class JamesDirectorPgRepository(JamesDirectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        
        '''제임스 감독의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JamesDirectorPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: JamesDirectorResponse = JamesDirectorResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def upload_titanic_file(
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
