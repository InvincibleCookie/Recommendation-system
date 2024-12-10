from typing import Tuple
from sqlalchemy import select, or_
from sqlalchemy.sql.selectable import Select
from src.database.postgres_author_table import AuthorInDB
from src.database.postgres_genre_table import GenreInDB
from src.data_models.book import BookFilterModel, BookModel
from src.database.postgres_book_table import BookInDB
from src.repositories.author_repository import AuthorRepository
from src.repositories.genre_repository import GenreRepository
from src.repositories.postgres.postgres_author_repository import PostgresAuthorRepository
from src.repositories.postgres.postgres_genre_repository import PostgresGenreRepository
from sqlalchemy.orm import Session
from src.database.postgres_db import PostgresDB
from src.repositories.book_repository import BookRepository


class PostgresBookRepository(BookRepository):
    def _get_engine(self):
        return PostgresDB().get_engine()

    def _get_author_repository(self) -> AuthorRepository:
        return PostgresAuthorRepository()

    def _get_genre_repository(self) -> GenreRepository:
        return PostgresGenreRepository()

    def book_model_to_db(self, book: BookModel) -> BookInDB:
        return BookInDB(
            title = book.title,
            genres = [],
            authors = [],
            publishDate = book.publishDate,
            publisher = book.publisher,
            description = book.description,
            coverLink = book.coverLink,
            raiting = book.raiting,
            popularity = book.popularity,
        )

    def add_book(self, book: BookModel) -> int:
        with Session(self._get_engine()) as session:
            new_book = self.book_model_to_db(book)

            try:
                session.add(new_book)
                session.flush()

                for i in book.genres:
                    new_book.genres.append(session.get_one(GenreInDB, i.id))

                for i in book.authors:
                    new_book.authors.append(session.get_one(AuthorInDB, i.id))

                session.add(new_book)
                session.commit()
                return new_book.id
            except Exception as e:
                print(e)
                return -1


    def get_book(self, book_id: int) -> BookModel | None:
        with Session(self._get_engine()) as session:
            try:
                book_db = session.get_one(BookInDB, book_id)
                return BookModel.from_db(book_db)
            except:
                return None

    def add_sort(self, filt: BookFilterModel, stmt: Select[Tuple[BookInDB]]) -> Select[Tuple[BookInDB]]:
        if filt.sortBy is None:
            return stmt

        col = None

        match filt.sortBy:
            case "title": col = BookInDB.title
            case "publishdate": col = BookInDB.publishDate
            case "raiting": col = BookInDB.raiting
            case "popularity": col = BookInDB.popularity
            case _: return stmt

        if filt.ascendingSort or filt.ascendingSort is None:
            return stmt.order_by(col.asc())

        return stmt.order_by(col.desc())


    def get_books_by_filter(self, filt: BookFilterModel) -> list[BookModel]:
        books = []

        with Session(self._get_engine()) as session:
            stmt = select(BookInDB)

            if filt.titlePattern is not None:
                stmt = stmt.where(BookInDB.title.ilike(filt.titlePattern))

            if filt.authors is not None:
                author_filt = or_(*[BookInDB.authors.contains(i.to_db()) for i in filt.authors])
                stmt = stmt.where(author_filt)

            if filt.genres is not None:
                genre_filt = or_(*[BookInDB.genres.contains(i.to_db()) for i in filt.genres])
                stmt = stmt.where(genre_filt)

            if filt.publishDateFrom is not None:
                stmt = stmt.where(BookInDB.publishDate >= filt.publishDateFrom)

            if filt.publishDateTo is not None:
                stmt = stmt.where(BookInDB.publishDate <= filt.publishDateTo)

            if filt.raitingFrom is not None:
                stmt = stmt.where(BookInDB.raiting >= filt.raitingFrom)

            if filt.raitingTo is not None:
                stmt = stmt.where(BookInDB.raiting <= filt.raitingTo)

            stmt = self.add_sort(filt, stmt)


            for i in session.scalars(stmt.distinct()):
                books.append(BookModel.from_db(i))


            return books

