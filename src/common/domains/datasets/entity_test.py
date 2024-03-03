import hashlib
import random
import pytest
from src.common.base.entities import DatasetItem

from src.common.domains.datasets.entity import Dataset
from src.common.domains.datasets.exceptions import DatasetItemsIsEmpty
from src.common.utils import generateUUIDv4


@pytest.fixture
def item_ex1():
    return DatasetItem(
        item_type="image",
        url="https://picsum.photos/200/300",
        id="27bbd554-535a-48f9-b93e-d9f07f2595fe",
    )


@pytest.fixture
def dataset_ex1():
    return Dataset(
        id=generateUUIDv4(),
        name="DatasetEx1",
        description="An example of dataset",
    )


def test_cannot_remove_item_when_item_is_empty(dataset_ex1: Dataset, item_ex1):
    with pytest.raises(DatasetItemsIsEmpty, match="DatasetItems is empty"):
        dataset_ex1.remove_items([item_ex1.hash])


def test_able_to_add_the_same_datasetitems(dataset_ex1: Dataset, item_ex1: DatasetItem):
    item_2 = DatasetItem(
        item_type="image",
        url="https://picsum.photos/200/300",
        id="27bbd554-535a-48f9-b93e-d9f07f2595fe",
    )

    dataset_ex1.add_items([item_ex1, item_2])

    assert len(dataset_ex1.items) == 2

    for item in dataset_ex1.items:
        assert item.hash is not None


def test_able_to_remove_items(dataset_ex1: Dataset):
    assert dataset_ex1.items[0].hash is not None

    hash_remove = [dataset_ex1.items[0].hash]
    dataset_ex1.remove_items(hash_remove)

    assert len(dataset_ex1.items) == 1


def test_not_able_to_throw_error_when_remove_greater_len_items_than_current_items(
    dataset_ex1: Dataset,
):
    assert dataset_ex1.items[0].hash is not None

    hash_remove = [dataset_ex1.items[0].hash, dataset_ex1.items[1].hash]
    hash_remove += [hashlib.md5(random.getrandbits(32).to_bytes(6, "big")).hexdigest()]
    dataset_ex1.remove_items(hash_remove)

    assert len(dataset_ex1.items) == 0
