from typing import List
from sqlalchemy.orm import  Mapped, mapped_column, relationship


from .postgres_db import Base

class UserInDB(Base):
    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] =  mapped_column(unique=True)
    password_hash: Mapped[str]

    tokens: Mapped[List["TokenInDB"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    liked_books: Mapped[List["BookInDB"]] = relationship(secondary="book_to_user_like_association")

    def __repr__(self) -> str:
        return f"User(id={self.id}), username={self.username}"

from .postgres_book_table import BookInDB # prevents circular import
from .postgres_token_table import TokenInDB # prevents circular import