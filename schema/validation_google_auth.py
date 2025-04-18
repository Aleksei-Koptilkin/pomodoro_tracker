from typing import Optional

from pydantic import BaseModel


class GoogleUserData(BaseModel):
    email: str
    name: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
