from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.user.models import Base, Login, User


@pytest.fixture(scope="function")
def engine():
    """Create a fresh in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def session(engine):
    """Create a new session for each test."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def user(session):
    """Create a test user."""
    user = User(username="testuser", password="testpass")
    session.add(user)
    session.commit()
    return user


class TestUser:
    def test_create_user(self, session):
        """Test creating a new user."""
        user = User(username="newuser", password="password123")
        session.add(user)
        session.commit()
        # get the user from the database
        user = session.query(User).filter_by(id=user.id).one()

        assert user.id is not None
        assert user.username == "newuser"
        assert user.password == "password123"
        assert isinstance(user.created_at, datetime)
        assert len(user.logins) == 0

    def test_unique_username(self, session, user):
        """Test that usernames must be unique."""
        with pytest.raises(Exception):  # SQLAlchemy will raise an integrity error
            duplicate_user = User(username="testuser", password="different_pass")
            session.add(duplicate_user)
            session.commit()

    def test_user_login_relationship(self, session, user):
        """Test the relationship between User and Login."""
        login = Login(user=user)
        session.add(login)
        session.commit()
        # get the user from the database
        user = session.query(User).filter_by(id=user.id).one()
        assert len(user.logins) == 1
        assert user.logins[0].user_id == user.id
        assert isinstance(user.logins[0].login_date, datetime)


class TestLogin:
    def test_create_login(self, session, user):
        """Test creating a new login entry."""
        login = Login(user_id=user.id)
        session.add(login)
        session.commit()

        assert login.id is not None
        assert login.user_id == user.id
        assert isinstance(login.login_date, datetime)
        assert login.user == user

    def test_login_user_relationship(self, session):
        """Test creating a login entry with user relationship."""
        user = User(username="logintest", password="pass123")
        login = Login(user=user)

        session.add(user)
        session.add(login)
        session.commit()

        assert login.user_id == user.id
        assert login.user.username == "logintest"

    def test_multiple_logins(self, session, user):
        """Test that a user can have multiple login entries."""
        login1 = Login(user=user)
        login2 = Login(user=user)

        session.add_all([login1, login2])
        session.commit()

        assert len(user.logins) == 2
        assert all(isinstance(login.login_date, datetime) for login in user.logins)
