from typing import Dict, Generic, List, Optional
from sqlalchemy import delete, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from src.common.types import ModelT, DomainT
from src.common.utils import RepositoryUtils


class Repository(Generic[ModelT, DomainT]):
    """Repository provides a basic CRUD operation abstraction."""

    model: type[ModelT]
    domain: type[DomainT]
    session: AsyncSession
    repo_utils: RepositoryUtils

    def __init__(
        self,
        model: type[ModelT],
        domain: type[DomainT],
        session: AsyncSession,
    ):
        self.model = model
        self.domain = domain
        self.session = session
        self.repo_utils = RepositoryUtils(self.session, self.model)

    async def find_all(self, filter: Dict, pagination: Dict) -> List[DomainT]:
        ret = await self.repo_utils.get_all(filter, pagination)
        return [self.domain.model_validate(row, strict=False) for row in ret]

    async def find_by_id(self, id: str) -> Optional[DomainT]:
        ret = await self.session.scalar(select(self.model).where(self.model.id == id))
        if not ret:
            return
        return self.domain.model_validate(ret, strict=False)

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
        return self.domain.model_validate(ret, strict=False)

    async def update_by_id(self, id: str, data: Dict) -> DomainT:
        ret = await self.session.scalar(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        return self.domain.model_validate(ret, strict=False)
