from src.data_models.book import BookIdModel
from src.database.postgres_book_table import BookInDB
import src.auth as auth
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.data_models.user import FullUserModel, PublicUser, TokenData
from src.database.postgres_db import PostgresDB
from src.database.postgres_token_table import TokenInDB
from src.database.postgres_user_table import UserInDB
from src.repositories.user_repository import UserRepository


class PostgresUserRepository(UserRepository):
    def _get_engine(self):
        return PostgresDB().get_engine()

    def register(self, user : FullUserModel) -> bool:
        with Session(self._get_engine()) as session:
            new_user = UserInDB(
                username = user.username,
                email = user.email,
                password_hash = auth.get_password_hash(user.password),
                tokens = []
            )

            try:
                session.add(new_user)
                session.commit()
            except:
                return False

        return True

    def autheticate_by_password(self, username, password) -> bool:
        with Session(self._get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)
            user = session.scalar(stmt)
            if user is None:
                return False

        return auth.verify_password(password, user.password_hash)

    def invalidate_refresh_token(self, token_data: TokenData) -> bool:
        with Session(self._get_engine()) as session:
            stmt = (select(UserInDB)
                    .join(TokenInDB)
                    .where(UserInDB.username == token_data.username)
                    .where(TokenInDB.token_id== token_data.token_id)
            )

            user = session.scalar(stmt)
            if user is None:
                return False

            token = None

            for i in user.tokens:
                if i.token_id== token_data.token_id:
                    token = i
                    break

            if token == None:
                return False

            user.tokens.remove(token)
            session.commit()

            return True

    def add_refresh_token(self, token: TokenData) -> bool:
        with Session(self._get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == token.username)
            users = session.scalars(stmt).all()

            if len(users) != 1:
                return False

            users[0].tokens.append(TokenInDB(token_id=token.token_id, expiry_date=token.expiry_date))
            session.commit()
            return True

    def get_user(self, username) -> PublicUser | None:
        with Session(self._get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)

            user = session.scalar(stmt)

            if user is None:
                return None

            return PublicUser.from_db(user)

    def like_book(self, username: str, book_id: int) -> bool:
        with Session(self._get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)
            users = session.scalars(stmt).all()

            if len(users) != 1:
                return False

            book = None
            try:
                book = session.get_one(BookInDB, book_id)
            except:
                return False

            users[0].liked_books.append(book)
            session.commit()
            return True


    def get_liked_books(self, username: str) -> list[BookIdModel]:
        with Session(self._get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)
            users = session.scalars(stmt).all()

            if len(users) != 1:
                return []

            books = []

            for i in users[0].liked_books:
                books.append(BookIdModel.from_db(i))

            return books

