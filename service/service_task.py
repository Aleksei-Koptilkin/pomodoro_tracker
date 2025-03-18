from dataclasses import dataclass

from database import Tasks
from repository import TaskRepository, CacheRepository
from schema import TaskSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    cache_repository: CacheRepository

    def get_tasks(self) -> list[TaskSchema]:
        tasks_cache = self.cache_repository.get_tasks()
        if tasks_cache:
            return tasks_cache
        else:
            tasks_bd_model = self.task_repository.get_tasks()
            tasks_pydantic_model = [TaskSchema.model_validate(task) for task in tasks_bd_model]
            self.cache_repository.set_tasks(tasks_pydantic_model, ttl=60)
            return tasks_pydantic_model

    def create_task(self, task: TaskSchema) -> TaskSchema:
        task_id = self.task_repository.create_task(task)
        task.id = task_id
        return task

    def get_task(self, task_id: int) -> Tasks:
        return self.task_repository.get_task(task_id)

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        return self.task_repository.update_task_name(task_id, name)

    def delete_task(self, task_id: int) -> dict[str, str]:
        self.task_repository.delete_task(task_id)
        return {'message':'task deleted'}

    def get_tasks_by_category(self, category_id: int) -> list[Tasks]:
        return self.task_repository.get_tasks_by_category(category_id)

    def update_task(
            self,
            task_id: int,
            name: str,
            pomodoro_count: int,
            categories_id: int
        ):
        return self.task_repository.update_task(task_id, name, pomodoro_count, categories_id)

