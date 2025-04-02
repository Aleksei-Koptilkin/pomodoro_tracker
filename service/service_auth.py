from dataclasses import dataclass

from database import UserProfile
from exception import UserNotFoundException, UserNotCorrectPasswordException
from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException


    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username=username)
        self._validate_auth_user(user=user, password=password)
        return UserLoginSchema(id=user.id, access_token=user.access_token)
