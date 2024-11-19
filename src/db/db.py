from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..models import ModelBase

DATABASE_URL = "sqlite:///db.sqlite"


def engine(database_url=DATABASE_URL):
    engine = create_engine(database_url, echo=True)
    ModelBase.metadata.create_all(engine)
    return engine


def session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
