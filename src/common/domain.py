from datetime import datetime
import uuid
from pydantic import BaseModel


class CommonDate:
    created_at: datetime
    updated_at: datetime


class CommonActionBy:
    created_by: str
    updated_by: str


class Domain(BaseModel, CommonDate):
    id: uuid.UUID
