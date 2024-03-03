from fastapi import APIRouter
from src.api.trainings.schemas import Training, TrainingCreate

from src.common.schemas import RequestBody, SuccessListResponse, SuccessResponse


router = APIRouter(prefix="/trainings", tags=["Training"])


@router.post("/")
async def trainer_create(req: TrainingCreate) -> SuccessResponse:
    return SuccessResponse(message="success", success=True)


@router.post("/list")
async def trainer_list(req: RequestBody) -> SuccessListResponse[Training]:
    return SuccessListResponse(message="success", success=True, data=[])
