from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def play_violin(self) -> dict[str, Any]:
        ...
