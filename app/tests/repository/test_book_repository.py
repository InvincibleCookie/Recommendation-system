from os import name
import pytest
from unittest import mock
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

from src.data_models.author import AuthorIdModel, AuthorModel
from src.data_models.genres import GenreIdModel, GenreModel
from src.repositories.postgres.postgres_author_repository import PostgresAuthorRepository
from src.repositories.postgres.postgres_genre_repository import PostgresGenreRepository
from src.database.postgres_book_table import BookInDB
from src.data_models.book import BookFilterModel, BookModel
from src.repositories.postgres.postgres_book_repository import PostgresBookRepository
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
    with mock.patch.object(PostgresBookRepository, "_get_engine", return_value=engine):
        yield PostgresBookRepository()

@pytest.fixture
def genre_repository(engine):
    with mock.patch.object(PostgresGenreRepository, "_get_engine", return_value=engine):
        yield PostgresGenreRepository()

@pytest.fixture
def author_repository(engine):
    with mock.patch.object(PostgresAuthorRepository, "_get_engine", return_value=engine):
        yield PostgresAuthorRepository()

def test_add_book(repository: PostgresBookRepository,
                  genre_repository: PostgresGenreRepository,
                  author_repository: PostgresAuthorRepository,
                  engine):
    author1 = AuthorModel(
        id = -1,
        name = "author1",
    )

    author_idx1 = author_repository.add_author(author1)
    assert author_idx1 != -1
    author1.id = author_idx1

    author2 = AuthorModel(
        id = -1,
        name = "author2",
    )

    author_idx2 = author_repository.add_author(author2)
    assert author_idx2 != -1
    author2.id = author_idx2


    genre = GenreModel(
        id = -1,
        name = "genre1",
    )

    genre_idx1 = genre_repository.add_genre(genre)
    assert genre_idx1 != -1
    genre.id = genre_idx1

    book = BookModel(
        id = -1,
        title = "title",
        authors = [author1, author2],
        genres = [genre],
        publishDate = datetime.now(),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
        popularity=100,
    )
    repository.add_book(book)

    assert repository.add_book(book) != -1

    with Session(engine) as session:
        stmt = select(BookInDB)
        book_db = session.scalar(stmt)


        assert book_db is not None
        assert book_db.id != -1
        assert book_db.title == "title"

def test_get_book(repository: PostgresBookRepository):
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

    book_id = repository.add_book(book)
    assert book_id is not None

    book_db = repository.get_book(book_id)
    assert book_db is not None
    assert book_db.title == book.title

def test_get_books_by_filter(repository: PostgresBookRepository,
                             genre_repository: PostgresGenreRepository,
                             author_repository: PostgresAuthorRepository):
    base_time = datetime.now()

    author1 = AuthorModel(
        id = -1,
        name = "author1",
    )

    author_idx1 = author_repository.add_author(author1)
    assert author_idx1 != -1
    author1.id = author_idx1

    author2 = AuthorModel(
        id = -1,
        name = "author2",
    )

    author_idx2 = author_repository.add_author(author2)
    assert author_idx2 != -1
    author2.id = author_idx2

    genre1 = GenreModel(
        id = -1,
        name = "genre1",
    )

    genre2 = GenreModel(
        id = -1,
        name = "genre2",
    )

    genre_idx1 = genre_repository.add_genre(genre1)
    assert genre_idx1 != -1
    genre1.id = genre_idx1

    genre_idx2 = genre_repository.add_genre(genre2)
    assert genre_idx2 != -1
    genre2.id = genre_idx2

    book = BookModel(
        id = -1,
        title = "title",
        authors = [author1, author2],
        genres = [genre1],
        publishDate = base_time + timedelta(hours=1),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
        popularity=10,
    )
    repository.add_book(book)

    book = BookModel(
        id = -1,
        title = "title2",
        authors = [author1],
        genres = [genre2, genre1],
        publishDate = base_time - timedelta(hours=1),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
        popularity=90,
    )
    repository.add_book(book)

    book = BookModel(
        id = -1,
        title = "title3",
        authors = [author2],
        genres = [genre2],
        publishDate = base_time + timedelta(hours=2),
        publisher = "pub",
        description = "its a book",
        coverLink = "link",
        raiting = 5,
        popularity=100,
    )
    repository.add_book(book)

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = "%Titl%",
            authors = None,
            genres = None,
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )

    assert len(filtered) == 3

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            authors = None,
            genres = None,
            publishDateFrom = base_time,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )

    assert len(filtered) == 2

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            authors = None,
            genres = None,
            publishDateFrom = None,
            publishDateTo = base_time,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 1

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            authors = None,
            genres = [GenreIdModel(id = genre_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 2

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            authors = None,
            genres = [GenreIdModel(id = genre_idx2)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 2

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            authors = None,
            genres = [GenreIdModel(id = genre_idx2), GenreIdModel(id = genre_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 3


    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres = None,
            authors = [AuthorIdModel(id = author_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 2

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [AuthorIdModel(id = author_idx2)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 2

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [AuthorIdModel(id = author_idx2), AuthorIdModel(id = author_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy=None,
            ascendingSort=None,
        )
    )
    assert len(filtered) == 3

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [AuthorIdModel(id = author_idx2), AuthorIdModel(id = author_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy='title',
            ascendingSort=None,
        )
    )
    assert len(filtered) == 3
    assert filtered == sorted(filtered, key = lambda a: a.title)

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [AuthorIdModel(id = author_idx2), AuthorIdModel(id = author_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy='title',
            ascendingSort=True,
        )
    )
    assert len(filtered) == 3
    assert filtered == sorted(filtered, key = lambda a: a.title)

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [AuthorIdModel(id = author_idx2), AuthorIdModel(id = author_idx1)],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy='title',
            ascendingSort=False,
        )
    )
    assert len(filtered) == 3
    assert filtered == sorted(filtered, key = lambda a: a.title, reverse=True)

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy='popularity',
            ascendingSort=False,
        )
    )
    assert len(filtered) == 3
    assert filtered == sorted(filtered, key = lambda a: a.popularity, reverse=True)

    filtered = repository.get_books_by_filter(
        BookFilterModel(
            titlePattern = None,
            genres= None,
            authors = [],
            publishDateFrom = None,
            publishDateTo = None,
            raitingFrom = None,
            raitingTo = None,
            sortBy='popularity',
            ascendingSort=True,
        )
    )
    assert len(filtered) == 3
    assert filtered == sorted(filtered, key = lambda a: a.popularity, reverse=False)
