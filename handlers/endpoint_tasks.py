from typing import Annotated
from fastapi import APIRouter, status, Depends
from schema.validation_tasks import TaskSchema
from repository import TaskRepository
from dependency import get_task_repository


router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def tasks(task_repository: Annotated[TaskRepository, Depends(get_task_repository)]):
    result = task_repository.get_tasks()
    return result


@router.post("/", response_model=TaskSchema)
async def create_task(
        task: TaskSchema,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
    ):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task_name(
        task_id: int,
        name: str,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
    ):
    task = task_repository.update_task_name(task_id, name)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
    ):
    task_repository.delete_task(task_id)
    return {"message": "task deleted"}


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
    ):
    task = task_repository.get_task(task_id)
    return task

@router.get("/tasks/categories/{categories_id}", response_model=list[TaskSchema])
async def get_tasks_by_categories(
        categories_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
    ):
    result = task_repository.get_task_by_categories(categories_id)
    return result
