from datetime import datetime
from typing import List
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .postgres_db import Base
from .postgres_association_tables import book_to_author_association, book_to_genre_association

class BookInDB(Base):
    __tablename__ = "book_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    publisher: Mapped[str]
    publishDate: Mapped[datetime]
    coverLink: Mapped[str]
    raiting: Mapped[float]
    genres: Mapped[List["GenreInDB"]] = relationship(secondary=book_to_genre_association, back_populates="books")
    authors: Mapped[List["AuthorInDB"]] = relationship(secondary=book_to_author_association, back_populates="books")

    reviews: Mapped[List["ReviewInDB"]] = relationship(back_populates="book")

    def __repr__(self) -> str:
        return f"Book(id={self.id}), title={self.title}"

# prevents circular import
from .postgres_genre_table import GenreInDB
from .postgres_author_table import AuthorInDB
from .postgres_review_table import ReviewInDB
