from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesRepository(ABC):
    @abstractmethod
    async def save_all(self, records: list[dict[str, Any]]) -> int:
        ...

    @abstractmethod
    async def list_paginated(self, page: int, page_size: int) -> tuple[int, list[dict[str, Any]]]:
        ...
