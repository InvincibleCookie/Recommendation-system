import pytest
from unittest import mock
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

from src.data_models.genres import GenreFilterModel, GenreModel
from src.database.postgres_genre_table import GenreInDB
from src.repositories.postgres.postgres_genre_repository import PostgresGenreRepository
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
    with mock.patch.object(PostgresGenreRepository, "_get_engine", return_value=engine):
        yield PostgresGenreRepository()

def test_add_genre(repository: PostgresGenreRepository, engine):
    genre_idx = repository.add_genre(
        GenreModel(
            id = -1,
            name = "genre",
        )
    )

    assert genre_idx != -1

    with Session(engine) as session:
        stmt = select(GenreInDB)
        genre_db = session.scalar(stmt)

        assert genre_db is not None
        assert genre_db.name == "genre"

def test_get_genre(repository: PostgresGenreRepository):
    genre_idx = repository.add_genre(
        GenreModel(
            id = -1,
            name = "genre",
        )
    )

    genre = repository.get_genre(genre_idx)
    assert genre is not None
    assert genre.name == "genre"


def test_get_author_by_filt(repository: PostgresGenreRepository):
    genre_idx1 = repository.add_genre(
        GenreModel(
            id = -1,
            name = "genre1",
        )
    )
    assert genre_idx1 != -1

    genre_idx2 = repository.add_genre(
        GenreModel(
            id = -1,
            name = "genre2",
        )
    )
    assert genre_idx2 != -1

    genre_idx3 = repository.add_genre(
        GenreModel(
            id = -1,
            name = "genre3",
        )
    )
    assert genre_idx3 != -1


    filtered = repository.get_genres_by_filter(
        GenreFilterModel(
            namePattern="genre1",
            sortBy=None,
            ascendingSort=None,
        )
    )

    assert len(filtered) == 1
    assert filtered[0].name == "genre1"

    filtered = repository.get_genres_by_filter(
        GenreFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=None,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name)

    filtered = repository.get_genres_by_filter(
        GenreFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=True,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name)


    filtered = repository.get_genres_by_filter(
        GenreFilterModel(
            namePattern="%%",
            sortBy="name",
            ascendingSort=False,
        )
    )

    assert len(filtered) == 3
    assert filtered == sorted(filtered, key=lambda a: a.name, reverse=True)
