from dataclasses import dataclass
import datetime

from jose import jwt, JWTError

from client import GoogleClient
from settings import Settings
from database import UserProfile
from exception import (UserNotFoundException, UserNotCorrectPasswordException,
                       TokenNotCorrectException, TokenExpiredException)
from repository import UserRepository
from schema import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    google_client: GoogleClient
    settings: Settings

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
        token = jwt.encode(
            {'user_id': user_id, 'expire': expires_date_unix},
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ENCODE_ALGORITHM)
        return token

    def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
            if payload['expire'] < datetime.datetime.now().timestamp():
                raise TokenExpiredException
        except JWTError:
            raise TokenNotCorrectException
        return payload['user_id']

    def google_redirect(self):
        return self.settings.google_redirect_url

    def google_auth(self, code: str):
        user_google_data = self.google_client.get_user_info(code=code)
        print(user_google_data)
