from typing import List
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .postgres_db import Base
from .postgres_association_tables import book_to_genre_association

class GenreInDB(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[List["BookInDB"]] = relationship(secondary=book_to_genre_association, back_populates="genres")

    def __repr__(self) -> str:
        return f"Genre(id={self.id}), name={self.name}"

from .postgres_book_table import BookInDB # prevents circular import
