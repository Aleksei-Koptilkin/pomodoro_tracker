from repository import TaskRepository, CacheRepository
from database import get_db_session
from cache import get_redis_connection
from service import TaskService


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)


def get_cache_repository() -> CacheRepository:
    cache_connection = get_redis_connection()
    return CacheRepository(cache_connection)


def get_task_service() -> TaskService:
    task_repository = get_task_repository()
    cache_repository = get_cache_repository()
    return TaskService(task_repository, cache_repository)