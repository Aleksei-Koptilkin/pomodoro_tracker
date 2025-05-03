from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.model import Base
from database.models.user import UserProfile


class Tasks(Base):
    __tablename__ = 'Tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)


class Category(Base):
    __tablename__ = 'Category'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
