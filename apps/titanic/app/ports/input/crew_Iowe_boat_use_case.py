from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IoweBoatUseCase(ABC):

    @abstractmethod
    async def get_boat_status(self) -> dict[str, Any]:
        ...
