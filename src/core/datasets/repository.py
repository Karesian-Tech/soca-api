from sqlalchemy.ext.asyncio import AsyncSession
from src.common.models import DatasetOrm
from src.common.repository import BaseRepository
from src.core.datasets.entity import Dataset as DatasetDomain


class DatasetRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(DatasetOrm, DatasetDomain, session)
