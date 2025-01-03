import os
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import random, string
from src.data_models.user import FullTokenData, TokenData
from datetime import datetime, timedelta, timezone
import bcrypt

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "fail")

if SECRET_KEY == "fail":
    print("Bad environment")
    exit(1)

ALGORITHM = "HS256"
ACCESS_KEY_EXPIRY_DELTA = timedelta(hours=24)
REFRESH_KEY_EXPIRY_DELTA = timedelta(days=30)
ACCESS_KEY_TYPE_KEY = "access"
REFRESH_KEY_TYPE_KEY = "refresh"

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def decrypt_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            return None

        username = payload.get("username")
        token_type = payload.get("type")
        token_id = payload.get("token_id")
        expire = payload.get("exp")

        assert(username is not None)
        assert(token_id is not None)
        assert(token_type is not None)
        assert(expire is not None)

        expire_date = datetime.fromtimestamp(expire, tz=timezone.utc)

        return TokenData(
            username=username,
            token_type=token_type,
            token_id=token_id,
            expiry_date=expire_date
        )
    except Exception:
        return None

def create_token(username: str, delta: timedelta, token_type: str) -> FullTokenData:
    to_encode: dict[str, ...] = {"username": username}


    expire = datetime.now(timezone.utc) + delta
    token_id = ''.join(random.choice(string.printable) for _ in range(10))

    to_encode.update({"token_id": token_id})
    to_encode.update({"exp": expire})
    to_encode.update({"type": token_type})

    return FullTokenData(
        username=to_encode.get("username", "fail"),
        token_id=token_id,
        token_type=token_type,
        token_str=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM),
        expiry_date=expire
    )

def create_access_token(username: str):
        return create_token(username, ACCESS_KEY_EXPIRY_DELTA, ACCESS_KEY_TYPE_KEY)

def create_refresh_token(username) -> FullTokenData:
        return create_token(username, REFRESH_KEY_EXPIRY_DELTA, REFRESH_KEY_TYPE_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def authenticate_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = decrypt_token(token)
    if (token_data is None or
            token_data.token_type != ACCESS_KEY_TYPE_KEY):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return token_data

async def authenticate_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_data = decrypt_token(token)
    if (token_data is None or
            token_data.token_type != REFRESH_KEY_TYPE_KEY):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    return token_data
