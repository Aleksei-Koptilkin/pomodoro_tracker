from dataclasses import dataclass
import httpx

from schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self.get_user_access_token(code=code)
        user_info = await self.async_client.get('https://www.googleapis.com/oauth2/v1/userinfo',
                          headers={'Authorization': f'Bearer {access_token}'})
        await self.async_client.aclose()
        return GoogleUserData(**user_info.json())

    async def get_user_access_token(self, code: str) -> dict:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = await self.async_client.post(self.settings.GOOGLE_TOKEN_URL, data=data)
        response_json = response.json()
        return response_json['access_token']