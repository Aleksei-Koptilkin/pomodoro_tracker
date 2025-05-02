from dataclasses import dataclass
import httpx

from schema import YandexUserData
from settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> YandexUserData:
        access_token = await self.get_user_access_token(code=code)
        user_info = await self.async_client.get(
                'https://login.yandex.ru/info?',
                headers={'Authorization': f'Oauth {access_token}'}
        )
        await self.async_client.aclose()
        return YandexUserData(**user_info.json())

    async def get_user_access_token(self, code: str) -> str:
        data ={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET
        }
        response = await self.async_client.post(self.settings.YANDEX_TOKEN_URI, data=data)
        return response.json()['access_token']
