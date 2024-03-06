from typing import Dict

from src.common.repository import Repository


class MockRepository(Repository):
    def __init__(self):
        pass

    async def find_all(self, filter: Dict, pagination: Dict):
        return []
