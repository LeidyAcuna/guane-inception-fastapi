from typing import Optional, List

from pydantic import UUID4, BaseModel


class HTTPError(BaseModel):
    detail: str


# Auth Model
class UserAuthBase(BaseModel):
    username: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    disabled: Optional[bool] = None


class UserAuthInDB(UserAuthBase):
    hashed_password: str


# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None