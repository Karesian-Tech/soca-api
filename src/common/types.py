from typing import TypeVar
from src.common.database import Base
from src.common.domain import Domain


ModelT = TypeVar("ModelT", bound=Base)
DomainT = TypeVar("DomainT", bound=Domain)
