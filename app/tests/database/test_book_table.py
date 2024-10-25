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

    author = AuthorInDB(
        name = "Arthur Dent"
    )

    genre = GenreInDB(
        name = "Novel"
    )

    with Session(engine) as session:
        session.add(book)
        session.add(author)
        session.add(genre)
        session.flush()

        book.authors.append(author)
        book.genres.append(genre)

        session.flush()

        got_book = session.get(BookInDB, book.id)
        assert(got_book is not None)
        assert(got_book.title == book.title)
        assert(len(got_book.authors) == 1)
        assert(len(got_book.genres) == 1)
        assert(got_book.authors[0].name == author.name)
        assert(got_book.genres[0].name == genre.name)



