from src.data_models.author import AuthorFilterModel, AuthorModel
from src.repositories.postgres.postgres_author_repository import PostgresAuthorRepository


class AuthorService:
    def __init__(self) -> None:
        self.respository = PostgresAuthorRepository()

    def get_author(self, author_id: int) -> AuthorModel| None:
        return self.respository.get_author(author_id)

    def get_authors_by_filter(self, filt: AuthorFilterModel) -> list[AuthorModel]:
        return self.respository.get_authors_by_filter(filt)
