from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


@dataclass
class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
