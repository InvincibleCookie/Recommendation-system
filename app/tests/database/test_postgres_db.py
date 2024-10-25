import os
import dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import create_database, database_exists

from src.database.postgres_db import Base

class PostgresDB():
    _engine: Engine

    def __init__(self) -> None:
        dotenv.load_dotenv("test.env")
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

