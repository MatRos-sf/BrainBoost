from sqlalchemy import Engine, create_engine, update
from sqlalchemy.orm import sessionmaker

from src.models.enum_types import GameName, PointsCategory

from ..models.games import AssociativeChangingModel, ResultKeeperModel
from ..models.user import PointsModel, User
from ..user.session import hash_password

DATABASE_URL = "sqlite:///db.sqlite"


def engine(database_url: str = DATABASE_URL) -> Engine:
    engine = create_engine(database_url, echo=True)
    return engine


class DBManager:
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = engine(database_url)
        self.session = sessionmaker(bind=self.engine)()

    def find_record(self, model, **kwargs):
        return self.session.query(model).filter_by(**kwargs).first()

    def add_record(self, model, **kwargs):
        record = model(**kwargs)
        self.session.add(record)
        self.session.commit()

    def update_record(self, model, id: int, fields: dict):
        stmt = update(model).where(model.id == id).values(**fields)
        self.session.execute(stmt)
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def create_account(self, username: str, password: str):
        # Hash the password
        password = hash_password(password)
        try:
            # First create and commit the user
            user = User(username=username, password=password)
            self.session.add(user)
            self.session.commit()

            # Now create game levels with the user's ID
            for game in GameName:
                self.init_game(user.id, game)

            return self.find_record(User, username=username, id=user.id)
        except:
            self.session.rollback()
            raise

    def add_points_for_game(self, user_id: int, point: int, category: PointsCategory):
        self.add_record(
            PointsModel, user_id=user_id, point=point, category=category.value[0]
        )

    def add_points_for_first_game(self, user_id: int, category: PointsCategory):
        self.add_record(
            PointsModel,
            user_id=user_id,
            point=category.value[1],
            category=category.value[0],
        )

    def init_game(self, user_id, game_name: str):
        match game_name:
            case GameName.RESULT_KEEPER:
                self.add_record(ResultKeeperModel, user_id=user_id, game_name=game_name)
            case GameName.ASSOCIATIVE_CHANGING:
                self.add_record(
                    AssociativeChangingModel, user_id=user_id, game_name=game_name
                )
            case _:
                raise ValueError("Invalid game name. Please implement new case!")
