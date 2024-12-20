from abc import abstractmethod

from src.data_models.book import BookFilterModel, BookModel


class BookRepository:

    @abstractmethod
    def get_book(self, book_id: int) -> BookModel | None: pass

    @abstractmethod
    def get_books_by_filter(self, filt: BookFilterModel) -> list[BookModel]: pass

    @abstractmethod
    def add_book(self, book: BookModel) -> int: pass
