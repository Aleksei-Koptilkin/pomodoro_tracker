from  typing import Optional
from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: Optional[int] = None
    name: str
    pomodoro_count: int
    categories_id: int


    class Config:
        from_attributes = True