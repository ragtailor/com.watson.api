from __future__ import annotations

from typing import Any

from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm

# RoseModelEntity is not yet defined — mapper provides ORM ↔ dict conversion
# until the domain entity is implemented.


class RoseModelMapper:

    @staticmethod
    def to_dict(orm: RoseModelOrm) -> dict[str, Any]:
        return {
            "id": orm.id,
            "person_id": orm.person_id,
            "pclass": orm.pclass,
            "ticket": orm.ticket,
            "fare": orm.fare,
            "cabin": orm.cabin,
            "embarked": orm.embarked,
        }

    @staticmethod
    def to_orm(
        person_id: int | None,
        pclass: str | None,
        ticket: str | None,
        fare: str | None,
        cabin: str | None,
        embarked: str | None,
    ) -> RoseModelOrm:
        return RoseModelOrm(
            person_id=person_id,
            pclass=pclass,
            ticket=ticket,
            fare=fare,
            cabin=cabin,
            embarked=embarked,
        )
