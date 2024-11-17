from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Tuple
from sqlalchemy.sql.selectable import Select
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

    def add_sort(self, filt: GenreFilterModel, stmt: Select[Tuple[GenreInDB]]) -> Select[Tuple[GenreInDB]]:
        if filt.sortBy is None:
            return stmt

        col = None

        match filt.sortBy:
            case "name": col = GenreInDB.name
            case _: return stmt

        if filt.ascendingSort or filt.ascendingSort is None:
            return stmt.order_by(col.asc())

        return stmt.order_by(col.desc())

    def get_genres_by_filter(self, filt: GenreFilterModel) -> list[GenreModel]:
        genres = []

        with Session(self._get_engine()) as session:
            stmt = select(GenreInDB)

            if filt.namePattern is not None:
                stmt = stmt.where(GenreInDB.name.ilike(filt.namePattern))

            stmt = self.add_sort(filt, stmt)

            for i in session.scalars(stmt):
                genres.append(GenreModel.from_db(i))

            return genres
