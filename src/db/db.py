from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db.sqlite"


def engine(database_url: str = DATABASE_URL) -> Engine:
    engine = create_engine(database_url, echo=True)
    return engine


def session(engine: Engine) -> sessionmaker:
    Session = sessionmaker(bind=engine)
    return Session()


class DBManager:
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = engine(database_url)
        self.session = session(self.engine)

    def find_record(self, model, **kwargs):
        if not kwargs:
            raise ValueError("No keyword arguments profide to find a record!")
        return self.session.query(model).filter_by(**kwargs).first()

    def add_record(self, model, **kwargs):
        model = model(**kwargs)
        self.session.add(model)
        self.session.commit()

    def update_record(self, model, id, fields: dict):
        self.session.query(model).filter_by(id=id).update(fields)
        self.session.commit()
