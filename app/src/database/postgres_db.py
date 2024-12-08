import os
from sqlalchemy import  Engine, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_utils import database_exists, create_database
from src.common.sigleton import Singleton


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
