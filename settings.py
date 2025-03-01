from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite3_db_name: str = "pomodoro_db"
