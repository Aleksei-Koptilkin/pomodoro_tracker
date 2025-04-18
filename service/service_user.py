import string
from dataclasses import dataclass
from random import choice


from schema import UserLoginSchema
from repository import UserRepository
from service.service_auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username=username, password=password)
        access_token = self.auth_service.get_user_access_token(user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)
