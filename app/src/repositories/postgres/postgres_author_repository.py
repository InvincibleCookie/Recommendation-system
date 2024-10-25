from sqlalchemy import select
from sqlalchemy.orm import Session
from src.data_models.author import AuthorFilterModel, AuthorModel
from src.database.postgres_author_table import AuthorInDB
from src.database.postgres_db import PostgresDB
from src.repositories.author_repository import AuthorRepository

class PostgresAuthorRepository(AuthorRepository):

    def _get_engine(self):
        return PostgresDB().get_engine()

    def add_author(self, author: AuthorModel) -> int:
        with Session(self._get_engine()) as session:
            author_db = AuthorInDB(
                name = author.name,
            )

            try:
                session.add(author_db)
                session.commit()

                return author_db.id
            except:
                return -1


    def get_author(self, author_id: int) -> AuthorModel | None:
        with Session(self._get_engine()) as session:
            try:
                return AuthorModel.from_db(session.get_one(AuthorInDB, author_id))
            except:
                return None

    def get_authors_by_filter(self, filt: AuthorFilterModel) -> list[AuthorModel]:
        authors = []

        with Session(self._get_engine()) as session:
            stmt = select(AuthorInDB)

            if filt.namePattern is not None:
                stmt = stmt.where(AuthorInDB.name.ilike(filt.namePattern))

            for i in session.scalars(stmt):
                authors.append(AuthorModel.from_db(i))

            return authors

