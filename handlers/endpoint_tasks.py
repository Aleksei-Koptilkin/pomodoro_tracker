from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from exception import NoTasksForUserException, TaskNotFoundException, NoTasksThisCategoryException
from schema import TaskSchema, CreateTaskSchema
from repository import TaskRepository, CacheRepository
from dependency import get_task_repository, get_task_service, get_request_user_id
from service import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[TaskSchema])
async def tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
        ) -> list[TaskSchema]:
    try:
        return await task_service.get_tasks(user_id, session)
    except NoTasksForUserException as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=e.detail
        )


@router.post("/", response_model=TaskSchema)
async def create_task(
        task: CreateTaskSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    return await task_service.create_task(task, user_id, session)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task_name(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        return await task_service.update_task_name(task_id, name, user_id, session)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        await task_service.delete_task(task_id, user_id, session)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        return await task_service.get_task(task_id, user_id, session)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.get("/tasks/category/{category_id}", response_model=list[TaskSchema])
async def get_tasks_by_category(
        category_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        return await task_service.get_tasks_by_category(category_id, user_id, session)
    except NoTasksThisCategoryException as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=e.detail
        )


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
        task: TaskSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id),
        session: AsyncSession = Depends(get_db_session)
    ):
    try:
        return await task_service.update_task(task, user_id, session)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )