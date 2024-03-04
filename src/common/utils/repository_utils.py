from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import Base
from src.common.types import ModelT


class Utils:
    @staticmethod
    async def find_all(session: AsyncSession, model: type[ModelT]) -> Sequence[Base]:
        return (await session.scalars(select(model))).all()
