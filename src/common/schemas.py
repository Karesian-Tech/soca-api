from datetime import datetime
from enum import Enum
from typing import Generic, List, Tuple, TypeVar
from typing_extensions import Optional
from pydantic import BaseModel, model_serializer
from src.common.types import DomainT

T = TypeVar("T")


class OrderType(str, Enum):
    DESC = "desc"
    ASC = "asc"


class CommonDate:
    created_at: datetime
    updated_at: datetime


class FilterObject(BaseModel, Generic[T]):
    gte: Optional[T] = None
    lte: Optional[T] = None
    lt: Optional[T] = None
    gt: Optional[T] = None


class SuccessResponse(BaseModel):
    message: str
    success: bool


class SuccessListResponse(SuccessResponse, Generic[T]):
    data: List[T]


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 25
    order_by: str = "created_at"
    order: OrderType = OrderType.DESC

    def _process_page_params(self, page: int, per_page: int) -> Tuple[int, int]:
        limit = per_page
        offset = (page - 1) * per_page
        return limit, offset

    @model_serializer
    def dump_pagination_repo(self):
        limit, offset = self._process_page_params(self.page, self.per_page)
        return {
            "limit": limit,
            "offset": offset,
            "order_by": self.order_by,
            "order": self.order,
        }


class RequestBody(BaseModel):
    pagination: Pagination = Pagination()


FieldReq = T | FilterObject | List[T]
