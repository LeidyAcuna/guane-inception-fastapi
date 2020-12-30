from fastapi import APIRouter
from typing import Any, List
from fastapi import Depends, FastAPI, HTTPException, status
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session
from app.infra.postgres.crud.dog import dogs
from app.infra.postgres.crud.user import users
from app.schemas import dog
from app.infra.postgres.models.base import get_db
from app.auth import functions
from app.schemas import auth


router = APIRouter()

# Dog API

@router.get("/", response_model=List[dog.Dog], tags=["Dogs"])
def list_dogs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    dogs_get = dogs.get_all(db=db, skip=skip, limit=limit)
    return dogs_get

@router.get("/is_adopted", response_model=List[dog.Dog], tags=["Dogs"])
def list_dogs_adopted(
                    db: Session = Depends(get_db),
                    skip: int = 0,
                    limit: int = 100) -> Any:
    list_dogs = dogs.get_adopted(db=db, skip=skip, limit=limit)
    return list_dogs


@router.get(
        "/{name}", response_model=dog.Dog,
        responses={HTTP_404_NOT_FOUND: {"model": dog.HTTPError}},
        tags=["Dogs"])
def get_dog(*, db: Session = Depends(get_db), name: str) -> Any:
    data_dog = dogs.get_name(db=db, name=name)
    if not data_dog:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Dog not found")
    return data_dog


@router.post(
        "/{user_email}/",
        response_model=dog.Dog,
        status_code=HTTP_201_CREATED,
        tags=["Dogs"])
def create_dog_for_user(
                        *,
                        db: Session = Depends(get_db),
                        dog_obj: dog.DogCreate,
                        email: str,
                        current_user: auth.UserAuthBase = Depends(functions.get_current_user)) -> Any:
    data_user = users.get_email(db=db, email=email)
    if not data_user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    id = data_user.id
    dog = dogs.create_dog_user(db=db, obj_in=dog_obj, id=id)
    return dog


@router.put(
        "/{name}", response_model=dog.Dog,
        responses={HTTP_404_NOT_FOUND: {"model": dog.HTTPError}},
        tags=["Dogs"])
def update_dog(
                *, db: Session = Depends(get_db),
                name: str,
                dog_obj: dog.DogUpdate,
                current_user: auth.UserAuthBase = Depends(functions.get_current_user)) -> Any:
    data_dog = dogs.get_name(db=db, name=name)
    if not data_dog:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Dog not found")
    data_dog = dogs.update(db=db, db_obj=data_dog, obj_in=dog_obj)
    return data_dog


@router.delete("/{name}", response_model=dog.Dog,
            responses={HTTP_404_NOT_FOUND: {"model": dog.HTTPError}},
            tags=["Dogs"])
def delete_dogs(*, db: Session = Depends(get_db), name: str) -> Any:
    data_dog = dogs.get_name(db=db, name=name)
    if not data_dog:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Dog not found")
    data_dog = dogs.remove(db=db, name=name)
    return data_dog