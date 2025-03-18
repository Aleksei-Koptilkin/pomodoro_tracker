import json

from redis import Redis
from schema import TaskSchema


class CacheRepository:

    def __init__(self, redis_connection: Redis):
        self.redis_connection = redis_connection

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis_connection as redis:
            tasks_json = redis.lrange('tasks', 0, -1)
            tasks_pydantic_model = [TaskSchema.model_validate(json.loads(task_json)) for task_json in tasks_json]
            return tasks_pydantic_model

    def set_tasks(self, tasks: list[TaskSchema], ttl: int | None = None) -> None:
        tasks_json = [task.json() for task in tasks]
        with self.redis_connection as redis:
            redis.lpush('tasks', *tasks_json)
            if ttl:
                redis.expire('tasks', ttl)
