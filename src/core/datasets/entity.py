from datetime import datetime
import hashlib
import random
from typing import List, Optional
import uuid

from pydantic import BaseModel, ConfigDict
from pydantic.dataclasses import dataclass
from src.core.datasets.exceptions import DatasetItemsIsEmpty
from src.common.domain import Domain


@dataclass
class DataItem:
    id: uuid.UUID
    item_type: str
    url: str

    def _get_hash(self):
        hash = hashlib.md5(self.id.hex.encode("utf-8"))
        hash.update(self.url.encode("utf-8"))
        hash.update(int(datetime.now().timestamp()).to_bytes(5, "big"))

    @property
    def hash(self):
        hash = hashlib.md5(self.id.hex.encode("utf-8"))
        hash.update(self.url.encode("utf-8"))
        hash.update(int(datetime.now().timestamp()).to_bytes(5, "big"))
        return hash.hexdigest()


class Dataset(Domain):
    name: str
    description: str
    items: Optional[List[DataItem]] = []

    model_config = ConfigDict(
        from_attributes=True,
    )

    def _item_empty(self) -> bool:
        if not self.items:
            return True
        return len(self.items) == 0

    def remove_items(self, list_hash: List[str]) -> None:
        if self._item_empty():
            raise DatasetItemsIsEmpty
        self.items = [item for item in self.items if item.hash not in list_hash]  # type: ignore

    def add_items(self, items: List[DataItem]) -> None:
        self.items += items


class DatasetCreate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    items: Optional[List[DataItem]] = None


class DatasetUpdate(DatasetCreate):
    id: Optional[str] = None
