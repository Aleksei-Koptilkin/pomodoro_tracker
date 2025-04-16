import redis
from fastapi import Depends, Request, security, Security, HTTPException
from sqlalchemy.orm import Session

from client import GoogleClient
from exception import TokenExpiredException, TokenNotCorrectException
from repository import TaskRepository, CacheRepository, UserRepository
from database import get_db_session
from cache import get_redis_connection
from service import TaskService, UserService, AuthService
from settings import Settings


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session=db_session)


def get_cache_repository() -> CacheRepository:
    redis_connection = get_redis_connection()
    return CacheRepository(redis_connection=redis_connection)


def get_task_service() -> TaskService:
    task_repository = get_task_repository()
    cache_repository = get_cache_repository()
    return TaskService(task_repository, cache_repository)


def get_user_repository() -> UserRepository:
    db_session = get_db_session()
    return UserRepository(db_session=db_session)


def get_auth_service() -> AuthService:
    user_repository = get_user_repository()
    google_client = get_google_client()
    settings = Settings()
    return AuthService(
        user_repository=user_repository,
        google_client=google_client,
        settings=settings,
    )


def get_user_service() -> UserService:
    user_repository = get_user_repository()
    return UserService(user_repository=user_repository, auth_service=get_auth_service())


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


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())
