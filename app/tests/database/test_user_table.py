import unittest
import pytest

from sqlalchemy.orm import Session
from .test_postgres_db import PostgresDB
from sqlalchemy_utils import drop_database

from src.database.postgres_user_table import UserInDB

@pytest.fixture
def engine():
    engine = PostgresDB().connect()
    yield engine
    url = engine.url
    engine.dispose()
    drop_database(url)

def test_table(engine):
    user  = UserInDB(
        username = "user",
        email = "mail",
        password_hash = "hash",
    )
    with Session(engine) as session:
        session.add(user)

        session.commit()

        got_user = session.get_one(UserInDB, user.id)
        assert(got_user.username == user.username)
