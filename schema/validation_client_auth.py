from typing import Optional

from pydantic import BaseModel


class GoogleUserData(BaseModel):
    email: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None


class YandexUserData(BaseModel):
    default_email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
