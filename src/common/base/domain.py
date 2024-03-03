from typing import Any

from src.common.base import CommonField


class DomainModel(CommonField):
    id: str | int

    def __init__(self, id) -> None:
        self.id = id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DomainModel):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)
