import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.common.config import settings
from src.common.database import Base


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(settings.get_db_url("test"))
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine):
    async with AsyncSession(engine) as session:
        yield session
