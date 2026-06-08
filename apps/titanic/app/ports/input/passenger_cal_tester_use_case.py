from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CalTestUseCase(ABC):

    @abstractmethod
    async def validate_passenger(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        ...
