from __future__ import annotations

from typing import Any

from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.use_cases.james_command import JamesCommand


class JamesUseCase:
    def __init__(self, repository: JamesRepository) -> None:
        self.repository = repository
        self.command = JamesCommand(repository)

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        return await self.command.receive_uploaded_records(records)

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self.repository.list_paginated(page, page_size)
        return {"total": total, "page": page, "page_size": page_size, "items": items}
