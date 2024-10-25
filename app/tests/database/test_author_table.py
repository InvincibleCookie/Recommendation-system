from datetime import datetime
import pytest

from sqlalchemy.orm import Session

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
        name = "Novel"
    )

    with Session(engine) as session:
        session.add(book)
        session.add(author)
        session.flush()

        book.authors.append(author)
        session.flush()

        got_author = session.get(AuthorInDB, book.id)
        assert(got_author is not None)
        assert(got_author.name== author.name)
        assert(len(got_author.books) == 1)
        assert(got_author.books[0].title == book.title)



