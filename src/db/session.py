from typing import NamedTuple

from .db import DATABASE_URL, DBManager


class UserSession(NamedTuple):
    id: int
    username: str
    points: int


class GameManager:
    def __init__(self, database_url=DATABASE_URL):
        self.db = DBManager(database_url)
        self.current_session = None
