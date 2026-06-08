from dataclasses import dataclass
from typing import Any


@dataclass
class CalPassengerInputDTO:
    pclass: int
    sex: str
    age: float
    sibsp: int
    parch: int
    fare: float


@dataclass
class CalValidationResultDTO:
    valid: bool
    passenger: dict[str, Any]
