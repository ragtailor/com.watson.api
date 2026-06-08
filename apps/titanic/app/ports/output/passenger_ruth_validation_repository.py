from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RuthValidationRepository(ABC):

    @abstractmethod
    async def list_by_pclass(
        self, pclass: int, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        ...
