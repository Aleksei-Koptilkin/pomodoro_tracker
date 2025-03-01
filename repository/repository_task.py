from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from database import Tasks, Categories, get_db_session


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

    def create_task(self, task: Tasks) -> None:
        with self.db_session as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        with self.db_session as session:
            session.execute(delete(Tasks).where(Tasks.id == task_id))
            session.commit()

    def get_task_by_categories(self, categories_id: str) -> list[Tasks]:
        query = (select(Tasks).join(Categories, Tasks.categories_id == Categories.id)
                 .where(Categories.name == categories_id))
        with self.db_session as session:
            tasks_by_categories = session.execute(query).scalars().all()
        return tasks_by_categories


def get_task_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)
