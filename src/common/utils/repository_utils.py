from typing import Dict, Generic, List, Sequence, Tuple
from sqlalchemy import HasSuffixes, Select, asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import Base
from src.common.types import FilterDateFromTo, ModelT
from src.common.schemas import OrderType


class Utils(Generic[ModelT]):
    session: AsyncSession
    model: type[ModelT]

    def __init__(self, session: AsyncSession, model: type[ModelT]):
        self.session = session
        self.model = model

    @staticmethod
    async def find_all(session: AsyncSession, model: type[ModelT]) -> Sequence[Base]:
        return (await session.scalars(select(model))).all()

    def _get_order_type(self, order_by: str, order_type: str):
        if order_type == OrderType.DESC:
            return desc(getattr(self.model, order_by))
        if order_type == OrderType.ASC:
            return asc(getattr(self.model, order_by))
        return desc(getattr(self.model, order_by))

    def _get_pagination_query(self, q: Select[Tuple[ModelT]], pagination: Dict):
        limit = pagination.get("limit", None)
        offset = pagination.get("offset", None)
        if not limit:
            q = q.limit(25)
        else:
            q = q.limit(limit)

        if not offset:
            q = q.offset(0)
        else:
            q = q.offset(offset)
        if not pagination:
            q = q.order_by(self._get_order_type("created_at", "desc"))

        order_by = pagination.get("order_by", None)
        order = pagination.get("order", None)
        if not order_by:
            q = q.order_by(self._get_order_type("created_at", "desc"))
        if order_by and not order:
            q = q.order_by(self._get_order_type("created_at", "desc"))
        elif order_by and order:
            q = q.order_by(self._get_order_type(order_by, order))
        return q

    def _is_filter_date(self, val: Dict) -> bool:
        if hasattr(val, "from"):
            return True
        if hasattr(val, "to"):
            return True
        return False

    def _get_filter_date(self, q: Select[Tuple[ModelT]], field: str, val: Dict):
        if hasattr(val, "from") and hasattr(val, "to"):
            return q.filter(getattr(self.model, field).beetween(val["from"], val["to"]))
        if hasattr(val, "from"):
            return q.where(getattr(self.model, field) > val["from"])
        if hasattr(val, "to"):
            return q.where(getattr(self.model, field) <= val["to"])
        return q

    def _get_filter(self, q: Select[Tuple[ModelT]], filter: Dict):
        for k, v in filter.items():
            attr = getattr(self.model, k)
            if isinstance(v, List):
                q = q.where(attr.in_(v))
            elif self._is_filter_date(v):
                q = self._get_filter_date(q, k, v)
            else:
                q = q.where(attr == v)
        return q

    def get_queries(self, filter: Dict, pagination: Dict) -> Select[Tuple[ModelT]]:
        q = select(self.model)
        if filter:
            q = self._get_filter(q, filter)
        q = self._get_pagination_query(q, pagination)
        return q

    async def get_all(self, filter: Dict, pagination: Dict) -> Sequence[Base]:
        q = self.get_queries(filter, pagination)
        return (await self.session.scalars(q)).all()
