from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)


class JackTrainerMapper:

    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: PassengerEntity) -> JackTrainerOrm:
        survival_raw: str | None
        if entity.survival_status.survived is True:
            survival_raw = "1"
        elif entity.survival_status.survived is False:
            survival_raw = "0"
        else:
            survival_raw = None

        return JackTrainerOrm(
            id=entity.id,
            passenger_id=str(entity.passenger_id) if entity.passenger_id else None,
            name=entity.name.full_name if entity.name else None,
            gender=str(entity.gender),
            age=str(entity.age.value) if entity.age.value is not None else None,
            sib_sp=str(entity.family_relation.sib_sp),
            parch=str(entity.family_relation.parch),
            survived=survival_raw,
        )
