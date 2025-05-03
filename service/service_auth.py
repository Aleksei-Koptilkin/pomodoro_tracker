from dataclasses import dataclass
import datetime

from jose import jwt, JWTError

from client import GoogleClient, YandexClient
from settings import Settings
from database import UserProfile
from exception import (UserNotFoundException, UserNotCorrectPasswordException,
                       TokenNotCorrectException, TokenExpiredException)
from repository import UserRepository
from schema import UserLoginSchema, UserCreateSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    google_client: GoogleClient
    yandex_client: YandexClient
    settings: Settings

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str) -> None:
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    async def login(
            self,
            username: str,
            password: str
    ) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username=username)
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

    async def google_auth(self, code: str):
        user_google_data = await self.google_client.get_user_info(code=code)

        if user:= await self.user_repository.get_client_user(email=user_google_data.email):
            access_token = self.get_user_access_token(user.id)
            return UserLoginSchema(id=user.id, access_token=access_token)

        user_create_schema = UserCreateSchema(
            email=user_google_data.email,
            given_name=user_google_data.given_name,
            family_name=user_google_data.family_name
        )
        created_user = await self.user_repository.create_user(user_create_schema)
        access_token = self.get_user_access_token(created_user.id)
        return UserLoginSchema(id=created_user.id, access_token=access_token)

    def yandex_redirect(self):
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_yandex_data = await self.yandex_client.get_user_info(code=code)
        if user:= await self.user_repository.get_client_user(email=user_yandex_data.default_email):
            access_token = self.get_user_access_token(user.id)
            return UserLoginSchema(id=user.id, access_token=access_token)
        else:
            user_create_schema = UserCreateSchema(
                email=user_yandex_data.default_email,
                given_name=user_yandex_data.first_name,
                family_name=user_yandex_data.last_name
            )
            created_user = await self.user_repository.create_user(user_create_schema)
            access_token = self.get_user_access_token(created_user.id)
            return UserLoginSchema(id=created_user.id, access_token=access_token)