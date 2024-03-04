from typing import Dict, Generic, Optional
from sqlalchemy import delete, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from src.common.types import ModelT, DomainT


class BaseRepository(Generic[ModelT, DomainT]):
    """BaseRepository provides a basic CRUD operation abstraction."""

    model: type[ModelT]
    domain: type[DomainT]
    session: AsyncSession

    def __init__(
        self,
        model: type[ModelT],
        domain: type[DomainT],
        session: AsyncSession,
    ):
        self.model = model
        self.domain = domain
        self.session = session

    async def find_all(self, **kwargs):
        return

    async def find_by_id(self, id: str) -> Optional[DomainT]:
        ret = await self.session.scalar(select(self.model).where(self.model.id == id))
        if not ret:
            return
        return self.domain.model_validate(ret, from_attributes=True)

    async def create(self, data: Dict) -> DomainT:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self.domain.model_validate(instance, from_attributes=True)

    async def delete_by_id(self, id: str) -> Optional[DomainT]:
        ret = await self.session.scalar(
            delete(self.model).where(self.model.id == id).returning(self.model)
        )
        if not ret:
            return
        return self.domain.model_validate(ret)

    async def update_by_id(self, id: str, data: Dict) -> DomainT:
        ret = await self.session.scalar(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        return self.domain.model_validate(ret, from_attributes=True)
