from sqlalchemy import Column, ForeignKey, Table
from .postgres_db import Base

book_to_genre_association = Table(
    "book_to_genre_association",
    Base.metadata,
    Column("book_id", ForeignKey("book_data.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)

book_to_author_association = Table(
    "book_to_author_association",
    Base.metadata,
    Column("book_id", ForeignKey("book_data.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True),
)

book_to_user_like = Table(
    "book_to_user_like_association",
    Base.metadata,
    Column("book_id", ForeignKey("book_data.id"), primary_key=True),
    Column("user_id", ForeignKey("user_data.id"), primary_key=True),
)

