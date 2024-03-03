from dataclasses import dataclass
from typing import Optional


@dataclass
class DatasetItem:
    id: str
    item_type: str
    url: str
    hash: Optional[str] = None
