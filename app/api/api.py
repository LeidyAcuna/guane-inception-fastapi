from fastapi import APIRouter

from app.api.endpoints import dog

api_router = APIRouter()

api_router.include_router(dog.router, prefix="/dogs", tags=["Dogs"])