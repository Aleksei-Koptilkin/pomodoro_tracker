import json

from redis.asyncio.client import  Redis
from schema import TaskSchema


class CacheRepository:

    def __init__(self, redis_connection: Redis):
        self.redis_connection = redis_connection

    async def get_tasks(self, key_name: str) -> list[TaskSchema]:
        async with self.redis_connection as redis:
            tasks_json = await redis.lrange(key_name, 0, -1)
            tasks_pydantic_model = [TaskSchema.model_validate(json.loads(task_json)) for task_json in tasks_json]
            return tasks_pydantic_model

    async def set_tasks(
            self,
            tasks: list[TaskSchema],
            key_name: str,
            ttl: int | None = None
        ) -> None:
        tasks_json = [task.model_dump_json() for task in tasks]
        async with self.redis_connection as redis:
            await redis.lpush(key_name, *tasks_json)
            if ttl:
                await redis.expire(key_name, ttl)
