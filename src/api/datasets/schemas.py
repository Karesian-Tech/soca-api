from typing import Any, List
from pydantic import BaseModel
from src.common.entities import DataItem

from src.common.schemas import FieldReq, RequestBody


class DatasetCreate(BaseModel):
    pass


class DatasetItem(RequestBody):
    id: FieldReq[str]
    name: FieldReq[str]
    description: FieldReq[str]
    items: FieldReq[DataItem]
