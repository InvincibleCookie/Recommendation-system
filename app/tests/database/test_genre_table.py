from datetime import datetime
import pytest

from sqlalchemy.orm import Session

from src.database.postgres_genre_table import GenreInDB
from src.database.postgres_author_table import AuthorInDB

from .test_postgres_db import PostgresDB
from src.database.postgres_book_table import BookInDB
from sqlalchemy_utils import drop_database

import pytest

@pytest.fixture
def engine():
    engine = PostgresDB().connect()
    yield engine
    url = engine.url
    engine.dispose()
    drop_database(url)

def test_table(engine):
    book = BookInDB(
        title = "book",
        description = "book about books",
        publisher = "man",
        publishDate = datetime.now(),
        coverLink = "link",
        raiting = 5.0
    )

    genre = GenreInDB(
        name = "Novel"
    )

    with Session(engine) as session:
        session.add(book)
        session.add(genre)
        session.flush()

        book.genres.append(genre)
        session.flush()

        got_genre = session.get(GenreInDB, book.id)
        assert(got_genre is not None)
        assert(got_genre.name== genre.name)
        assert(len(got_genre.books) == 1)
        assert(got_genre.books[0].title == book.title)



