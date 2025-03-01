from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    pomodoro_count: int
    categories_id: int
