from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AndrewsArchitectUseCase(ABC):

    @abstractmethod
    async def get_blueprint(self) -> dict[str, Any]:
        ...
