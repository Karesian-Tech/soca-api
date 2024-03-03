from typing import List
from fastapi import APIRouter, FastAPI


def register_routers(app: FastAPI, routers: List[APIRouter]) -> FastAPI:
    for router in routers:
        app.include_router(router)
    return app


def init_routers(app: FastAPI) -> FastAPI:
    from src.api.trainings.router import router as trainings_router
    from src.api.datasets.router import router as datasets_router

    return register_routers(app, [trainings_router, datasets_router])
