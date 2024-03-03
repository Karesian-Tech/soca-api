from dataclasses import dataclass
import hashlib
import random
from typing import List, Optional
from src.common.base.domain import DomainModel
from src.common.base.entities import DatasetItem
from src.common.domains.datasets.exceptions import DatasetItemsIsEmpty


class Dataset(DomainModel):
    name: str
    description: str
    items: List[DatasetItem]

    def __init__(
        self, id: str, name: str, description: str, items: List[DatasetItem] = []
    ) -> None:
        super().__init__(id)
        self.name = name
        self.description = description
        self.items = items

    def _gen_item_hash(self, item: DatasetItem) -> str:
        hash = hashlib.md5(item.id.encode())
        hash.update(random.getrandbits(32).to_bytes(5, "big"))
        return hash.hexdigest()

    def remove_items(self, list_hash: List[str]) -> None:
        if len(self.items) == 0:
            raise DatasetItemsIsEmpty

        self.items = [item for item in self.items if item.hash not in list_hash]

    def _get_items_hashed(self, items: List[DatasetItem]) -> List[DatasetItem]:
        for item in items:
            item.hash = self._gen_item_hash(item)
        return items

    def add_items(self, items: List[DatasetItem]) -> None:
        self.items += self._get_items_hashed(items)
