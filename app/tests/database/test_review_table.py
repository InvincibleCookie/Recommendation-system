from datetime import datetime
import pytest

from sqlalchemy.orm import Session

from src.database.postgres_book_table import BookInDB
from src.database.postgres_review_table import ReviewInDB
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

    book = BookInDB(
        title = "book",
        description = "book about books",
        publisher = "man",
        publishDate = datetime.now(),
        coverLink = "link",
        raiting = 5.0,
        popularity = 100,
    )

    ireview = ReviewInDB(
        title = "title",
        price = 93.3,
        foreign_user_id = 10,
        foreign_username = 'user',
        helpfulness = 10,
        score = 10,
        date = datetime.now(),
        summary = "ok",
        review_text = "fine",
        is_internal_user = True,
        internal_user_id = 0,
        book_id = 0
    )

    review = ReviewInDB(
        title = "title",
        price = 93.3,
        foreign_user_id = 10,
        foreign_username = 'user',
        helpfulness = 10,
        score = 10,
        date = datetime.now(),
        summary = "ok",
        review_text = "fine",

        is_internal_user = False
    )

    with Session(engine) as session:
        session.add(book)
        session.add(user)

        session.commit()

        ireview.internal_user_id = user.id
        ireview.book_id = book.id
        review.book_id = book.id

        session.add(ireview)
        session.add(review)

        session.commit()


        got_review = session.get_one(ReviewInDB, ireview.id)
        got_user= session.get_one(UserInDB, user.id)
        assert(got_review.is_internal_user)
        assert(got_review.internal_user.username == user.username)
        assert(len(got_user.reviews) == 1)

        got_review = session.get_one(ReviewInDB, review.id)
        assert(not got_review.is_internal_user)
