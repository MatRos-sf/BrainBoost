from typing import NamedTuple


class UserSession(NamedTuple):
    id: int
    username: str
    points: int
