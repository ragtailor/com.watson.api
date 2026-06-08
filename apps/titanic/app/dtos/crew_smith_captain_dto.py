from dataclasses import dataclass


@dataclass
class SmithStatsDTO:
    total: int
    survived: int
    perished: int
