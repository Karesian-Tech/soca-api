from typing import Any, List
from pydantic import BaseModel


class DatasetCreate(BaseModel):
    pass


class DatasetItem(BaseModel):
    id: str
    name: str
    description: str
    items: List[Any]
