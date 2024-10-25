from src.data_models.book import BookFilterModel, BookModel
from src.repositories.postgres.postgres_book_repository import PostgresBookRepository


class BookService:
    def __init__(self) -> None:
        self.respository = PostgresBookRepository()

    def get_book(self, book_id: int) -> BookModel | None:
        return self.respository.get_book(book_id)

    def get_books_by_filter(self, filt: BookFilterModel) -> list[BookModel]:
        return self.respository.get_books_by_filter(filt)
