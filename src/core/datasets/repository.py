from sqlalchemy.ext.asyncio import AsyncSession
from src.common.models import DatasetOrm
from src.common.repository import Repository
from src.core.datasets.entity import Dataset as DatasetDomain


class DatasetRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(DatasetOrm, DatasetDomain, session)
