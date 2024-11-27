from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db.sqlite"


def engine(database_url: str = DATABASE_URL) -> Engine:
    engine = create_engine(database_url, echo=True)
    return engine


def session(engine: Engine) -> sessionmaker:
    Session = sessionmaker(bind=engine)
    return Session()
