from dataclasses import dataclass
from typing import Dict

from .db import DATABASE_URL, DBManager


@dataclass
class UserSession:
    id: int
    username: str
    points: int


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
    def current_session(self):
        self._current_session = None

    def update_session(self, attributes: Dict[str, str | int]):
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
