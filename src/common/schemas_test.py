from datetime import datetime
from typing import Dict, List, Optional
from pydantic_core.core_schema import is_instance_schema
from sqlalchemy.orm import validates
from src.common.schemas import FieldReq, FilterObject, Pagination, RequestBody


def test_pagination_object_serialization():
    pagination = Pagination()
    pagination_dict = pagination.model_dump()
    assert pagination_dict.get("limit", None) == 25
    assert pagination_dict.get("offset", None) == 0
    assert pagination_dict.get("order", None) == "desc"
    assert pagination_dict.get("order_by", None) == "created_at"


def test_pagination_object_deserialization():
    pagination = {"page": 1, "per_page": 10, "order": "asc", "order_by": "created_at"}
    validation = Pagination.model_validate(pagination)
    assert isinstance(validation, Pagination)
    assert validation.per_page == 10
    assert validation.order == "asc"
    pagination = {}
    validation = Pagination.model_validate(pagination)
    assert validation.page == 1
    assert validation.per_page == 25
    assert validation.order == "desc"
    assert validation.order_by == "created_at"


class MockSchema(RequestBody):
    name: Optional[FieldReq[str]] = None
    created_at: Optional[FieldReq[datetime]] = None


def test_request_body_deserialization():
    req_body = RequestBody()
    assert getattr(req_body, "pagination") is not None

    mock_request_dict = {"name": "ex1"}

    validation = MockSchema.model_validate(mock_request_dict)
    assert getattr(validation, "name") == "ex1"
    assert isinstance(validation.pagination, Pagination)
    assert validation.pagination.order == "desc"

    mock_request_dict = {}

    validation = MockSchema.model_validate(mock_request_dict)
    assert validation is not None
    assert validation.pagination is not None

    mock_request_dict = {"name": ["ex1", "ex2"]}

    validation = MockSchema.model_validate(mock_request_dict)

    assert isinstance(validation.name, List)
    assert len(validation.name) == 2

    mock_request_dict = {"created_at": {"lte": datetime.now()}}

    validation = MockSchema.model_validate(mock_request_dict)
    assert validation.created_at is not None
    assert isinstance(validation.created_at, FilterObject)
    assert validation.created_at.lte < datetime.now()  # type: ignore


def assert_dict_value_none(dump: Dict):
    for k, v in dump.items():
        if not v:
            return False
    return True


def test_request_body_serialization():
    schema = MockSchema()

    dump = schema.model_dump()
    assert dump.get("pagination") is not None
    assert isinstance(dump.get("pagination"), Dict)

    dump_pagination = dump.get("pagination")
    assert dump_pagination.get("offset") == 0  # type: ignore

    schema = MockSchema(name=["ex", "ex2"])

    dump = schema.model_dump(exclude_none=True)
    assert len(dump.get("name")) == 2  # type: ignore
    assert assert_dict_value_none(dump)

    schema = MockSchema(created_at=FilterObject(lte=datetime))

    dump = schema.model_dump(exclude_none=True)
    assert assert_dict_value_none(dump)
    assert dump.get("created_at").get("lte") is datetime  # type: ignore.
