from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DatasetItem(BaseModel):
    id: str
    item_type: str
    url: str
    hash: Optional[str] = None

    model_config = ConfigDict(frozen=True)
