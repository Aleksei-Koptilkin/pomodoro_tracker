from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, mapped_collection

from database import Base


@dataclass
class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True)
    given_name: Mapped[str] = mapped_column(nullable=True)
    family_name: Mapped[str] = mapped_column(nullable=True)
