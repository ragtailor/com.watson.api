from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class JackModelInfoDTO:
    model_name: str
    train_accuracy: str


@dataclass
class JackPredictionDTO:
    survived: int
    survival_probability: str
    death_probability: str
    passenger_info: dict[str, Any]
    message: Optional[str] = None
    analysis: Optional[str] = None
