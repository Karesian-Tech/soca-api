from datetime import datetime
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


class Pagination:
    limit: int
    offset: int


class RequestBody(BaseModel, Pagination, CommonDate):
    pass
