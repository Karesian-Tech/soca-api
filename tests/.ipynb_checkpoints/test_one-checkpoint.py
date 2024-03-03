import pytest
from sqlalchemy.orm import Session

from src.common.models.dataset import Dataset
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.common.config import settings
from src.common.database import Base


@pytest.fixture(scope="session")
def engine():
    eng = create_async_engine(settings.get_db_url("test"))
    yield eng
    eng.sync_engine.dispose()


@pytest.fixture
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, create):
    async with AsyncSession(engine) as sess:
        yield sess


@pytest.mark.asyncio
async def test_one(session: AsyncSession):
    data = Dataset(name="ss", description="asds", items=[])
    session.add(data)
    await session.commit()
    assert len((await session.execute(sa.select(Dataset))).scalar().all()) == 2
