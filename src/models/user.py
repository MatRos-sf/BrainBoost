import datetime
from typing import List, Optional

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlmodel import Column, Field, Relationship

from src.models.enum_types import Language, PointsCategory

from . import ModelBase
from .games import ResultKeeperModel


class User(ModelBase, table=True):
    __tablename__ = "user_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    logins: List["Login"] = Relationship(back_populates="user")
    language: str = Field(
        sa_column=Column(SQLEnum(Language), nullable=False, default=Language.EN)
    )
    # stats
    point: int = Field(default=0)  # sum points
    points: List["PointsModel"] = Relationship(back_populates="user")
    # games one-to-one relationship
    result_keeper: Optional["ResultKeeperModel"] = Relationship(back_populates="user")
    associative_changing: Optional[
        "AssociativeChangingModel"  # noqa: F821
    ] = Relationship(back_populates="user")

    # TODO: scal day -> [PN,NDZ]


class Login(ModelBase, table=True):
    __tablename__ = "login_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    login_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    user: User = Relationship(back_populates="logins")


class PointsModel(ModelBase, table=True):
    """Models hold information about assigned points"""

    __tablename__ = "points_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    user: User = Relationship(back_populates="points")
    category: str
    point: int
    saved_date: datetime.datetime = Field(default_factory=datetime.datetime.now)


# Events


@event.listens_for(User, "after_insert")
def add_first_points_after_create_account(mapper, connection, target):
    """When user create account should get points for it"""
    with Session(bind=connection) as session:
        session.add(
            PointsModel(
                user_id=target.id,
                category=PointsCategory.CREATE_ACCOUNT.value[0],
                point=PointsCategory.CREATE_ACCOUNT.value[1],
            )
        )
        session.commit()


@event.listens_for(PointsModel, "after_insert")
def update_point_in_user_model(mapper, connection, target):
    """Events update point in User model when PointsModel is added"""
    connection.execute(
        User.__table__.update()
        .where(User.id == target.user_id)
        .values(point=User.__table__.c.point + target.point)
    )
