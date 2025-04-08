import json

from redis import Redis
from schema import TaskSchema


class CacheRepository:

    def __init__(self, redis_connection: Redis):
        self.redis_connection = redis_connection

    def get_tasks(self, key_name: str) -> list[TaskSchema]:
        with self.redis_connection as redis:
            tasks_json = redis.lrange(key_name, 0, -1)
            tasks_pydantic_model = [TaskSchema.model_validate(json.loads(task_json)) for task_json in tasks_json]
            return tasks_pydantic_model

    def set_tasks(
            self,
            tasks: list[TaskSchema],
            key_name: str,
            ttl: int | None = None
        ) -> None:
        tasks_json = [task.json() for task in tasks]
        with self.redis_connection as redis:
            redis.lpush(key_name, *tasks_json)
            if ttl:
                redis.expire(key_name, ttl)
