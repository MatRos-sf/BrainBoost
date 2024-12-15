import datetime
from enum import StrEnum
from typing import List, Optional

from sqlmodel import Field, Relationship

from . import ModelBase


class GameName(StrEnum):
    RESULT_KEEPER = "Result Keeper"


class ResultKeeperModel(ModelBase, table=True):
    __tablename__ = "result_keeper_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    user: "User" = Relationship(back_populates="result_keeper")  # noqa: F821
    game_name: GameName
    level: int = Field(default=None, nullable=True)
    result_keeper_session: List["ResultKeeperSessionModel"] = Relationship(
        back_populates="result_keeper"
    )


class ResultKeeperSessionModel(ModelBase, table=True):
    __tablename__ = "result_keeper_session_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    result_keeper_id: int = Field(foreign_key="result_keeper_table.id")
    result_keeper: ResultKeeperModel = Relationship(
        back_populates="result_keeper_session"
    )

    # stats
    range_min: int = Field(default=0)
    range_max: int
    points_earned: int
    started_level: int
    finished_level: int
    duration: int = Field(default=60)  # here implemented
    finished_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    steps: int
    wrong_answers: int
    correct_answers: int
