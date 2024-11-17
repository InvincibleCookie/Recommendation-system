from pydantic import BaseModel

from src.database.postgres_author_table import AuthorInDB


class AuthorIdModel(BaseModel):
    id: int

    @staticmethod
    def from_db(author: AuthorInDB) -> 'AuthorIdModel':
        return AuthorIdModel(
            id = author.id,
        )

    def to_db(self) -> AuthorInDB:
        return AuthorInDB(
            id = self.id,
        )

class AuthorModel(AuthorIdModel):
    name: str

    @staticmethod
    def from_db(author: AuthorInDB) -> 'AuthorModel':
        return AuthorModel(
            id = author.id,
            name = author.name,
        )


    def to_db(self) -> AuthorInDB:
        return AuthorInDB(
            id = self.id,
            name = self.name,
        )

class AuthorFilterModel(BaseModel):
    namePattern: str
    ascendingSort: bool | None
    sortBy: str | None
