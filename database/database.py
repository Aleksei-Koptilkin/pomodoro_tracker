from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "sqlite:///pomodoro_db"


engine = create_engine(db_url)


Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session()
