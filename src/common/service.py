from typing import Dict
from src.common.repository import Repository
from src.common.schemas import RequestBody


class Service:
    _repo: Repository

    def __init__(self, repo: Repository):
        self._repo = repo

    def _preprocess_request_body(self, req: Dict):
        return

    async def list(self, req: RequestBody):
        filter, pagination = self._preprocess_request_body()
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
