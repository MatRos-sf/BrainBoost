import datetime
from enum import StrEnum
from typing import List, Optional

from sqlalchemy import Enum as SQLEnum
from sqlmodel import Column, Field, Relationship

from . import ModelBase
from .enum_types import Language


class GameName(StrEnum):
    RESULT_KEEPER = "Result Keeper"
    ASSOCIATIVE_CHANGING = "Associative Changing"


class GameModel(ModelBase):
    __abstract__ = True
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")

    game_name: GameName
    level: int = Field(default=None, nullable=True)


class SessionModel(ModelBase):
    __abstract__ = True

    id: Optional[int] = Field(default=None, primary_key=True)
    points_earned: int
    started_level: int
    finished_level: int
    duration: int = Field(default=60)  # here implemented
    finished_datetime: datetime.datetime = Field(default_factory=datetime.datetime.now)
    wrong_answers: int
    correct_answers: int


class ResultKeeperModel(GameModel, table=True):
    __tablename__ = "result_keeper_table"

    user: "User" = Relationship(back_populates="result_keeper")  # noqa: F821
    level: int = Field(default=None, nullable=True)
    sessions: List["ResultKeeperSessionModel"] = Relationship(
        back_populates="result_keeper"
    )


class ResultKeeperSessionModel(SessionModel, table=True):
    __tablename__ = "result_keeper_session_table"
    result_keeper_id: int = Field(foreign_key="result_keeper_table.id")
    result_keeper: ResultKeeperModel = Relationship(back_populates="sessions")

    # stats
    range_min: int = Field(default=0)
    range_max: int
    steps: int


class AssociativeChangingModel(GameModel, table=True):
    __tablename__ = "associative_changing_table"

    user: "User" = Relationship(back_populates="associative_changing")  # noqa: F821
    session: List["AssociativeChangingSessionModel"] = Relationship(
        back_populates="associative_changing"
    )


class AssociativeChangingSessionModel(SessionModel, table=True):
    __tablename__ = "associative_changing_session_table"
    associative_changing_id: int = Field(foreign_key="associative_changing_table.id")
    associative_changing: AssociativeChangingModel = Relationship(
        back_populates="session"
    )

    # stats
    words: str
    user_answers: str
    amt_words: int
    skip_answers: int
    memorization_time: int  # when user press start answer
    language: str = Field(
        sa_column=Column(SQLEnum(Language), nullable=False, default=Language.EN)
    )
