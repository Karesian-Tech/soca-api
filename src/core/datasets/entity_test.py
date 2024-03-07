from datetime import datetime
import hashlib
import random
import uuid
import pytest

from src.core.datasets.entity import Dataset, DataItem
from src.core.datasets.exceptions import DatasetItemsIsEmpty


@pytest.fixture
def item_ex1():
    return DataItem(
        item_type="image",
        url="https://picsum.photos/200/300",
        id=uuid.uuid4(),
    )


@pytest.fixture
def dataset_ex1():
    return Dataset(
        id=uuid.uuid4(),
        name="DatasetEx1",
        description="An example of dataset",
        created_at=datetime.now(),  # type: ignore
        updated_at=datetime.now(),  # type: ignore
    )


def test_cannot_remove_item_when_item_is_empty(dataset_ex1: Dataset, item_ex1):
    with pytest.raises(DatasetItemsIsEmpty, match="DatasetItems is empty"):
        dataset_ex1.remove_items([item_ex1.hash])


def test_able_to_add_the_same_datasetitems(dataset_ex1: Dataset, item_ex1: DataItem):
    item_2 = DataItem(
        item_type="image",
        url="https://picsum.photos/200/300",
        id=uuid.uuid4(),
    )

    dataset_ex1.add_items([item_ex1, item_2])

    assert len(dataset_ex1.items) == 2

    for item in dataset_ex1.items:
        assert item.hash is not None


def test_able_to_remove_items(dataset_ex1: Dataset, item_ex1: DataItem):
    dataset_ex1.items = [item_ex1]

    assert dataset_ex1.items[0].hash is not None
    assert len(dataset_ex1.items) == 1

    hash_remove = [dataset_ex1.items[0].hash]
    dataset_ex1.remove_items(hash_remove)

    assert len(dataset_ex1.items) == 0


def test_not_able_to_throw_error_when_remove_greater_len_items_than_current_items(
    dataset_ex1: Dataset, item_ex1: DataItem
):
    item_ex2 = DataItem(
        id=uuid.uuid4(),
        item_type="image",
        url="Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat.",
    )
    dataset_ex1.items = [item_ex1, item_ex2]
    assert dataset_ex1.items[0].hash is not None

    hash_remove = [dataset_ex1.items[0].hash, dataset_ex1.items[1].hash]
    hash_remove += [hashlib.md5(random.getrandbits(32).to_bytes(6, "big")).hexdigest()]
    dataset_ex1.remove_items(hash_remove)

    assert len(dataset_ex1.items) == 0
