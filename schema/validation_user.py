from typing import Optional

from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None