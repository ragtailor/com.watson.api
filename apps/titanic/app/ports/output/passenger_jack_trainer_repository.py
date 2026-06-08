from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainRepository(ABC):

    @abstractmethod
    async def get_training_data(self) -> list[dict[str, Any]]:
        ...
