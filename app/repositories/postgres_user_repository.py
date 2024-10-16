import auth
from sqlalchemy import select
from sqlalchemy.orm import Session
from data_models.user import FullUserModel, PublicUser, TokenData
from auth import verify_password
from repositories.postgres_repository import PostgresDB, TokenInDB, UserInDB
from repositories.user_repository import UserRepository

class PostgresUserRepository(UserRepository):
    def register(self, user : FullUserModel) -> bool:
        with Session(PostgresDB().get_engine()) as session:
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
        with Session(PostgresDB().get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)
            user = session.scalar(stmt)
            if user is None:
                return False

            return verify_password(password, user.password_hash)

    def invalidate_refresh_token(self, token_data: TokenData) -> bool:
        with Session(PostgresDB().get_engine()) as session:
            stmt = (select(UserInDB)
                    .join(TokenInDB)
                    .where(UserInDB.username == token_data.username)
                    .where(TokenInDB.token_id == token_data.token_id)
            )

            user = session.scalar(stmt)
            if user is None:
                return False

            token = None

            for i in user.tokens:
                if i.token_id == token_data.token_id:
                    token = i
                    break

            if token == None:
                return False

            user.tokens.remove(token)
            session.flush()

            session.delete(token)
            session.commit()

            return True

    def add_refresh_token(self, token: TokenData) -> bool:
        with Session(PostgresDB().get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == token.username)
            users = session.scalars(stmt).all()

            if len(users) != 1:
                return False

            users[0].tokens.append(TokenInDB(token_id=token.token_id, expiry_date=token.expiry_date))
            session.commit()
            return True

    def get_user(self, username) -> PublicUser | None:
        with Session(PostgresDB().get_engine()) as session:
            stmt = select(UserInDB).where(UserInDB.username == username)

            user = session.scalar(stmt)

            if user is None:
                return None

            return PublicUser(
                username = user.username,
                email = user.email,
            )

