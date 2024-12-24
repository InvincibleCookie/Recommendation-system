from datetime import datetime
from pydantic import BaseModel
import ast

from src.database.postgres_book_table import BookInDB
from src.data_models.genres import GenreIdModel, GenreModel
from src.data_models.author import AuthorIdModel, AuthorModel

class BookIdModel(BaseModel):
    id: int

    @staticmethod
    def from_db(book: BookInDB) -> 'BookIdModel':
        return BookIdModel(id = book.id)

class BookLikeModel(BookIdModel):
    like: bool

class BookModel(BookIdModel):
    title: str
    authors: list[AuthorModel]
    genres: list[GenreModel]
    publishDate: datetime
    publisher: str
    description: str
    coverLink: str
    raiting: float
    popularity: int


    @staticmethod
    def from_db(book: BookInDB) -> 'BookModel':
        return BookModel(
            id = book.id,
            title = book.title,
            genres = list(map(GenreModel.from_db, book.genres)),
            authors = list(map(AuthorModel.from_db, book.authors)),
            publishDate = book.publishDate,
            publisher = book.publisher,
            description = book.description,
            coverLink = book.coverLink,
            raiting = book.raiting,
            popularity = book.popularity,
        )

class BookFilterModel(BaseModel):
    titlePattern: str | None
    authors: list[AuthorIdModel] | None
    genres: list[GenreIdModel] | None
    publishDateFrom: datetime | None
    publishDateTo: datetime | None
    raitingFrom: float | None
    raitingTo: float | None
    ascendingSort: bool | None
    sortBy: str | None

class SimpleBook(BaseModel):
    title: str
    authors: list[str]
    cover_link: str

class BookRecommedation(BaseModel):
    recommend: list[SimpleBook]

    @staticmethod
    def from_list(df: list) -> 'None | BookRecommedation':
        res = []
        for i in df:
            if len(i) != 3:
                return None
            try:
                ls = ast.literal_eval(i[1])
                if type(i[0]) is not str:
                    i[0] = "Unknown"

                if type(ls) is not list:
                    ls = []

                offset = 0
                for idx in range(len(ls)):
                    if type(ls[idx-offset]) is not str:
                        ls.pop(idx-offset)
                        offset+=1

                if type(i[2]) is not str:
                    i[2] = "Unknown"

                res.append(
                    SimpleBook(
                        title=i[0],
                        authors=ls,
                        cover_link=i[2]
                    )
                )
            except:
                pass

        return BookRecommedation(recommend=res)


