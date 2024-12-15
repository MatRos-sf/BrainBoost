from dataclasses import dataclass
from typing import Dict, Optional

from src.exceptions.database_exceptions import UserNotFoundException

from ..models.games import GameName, ResultKeeperModel
from ..models.user import User
from .db import DATABASE_URL, DBManager


@dataclass
class GameStatistic:
    id: int
    game: GameName
    level: Optional[int]


@dataclass
class UserSession:
    id: int
    username: str
    point: int
    stats: Dict[GameName, GameStatistic]


class GameManager:
    NAME_GAME = None

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

    def get_level_game(self, game_name: GameName) -> Optional[int]:
        if not self.current_session:
            raise ValueError("No current session set")

        game_stats = self.current_session.stats.get(game_name.value)
        return game_stats.level

    def update_point(self, point) -> None:
        """
        Update the current session with the provided attributes.
        When the attribute is not an attribute of UserSession raise a ValueError
        """
        self.current_session.point += point

    def update_level_of_game(self, game_name: GameName, level: int):
        """
        Update the level of game in the current session with the provided attributes.
        When the attribute is not an attribute of GameLevel raise a ValueError
        """
        game_stats = self.current_session.stats.get(game_name.value)
        if not game_stats:
            raise ValueError(f"Game {game_name}not found in current session")

        game_stats.level = level
        self.current_session.stats[game_name.value] = game_stats

    def _check_games(self, user: User) -> Dict[str, GameStatistic]:
        """
        Method check whether all games are existing in the user session. If some games are not exists then create
        a new record with that game.
        """
        stats = {}
        for game in GameName:
            name_game = game.lower().replace(" ", "_")
            game_stat: Optional[ResultKeeperModel] = getattr(user, name_game)
            if game_stat:
                stats[game.value] = GameStatistic(
                    id=game_stat.id, game=game.value, level=game_stat.level
                )
            else:
                stats[game.value] = GameStatistic(id=None, game=game.value, level=None)
        return stats

    def load_session(self, user_id) -> None:
        """
        Method captures the user with the specified 'user_id' from the database and then checks whether all games exist.
        Assigns the 'current_session' to user when user exist.
        """
        user = self.db.find_record(User, id=user_id)
        if user:
            # check if all game exists
            games = self._check_games(user)
        else:
            raise UserNotFoundException(user_id)
        self.current_session = UserSession(
            id=user.id, username=user.username, point=user.point, stats=games
        )
