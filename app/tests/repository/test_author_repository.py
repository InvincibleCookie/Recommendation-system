import pytest
from unittest import mock
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

from src.database.postgres_author_table import AuthorInDB
from src.data_models.author import AuthorFilterModel, AuthorModel
from src.repositories.postgres.postgres_author_repository import PostgresAuthorRepository
from ..database.test_postgres_db import PostgresDB

@pytest.fixture
def engine():
    engine = PostgresDB().connect()
    yield engine
    url = engine.url
    engine.dispose()
    drop_database(url)

@pytest.fixture
def repository(engine):
    with mock.patch.object(PostgresAuthorRepository, "_get_engine", return_value=engine):
        yield PostgresAuthorRepository()

def test_add_author(repository: PostgresAuthorRepository, engine):
    author_idx = repository.add_author(
        AuthorModel(
            id = -1,
            name = "author",
        )
    )

    assert author_idx != -1

    with Session(engine) as session:
        stmt = select(AuthorInDB)
        author_db = session.scalar(stmt)

        assert author_db is not None
        assert author_db.name == "author"

def test_get_author(repository: PostgresAuthorRepository):
    author_idx = repository.add_author(
        AuthorModel(
            id = -1,
            name = "author",
        )
    )

    author = repository.get_author(author_idx)
    assert author is not None
    assert author.name == "author"

def test_get_author_by_filt(repository: PostgresAuthorRepository):
    author_idx1 = repository.add_author(
        AuthorModel(
            id = -1,
            name = "author1",
        )
    )
    assert author_idx1 != -1

    author_idx2 = repository.add_author(
        AuthorModel(
            id = -1,
            name = "author2",
        )
    )
    assert author_idx2 != -1

    author_idx3 = repository.add_author(
        AuthorModel(
            id = -1,
            name = "author3",
        )
    )
    assert author_idx3 != -1


    filtered = repository.get_authors_by_filter(
        AuthorFilterModel(
            namePattern="author1",
            sortBy=None,
            ascendingSort=None,
        )
    )

    assert len(filtered) == 1
    assert filtered[0].name == "author1"

    filtered = repository.get_authors_by_filter(
        AuthorFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=None,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name)

    filtered = repository.get_authors_by_filter(
        AuthorFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=True,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name)


    filtered = repository.get_authors_by_filter(
        AuthorFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=False,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name, reverse=True)
