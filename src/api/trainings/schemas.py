from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel
from datetime import datetime

from src.common.schemas import CommonDate


class ProcessStatus(str, Enum):
    Ready = "ready"
    InQueue = "in_queue"
    Processing = "processing"
    Failed = "failed"
    Completed = "completed"


class DatasetDetail(BaseModel):
    id: str
    data: List[Any]


class TrainingConfig(BaseModel):
    pass


class Training(BaseModel, CommonDate):
    name: str
    description: str | None = None
    process_status: ProcessStatus
    process_status_history: Dict[ProcessStatus, datetime]
    dataset_detail: DatasetDetail
    config_detail: Dict[str, Any]


class TrainingCreate(BaseModel):
    user_id: str
    description: str | None = None
    name: str
    schedule_at: datetime | None = None
    dataset_id: str
    training_config: TrainingConfig
