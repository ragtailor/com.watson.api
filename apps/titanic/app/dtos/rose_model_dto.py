from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RoseSurvivalResultDTO:
    survived: int
    survival_probability: str
    death_probability: str
    passenger_info: dict[str, Any]
    analysis: Optional[str] = None
