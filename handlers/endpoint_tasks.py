from fastapi import APIRouter, status
from schema.validation_tasks import Task
from database import get_db_connect


router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=list[Task])
async def tasks():
    result: list[Task] = []
    cursor = get_db_connect().cursor()
    lst_tasks = cursor.execute("SELECT id, name, pomodoro_count, categories_id from Tasks").fetchall()
    for task in lst_tasks:
        result.append(Task(
            id=task[0],
            name=task[1],
            pomodoro_count=task[2],
            categories_id=task[3]
        ))
    return result


@router.post("/", response_model=Task)
async def create_task(task: Task):
    connect = get_db_connect()
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Tasks (name, pomodoro_count, categories_id) VALUES (?,?,?);",
                   (task.name, task.pomodoro_count, task.categories_id))
    connect.commit()
    connect.close()
    return task


@router.patch("/{task_id}")
async def update_task(task_id: int, name: str, pomodoro_count: int, categories_id):
    connect = get_db_connect()
    cursor = connect.cursor()
    cursor.execute("UPDATE Tasks SET name = ?, pomodoro_count = ?, categories_id = ? WHERE id = ?;",
                   (name, pomodoro_count, categories_id, task_id))
    connect.commit()
    task = cursor.execute("SELECT id, name, pomodoro_count, categories_id FROM Tasks WHERE id = ?;",
                          (task_id,)).fetchall()[0]
    connect.close()

    return Task(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        categories_id=task[3]
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    connect = get_db_connect()
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Tasks WHERE id = ?;", (task_id,))
    connect.commit()
    connect.close()
    return {"message": "task deleted"}


@router.get("/{task_id}")
async def get_task(task_id: int):
    cursor = get_db_connect().cursor()
    task = cursor.execute("SELECT id, name, pomodoro_count, categories_id FROM Tasks WHERE id = ?;",
                          (task_id,)).fetchall()[0]

    return Task(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        categories_id=task[3]
    )
