from typing import Generator
import asyncio
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.common.config import settings
from src.common.database import Base


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def engine():
    eng = create_async_engine(settings.get_db_url("test"))
    yield eng
    eng.sync_engine.dispose()


@pytest_asyncio.fixture
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
