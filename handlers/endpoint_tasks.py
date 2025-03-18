from typing import Annotated

from fastapi import APIRouter, status, Depends

from schema import TaskSchema
from repository import TaskRepository, CacheRepository
from dependency import get_task_repository, get_task_service
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
        ) -> list[TaskSchema]:
    return task_service.get_tasks()


@router.post("/", response_model=TaskSchema)
async def create_task(
        task: TaskSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.create_task(task)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task_name(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.update_task_name(task_id, name)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    task_service.delete_task(task_id)
    return {"message": "task deleted"}


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.get_task(task_id)


@router.get("/tasks/categories/{categories_id}", response_model=list[TaskSchema])
async def get_tasks_by_category(
        category_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.get_tasks_by_category(category_id)


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
        task_id: int,
        name: str,
        pomodoro_count: int,
        categories_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)]
    ):
    return task_service.update_task(task_id, name, pomodoro_count, categories_id)
