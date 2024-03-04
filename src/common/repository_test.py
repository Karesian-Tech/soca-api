import uuid
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.models import DatasetOrm
from src.common.utils import RepositoryUtils
from src.core.datasets.repository import DatasetRepository
from src.core.datasets.entity import DatasetCreate


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


@pytest.mark.asyncio
async def test_find_all():
    pass
