import auth
from data_models.user import FullUserModel, PublicUser, TokenData
from repositories.postgres_user_repository import PostgresUserRepository

class UserService:
    def __init__(self):
        self.userRepository = PostgresUserRepository()

    def register(self, user: FullUserModel):
        return self.userRepository.register(user)

    def authenticate_by_password(self, username: str, password: str) -> bool:
        return self.userRepository.autheticate_by_password(username, password)

    def create_access_token(self, username: str):
        return auth.create_access_token(username)

    def create_refresh_token(self, username: str):
        return auth.create_refresh_token(username)

    def add_refresh_token(self, token: TokenData) -> bool:
        return self.userRepository.add_refresh_token(token)

    def invalidate_refresh_token(self, token: TokenData) -> bool:
        return self.userRepository.invalidate_refresh_token(token)

    def get_user(self, username) -> PublicUser | None:
        return  self.userRepository.get_user(username)


