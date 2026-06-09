from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class PassengerId:
    """
    승객 식별자 VO.
    ORM의 passenger_id(외부 원천 ID)를 래핑.
    """
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("PassengerId는 빈 값일 수 없습니다.")

    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class PassengerName:
    """
    승객 이름 VO.
    타이타닉 원본 데이터는 'Last, Title. First' 형식.
    """
    full_name: str

    def __post_init__(self) -> None:
        if not self.full_name or not self.full_name.strip():
            raise ValueError("PassengerName은 빈 값일 수 없습니다.")
        if len(self.full_name) > 200:
            raise ValueError("PassengerName은 200자를 초과할 수 없습니다.")

    @property
    def normalized(self) -> str:
        return self.full_name.strip()

    def __str__(self) -> str:
        return self.normalized

from enum import Enum

class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    """
    성별 VO.
    원천 데이터의 'male'/'female' 문자열을 도메인 타입으로 정규화.
    """
    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        if raw is None:
            return cls(value=GenderType.UNKNOWN)
        mapping = {
            "male": GenderType.MALE,
            "female": GenderType.FEMALE,
        }
        normalized = raw.strip().lower()
        gender_type = mapping.get(normalized, GenderType.UNKNOWN)
        return cls(value=gender_type)

    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    def __str__(self) -> str:
        return self.value.value

@dataclass(frozen=True)
class Age:
    """
    나이 VO.
    원천 데이터가 String이므로 파싱 + 도메인 유효성 검증.
    """
    value: Optional[float]  # 타이타닉 데이터셋은 소수점 나이 존재

    def __post_init__(self) -> None:
        if self.value is not None:
            if self.value < 0 or self.value > 120:
                raise ValueError(f"Age 유효 범위 초과: {self.value}")

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Age":
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            return cls(value=float(raw))
        except ValueError:
            raise ValueError(f"Age 파싱 실패: '{raw}'")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def is_minor(self) -> bool:
        return self.value is not None and self.value < 18

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "Unknown"


@dataclass(frozen=True)
class FamilyRelation:
    """
    가족 동승 VO.
    SibSp(형제/배우자)와 Parch(부모/자녀)를 하나의 도메인 개념으로 묶음.
    """
    sib_sp: int  # 형제자매 + 배우자 수
    parch: int   # 부모 + 자녀 수

    def __post_init__(self) -> None:
        if self.sib_sp < 0:
            raise ValueError("sib_sp는 0 이상이어야 합니다.")
        if self.parch < 0:
            raise ValueError("parch는 0 이상이어야 합니다.")

    @classmethod
    def from_raw(cls, sib_sp_raw: Optional[str], parch_raw: Optional[str]) -> "FamilyRelation":
        try:
            sib_sp = int(sib_sp_raw) if sib_sp_raw and sib_sp_raw.strip() else 0
            parch = int(parch_raw) if parch_raw and parch_raw.strip() else 0
        except ValueError as e:
            raise ValueError(f"FamilyRelation 파싱 실패: {e}")
        return cls(sib_sp=sib_sp, parch=parch)

    @property
    def total_family_size(self) -> int:
        return self.sib_sp + self.parch

    @property
    def is_alone(self) -> bool:
        return self.total_family_size == 0

    def __str__(self) -> str:
        return f"SibSp={self.sib_sp}, Parch={self.parch}"


@dataclass(frozen=True)
class SurvivalStatus:
    """
    생존 여부 VO.
    타이타닉 데이터: '0'=사망, '1'=생존, None=미확인
    """
    survived: Optional[bool]

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "SurvivalStatus":
        if raw is None or raw.strip() == "":
            return cls(survived=None)
        if raw.strip() == "1":
            return cls(survived=True)
        if raw.strip() == "0":
            return cls(survived=False)
        raise ValueError(f"SurvivalStatus 파싱 실패: '{raw}'")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None

    def __str__(self) -> str:
        if self.survived is None:
            return "Unknown"
        return "Survived" if self.survived else "Did not survive"



