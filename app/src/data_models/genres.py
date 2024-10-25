from pydantic import BaseModel

from src.database.postgres_genre_table import GenreInDB

class GenreIdModel(BaseModel):
    id: int

    def to_db(self) -> GenreInDB:
        return GenreInDB(
            id = self.id,
        )

    @staticmethod
    def from_db(genre: GenreInDB) -> 'GenreIdModel':
        return GenreIdModel(
            id = genre.id,
        )

class GenreModel(GenreIdModel):
    name: str

    def to_db(self) -> GenreInDB:
        return GenreInDB(
            name = self.name,
        )

    @staticmethod
    def from_db(genre: GenreInDB) -> 'GenreModel':
        return GenreModel(
            id = genre.id,
            name = genre.name,
        )

class GenreFilterModel(BaseModel):
    namePattern: str
