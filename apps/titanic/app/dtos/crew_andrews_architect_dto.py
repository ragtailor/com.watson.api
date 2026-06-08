from dataclasses import dataclass, field


@dataclass
class AndrewsArchitectDTO:
    ship: str
    columns: list[str] = field(default_factory=list)
