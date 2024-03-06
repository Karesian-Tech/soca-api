from typing import List, Tuple
import pytest
import pytest_asyncio
from pytest_mock.plugin import MockType, MockerFixture
from src.common.repository import Repository
from src.common.repositry_mock import MockRepository


from src.common.service import Service

ServiceFixture = Tuple[Service, MockRepository, MockerFixture, MockType]


@pytest_asyncio.fixture
def srv_fixture(mocker: MockerFixture):
    repo = MockRepository()
    spy = mocker.spy(repo, "find_all")
    srv = Service(repo=repo)
    yield srv, repo, mocker, spy


@pytest.mark.asyncio
async def test_service_crud(srv_fixture: ServiceFixture, monkeypatch):
    service, repo, mocker, spy = srv_fixture

    async def mock_find_all():
        return []

    monkeypatch.setattr(Repository, "find_all", mock_find_all)
    ret = await service.list({}, {})
    assert ret == []
