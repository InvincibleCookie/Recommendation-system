from abc import abstractmethod

from src.data_models.user import FullTokenData, FullUserModel, InternalUser, PublicUser, TokenData

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
    def create_access_token(self, username: str) -> FullTokenData: pass

    @abstractmethod
    def create_refresh_token(self, username: str) -> FullTokenData: pass

    @abstractmethod
    def like_book(self, username: str, book_id: int) -> bool: pass

    @abstractmethod
    def unlike_book(self, username: str, book_id: int) -> bool: pass

    @abstractmethod
    def get_user(self, username) -> PublicUser | None: pass

    @abstractmethod
    def get_internal_user(self, username) -> InternalUser | None:
        '''
        FOR INTERNAL USE ONLY!!!!
        '''
        pass
