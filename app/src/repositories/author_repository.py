from abc import abstractmethod

from src.data_models.author import AuthorFilterModel, AuthorModel

class AuthorRepository:
    @abstractmethod
    def add_author(self, author: AuthorModel) -> int: pass

    @abstractmethod
    def get_author(self, author_id: int) -> AuthorModel | None: pass

    @abstractmethod
    def get_authors_by_filter(self, filt: AuthorFilterModel) -> list[AuthorModel]: pass
