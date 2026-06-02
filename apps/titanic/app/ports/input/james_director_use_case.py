from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import TitanicRecordSchema


class JamesDirectorUseCase(ABC):

    @abstractmethod
    async def receive_uploaded_records(self, schema: list[TitanicRecordSchema]) -> dict[str, Any]:
        """CSV 파일업로드 """
        pass

