import hashlib
import random
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from src.common.entities import DatasetItem
from src.core.datasets.exceptions import DatasetItemsIsEmpty
from src.common.domain import Domain


class Dataset(Domain):
    name: str
    description: str
    items: Optional[List[DatasetItem]] = None

    model_config = ConfigDict(
        from_attributes=True,
    )

    def _gen_item_hash(self, item: DatasetItem) -> str:
        hash = hashlib.md5(item.id.encode())
        hash.update(random.getrandbits(32).to_bytes(5, "big"))
        return hash.hexdigest()

    def _item_empty(self) -> bool:
        if not self.items:
            return False
        return len(self.items) == 0

    def remove_items(self, list_hash: List[str]) -> None:
        if self._item_empty():
            raise DatasetItemsIsEmpty
        self.items = [item for item in self.items if item.hash not in list_hash]

    def _get_items_hashed(self, items: List[DatasetItem]) -> List[DatasetItem]:
        for item in items:
            item.hash = self._gen_item_hash(item)
        return items

    def add_items(self, items: List[DatasetItem]) -> None:
        self.items += self._get_items_hashed(items)


class DatasetCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    items: Optional[List[DatasetItem]] = None


class DatasetUpdate(DatasetCreate):
    id: Optional[str] = None
