from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from settings import Settings


settings = Settings()
db_url = settings.db_url


engine = create_engine(db_url)


Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session()
