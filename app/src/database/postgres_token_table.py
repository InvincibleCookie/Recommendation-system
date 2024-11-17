from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from .postgres_db import Base

class TokenInDB(Base):
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.id"))
    token_id: Mapped[str]
    expiry_date: Mapped[datetime]

    user: Mapped["UserInDB"] = relationship(back_populates="tokens")

    def __repr__(self) -> str:
        return f"Token(id={self.id}), token={self.token_id}"

# prevents circular import
from .postgres_user_table import UserInDB
