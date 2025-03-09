from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from database import Tasks, Categories, get_db_session
from schema import TaskSchema


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session as session:
            task = session.execute(select(Tasks).where(Tasks.id == task_id)).scalar_one_or_none()
        return task

    def get_tasks(self) -> list[Tasks]:
        with self.db_session as session:
            tasks = session.execute(select(Tasks)).scalars().all()
        return tasks

    def create_task(self, task: TaskSchema) -> int:
        task_model = Tasks(name=task.name, pomodoro_count=task.pomodoro_count, categories_id=task.categories_id)
        with self.db_session as session:
            session.add(task_model)
            session.commit()
            return task_model.id

    def delete_task(self, task_id: int) -> None:
        with self.db_session as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id))
            session.commit()

    def get_task_by_categories(self, categories_id: int) -> list[Tasks]:
        query = (select(Tasks).join(Categories, Tasks.categories_id == Categories.id)
                 .where(Categories.id == categories_id))
        with self.db_session as session:
            tasks_by_categories = session.execute(query).scalars().all()
        return tasks_by_categories

    def update_task_name(self, task_id: int, name: str) -> TaskSchema:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        with self.db_session as session:
            task_id = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
