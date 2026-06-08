from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseModelRepository(ABC):

    @abstractmethod
    async def get_all_records(self) -> list[dict[str, Any]]:
        ...
