from datetime import datetime
from pydantic import BaseModel

from src.database.postgres_book_table import BookInDB
from src.data_models.genres import GenreIdModel, GenreModel
from src.data_models.author import AuthorIdModel, AuthorModel

class BookIdModel(BaseModel):
    id: int

    @staticmethod
    def from_db(book: BookInDB) -> 'BookIdModel':
        return BookIdModel(id = book.id)

class FullBookModel(BookIdModel):
    title: str
    authors: list[AuthorModel]
    genres: list[GenreModel]
    publishDate: datetime
    publisher: str
    description: str
    coverLink: str
    raiting: float

class BookModel(BookIdModel):
    title: str
    authors: list[AuthorIdModel]
    genres: list[GenreIdModel]
    publishDate: datetime
    publisher: str
    description: str
    coverLink: str
    raiting: float


    @staticmethod
    def from_db(book: BookInDB) -> 'BookModel':
        return BookModel(
            id = book.id,
            title = book.title,
            genres = list(map(GenreIdModel.from_db, book.genres)),
            authors = list(map(AuthorIdModel.from_db, book.authors)),
            publishDate = book.publishDate,
            publisher = book.publisher,
            description = book.description,
            coverLink = book.coverLink,
            raiting = book.raiting,
        )

class BookFilterModel(BaseModel):
    titlePattern: str | None
    authors: list[AuthorIdModel] | None
    genres: list[GenreIdModel] | None
    publishDateFrom: datetime | None
    publishDateTo: datetime | None
    raitingFrom: float | None
    raitingTo: float | None

