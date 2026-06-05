from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import BookingOrm
from titanic.adapter.outbound.orm.person_orm import PersonOrm
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger(__name__)


def _row_to_dict(person: PersonOrm, booking: BookingOrm | None) -> dict[str, Any]:
    return {
        "id": person.id,
        "passenger": person.passenger_id,
        "survived": person.survived,
        "pclass": booking.pclass if booking else None,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sibsp": person.sib_sp,
        "parch": person.parch,
        "ticket": booking.ticket if booking else None,
        "fare": booking.fare if booking else None,
        "cabin": booking.cabin if booking else None,
        "embarked": booking.embarked if booking else None,
    }



class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 이용한 월터의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def introduce_myself(self, query: WalterRoasterQuery):
        '''승객 명단을 가져오는 메소드'''
        logger.info("###############################################")
        logger.info("💊[월터 레포지토리] 유스케이스에서 가져온 월터 정보")
        logger.info(f"👍🏻ID: {query.id}")
        logger.info(f"🐥이름: {query.name}")
        logger.info(f"🦜메모: {query.memo}")
        logger.info("###############################################")

        pass
