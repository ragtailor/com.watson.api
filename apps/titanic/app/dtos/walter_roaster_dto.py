from dataclasses import dataclass


@dataclass
class WalterRoasterQuery:
    id: int
    name: str
    memo: str