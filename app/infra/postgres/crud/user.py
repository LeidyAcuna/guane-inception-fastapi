from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.schemas import user
from app.infra.postgres.models.base import Base
from app.infra.postgres.models.user import User

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# CRUD Users
class BaseActionsUsers(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):

        self.model = model

    def get_all(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_email(self, db: Session, email: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.email == email).first()

    def create(self, db: Session, *, obj_in: user.UserCreate) -> ModelType:
        user_obj = user.UserInDBBase(
                                        name=obj_in.name,
                                        lastname=obj_in.lastname,
                                        email=obj_in.email)
        user_data = jsonable_encoder(user_obj)
        db_obj = self.model(**user_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, email: str) -> ModelType:
        user_delete = db.query(self.model).filter(self.model.email == email).first()
        obj = db.query(self.model).get(user_delete.id)
        db.delete(obj)
        db.commit()
        return obj


class UserActions(BaseActionsUsers[User, user.UserCreate, user.UserUpdate]):
    """Users actions with CRUD operations"""

    pass


users = UserActions(User)