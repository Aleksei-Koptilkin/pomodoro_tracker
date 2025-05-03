from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserProfile
from schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(
            self,
            user_create_schema: UserCreateSchema
    ) -> UserProfile:

        query = insert(UserProfile).values(
            username=user_create_schema.username,
            password=user_create_schema.password,
            email=user_create_schema.email,
            given_name=user_create_schema.given_name,
            family_name=user_create_schema.family_name,
        ).returning(UserProfile.id)

        user_id = (await self.db_session.execute(query)).scalar()
        await self.db_session.commit()
        return await self.get_user(user_id)

    async def get_user(self, id: int) -> UserProfile:
        query = select(UserProfile).where(UserProfile.id == id)
        user = (await self.db_session.execute(query)).scalar_one_or_none()
        return user

    async def get_user_by_username(self, username: str) -> UserProfile:
        query = select(UserProfile).where(UserProfile.username == username)
        return (await self.db_session.execute(query)).scalar_one_or_none()

    async def get_client_user(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        return (await self.db_session.execute(query)).scalar_one_or_none()
