from src.data_models.genres import GenreFilterModel, GenreModel
from src.repositories.postgres.postgres_genre_repository import PostgresGenreRepository

class GenreService:
    def __init__(self) -> None:
        self.respository = PostgresGenreRepository()

    def get_genre(self, genre_id: int) -> GenreModel | None:
        return self.respository.get_genre(genre_id)

    def get_genres_by_filt(self, filt: GenreFilterModel) -> list[GenreModel]:
        return self.respository.get_genres_by_filter(filt)
