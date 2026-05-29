from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesRepository(ABC):
    @abstractmethod
    async def save_all(self, records: list[dict[str, Any]]) -> int:
        ...

