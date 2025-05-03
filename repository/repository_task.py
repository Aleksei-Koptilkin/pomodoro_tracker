from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from database import Tasks, Category
from schema import TaskSchema, CreateTaskSchema


class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        task = (await self.db_session.execute(query)).scalar_one_or_none()
        return task

    async def get_tasks(self, user_id: int) -> list[Tasks]:
        tasks = (await self.db_session.execute(select(Tasks).where(Tasks.user_id == user_id))).scalars().all()
        return tasks

    async def create_task(self, task: CreateTaskSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        )
        self.db_session.add(task_model)
        await self.db_session.commit()
        return task_model.id

    async def delete_task(self, task_id: int, user_id: int) -> None:
        await self.db_session.execute(delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id))
        await self.db_session.commit()

    async def get_tasks_by_category(self, category_id: int, user_id: int) -> list[Tasks]:
        query = (select(Tasks).join(Category, Tasks.category_id == Category.id)
                 .where(Category.id == category_id, Tasks.user_id == user_id))
        tasks_by_category = (await self.db_session.execute(query)).scalars().all()
        return tasks_by_category

    async def update_task_name(self, task_id: int, name: str, user_id) -> Tasks:
        query = update(Tasks).where(
            Tasks.id == task_id,
            Tasks.user_id == user_id
        ).values(name=name).returning(Tasks.id)
        task_id = (await self.db_session.execute(query)).scalar_one_or_none()
        await self.db_session.commit()
        return await self.get_task(task_id, user_id)

    async def update_task(self, task: TaskSchema, user_id: int) -> Tasks:
        query = (update(Tasks).where(
            Tasks.id == task.id,
            Tasks.user_id == user_id
        ).values
            (
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id
        ))
        await self.db_session.execute(query)
        await self.db_session.commit()
        return await self.get_task(task.id, user_id)
