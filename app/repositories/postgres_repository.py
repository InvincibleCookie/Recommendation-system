import os
from datetime import datetime
from typing import List
from sqlalchemy import Engine, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_utils import database_exists, create_database

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Base(DeclarativeBase):
    pass

class PostgresDB(metaclass=Singleton):
    _engine: Engine

    def __init__(self) -> None:
        self._engine = self.connect()

    def get_engine(self):
        return self._engine

    def connect(self) -> Engine:
        db_name = os.environ['DB_NAME']
        db_host = os.environ['POSTGRES_HOST']
        db_port = os.environ['POSTGRES_PORT']
        db_user = os.environ['POSTGRES_USER']
        db_password = os.environ['POSTGRES_PASSWORD']

        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

        if not database_exists(engine.url):
            create_database(engine.url)

        Base.metadata.create_all(engine)
        return engine

class UserInDB(Base):
    __tablename__ = "user_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] =  mapped_column(unique=True)
    password_hash: Mapped[str]

    tokens: Mapped[List["TokenInDB"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id}), username={self.username}"

class TokenInDB(Base):
    __tablename__ = "user_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.id"))
    token_id: Mapped[str]
    expiry_date: Mapped[datetime]

    user: Mapped["UserInDB"] = relationship(back_populates="tokens")

    def __repr__(self) -> str:
        return f"Token(id={self.id}), token={self.token_id}"


