from dataclasses import dataclass
from typing import Optional
from tailor.apps.titanic.domain.value_objects.passenger_jack_trainer_vo import Age, FamilyRelation, Gender, PassengerId, PassengerName, SurvivalStatus

@dataclass
class PassengerEntity:
    """
    Passenger 도메인 Entity.

    - 동등성: id (DB PK) 기반
    - 불변 VO 조합으로 상태 표현
    - 도메인 행위(비즈니스 로직)는 이 클래스 내부에서만 처리
    - ORM / SQLAlchemy 완전 분리
    """

    id: int                             # DB PK (영속성 식별자)
    passenger_id: Optional[PassengerId] # 원천 승객 ID VO
    name: Optional[PassengerName]       # 이름 VO
    gender: Gender                      # 성별 VO
    age: Age                            # 나이 VO
    family_relation: FamilyRelation     # 가족 동승 VO
    survival_status: SurvivalStatus     # 생존 여부 VO

    # ──────────────────────────────────────
    # 팩토리 메서드: ORM → Entity 변환
    # ──────────────────────────────────────
    @classmethod
    def from_orm(cls, orm) -> "PassengerEntity":
        """
        JackTrainerOrm 인스턴스를 받아 도메인 Entity로 재구성.
        인프라 계층(repo_impl)에서만 호출해야 함.
        """
        return cls(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    # ──────────────────────────────────────
    # 도메인 행위 (Business Logic)
    # ──────────────────────────────────────
    def is_high_risk(self) -> bool:
        """
        고위험군 판정.
        규칙: 남성 + 성인 + 혼자 탑승 → 생존 가능성 통계적으로 낮음
        """
        return (
            not self.gender.is_female()
            and not self.age.is_minor
            and self.family_relation.is_alone
        )

    def record_survival(self, survived: bool) -> None:
        """
        생존 결과 기록. (도메인 이벤트 발행 포인트)
        frozen=True VO이므로 새 VO로 교체.
        """
        object.__setattr__(
            self,
            "survival_status",
            SurvivalStatus(survived=survived),
        )

    def has_family(self) -> bool:
        return not self.family_relation.is_alone

    # ──────────────────────────────────────
    # 동등성: ID 기반
    # ──────────────────────────────────────
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return (
            f"PassengerEntity("
            f"id={self.id}, "
            f"name={self.name}, "
            f"gender={self.gender}, "
            f"age={self.age}, "
            f"survival={self.survival_status})"
        )