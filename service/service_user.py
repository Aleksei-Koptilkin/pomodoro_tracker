import string
from dataclasses import dataclass
from random import choice

from sqlalchemy.ext.asyncio import AsyncSession

from schema import UserLoginSchema, UserCreateSchema
from repository import UserRepository
from service.service_auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, user_schema: UserCreateSchema, session: AsyncSession) -> UserLoginSchema:
        user = await self.user_repository.create_user(user_schema, session)
        access_token = self.auth_service.get_user_access_token(user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)
