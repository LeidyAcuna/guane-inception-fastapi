from typing import Optional, List

from pydantic import UUID4, BaseModel
from .dog  import Dog

class HTTPError(BaseModel):
    detail: str


# User schema
# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    lastname: str
    email: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: Optional[UUID4] = None
    dogs: List[Dog] = []

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass