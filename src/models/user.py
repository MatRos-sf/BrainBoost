from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship

from . import ModelBase


class User(ModelBase, table=True):
    __tablename__ = "user_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    logins: List["Login"] = Relationship(back_populates="user")


class Login(ModelBase, table=True):
    __tablename__ = "login_table"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_table.id")
    login_date: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="logins")
