from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database import Tasks
from exception import TaskNotFoundException, NoTasksThisCategoryException, NoTasksForUserException
from repository import TaskRepository, CacheRepository
from schema import TaskSchema, CreateTaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_repository: CacheRepository

    async def get_tasks(self, user_id: int, session: AsyncSession) -> list[TaskSchema]:
        tasks_cache = await self.cache_repository.get_tasks(key_name=f'tasks_for_user_{user_id}')
        if tasks_cache:
            return tasks_cache
        else:
            tasks_bd_model = await self.task_repository.get_tasks(user_id, session)
            if not tasks_bd_model:
                raise NoTasksForUserException
            tasks_pydantic_model = [TaskSchema.model_validate(task) for task in tasks_bd_model]
            await self.cache_repository.set_tasks(tasks_pydantic_model, key_name=f'tasks_for_user_{user_id}', ttl=60)
            return tasks_pydantic_model

    async def create_task(self, task: CreateTaskSchema, user_id: int, session: AsyncSession) -> TaskSchema:
        task_id = await self.task_repository.create_task(task, user_id, session)
        task_schema = await self.get_task(task_id, user_id, session)
        return TaskSchema.model_validate(task_schema)

    async def get_task(self, task_id: int, user_id, session: AsyncSession) -> TaskSchema:
        task = await self.task_repository.get_task(task_id, user_id, session)
        if not task:
            raise TaskNotFoundException
        return TaskSchema.model_validate(task)

    async def update_task_name(self, task_id: int, name: str, user_id: int, session: AsyncSession) -> Tasks:
        await self.get_task(task_id, user_id, session)
        return await self.task_repository.update_task_name(task_id, name, user_id, session)

    async def delete_task(self, task_id: int, user_id, session: AsyncSession) -> None:
        await self.get_task(task_id, user_id, session)
        await self.task_repository.delete_task(task_id, user_id, session)

    async def get_tasks_by_category(self, category_id: int, user_id: int, session: AsyncSession) -> list[TaskSchema]:
        tasks_by_category_cache = await self.cache_repository.get_tasks(f'tasks_by_category{category_id}_for_user_{user_id}')
        if tasks_by_category_cache:
            return tasks_by_category_cache
        else:
            tasks_by_category_model = await self.task_repository.get_tasks_by_category(category_id, user_id, session)
            if not tasks_by_category_model:
                raise NoTasksThisCategoryException
            tasks_by_category_schema = [TaskSchema.model_validate(task_model)
                                        for task_model in tasks_by_category_model]
            await self.cache_repository.set_tasks(tasks_by_category_schema,
                                            key_name=f'tasks_by_category{category_id}_for_user_{user_id}', ttl=90)
            return tasks_by_category_schema

    async def update_task(
            self,
            task: TaskSchema,
            user_id: int,
            session: AsyncSession
        ):
        await self.get_task(task.id, user_id, session)
        return await self.task_repository.update_task(task, user_id, session)
