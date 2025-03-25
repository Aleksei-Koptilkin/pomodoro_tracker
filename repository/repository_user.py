from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from database import UserProfile


@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, username: str, password: str, access_token: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password,
            access_token=access_token,
        ).returning(UserProfile.id)
        with self.db_session as session:
            user_id = session.execute(query).scalar()
            session.commit()
        return self.get_user(user_id)

    def get_user(self, id: int) -> UserProfile:
        query = select(UserProfile).where(UserProfile.id == id)
        with self. db_session as session:
            return session.execute(query).scalar_one_or_none()
