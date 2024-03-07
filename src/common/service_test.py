from typing import List, Tuple
import pytest
import pytest_asyncio
import asyncio
from pytest_mock.plugin import MockType, MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database import Base
from src.common.domain import Domain
from src.common.repository import Repository
from src.common.repositry_mock import MockRepository
from src.common.schemas import RequestBody


from src.common.service import Service

ServiceFixture = Tuple[Service, MockRepository, MockerFixture]


@pytest_asyncio.fixture
def srv_fixture(mocker: MockerFixture):
    repo = MockRepository()
    srv = Service(repo=repo)
    yield srv, repo, mocker


@pytest.mark.asyncio
async def test_service_crud(srv_fixture: ServiceFixture, monkeypatch):
    service, repo, mocker = srv_fixture

    async def mock_find_all(self, filter, pagination):
        return []

    monkeypatch.setattr(MockRepository, "find_all", mock_find_all)
    spy = mocker.spy(MockRepository, "find_all")

    ret = await service.list(RequestBody())
    spy.assert_called_with(
        repo, {}, {"order": "desc", "order_by": "created_at", "limit": 25, "offset": 0}
    )
    assert ret == []
