from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from src.common.entities import DatasetItem
from src.common.utils import ModelOrmUtils
from src.common.database import Base


import uuid


class DatasetOrm(Base, ModelOrmUtils.CommonDateOrm):
    __tablename__ = "datatsets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid.uuid4().hex)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    items: Mapped[List[DatasetItem]] = mapped_column(JSONB, nullable=True)
