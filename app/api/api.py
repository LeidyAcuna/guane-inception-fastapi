from fastapi import APIRouter

from app.api.endpoints import dog
from app.api.endpoints import user

api_router = APIRouter()


api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(dog.router, prefix="/dogs", tags=["Dogs"])
