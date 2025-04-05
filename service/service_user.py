import string
from dataclasses import dataclass
from random import choice


from schema import UserLoginSchema
from repository import UserRepository


@dataclass
class UserService:
    user_repository: UserRepository

    def create_user(self, username: str, password: str) -> UserLoginSchema:
        access_token = self.get_user_access_token()
        user = self.user_repository.create_user(username=username, password=password, access_token=access_token)
        return UserLoginSchema(id=user.id, access_token=user.access_token)

    @staticmethod
    def get_user_access_token():
        return ''.join(choice(string.ascii_uppercase + string.digits) for i in range(10))
