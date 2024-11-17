from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship


from .postgres_db import Base

class ReviewInDB(Base):
    __tablename__ = "review_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    price: Mapped[float]
    helpfulness: Mapped[float]
    score: Mapped[float]
    date: Mapped[datetime]
    summary: Mapped[str]
    review_text: Mapped[str]

    book_id: Mapped[int] = mapped_column(ForeignKey('book_data.id'))
    book: Mapped["BookInDB"] = relationship(back_populates="reviews")

    foreign_user_id: Mapped[int] = mapped_column(nullable = True)
    foreign_username: Mapped[str] = mapped_column(nullable = True)

    is_internal_user: Mapped[bool]

    internal_user_id: Mapped[int] = mapped_column(ForeignKey('user_data.id'), nullable = True)
    internal_user: Mapped["UserInDB"] = relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"Review(id={self.id}), title={self.title}"

# prevents circular import
from .postgres_book_table import BookInDB
from .postgres_user_table import UserInDB
