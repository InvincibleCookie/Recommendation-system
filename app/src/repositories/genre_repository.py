from abc import abstractmethod
from src.data_models.genres import GenreFilterModel, GenreModel


class GenreRepository:
    @abstractmethod
    def add_genre(self, genre: GenreModel) -> int: pass

    @abstractmethod
    def get_genre(self, genre_id: int) -> GenreModel | None: pass

    @abstractmethod
    def get_genre_by_filter(self, filt: GenreFilterModel) -> list[GenreModel]: pass
