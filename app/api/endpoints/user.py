from fastapi import APIRouter
from typing import Any, List
from fastapi import Depends, FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session
from app.infra.postgres.crud.user import users
from app.schemas import user
from app.infra.postgres.models.base import get_db
from app.auth import functions
from app.schemas import auth


router = APIRouter()

@router.get("/", response_model=List[user.User], tags=["Users"])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    data_users = users.get_all(db=db, skip=skip, limit=limit)
    return data_users

@router.post(
        "/",
        response_model=user.User,
        status_code=HTTP_201_CREATED,
        tags=["Users"])
def create_users(*, db: Session = Depends(get_db),
                 user_obj: user.UserCreate,
                 current_user: auth.UserAuthBase = Depends(functions.get_current_user)) -> Any:
    data_user = users.get_email(db=db, email=user_obj.email)
    if data_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print
    data_user = users.create(db=db, obj_in=user_obj)
    return data_user


@router.put(
        "/{email}", response_model=user.User,
        responses={HTTP_404_NOT_FOUND: {"model": user.HTTPError}},
        tags=["Users"])
def update_user(
                *, db: Session = Depends(get_db),
                email: str,
                user_obj: user.UserUpdate,
                current_user: auth.UserAuthBase = Depends(functions.get_current_user)) -> Any:
    data_user = users.get_email(db=db, email=email)
    if not data_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    data_user = users.update(db=db, db_obj=data_user, obj_in=user_obj)
    return data_user


@router.delete("/{email}", response_model=user.User,
            responses={HTTP_404_NOT_FOUND: {"model": user.HTTPError}},
            tags=["Users"])
def delete_users(*, db: Session = Depends(get_db), email: str) -> Any:
    data_user = users.get_email(db=db, email=email)
    if not data_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    data_user = users.remove(db=db, email=email)
    return data_user