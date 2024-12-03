from dataclasses import dataclass
from typing import Dict, List

from src.exceptions.database_exceptions import UserNotFoundException

from ..models.games import GameLevel, GameName
from ..models.user import User
from .db import DATABASE_URL, DBManager


@dataclass
class GameStatistic:
    id: int
    game: GameName
    level: int


@dataclass
class UserSession:
    id: int
    username: str
    points: int
    stats: List[GameStatistic]

    @classmethod
    def parse_data(cls, data):
        games = [
            GameStatistic(id=game.id, game=game.game_name, level=game.level)
            for game in data.game_levels
        ]
        return cls(id=data.id, username=data.username, points=data.points, stats=games)


class GameManager:
    def __init__(self, database_url=DATABASE_URL):
        self.db = DBManager(database_url)
        self._current_session = None

    @property
    def current_session(self):
        return self._current_session

    @current_session.setter
    def current_session(self, value: UserSession):
        if not isinstance(value, UserSession):
            raise ValueError("current_session must be a UserSession object")
        self._current_session = value

    @current_session.deleter
    def current_session(self) -> None:
        self._current_session = None

    def update_session(self, attributes: Dict[str, str | int]) -> None:
        """
        Update the current session with the provided attributes.
        When the attribute is not a attribute of UserSession raise a ValueError
        """
        user_session_attributes = UserSession.__annotations__.keys()
        for key, value in attributes.items():
            if key in user_session_attributes:
                setattr(self.current_session, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

    def _check_games(self, user: User):
        """
        Method check whether all games are existing in the user session. If some games are not exists then create
        a new record with that game.
        """
        if len(user.game_levels) < len(GameName):
            for game in GameName:
                if len(list(filter(lambda x: x.game == game, user.game_levels))) == 0:
                    self.db.add_record(
                        GameLevel, user_id=user.id, game_name=game, level=1
                    )
            user = self.db.find_record(User, id=user.id)
        return user

    def load_session(self, user_id) -> None:
        """
        Method captures the user with the specified 'user_id' from the database and then checks whether all games exist.
        Assigns the 'current_session' to user when user exist.
        """
        user = self.db.find_record(User, id=user_id)
        if user:
            # check if all game exists
            user = self._check_games(user)
        else:
            raise UserNotFoundException(user_id)
        self.current_session = UserSession.parse_data(user)
