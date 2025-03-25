from dataclasses import dataclass

from schema import UserLoginSchema


@dataclass
class AuthService:
    auth_repository = AuthRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        pass