from typing import Dict, Tuple
from src.common.repository import Repository
from src.common.schemas import Pagination, RequestBody


class Service:
    _repo: Repository

    def __init__(self, repo: Repository):
        self._repo = repo

    def _preprocess_request_body(self, req: RequestBody) -> Tuple[Dict, Dict]:
        dump = req.model_dump()
        pagination = dump.get("pagination", Pagination().model_dump())
        dump.pop("pagination")
        filter = dump

        return filter, pagination

    async def list(self, req: RequestBody):
        filter, pagination = self._preprocess_request_body(req)
        return await self._repo.find_all(filter, pagination)

    async def find(self):
        return

    async def add(self):
        return

    async def find_one(self):
        return

    async def update(self):
        return

    async def delete(self):
        return
