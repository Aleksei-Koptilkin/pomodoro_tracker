from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "postgresql+psycopg2://postgres:password@localhost:5432/pomodoro"


engine = create_engine(db_url)


Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session()
