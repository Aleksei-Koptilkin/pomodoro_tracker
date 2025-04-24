from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from database import UserProfile
from schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, user_create_schema: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            username=user_create_schema.username,
            password=user_create_schema.password,
            email=user_create_schema.email,
            given_name=user_create_schema.given_name,
            family_name=user_create_schema.family_name,
        ).returning(UserProfile.id)
        with self.db_session as session:
            user_id = session.execute(query).scalar()
            session.commit()
        return self.get_user(user_id)

    def get_user(self, id: int) -> UserProfile:
        query = select(UserProfile).where(UserProfile.id == id)
        with self. db_session as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()

    def get_client_user(self, email):
        query = select(UserProfile).where(UserProfile.email == email)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()
