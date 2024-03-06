from datetime import datetime
from typing import Sequence, Tuple
import uuid
import pytest
import pytest_asyncio
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from scripts.dataset_stub import DatasetStubs
from src.common.models import DatasetOrm, dataset
from src.common.utils import RepositoryUtils
from src.core.datasets.repository import DatasetRepository
from src.core.datasets.entity import DatasetCreate
from src.common.utils import find_one


@pytest_asyncio.fixture
def session_cur(session):
    yield session


@pytest_asyncio.fixture
def repo(session_cur: AsyncSession):
    repository = DatasetRepository(session_cur)
    return repository


@pytest_asyncio.fixture
def datacreate_stub():
    dataset = DatasetCreate(name="ex1", description="an example of dataset")
    return dataset.model_dump()


@pytest.mark.asyncio
async def test_create_dataset_repo(
    repo: DatasetRepository, session_cur: AsyncSession, datacreate_stub
):
    ret = await repo.create(datacreate_stub)
    all = await RepositoryUtils.find_all(session_cur, DatasetOrm)
    assert len(all) == 1
    assert ret.id is not None


@pytest_asyncio.fixture
async def find_by_id_stub(session_cur: AsyncSession, datacreate_stub):
    instance = DatasetOrm(**datacreate_stub)
    session_cur.add(instance)
    await session_cur.commit()
    await session_cur.refresh(instance)
    yield session_cur, instance
    await session_cur.delete(instance)
    await session_cur.commit()


@pytest.mark.asyncio
async def test_find_by_id(repo: DatasetRepository, find_by_id_stub):
    _, dataset = find_by_id_stub
    dataset_id = dataset.id
    ret = await repo.find_by_id(dataset_id)
    assert ret is not None
    assert ret.id == dataset_id


@pytest.mark.asyncio
async def test_find_by_id_not_found(repo: DatasetRepository):
    dataset_id = uuid.uuid4().hex
    ret = await repo.find_by_id(dataset_id)
    assert ret is None


@pytest.mark.asyncio
async def test_delete_by_id(repo: DatasetRepository, find_by_id_stub):
    session, dataset = find_by_id_stub

    all = await RepositoryUtils.find_all(session, DatasetOrm)

    assert len(all) == 1

    dataset_id = dataset.id
    ret = await repo.delete_by_id(dataset_id)

    all = await RepositoryUtils.find_all(session, DatasetOrm)

    assert len(all) == 0
    assert ret is not None
    assert ret.id == dataset_id


@pytest.mark.asyncio
async def test_update_by_id(repo: DatasetRepository, find_by_id_stub):
    session, dataset = find_by_id_stub

    all = await RepositoryUtils.find_all(session, DatasetOrm)

    assert len(all) == 1
    assert all[0] is not None

    dataset_id = dataset.id
    data = {
        "items": [{"id": uuid.uuid4().hex, "url": "placeholder", "item_type": "image"}]
    }

    ret = await repo.update_by_id(dataset_id, data)

    assert ret is not None
    assert ret.id == dataset_id
    assert ret.items is not None


@pytest_asyncio.fixture
async def find_all_stub(session_cur: AsyncSession):
    dataset_stubs = DatasetStubs()
    stubs = (
        await session_cur.scalars(
            insert(DatasetOrm).returning(DatasetOrm), dataset_stubs
        )
    ).all()
    await session_cur.commit()
    yield session_cur, stubs


FindAllStub = Tuple[AsyncSession, Sequence[DatasetOrm]]


@pytest.mark.asyncio
async def test_find_page(repo: DatasetRepository, find_all_stub: FindAllStub):
    session, stubs = find_all_stub
    ret = await repo.find_all({}, {})
    assert len(ret) == 25


@pytest.mark.asyncio
async def test_find_page_pagination(
    repo: DatasetRepository, find_all_stub: FindAllStub
):
    session, stubs = find_all_stub
    ret = await repo.find_all({}, {"limit": 25})
    assert len(ret) == 25
    ret = await repo.find_all({}, {"offset": 25})
    assert len(ret) == 25
    ret = await repo.find_all({}, {"offset": 25, "limit": 75})
    assert len(ret) == 75
    ret = await repo.find_all({}, {"offset": 25, "limit": 50})
    assert len(ret) == 50
    ret = await repo.find_all({}, {"offset": 75, "limit": 50})
    assert len(ret) == 25


@pytest_asyncio.fixture
async def find_all_order_stub(session_cur: AsyncSession):
    dataset_stubs = DatasetStubs()
    datasets = [DatasetOrm(**data) for data in dataset_stubs]
    session_cur.add_all(datasets)
    await session_cur.commit()
    yield session_cur


@pytest.mark.asyncio
async def test_find_page_order(
    repo: DatasetRepository, find_all_order_stub: AsyncSession
):
    session = find_all_order_stub

    datasets = await repo.find_all({}, {"order_by": "created_at", "order": "desc"})
    assert datasets[0].created_at > datasets[-1].created_at

    datasets = await repo.find_all({}, {"order_by": "created_at", "order": "asc"})
    assert datasets[0].created_at < datasets[-1].created_at

    datasets = await repo.find_all({}, {})
    assert datasets[0].created_at > datasets[-1].created_at

    datasets = await repo.find_all({}, {"order_by": "created_at"})
    assert datasets[0].created_at > datasets[-1].created_at


@pytest.mark.asyncio
async def test_find_page_filter(repo: DatasetRepository, find_all_order_stub):
    session = find_all_order_stub

    ret = await repo.find_all({"name": "ex12"}, {})
    assert len(ret) == 1
    assert ret[0].name == "ex12"

    ret = await repo.find_all({"name": ["ex12", "ex2"]}, {})
    assert len(ret) == 2

    found = find_one(ret, lambda x: x.name == "ex12")
    assert found is not None
    assert found.name == "ex12"
