from __future__ import annotations

from typing import Any

from titanic.app.ports.output.james_repository import JamesRepository


class JamesCommand:
    def __init__(self, repository: JamesRepository) -> None:
        self.repository = repository

    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        saved = await self.repository.save_all(records)
        return {"received": len(records), "saved": saved}
