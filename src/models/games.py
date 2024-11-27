import datetime
from enum import StrEnum
from typing import List, Optional

from sqlmodel import Field, Relationship

from . import ModelBase


class GameName(StrEnum):
    RESULT_KEEPER = "Result Keeper"


class GameLevel(ModelBase, table=True):
    __tablename__ = "game_level"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    game_name: GameName
    level: int = Field(default=1)
    user: "User" = Relationship(back_populates="game_levels")  # noqa: F821
    game_sessions: List["GameSession"] = Relationship(back_populates="game_level")


class GameSession(ModelBase, table=True):
    __tablename__ = "game_session"

    id: Optional[int] = Field(default=None, primary_key=True)
    game_level_id: int = Field(foreign_key="game_level.id")
    finished: datetime.datetime = Field(default_factory=datetime.datetime.now)
    started_level: int
    finished_level: int
    points_earned: int
    duration: Optional[int] = Field(default=None)
    game_level: "GameLevel" = Relationship(back_populates="game_sessions")
