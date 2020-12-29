from fastapi import APIRouter
from typing import Any, List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.infra.postgres.crud.dog import dogs
from app.schemas import dog
from app.infra.postgres.models.base import get_db

router = APIRouter()

# Dog API

@router.get("/", response_model=List[dog.Dog], tags=["Dogs"])
def list_dogs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    dogs_get = dogs.get_all(db=db, skip=skip, limit=limit)
    return dogs_get
