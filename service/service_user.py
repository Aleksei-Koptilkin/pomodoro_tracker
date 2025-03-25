from dataclasses import dataclass

from schema import UserLoginSchema


@dataclass
class UserService:
    user_repository = UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(username, password)
        return UserLoginSchema(id=user.id, access_token=user.access_token)