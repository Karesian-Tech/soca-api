import pytest
import pytest_asyncio

from src.common.models.dataset import Dataset
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.common.config import settings
from src.common.database import Base


@pytest_asyncio.fixture(scope="session")
def engine():
    eng = create_async_engine(settings.get_db_url("test"))
    yield eng
    eng.sync_engine.dispose()


@pytest_asyncio.fixture()
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def session(engine, create):
    async with AsyncSession(engine) as sess:
        yield sess


@pytest.mark.asyncio
async def test_one(session: AsyncSession):
    data = Dataset(name="ss", description="asds", items=[])
    session.add(data)
    await session.commit()
    q = await session.scalars(sa.select(Dataset))
    ret = q.all()
    o = ret[0]
    print(o.name)

    assert len(ret) == 1
