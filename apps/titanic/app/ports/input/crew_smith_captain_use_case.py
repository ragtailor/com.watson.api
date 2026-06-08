from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        ...
