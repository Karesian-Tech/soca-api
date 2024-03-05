from datetime import datetime
from enum import Enum
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel):
    message: str
    success: bool


class SuccessListResponse(SuccessResponse, Generic[T]):
    data: List[T]


class CommonDate:
    created_at: datetime
    updated_at: datetime


class OrderType(str, Enum):
    DESC = "desc"
    ASC = "asc"


class Pagination:
    page: int
    per_page: int


class RequestBody(CommonDate):
    page: Pagination
    order_by: str
    order: OrderType
