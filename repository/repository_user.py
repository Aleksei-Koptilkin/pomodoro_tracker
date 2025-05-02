from dataclasses import dataclass
from typing import AsyncGenerator

from fastapi.params import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserProfile, get_db_session
from schema import UserCreateSchema


@dataclass
class UserRepository:

    async def create_user(
            self,
            user_create_schema: UserCreateSchema,
            session: AsyncSession
    ) -> UserProfile:

        query = insert(UserProfile).values(
            username=user_create_schema.username,
            password=user_create_schema.password,
            email=user_create_schema.email,
            given_name=user_create_schema.given_name,
            family_name=user_create_schema.family_name,
        ).returning(UserProfile.id)

        async with session:
            user_id = (await session.execute(query)).scalar()
            print(user_id)
            await session.commit()
            return await self.get_user(user_id, session)

    async def get_user(self, id: int, session: AsyncSession) -> UserProfile:
        query = select(UserProfile).where(UserProfile.id == id)
        async with session:
            print(session)
            user = (await session.execute(query)).scalar_one_or_none()
            return user

    async def get_user_by_username(self, username: str, session: AsyncSession) -> UserProfile:
        query = select(UserProfile).where(UserProfile.username == username)
        async with session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_client_user(self, email: str, session: AsyncSession) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with session:
            return (await session.execute(query)).scalar_one_or_none()
