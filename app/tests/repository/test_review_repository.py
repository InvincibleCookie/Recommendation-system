from copy import copy
import pytest
from datetime import datetime
from unittest import mock
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database
from src.database.postgres_review_table import ReviewInDB
from src.data_models.review import ReviewFilterModel, ReviewNoIdModel
from src.repositories.book_repository import BookRepository
from src.repositories.review_repository import ReviewRepository
from src.repositories.user_repository import UserRepository
from src.repositories.postgres.postgres_review_repository import PostgresReviewRepository
from src.data_models.book import BookModel
from src.repositories.postgres.postgres_book_repository import PostgresBookRepository
from src.data_models.user import FullUserModel
from src.database.postgres_user_table import UserInDB
from ..database.test_postgres_db import PostgresDB
from src.repositories.postgres.postgres_user_repository import PostgresUserRepository

@pytest.fixture
def engine():
    engine = PostgresDB().connect()
    yield engine
    url = engine.url
    engine.dispose()
    drop_database(url)

@pytest.fixture
def repository(engine):
    with mock.patch.object(PostgresReviewRepository, "_get_engine", return_value=engine):
        yield PostgresReviewRepository()

@pytest.fixture
def user_repository(engine):
    with mock.patch.object(PostgresUserRepository, "_get_engine", return_value=engine):
        yield PostgresUserRepository()

@pytest.fixture
def book_repository(engine):
    with mock.patch.object(PostgresBookRepository, "_get_engine", return_value=engine):
        yield PostgresBookRepository()

def test_add_review(repository: ReviewRepository, user_repository: UserRepository, book_repository: BookRepository, engine: Engine):
    user = FullUserModel(
        username="username",
        email="mail",
        password="password"
    )
    assert user_repository.register(user)

    book = BookModel(
        id = -1,
        title = "title",
        authors = [],
        genres = [],
        publishDate = datetime.now(),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
    )
    book_id = book_repository.add_book(book)
    assert book_id is not None

    rv = ReviewNoIdModel(
        title='title',
        price=10,
        username='user',
        helpfulness=10,
        score=10,
        date=datetime.now(),
        summary='sum',
        review_text='text',
        is_internal_user=False,
        book_id=book_id
    )
    urv = copy(rv)
    urv.is_internal_user = True

    rv_id = repository.add_review(rv, 0, False)
    assert rv_id != -1

    with Session(engine) as session:
        review = session.get_one(ReviewInDB, rv_id)
        assert review.book_id == book_id
        assert review.title == rv.title

        stmt = select(UserInDB).where(UserInDB.username == user.username)
        duser = session.scalar(stmt)
        assert duser is not None

        urv_id = repository.add_review(urv, duser.id, True)
        assert urv_id != -1

        review = session.get_one(ReviewInDB, urv_id)
        assert review.book_id == book_id
        assert review.title == rv.title
        assert review.foreign_username == None
        assert review.internal_user.username == user.username

def test_get_review(repository: ReviewRepository, book_repository: BookRepository):
    book = BookModel(
        id = -1,
        title = "title",
        authors = [],
        genres = [],
        publishDate = datetime.now(),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
    )
    book_id = book_repository.add_book(book)
    assert book_id is not None

    rv = ReviewNoIdModel(
        title='title',
        price=10,
        username='user',
        helpfulness=10,
        score=10,
        date=datetime.now(),
        summary='sum',
        review_text='text',
        is_internal_user=False,
        book_id=book_id
    )

    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1

    rv_db = repository.get_review(rv_idx)
    assert rv_db is not None
    assert rv_db.title == rv.title


def test_get_reviews_by_filter(repository: ReviewRepository, book_repository: BookRepository):
    book = BookModel(
        id = -1,
        title = "title",
        authors = [],
        genres = [],
        publishDate = datetime.now(),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
    )
    book_id1 = book_repository.add_book(book)
    assert book_id1 is not None

    book = BookModel(
        id = -1,
        title = "title2",
        authors = [],
        genres = [],
        publishDate = datetime.now(),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
    )
    book_id2 = book_repository.add_book(book)
    assert book_id2 is not None

    rv = ReviewNoIdModel(
        title='title',
        price=10,
        username='user',
        helpfulness=10,
        score=10,
        date=datetime.now(),
        summary='sum',
        review_text='text',
        is_internal_user=False,
        book_id=book_id1
    )

    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1

    rv.score = 9
    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1

    rv.score = 8
    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1

    rv.book_id = book_id2

    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1
    rv_idx = repository.add_review(rv, 0, False)
    assert rv_idx != -1

    filt = ReviewFilterModel(
        book_id = book_id1,
        sortBy=None,
        ascendingSort=None,
    )

    rvs = repository.get_reviews_by_filter(filt)

    filt.book_id = book_id2

    rvs = repository.get_reviews_by_filter(filt)
    assert len(rvs) == 2

    filt = ReviewFilterModel(
        book_id = book_id1,
        sortBy='score',
        ascendingSort=None,
    )

    rvs = repository.get_reviews_by_filter(filt)
    assert len(rvs) == 3
    assert rvs == sorted(rvs, key=lambda a: a.score)

    filt = ReviewFilterModel(
        book_id = book_id1,
        sortBy='score',
        ascendingSort=True,
    )

    rvs = repository.get_reviews_by_filter(filt)
    assert len(rvs) == 3
    assert rvs == sorted(rvs, key=lambda a: a.score)

    filt = ReviewFilterModel(
        book_id = book_id1,
        sortBy='score',
        ascendingSort=False,
    )

    rvs = repository.get_reviews_by_filter(filt)
    assert len(rvs) == 3
    assert rvs == sorted(rvs, key=lambda a: a.score, reverse=True)
