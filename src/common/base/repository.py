from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from src.common.base.domain import DomainModel

from src.common.database import Base

ModelGeneric = TypeVar("ModelGeneric", bound=Base)
DomainGeneric = TypeVar("DomainGeneric", bound=DomainModel)


class BaseRepository(Generic[ModelGeneric, DomainGeneric]):
    """BaseRepository provides a basic CRUD operation abstraction."""

    model: type[ModelGeneric]
    domain: type[DomainGeneric]
    session: AsyncSession

    def __init__(
        self,
        model: type[ModelGeneric],
        domain: type[DomainGeneric],
        session: AsyncSession,
    ):
        self.model = model
        self.domain = domain
        self.session = session

    def create(self) -> type[DomainGeneric]:
        return
