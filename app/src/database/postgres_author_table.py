from typing import List
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .postgres_db import Base
from .postgres_association_tables import book_to_author_association

class AuthorInDB(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Author(id={self.id}), name={self.name}"

    books: Mapped[List["BookInDB"]] = relationship(secondary=book_to_author_association, back_populates="authors")

# prevents circular import
from .postgres_book_table import BookInDB
