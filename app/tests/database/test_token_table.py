from datetime import datetime
import pytest

from sqlalchemy.orm import Session

from src.database.postgres_token_table import TokenInDB
from .test_postgres_db import PostgresDB
from sqlalchemy_utils import drop_database

from src.database.postgres_user_table import UserInDB

import pytest

@pytest.fixture
def engine():
    engine = PostgresDB().connect()
    yield engine
    url = engine.url
    engine.dispose()
    drop_database(url)

def test_table(engine):
    user = UserInDB(
        username="user",
        email="mail",
        password_hash="hash"
    )

    with Session(engine) as session:
        session.add(user)
        session.commit()

        token = TokenInDB(
            user_id=user.id,
            token_id="id",
            expiry_date=datetime.now(),
        )
        session.add(token)
        session.flush()

        got_token = session.get(TokenInDB, token.id)
        assert(got_token is not None)
        assert got_token.token_id == token.token_id
