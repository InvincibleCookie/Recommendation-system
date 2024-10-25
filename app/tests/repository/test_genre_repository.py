import pytest
from unittest import mock
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

from src.data_models.genres import GenreModel
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


