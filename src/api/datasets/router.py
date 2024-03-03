from fastapi import APIRouter
from src.common.schemas import SuccessListResponse, SuccessResponse

from src.api.datasets.schemas import DatasetCreate, DatasetItem


router = APIRouter(prefix="/datasets", tags=["Datasets"])


@router.post("/")
async def dataset_create(req: DatasetCreate) -> SuccessResponse:
    return SuccessResponse(message="success", success=True)


@router.get("/{dataset_id}")
async def dataset_detail(dataset_id: str) -> SuccessResponse:
    return SuccessResponse(message="success", success=True)


@router.post("/list")
async def dataset_list(req) -> SuccessListResponse[DatasetItem]:
    return SuccessListResponse(message="success", success=True, data=[])


@router.put("/{dataset_id}")
async def dataset_edit(
    dataset_id: str, req: DatasetCreate
) -> SuccessListResponse[DatasetItem]:
    return SuccessListResponse(message="success", success=True, data=[])


@router.delete("/{dataset_id}")
async def dataset_remove(
    dataset_id: str, req: DatasetCreate
) -> SuccessListResponse[DatasetItem]:
    return SuccessListResponse(message="success", success=True, data=[])
