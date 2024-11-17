from datetime import datetime
from pydantic import BaseModel

from src.database.postgres_user_table import UserInDB

class UserModel(BaseModel):
    username: str
    password: str

class FullUserModel(UserModel):
    email: str

class PublicUser(BaseModel):
    username: str
    email: str

    @staticmethod
    def from_db(user: UserInDB) -> 'PublicUser':
        return PublicUser(
            username = user.username,
            email = user.email,
        )

class TokenModel(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    token_id: str
    token_type: str
    expiry_date: datetime

class FullTokenData(TokenData):
    token_str: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
