from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # relationship with login table
    logins: Mapped[List["Login"]] = relationship(
        "Login", back_populates="user"
    )  # add cascade


class Login(Base):
    __tablename__ = "login_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    login_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # relationship
    user: Mapped[User] = relationship("User", back_populates="logins")
