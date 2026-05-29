from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WalterUseCase(ABC):

    @abstractmethod
    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        ...
