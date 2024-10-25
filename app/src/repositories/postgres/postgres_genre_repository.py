from sqlalchemy import select
from sqlalchemy.orm import Session
from src.data_models.genres import GenreFilterModel, GenreModel
from src.database.postgres_db import PostgresDB
from src.database.postgres_genre_table import GenreInDB
from src.repositories.genre_repository import GenreRepository

class PostgresGenreRepository(GenreRepository):

    def _get_engine(self):
        return PostgresDB().get_engine()

    def add_genre(self, genre: GenreModel) -> int:
        with Session(self._get_engine()) as session:
            genre_db = GenreInDB(
                name = genre.name,
            )

            try:
                session.add(genre_db)
                session.commit()

                return genre_db.id
            except:
                return -1


    def get_genre(self, genre_id: int) -> GenreModel | None:
        with Session(self._get_engine()) as session:
            try:
                return GenreModel.from_db(session.get_one(GenreInDB, genre_id))
            except:
                return None

    def get_genres_by_filter(self, filt: GenreFilterModel) -> list[GenreModel]:
        genres = []

        with Session(self._get_engine()) as session:
            stmt = select(GenreInDB)

            if filt.namePattern is not None:
                stmt = stmt.where(GenreInDB.name.ilike(filt.namePattern))

            for i in session.scalars(stmt):
                genres.append(GenreModel.from_db(i))

            return genres
