import hashlib
import random
import uuid

from .repository_utils import Utils as _RepositoryUtils
from .model_orm_utils import Utils as _ModelOrmUtils


RepositoryUtils = _RepositoryUtils
ModelOrmUtils = _ModelOrmUtils


def generateUUIDv4() -> str:
    return uuid.uuid4().hex


def get_hash(id: str) -> str:
    hash = hashlib.md5(id.encode())
    hash.update(random.getrandbits(32).to_bytes(5, "big"))
    return hash.hexdigest()
