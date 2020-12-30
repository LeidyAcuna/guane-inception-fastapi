from fastapi import APIRouter

from app.api.endpoints import dog, user, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/user_auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(dog.router, prefix="/dogs", tags=["Dogs"])
