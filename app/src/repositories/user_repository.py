from abc import abstractmethod

from src.data_models.user import FullUserModel, PublicUser, TokenData

class UserRepository:
    @abstractmethod
    def register(self, user: FullUserModel) -> bool: pass

    @abstractmethod
    def autheticate_by_password(self, username, password) -> bool: pass

    @abstractmethod
    def invalidate_refresh_token(self, token_data: TokenData) -> bool: pass

    @abstractmethod
    def add_refresh_token(self, token: TokenData) -> bool: pass

    @abstractmethod
    def get_user(self, username) -> PublicUser | None: pass

