import redis
import httpx

from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from client import GoogleClient, YandexClient
from exception import TokenExpiredException, TokenNotCorrectException
from repository import TaskRepository, CacheRepository, UserRepository
from database import get_db_session
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_task_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


def get_cache_repository(redis_connection: redis.Redis = Depends(get_redis_connection)) -> CacheRepository:
    return CacheRepository(redis_connection=redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
    cache_repository: CacheRepository = Depends(get_cache_repository)
    ) -> TaskService:
    return TaskService(task_repository, cache_repository)


async def get_user_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_settings() -> Settings:
    return Settings()


async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=httpx.AsyncClient())


async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings(), async_client=httpx.AsyncClient())



async def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client),
        settings: Settings = Depends(get_settings)
    ) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        settings=settings,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service)
    ) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
    ) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpiredException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
