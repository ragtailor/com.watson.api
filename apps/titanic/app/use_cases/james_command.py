from __future__ import annotations

from typing import Any

from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository


class JamesCommand(JamesUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        count = await self._repository.save_all(records)
        return {"saved": count}

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self._repository.list_paginated(page, page_size)
        return {"total": total, "page": page, "page_size": page_size, "items": items}
