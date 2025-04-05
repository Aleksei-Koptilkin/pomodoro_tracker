from dataclasses import dataclass
import datetime

from jose import jwt

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
        access_token = self.get_user_access_token(user.id)
        return UserLoginSchema(id=user.id, access_token=access_token)

    def get_user_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expires_date_unix}, 'secret', algorithm='HS256')
        return token
