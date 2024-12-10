import pytest
from datetime import datetime
from unittest import mock
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

from src.data_models.book import BookModel
from src.repositories.postgres.postgres_book_repository import PostgresBookRepository
from src import auth
from src.database.postgres_token_table import TokenInDB
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
    with mock.patch.object(PostgresUserRepository, "_get_engine", return_value=engine):
        yield PostgresUserRepository()

@pytest.fixture
def book_repository(engine):
    with mock.patch.object(PostgresBookRepository, "_get_engine", return_value=engine):
        yield PostgresBookRepository()

def test_register(repository, engine):
    user = FullUserModel(
        username="username",
        email="mail",
        password="password"
    )

    assert(repository.register(user))

    with Session(engine) as session:
        stmt = select(UserInDB)
        user_db = session.scalar(stmt)

        assert user_db is not None
        assert user_db.username == user.username

def test_autheticate_by_password(repository: PostgresUserRepository, engine):
    test_register(repository, engine)
    assert repository.autheticate_by_password("username", "password")


def test_add_refresh_token(repository: PostgresUserRepository, engine):
    test_register(repository, engine)
    token = auth.create_refresh_token("username")
    repository.add_refresh_token(token)


    with Session(engine) as session:
        stmt = select(TokenInDB)
        token_db= session.scalar(stmt)

        assert token_db is not None
        assert token_db.user.username == "username"


def test_invalidate_refresh_token(repository: PostgresUserRepository, engine):
    test_register(repository, engine)
    token = auth.create_refresh_token("username")

    assert repository.add_refresh_token(token)

    assert repository.invalidate_refresh_token(token)

    with Session(engine) as session:
        stmt = select(TokenInDB)
        token_db = session.scalar(stmt)

        assert token_db is None

def test_get_user(repository: PostgresUserRepository, engine):
    test_register(repository, engine)

    user = repository.get_user("username")

    assert user is not None
    assert user.username == "username"

def test_get_internal_user(repository: PostgresUserRepository, engine):
    test_register(repository, engine)

    user = repository.get_internal_user("username")

    assert user is not None
    assert user.username == "username"

def test_like_book(repository: PostgresUserRepository,
                   book_repository: PostgresBookRepository,
                   engine):
    test_register(repository, engine)

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
        popularity=100,
    )
    book_id = book_repository.add_book(book)
    assert book_id is not None

    assert repository.like_book("username", book_id)

    with Session(engine) as session:
        stmt = select(UserInDB)
        user_db = session.scalar(stmt)

        assert user_db is not  None
        assert len(user_db.liked_books) == 1
        assert user_db.liked_books[0].title == "title"

def test_unlike_book(repository: PostgresUserRepository,
                   book_repository: PostgresBookRepository,
                   engine):
    test_like_book(repository,book_repository, engine)
    ids = repository.get_liked_books("username")

    assert len(ids) > 0

    assert repository.unlike_book("username", ids[0].id)
    assert not repository.unlike_book("username", ids[0].id)

    ids2 = repository.get_liked_books("username")
    assert len(ids) == len(ids2)+1

def test_get_liked_books(repository: PostgresUserRepository,
                   book_repository: PostgresBookRepository,
                   engine):
    test_register(repository, engine)

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
        popularity=100,
    )
    book_id = book_repository.add_book(book)

    assert book_id != -1

    repository.like_book("username", book_id)

    books = repository.get_liked_books("username")

    assert len(books) == 1

